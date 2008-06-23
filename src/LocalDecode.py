import sys
import pdb
import getopt
import mx.DateTime
import ConfigParser

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
reset = False #for wiping out the database
pulse = None

decoder = SymbolDecoder.SymbolDecoder(jitter_magnitude=3)
decoder.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())

#parse opts
optlist, args = getopt.getopt(sys.argv[1:],'',['reset'])

for opt in optlist:
    if opt[0] == '--reset':
        reset = True

#get the pulse
ts_string = ''.join(args)
if ts_string != '':
    ts = mx.DateTime.DateTimeFrom(ts_string)
    pulse = Pulse(timeStamp=ts)

#open the local pulse database
layer = Layer(file='local.fs')
if reset:
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


#add the new data
if pulse is not None:
    layer.newData(pulse)
    
    pulses = layer.slice('pulse',begin=last)

    for p in pulses:
        new_data = decoder.decode(p)
        if new_data is not None:
            try:
                layer.newData(new_data)
                print new_data
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



