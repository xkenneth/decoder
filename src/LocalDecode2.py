import sys
import pdb
import getopt
import mx.DateTime
import ConfigParser
import os
from copy import copy

from PyDrill.Decoders.TwoOfFive import SymbolDecoder
from PyDrill.Objects.Pulse import Pulse
from PyDrill.DataBase import Layer
from PyDrill.Generation.TwoOfFive import Symbols, Frames

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


#get the pulse
new_pulses = []
for arg in args:
        ts = mx.DateTime.DateTimeFrom(arg)
        new_pulses.append(Pulse(timeStamp=ts))

#decoder!
identifiers = Symbols.generateIdentifiers()

last_bar = identifiers[0].bars[-1]
for i in range (4):
    
    if i > 0:
        new = copy(identifiers[-1])
        new.bars.append(last_bar)
        new.value = identifiers[-1].value-1
        identifiers.append(new)

decoder = SymbolDecoder.SymbolDecoder(jitter_magnitude=jitter)
decoder.addSymbols(symbols=Symbols.generateSymbols(),identifiers=identifiers)


show_deltas = True #TEMPORARY!
last = None

for pulse in new_pulses:
    if show_deltas:
        if last is not None:
            print pulse.timeStamp - last.timeStamp
        last = pulse
        
    new_data = decoder.decode(pulse)
    if new_data is not None:
        print new_data


    
