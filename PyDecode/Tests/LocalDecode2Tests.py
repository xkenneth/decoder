from PyDrill.Simulation import TwoOfFiveSimulator
from PyDrill.Generation.TwoOfFive import Symbols, Frames
import mx.DateTime
import os

frames = Frames.generate()
frame = frames[0]

sim = TwoOfFiveSimulator.TwoOfFiveSimulator()
sim.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())

new_pulses = sim.make(frame.sim(),mx.DateTime.now())

new_pulses = new_pulses[0]


my_str = ''

for t in new_pulses:
    s = str(t.timeStamp)
    s = s.replace(' ','')

    my_str += s + ' '

print my_str
call = '/Users/xkenneth/python/teledrilldev/bin/python ./LocalDecode2.py ' + my_str
print call
os.system(call)
#print this

