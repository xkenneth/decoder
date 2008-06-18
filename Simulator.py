from PyDrill.DataBase import Layer
from PyDrill.Objects.Pulse import Pulse
from PyDrill.Objects.Symbol import Symbol
from PyDrill.Objects.ToolData import ToolData
from PyDrill.Simulation.TwoOfFiveSimulator import TwoOfFiveSimulator
from PyDrill.Generation.TwoOfFive import Symbols
import time
import mx.DateTime
import random
import math
from copy import copy

def generateSequence(timeStamp):
    sim = TwoOfFiveSimulator()
    sim.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())

    sequence = [sim.identifiers[-1]]

    for i in range(random.randint(0,10)):
        sequence.append(sim.symbols[i])
        
    pulses,timeStamp = sim.make(sequence,timeStamp)

    return pulses,timeStamp
    
if __name__ == '__main__':
    d = Layer(configFile='zeoClient.cfg')

    x = 0
    
    pulses = []
    
    timeStamp = mx.DateTime.now()
    pulse_time = mx.DateTime.now()
    pulse_count = 0
    try:
        while(1):
            print "Starting loop"
            
            #if len(pulses)==0: #if we've got no pulses in our array
            #    pulses,timeStamp = generateSequence(timeStamp) #generate some
            #else:
            #    print pulses[0] #insert them until we don't have anymore
            #    d.newData(pulses.pop(0))
                
            p = Pulse(timeStamp=pulse_time)
            print p.fileKey
            d.newData(p)
            print p

            pulse_time += mx.DateTime.DateTimeDeltaFrom(2)
            pulse_count += 1

            if pulse_count > 24:
                pulse_count = 0
                pulse_time += mx.DateTime.DateTimeDeltaFrom(2)
            
            s = Symbol(value=random.randint(0,99),timeStamp=mx.DateTime.now())
            print s.fileKey
            d.newData(s)
            print s

            t = ToolData('inclination',value=random.randint(1,10000),timeStamp=mx.DateTime.now())
            print t.fileKey
            d.newData(t)
            print t
            
            t = ToolData(name='azimuth',value=random.randint(5000,6000),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t

            t = ToolData(name='toolface',value=random.randint(7000,8000),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='temperature',value=100+x%5+random.randint(0,10000),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='gammaray',value=random.randint(0,10000),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='gx',value=random.randint(0,100),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='gy',value=random.randint(0,100),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='gz',value=random.randint(0,100),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='hx',value=random.randint(0,100),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='hy',value=random.randint(0,100),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='hz',value=random.randint(0,100),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='toolstatus',value=random.randint(0,10),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            t = ToolData(name='pressure',value=random.randint(0,150),timeStamp=mx.DateTime.now())
            d.newData(t)
            print t
            
            x+=1
            time.sleep(1)
        
        
    
    except KeyboardInterrupt:
        print "Exiting"

        print "Exited Gracefully"
