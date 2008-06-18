import sys
import getopt
from PyDrill import DataBase
from PyDrill.Decoders.TwoOfFive import SymbolDecoder
from PyDrill.Generation.TwoOfFive import Symbols
from ZODB import FileStorage, DB
import mx.DateTime
import time
import pdb


optlist, args = getopt.getopt(sys.argv[1:],'',['readonly','reset','today','server=','showdeltas','showdots','debug-with-comm','print-count'])

print optlist, args

#open a connection to the local database for saving data
import transaction

storage = FileStorage.FileStorage('./settings.fs')
db = DB(storage)
conn = db.open()
root = conn.root()

#program options
readonly = False
server = None
port = 8050
show_deltas = False
show_dots = False
last = None
debug_with_comm = False
print_count = False

for opt in optlist:
    if opt[0] == '--server':
        server = opt[1]
    if opt[0] == '--reset':
        root['lastKey'] = None
    if opt[0] == '--today':
        root['lastKey'] = mx.DateTime.today()
    if opt[0] == '--readonly':
        readonly = True
    if opt[0] == '--showdeltas':
        show_deltas = True
    if opt[0] == '--showdots':
        show_dots = True
    if opt[0] == '--debug-with-comm':
        debug_with_comm = True
    if opt[0] == '--count':
        print_count = True
    
    
        
try:

    #setup up the database if it's not setup
    try:
        root['lastKey']
    except KeyError:
        root['lastKey'] = None
    


    recieved_pulses = 0
    pulses = []
    previous_pulses = []

    print "Client Initiated"
    decoder = SymbolDecoder.SymbolDecoder(jitter_magnitude=2)
    decoder.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())
    pdb.set_trace()
    key = 'pulse'

    if not debug_with_comm:
        #open a connection to the decoder ZEO server
        print "Initiating Client"
        if server is None:
            database_connection = DataBase.Layer(configFile='zeoClient.cfg')
        else:
            database_connection = DataBase.Layer(host=server,port=port)
    else: 
        import LabVIEWWrapper
        glue = LabVIEWWrapper.LabVIEWWrapper()
        
        
    while(1):
        if len(pulses) == 0:
            #print "Retrieving pulses..."
            
            #print "Last Key: ",root['lastKey']
            
            if not debug_with_comm:
                try:
                    
                    if root['lastKey'] is None:
                        pulses = database_connection.slice(key='pulse',first=10)
                        
                    else:
                        pulses = database_connection.slice(key='pulse',begin=root['lastKey'],first=10)

                    recieved_pulses += len(pulses) - 1

                    if print_count:
                        print recieved_pulses
                        

                    if show_dots:
                        print "."*len(pulses)
                        
                    root['lastKey'] = pulses[-1].timeStamp

                except KeyError:
                    print "No Pulses Yet Available..Sleeping..."
                    time.sleep(1)
                    
                try:
                    pulses.pop(-1)
                except IndexError:
                    pass

            else:
                #get a section of pulses from the labview wrapper
                new_pulses = glue.serve()
                if new_pulses != None and new_pulses != []:
                    if len(previous_pulses) == 0:
                        new = new_pulses.pop(0)
                        previous_pulses.append(new)
                        pulses.append(new)
                    else:
                        for new in new_pulses:
                            present = False
                            for old in previous_pulses:
                                if new == old:
                                    present = present or True
                            previous_pulses.append(new)
                            if not present:
                                recieved_pulses += 1
                                if print_count:
                                    print recieved_pulses
                                print new
                                pulses.append(new)
                else:
                    time.sleep(0.5)
                
        while(1):

            try:
                p = pulses.pop(0)
            except IndexError:
                break
            
            #print p
            
            if show_deltas:
                if last is not None:
                    print float(p.timeStamp - last.timeStamp)

            last = p

            new_data = decoder.decode(p)

            if new_data is not None:
                print "!",new_data
                if not readonly:
                    if not debug_with_comm:
                        try:
                            database_connection.newData(new_data)
                        except ValueError, e:
                            print e
                            

        #time.sleep(.25)
    
except KeyboardInterrupt:
    print "Exiting"
    print "Last Key Saved As:",root['lastKey']

    transaction.commit()
    print "Clean Exit"

#d.slice('pulses',root['lastKey']=10)
