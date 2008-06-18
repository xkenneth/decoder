#not sure any of this code should be modularized

if __name__ == '__main__':
    import sys
    from Ft.Xml import Parse, MarkupWriter
    from PyDrill.Objects.Pulse import Pulse
    from PyDrill.Decoders.TwoOfFive.SymbolDecoder import SymbolDecoder
    from PyDrill.Generation.TwoOfFive import Symbols
    from PyDrill.DataBase import Layer
    from BTrees import OOBTree
    #load the pulses
    
    from PyDrill.DataStructures import UPQueue
    from PyDrill import DataBase
    import mx.DateTime
    
    db = DataBase.Layer('192.168.15.91',8050)
    pulses = db.slice('pulse',begin=mx.DateTime.DateTimeFrom('21:00:41:00'))
    for p in pulses:
        print p
    cd = SymbolDecoder()
    cd.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())
    
    last = None
    try:
        while(1):
            try:
                p = pulses.pop(0)
                diff = None
                if last is not None:
                    diff = p.timeStamp - last.timeStamp
                last = p
                #print "Work",p,diff
                dC = cd.decode(p)

                if dC is not None:
                    print "!!!",dC

            except IndexError:
                break
    except KeyError:
        print "Exit"
    

            
    
    






    #pulseLog = file(sys.argv[1],'r') #open the pulse log, argument 1

    #doc = Parse(pulseLog) #parse it

    #pulseTags = doc.xpath('//Pulse') #find all the pulse tags

    #pulses = UPQueue() #to hold the pulses
    #pulses = OOBTree.OOBTree()
    #for pT in pulseTags: #for found pulse tags
    #    p = Pulse(xml=pT) #create the pulse
    #    pulses[p.timeStamp] = p
        
    # output = file('pulseList.xml','w')
#     writer = MarkupWriter(output,indent=u'yes')
#     writer.startDocument()
#     writer.startElement(u'Pulses')
#     last = None
#     for p in pulses:
#         #print p
#         if last is not None:
#             print p.timeStamp - last.timeStamp
#         last = p
#         p.writeToXml(writer)

#     writer.endElement(u'Pulses')
#     writer.endDocument()
