#frame defitions
#frameNumber = {'data':length]

from objects import block
from objects import symbol_frame

from copy import copy
import symbol_generation

frame0 = ['toolstatus__','toolstatus__']
frame1 = ['azimuth__','azimuth__']
frame2 = ['inclination__','inclination__']
frame3 = ['gravity__highres','gravity__highres','gravity__highres']
frame4 = ['magnetic__highres','magnetic__highres','magnetic__highres']
frame5 = ['gravity_z_highres','gravity_z_highres','gravity_z_highres']
frame6 = ['magnetic_z_highres','magnetic_z_highres','magnetic_z_highres']
frame7 = ['gravity_x_highres','gravity_x_highres','gravity_x_highres','gravit_y_highres','gravit_y_highres','gravit_y_highres']
frame8 = ['magnetic_x_highres','magnetic_x_highres','magnetic_x_highres','magnetic_y_highres','magnetic_y_highres','magnetic_y_highres']
frame9 = ['temperature__','temperature__']
frame10 = ['pressure__','pressure__']
frame11 = ['toolface__highres','toolface__highres']
frame12 = ['gammaray__highres','gammaray__highres']
frame13 = ['gravity__lowres']
frame14 = ['magnetic__lowres']
frame15 = ['gravity_x_lowres','gravity_x_lowres','gravity_y_lowres','gravity_y_lowres']
frame16 = ['magnetic_x_lowres','magnetic_x_lowres','magnetic_y_lowres','magnetic_y_lowres']
frame17 = ['toolface__lowres']
frame18 = ['gammaray__lowres']
frame19 = ['toolface__lowres','gammaray__lowres']

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
