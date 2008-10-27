import sys
import pdb
import getopt
import mx.DateTime
import ConfigParser
import os
from copy import copy

from decoder import Decoder
from frameDecoder import FrameDecoder

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
optlist, args = getopt.getopt(sys.argv[1:],'',['reset','clear','debug','print-keys','show-deltas','jitter=','host=','csv'])
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
        new_pulses.append(ts)

last = None
for p in new_pulses:
    if last is not None:
        if show_deltas:
            print p - last
    last = p
        

decoder = Decoder()

frame_decoder = FrameDecoder()

new_symbols = decoder.decode(new_pulses,debug=debug)

#for ns in new_symbols:
#    print ns

new_data = frame_decoder.decode(new_symbols)

for d in new_data:
    print d.name,"=",d.value,"@",d.timeStamp
    


    
