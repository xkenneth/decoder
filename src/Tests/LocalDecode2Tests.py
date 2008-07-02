from PyDrill.Simulation import TwoOfFiveSimulator
from PyDrill.Generation.TwoOfFive import Symbols, Frames
import mx.DateTime

frames = Frames.generate()
frame = frames[0]

print frame.sim()
sim = TwoOfFiveSimulator.TwoOfFiveSimulator()
sim.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())

new_symbols = sim.make(frame.sim(),mx.DateTime.now())

print new_symbols




