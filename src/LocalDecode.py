import sys
import pdb
import getopt
import mx.DateTime
import ConfigParser
import os

from PyDrill.Decoders.TwoOfFive import SymbolDecoder
from PyDrill.Objects.Pulse import Pulse
from PyDrill.DataBase import Layer
from PyDrill.Generation.TwoOfFive import Symbols
    

#globals
SETTINGS = 'settings.cfg'
SECTION = 'persistent'
LAST = 'last'
#for holding the last timestamp
last = None
reset = False #for resetting the last value
clear = False
pulse = None
debug = False
show_deltas = False
csv = False

print_keys = False
jitter = 10

#parse opts
optlist, args = getopt.getopt(sys.argv[1:],'',['reset','clear','debug','print-keys','show-deltas','jitter=','csv'])

for opt in optlist:
    if opt[0] == '--reset':
        reset = True
    if opt[0] == '--clear':
        clear = True
        reset = True #we have to reset as well
    if opt[0] == '--debug':
        debug = True
    if opt[0] == '--print-keys':
        print_keys = True
    if opt[0] == '--show-deltas':
        show_deltas = True
    if opt[0] == '--jitter':
        jitter = int(opt[1])
    if opt[0] == '--csv':
        csv = True


#initialize the decoder
decoder = SymbolDecoder.SymbolDecoder(jitter_magnitude=jitter)
decoder.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())

#get the pulse
new_pulses = []
for arg in args:
        ts = mx.DateTime.DateTimeFrom(arg)
        new_pulses.append(Pulse(timeStamp=ts))
        

#open the local pulse database
layer = Layer(file='local.fs')

if not csv:
    print "Store:", os.path.join(os.getcwd(),'local.fs')

last_key = None
if print_keys or show_deltas:
    for key in layer.root['pulse'].keys(): 
        if print_keys:
            print key
        if last_key is None:
            pass
        else:
            if show_deltas:
                print float(key-last_key)
        last_key = key
            
            

if clear:
    print "Clearing FS!!"
    layer.cleanSystem()

#get the local settings
cp = ConfigParser.ConfigParser()
cp.read(SETTINGS)

if not cp.has_section(SECTION):
    cp.add_section(SECTION) #set it up if need be
else:
    if not reset:
        if cp.get(SECTION,LAST) != 'None':
            last = mx.DateTime.DateTimeFrom(cp.get(SECTION,LAST))

if debug:
    pdb.set_trace()

#add the new data
if new_pulses != []:
    for new_pulse in new_pulses:
        print "Recieved:"
        try:
            layer.newData(new_pulse)
            print new_pulse
        except ValueError, e:
            print e
            print "Pulse already exists!",new_pulse
            
if debug:
    pdb.set_trace()

pulses = layer.slice('pulse',begin=last)

for p in pulses:
    new_data = decoder.decode(p)
    if new_data is not None:
        try:
            if not csv:
                print new_data
            layer.newData(new_data)
        except ValueError:
            pass
                
        if new_data.value < 0:
            last = new_data.pulses[0].timeStamp
            

#close it out
#save the last pulse
if not reset:
    pass
    cp.set(SECTION,LAST,last)
else:
    cp.set(SECTION,LAST,str(None))

cp.write(file(SETTINGS,'w'))

layer.disconnect()

if not csv:
    print "Success!" 

        

