#frame defitions
#frameNumber = {'data':length]

from objects import block
from objects import symbol_frame

from copy import copy
import symbol_generation

frame0 = ['toolstatus']
frame1 = ['azimuth','azimuth']
frame2 = ['inclination','inclination']
frame3 = ['G','G','G','G']
frame4 = ['H','H','H','H']
frame5 = ['gz','gz','gz']
frame6 = ['hz','hz','hz']
frame7 = ['gx','gx','gx','gy','gy','gy']
frame8 = ['hx','hx','hx','hy','hy','hy']
frame9 = ['temperature','temperature']
frame10 = ['pressure','pressure']
frame11 = ['toolface','toolface']
frame12 = ['gammaray','gammaray']
frame13 = ['g']
frame14 = ['h']
frame15 = ['gx','gx','gy','gy']
frame16 = ['hx','hx','hy','hy']
frame17 = ['toolface']
frame18 = ['gammaray']
frame19 = ['toolface','gammaray']

badFrame1 = ['baddata']
badFrame2 = ['baddata1','baddata2']

frames = [frame0,frame1,frame2,frame3,frame4,frame5,frame6,frame7,frame8,frame9,frame10,frame11,frame12,frame13,frame14,frame15,frame16,frame17,frame18,frame19] #frames take their ID from the order they're placed in here!!!

badFrames = [badFrame1,badFrame2]



def generate():
    frameObjects = [] #for holding the frame objects
    symbol_objects = symbol_generation.generateSymbols()
    
    #start with the first id
    id = 0
    
    for frame in frames: #for all of the frames
        
        lastData = None
        newData = []
        save_id = None
        
        id_symbol = [symbol for symbol in symbol_objects if symbol.value == id][0]
        
        for data in frame: #for the data in each frame
            
            if lastData is not None: 
                if lastData.name == data:
                    lastData.symbol_length += 1
                else:
                    newData.append(lastData)
                    lastData = block(name=data,symbol_length=1)
            else:
                lastData = block(name=data,symbol_length=1)
                
        newData.append(lastData)
        
        frameObjects.append(symbol_frame(identifier=id_symbol,blocks=newData))

        id += 1

    return frameObjects

def generateErrors():
    frameObjects = [] #for holding the frame objects
    id = 0
    for frame in badFrames: #for all of the frames
        lastData = None
        newData = []
        for data in frame: #for the data in each frame
            
            if lastData!=None: 
                if lastData.name == data:
                    lastData.symbol_length += 1
                else:
                    newData.append(lastData)
                    lastData = block(name=data,symbol_length=1)
            else:
                lastData = block(name=data,symbol_length=1)
                
        newData.append(lastData)

        frameObjects.append(Frame(header=id+63,subFrames=newData))

        id += 1

    return frameObjects

if __name__ == '__main__':
    

    generated_frames = generate()
    
    for i in generated_frames:
        print i.identifier, i.symbols, i.blocks
            
            
        
    #generate and save the frame defitions
