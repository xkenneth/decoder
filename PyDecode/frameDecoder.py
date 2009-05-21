from symbol_generation import generateSymbols, generateIdentifiers
from frame_generation import generate
from objects import symbol
from copy import copy
import pdb

def match_frame(data,frames):
    #if we've got junk
    if len(data) <= 1:
        return None
    
    try:
        found_frame = [frame for i, frame in enumerate(frames) if data[0].value == frame.identifier.value and len(frame) == len(data)][0]
    except IndexError:
        raise Exception('No frames found!')
    
    found_frame = copy(found_frame)
    found_frame.symbols = data[1:]
    
    return found_frame

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
            
            #check to see if we've got an identifier
            if d.value < 0:
                new_frames.append([]) #add a new buffer
                count +=1 #increment the index to the frame buffer
            else: #if it's not an identifier
                if count >= 0: #and we've already got a frame index
                    new_frames[count].append(d) #append it to the frame buffer
        
        #for all of our new frame
            
        
        #match all of the frames
        matched_frames = [match_frame(frame,self.frames) for frame in new_frames]
        
        new_data = []
        
        #decompose the data
        [new_data.extend(frame.decompose()) for frame in matched_frames]
        
        #for frame in new_frames:

            #see if it matches any of our current frames
        #new_data = match_frame(frame,self.frames)
        #    pdb.set_trace()
        #    if new_data is not None:
        #        new_data.extend(d)

        return new_data

if __name__ == '__main__':
    import unittest, pdb, random

    class FrameDecoderTests(unittest.TestCase):
        def setUp(self):
            self.frames = generate()
            self.symbols = generateSymbols()

        def testOne(self):
            frame_decoder = FrameDecoder()
            
            
            #check the result of a good frame
            test = [symbol(i) for i in [-1,0,5]]
            t = frame_decoder.decode(test)

            self.failUnlessEqual(t[0].value,5)
            self.failUnlessEqual(t[0].name,'toolstatus')
            
            #check the result of another good frame
            test = [symbol(i) for i in [-1,1,4,5]]
            t = frame_decoder.decode(test)

            self.failUnlessEqual(t[0].value,405)
            self.failUnlessEqual(t[0].name,'azimuth')
            
            try:
                test = [symbol(i) for i in [-1,1,5]]
                t = frame_decoder.decode(test)
                self.fail()
            except Exception:
                pass
            
    unittest.main()
    
