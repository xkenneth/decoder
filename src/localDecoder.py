import sys
import pdb
import getopt
import ConfigParser
import os
from copy import copy
from datetime import datetime

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

import re

for arg in args:
    ts = None
    month = int(arg[0:2])
    day = int(arg[3:5])
    year = int(arg[6:10])
    
    hour = int(arg[10:12])
    minute = int(arg[13:15])
    second = int(arg[16:18])
    microsecond = arg[19:]
    microsecond += (6-len(microsecond))*'0'
    microsecond = int(microsecond)
    

    new_pulses.append(datetime(year,month,day,hour,minute,second,microsecond))

last = None
for p in new_pulses:
    if last is not None:
        if show_deltas:
            print p - last
    last = p
        

decoder = Decoder()

frame_decoder = FrameDecoder()

new_symbols = decoder.decode(new_pulses,debug=False)

#for ns in new_symbols:
#    print ns

new_data = frame_decoder.decode(new_symbols)

for d in new_data:
    print d.name,"=",d.value,"@",d.timeStamp
    


    
