import unittest
import mx.DateTime
import os
import sys
import pdb
from PyDrill.Generation.TwoOfFive import Symbols
from PyDrill.Simulation.TwoOfFiveSimulator import TwoOfFiveSimulator
from PyDrill.Objects.Pulse import Pulse

program = '../LocalDecode.py'
interpreter = sys.executable

symbols = Symbols.generateSymbols()
identifiers = Symbols.generateIdentifiers()

reset_command = interpreter + ' '  + program + ' ' + '--reset'
command = interpreter + ' ' + program + ' '

if __name__ == '__main__':
    class LocalDecodeTests(unittest.TestCase):
        def setUp(self):
            self.sim = TwoOfFiveSimulator()
            
        #def testNow(self):
        #    command = interpreter + ' ' + program + ' ' + option + ' ' + str(mx.DateTime.now())
        #    print "Executing", command
        #    print os.system(command)
        def testSequence(self):
            seq = [identifiers[0],symbols[0]]
            ts = mx.DateTime.now()
            pulses = self.sim.make(seq,ts)
            pulses[0].append(Pulse(timeStamp=pulses[0][-1].timeStamp + mx.DateTime.DateTimeDeltaFrom(10)))
            print "!",os.system(reset_command)
            for pulse in pulses[0]:
                print "!",os.system(command+str(pulse.timeStamp))
            

    unittest.main()
            
