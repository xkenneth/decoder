import unittest

from PyDrill.helper import smart_datetime as datetime
from PyDrill.helper import smart_timedelta as timedelta

from copy import copy

#from PyDrill.Generation.TwoOfFive import Symbols
from PyDrill.symbol_generation import generateSymbols, generateIdentifiers

from PyDrill.simulator import TwoOfFiveSimulator

from PyDrill.objects import pulse

import pdb

modulus = 0.5

def to_float(dt):
    return float(dt.hour*60*60) + float(dt.minute*60) + float(dt.second) + float(dt.microsecond/1000000.0)

toDelta = lambda t: timedelta(0,t)

class DecoderException(Exception):
    def __init__(self,message='',data=None):
        self.message = self.__doc__
    def __str__(self):
        return self.message + str(data)

class NotEnoughpulses(DecoderException):
    """Not enough pulses remain to decode."""

#Helper Functions!
def check_values(sym_a,sym_b):
    equal = True
    for i in range(len(sym_a)):
        if sym_a[i].value != sym_b[i].value:
            equal &= False
    return equal

def to_ts(buf):
    """Turns a buffer of pulses into a buffer if timestamps"""
    t_buf = []
    try:
        for b in buf:
            t_buf.append(b.timeStamp)
    except AttributeError:
        return buf
    return t_buf

def to_pulse(buf):
    """Turns a buffer of timeStamps into a buffer of pulses"""
    t_buf = []
    for b in buf:
        t_buf.append(pulse(timeStamp=b))
    return t_buf

def got_enough(little_buf,big_buf):
    """Check to see if we have enough data in the buffers."""
    if len(big_buf) < len(little_buf):
        raise NotEnoughPulses()

def get_after(timeStamp,buf):
    t_buf = []
    for b in buf:
        if b >= timeStamp:
            t_buf.append(b)
    return t_buf
    

def next_symbol_area(last_symbol,jitter):
    narrow,wide,symbol = last_symbol.firstPossiblePeakAfter()

    #converting to seconds
    narrow = narrow*modulus
    wide = wide*modulus
    
    earliest = last_symbol.pulses[-1].timeStamp + toDelta(narrow) - toDelta(jitter)
    latest = last_symbol.pulses[-1].timeStamp + toDelta(wide) + toDelta(jitter) + toDelta(7.0)

    return earliest, latest

def retrieve_sub_buf(buf,min,max):
    t_buf = []
    for b in buf:
        if b >= min and b <= max:
            t_buf.append(b)
    return t_buf
            

    
    
    
    

def match(symbol_buf,data_buf,jitter):
    """Checks to see if two buffers of timestamps are approximately equal."""
    all_ok = True
    for count in range(len(symbol_buf)):
        close_enough = False
        for data in data_buf:

            t = to_float(symbol_buf[count]) - to_float(data)
            
            if abs(float(t)) < jitter:
                close_enough |= True
        all_ok &= close_enough
    return all_ok

class Decoder:
    def __init__(self,jitter=1.0/10.0):
        self.symbols = generateSymbols()
        self.identifiers = generateIdentifiers()
        self.sim = TwoOfFiveSimulator()
        self.sim.addSymbols(symbols=generateSymbols(),identifiers=generateIdentifiers())
        self.jitter = jitter

    def decode(self,buf,debug=False):
        """Decodes a buffer of timestamps. Each timestamp represents when a pulse occured.
        buf - iterable of timestamps"""

        
        #first find an identifer
        data = []

        found_id = False
        #while we still have data....
        while(1):

            while(1):
                for id in self.identifiers:
                    #create a perfect identifier
                    id_pulses,trash = self.sim.make([id],buf[0])
                    id_pulses = to_ts(id_pulses) #convert to TS
                    got_enough(id_pulses,buf)
                    if match(id_pulses,buf,self.jitter):
                        id.pulses = to_pulse(id_pulses)
                        id.timeStamp = id_pulses[0]
                        print id
                        data.append(id)
                        if debug:
                            print "Found ID"
                        found_id |= True

                if found_id: 
                    break
                #if not found_id:
                #    return data

                buf.pop(0) #else pop and search

        #once we've got the identifier, let's find as many symbols as we can
            earliest, latest = next_symbol_area(data[-1],self.jitter)
            
            while(1):

                if debug:
                    print "Searching for a symbol."
                
                found_sym = False
                
                sym_buf = retrieve_sub_buf(buf,earliest,latest)
            
                if len(sym_buf) < 5:
                    if debug:
                        print "Not enough symbols in buffer!"
                    break
                
                if debug: print "%d symbols in buffer, continuing.." % len(sym_buf)

                for sym in self.symbols:
                    sym_pulses, trash = self.sim.make([sym],sym_buf[0])
                    sym_pulses = to_ts(sym_pulses)
                    got_enough(sym_pulses,sym_buf)
                    if match(sym_pulses,sym_buf,self.jitter):
                        sym.pulses = to_pulse(sym_pulses)
                        sym.timeStamp = sym_pulses[0]
                        print sym
                        data.append(sym)
                        if debug:
                            print "Found Symbol!"
                        found_sym |= True
                        earliest, latest = next_symbol_area(data[-1],self.jitter)
            
                if not found_sym:
                    if debug: print "Symbol not found."
                    break

            last_buf = buf
            buf = get_after(earliest,buf)
            if last_buf == buf and not found_sym:
                return data

            if len(buf) < 5:
                return data

        return data
        


if __name__ == '__main__':

    def get_ts(pulses):
        ts = []
        for p in pulses:
            ts.append(p.timeStamp)
        return ts

    class DecoderTestCase(unittest.TestCase):
        def setUp(self):
            self.symbols = generateSymbols()
            self.identifiers = generateIdentifiers()
            self.decoder = Decoder()
            self.sim = TwoOfFiveSimulator()
            self.sim.addSymbols(symbols=generateSymbols(),identifiers=generateIdentifiers())

    class DecoderTests(DecoderTestCase):
        def testDoubleSymbol(self):
            pattern = []
            for sym in self.symbols:
                pattern.extend([self.identifiers[0],sym])

            pulses = self.sim.make(pattern,datetime.now())
            pulses = pulses[0]
            data = self.decoder.decode(get_ts(pulses))

            self.failIf(not(check_values(pattern,data)))

        def testFindIdentifier(self):
            for id in self.identifiers:
                pulses = self.sim.make([id],datetime.now())
                pulses = pulses[0]
                n_pulses = copy(pulses)
                data = self.decoder.decode(get_ts(pulses))
                if data[0].value != id.value:
                    self.fail()

        def testSingleSymbolPatterns(self):
            for id in self.identifiers:
                for sym in self.symbols:
                    pattern = [id,sym]

                    print pattern
            
                    pulses, trash = self.sim.make(pattern,datetime.now())

                    data = self.decoder.decode(get_ts(pulses))
                    
                    self.failUnless(check_values(pattern,data))

    class VeryLongTests(DecoderTestCase):
        def testMultiSymbolPatterns(self):
            depth = 0
            max_depth = 1
            for id in self.identifiers:
                for sym1 in self.symbols:
                    for sym2 in self.symbols:
                        for sym3 in self.symbols:
                            print id.value, sym1.value, sym2.value, sym3.value
                            for sym4 in self.symbols:
                                for sym5 in self.symbols:
                                    
                                    t = datetime.now()
                                    
                                    pattern = [id,sym1,sym2,sym3,sym4,sym5]

                                    pulses, trash = self.sim.make(pattern,datetime.now())
                                    
                                    data = self.decoder.decode(get_ts(pulses))
                                    
                                    self.failUnless(check_values(pattern,data))
                                    
                                    #print datetime.now() - t

                            
                        
                    
                
                
            
            
    unittest.main()

