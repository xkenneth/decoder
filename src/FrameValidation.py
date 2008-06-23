#not sure any of this code should be modularized

if __name__ == '__main__':
    import sys
    from Ft.Xml import Parse, MarkupWriter
    from PyDrill.Objects.Pulse import Pulse
    from PyDrill.Decoders.TwoOfFive.FrameDecoder import FrameDecoder
    from PyDrill.Generation.TwoOfFive import Symbols,Frames
    from PyDrill.DataBase import Layer
    from BTrees import OOBTree
    #load the symbols
    
    from PyDrill.DataStructures import UPQueue
    from PyDrill import DataBase
    import mx.DateTime
    
    db = DataBase.Layer('192.168.15.91',8050)
    symbols = db.slice('symbol',begin=mx.DateTime.DateTimeFrom('2008-04-28 17:17:50.66'))
    for s in symbols:
        print s
    fd = FrameDecoder()
    fd.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())
    fd.addFrames(frames=Frames.generate())
    
    last = None
    try:
        while(1):
            try:
                s = symbols.pop(0)
                diff = None
                if last is not None:
                    diff = s.timeStamp - last.timeStamp
                last = s
                #print "Work",p,diff
                dF = fd.decode(s)

                if dF is not None:
                    print "!"
                    #print len(dF.decompose())
                    #for td in dF.decompose():
                    #    print td
                    print dF.decompose()
                    print "!"

            except IndexError:
                break
    except KeyError:
        print "Exit"
    

            
    
    






