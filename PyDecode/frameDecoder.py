from PyDrill.symbol_generation import generateSymbols, generateIdentifiers
from PyDrill.frame_generation import generate

def match_frame(data,frames):
    if len(data) == 0:
        return None
    for count in range(len(frames)):
        #if we have the right frame ID
        if data[0].value == count:
            #if the frame is the same length
            if len(frames[count]) == len(data):
                #assign the data
                frames[count].symbols = data[1:]
                #and decompose it
                return frames[count].decompose()

class FrameDecoder:
    def __init__(self):
        self.frames = generate()
        self.identifiers = generateIdentifiers()
        self.symbols = generateSymbols()

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


if __name__ == '__main__':
    import unittest, pdb, random

    class FrameDecoderTests(unittest.TestCase):
        def setUp(self):
            self.frames = generate()
            self.symbols = generateSymbols()
        def testOne(self):
            for frame in self.frames:
                data = []
                for frame_length in range(len(frame)):
                    data.append(self.symbols[random.randint(0,99)])
                frame.symbols = data
            
                

    unittest.main()
    
