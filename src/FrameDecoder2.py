from PyDrill.Decoders.TwoOfFive.FrameDecoder import FrameDecoder
from PyDrill.Generation.TwoOfFive import Symbols, Frames

def match_frame(data,frames):
    for count in range(len(frames)):
        if data[0].value == count:
            if len(frames[count]) == len(data):
                frames[count].symbols = data
                return frames[count].decompose()

class FrameDecoder:
    def __init__(self):
        self.frames = Frames.generate()
        self.identifiers = Symbols.generateIdentifiers()
        self.symbols = Symbols.generateSymbols()

    def decode(self,data):
        """;)"""
        new_frames = []
        
        new_data = []

        count = -1
        for d in data:
            
            if d.value < 0:
                new_frames.append([])
                count +=1
            else:
                if count >= 0:
                    new_frames[count].append(d)
        
                    
        for frame in new_frames:
            d = match_frame(frame,self.frames)
            if d is not None:
                new_data.extend(d)

        return new_data
        
                

