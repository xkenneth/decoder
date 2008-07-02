import unittest

import mx.DateTime
import pdb
from copy import copy

from PyDrill.Generation.TwoOfFive import Symbols
from PyDrill.Simulation import TwoOfFiveSimulator
from PyDrill.Objects.Pulse import Pulse

modulus = 0.5

toDelta = mx.DateTime.DateTimeDeltaFrom

class DecoderException(Exception):
    def __init__(self,message='',data=None):
        self.message = self.__doc__
    def __str__(self):
        return self.message + str(data)

class NotEnoughPulses(DecoderException):
    """Not enough pulses remain to decode."""

#Helper Functions!
def check_values(sym_a,sym_b):
    equal = True
    for i in range(len(sym_a)):
        if sym_a[i].value != sym_b[i].value:
            equal &= False
    return equal

def to_ts(buffer):
    """Turns a buffer of pulses into a buffer if timestamps"""
    t_buffer = []
    try:
        for b in buffer:
            t_buffer.append(b.timeStamp)
    except AttributeError:
        return buffer
    return t_buffer

def to_pulse(buffer):
    """Turns a buffer of timeStamps into a buffer of pulses"""
    t_buffer = []
    for b in buffer:
        t_buffer.append(Pulse(timeStamp=b))
    return t_buffer

def got_enough(little_buffer,big_buffer):
    """Check to see if we have enough data in the buffers."""
    if len(big_buffer) < len(little_buffer):
        raise NotEnoughPulses()

def next_symbol_area(last_symbol,jitter):
    narrow,wide,symbol = last_symbol.firstPossiblePeakAfter()

    #converting to seconds
    narrow = narrow*modulus
    wide = wide*modulus
    
    earliest = last_symbol.pulses[-1].timeStamp + toDelta(narrow) - toDelta(jitter)
    latest = last_symbol.pulses[-1].timeStamp + toDelta(wide) + toDelta(jitter) + toDelta(7.0)

    return earliest, latest

def retrieve_sub_buffer(buffer,min,max):
    t_buffer = []
    for b in buffer:
        if b >= min and b <= max:
            t_buffer.append(b)
    return t_buffer
            

    
    
    
    

def match(symbol_buffer,data_buffer,jitter):
    """Checks to see if two buffers of timestamps are approximately equal."""
    all_ok = True
    for count in range(len(symbol_buffer)):
        close_enough = False
        for data in data_buffer:
            if abs(float( symbol_buffer[count] - data )) < jitter:
                close_enough |= True
        all_ok &= close_enough
    return all_ok


        
    

class Decoder:
    def __init__(self,jitter=1.0/10.0):
        self.symbols = Symbols.generateSymbols()
        self.identifiers = Symbols.generateIdentifiers()
        self.sim = TwoOfFiveSimulator.TwoOfFiveSimulator()
        self.sim.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())
        self.jitter = jitter

    def decode(self,buffer):
        """Decodes a buffer of pulses or timestamps!"""
        buffer = to_ts(buffer) #convert to timeStamps
        #first find an identifer
        data = []

        found_id = False
        while(1):
            for id in self.identifiers:
                id_pulses,trash = self.sim.make([id],buffer[0])
                id_pulses = to_ts(id_pulses) #convert to TS
                got_enough(id_pulses,buffer)
                if match(id_pulses,buffer,self.jitter):
                    id.pulses = to_pulse(id_pulses)
                    data.append(id)
                    found_id |= True
            if found_id:
                break
            buffer.pop(0) #else pop and search

        #once we've got the identifier, let's find as many symbols as we can
        earliest, latest = next_symbol_area(data[-1],self.jitter)
        while(1):

            found_sym = False

            sym_buffer = retrieve_sub_buffer(buffer,earliest,latest)
            
            if len(sym_buffer) < 5:
                break

            for sym in self.symbols:
                sym_pulses, trash = self.sim.make([sym],sym_buffer[0])
                sym_pulses = to_ts(sym_pulses)
                got_enough(sym_pulses,sym_buffer)
                if match(sym_pulses,sym_buffer,self.jitter):
                    sym.pulses = to_pulse(sym_pulses)
                    data.append(sym)
                    found_sym |= True
                    earliest, latest = next_symbol_area(data[-1],self.jitter)
            
            if not found_sym:
                break
                    
                
        
            
            


        return data
        


        

    
            
        
            
            
        
        



if __name__ == '__main__':
    
    class DecoderTestCase(unittest.TestCase):
        def setUp(self):
            self.symbols = Symbols.generateSymbols()
            self.identifiers = Symbols.generateIdentifiers()
            self.decoder = Decoder()
            self.sim = TwoOfFiveSimulator.TwoOfFiveSimulator()
            self.sim.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())

    class DecoderTests(DecoderTestCase):
        def testFindIdentifier(self):
            for id in self.identifiers:
                pulses = self.sim.make([id],mx.DateTime.now())
                pulses = pulses[0]
                n_pulses = copy(pulses)
                data = self.decoder.decode(pulses)
                if data[0] != id:
                    self.fail()

                n_pulses.insert(0,Pulse(n_pulses[0].timeStamp-toDelta(5)))
                data = self.decoder.decode(n_pulses)
                if data[0] != id:
                    self.fail()

        def testSingleSymbolPatterns(self):
            for id in self.identifiers:
                for sym in self.symbols:
                    print '.',
                    pattern = [id,sym]
            
                    pulses, trash = self.sim.make(pattern,mx.DateTime.now())

                    data = self.decoder.decode(pulses)
                    
                    self.failUnless(check_values(pattern,data))

    class VeryLongTests(DecoderTestCase):
        def testMultiSymbolPatterns(self):
            depth = 0
            max_depth = 1
            for id in self.identifiers:
                for sym1 in self.symbols:
                    for sym2 in self.symbols:
                        for sym3 in self.symbols:
                            for sym4 in self.symbols:
                                for sym5 in self.symbols:
                                    t = mx.DateTime.now()
                                    
                                    pattern = [id,sym1,sym2,sym3,sym4,sym5]

                                    pulses, trash = self.sim.make(pattern,mx.DateTime.now())
                                    
                                    data = self.decoder.decode(pulses)
                                    
                                    self.failUnless(check_values(pattern,data))
                                    
                                    print mx.DateTime.now() - t

                            
                        
                    
                
                
            
            
    unittest.main()

