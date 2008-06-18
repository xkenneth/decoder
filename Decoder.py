import sys
import getopt
from PyDrill import DataBase
from PyDrill.Decoders.TwoOfFive import SymbolDecoder
from PyDrill.Generation.TwoOfFive import Symbols
from ZODB import FileStorage, DB
import mx.DateTime
import time



optlist, args = getopt.getopt(sys.argv[1:],'',['readonly','reset','today','server=','showdeltas','showdots'])

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
    
        
try:

    #setup up the database if it's not setup
    try:
        root['lastKey']
    except KeyError:
        root['lastKey'] = None
    


    #open a connection to the decoder server
    print "Initiating Client"
    if server is None:
        database_connection = DataBase.Layer(configFile='zeoClient.cfg')
    else:
        database_connection = DataBase.Layer(host=server,port=port)
        
    print "Client Initiated"
    decoder = SymbolDecoder.SymbolDecoder()
    decoder.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())
    pulses = []
    key = 'pulse'

    while(1):
        if len(pulses) == 0:
            #print "Retrieving pulses..."
            
            #print "Last Key: ",root['lastKey']
            
            try:

                if root['lastKey'] is None:
                    pulses = database_connection.slice(key='pulse',first=10)
                else:
                    pulses = database_connection.slice(key='pulse',begin=root['lastKey'],first=10)

                if show_dots:
                    print "."*len(pulses)
                    
                root['lastKey'] = pulses[-1].timeStamp

            except KeyError:

                print "No Pulses Yet Available..Sleeping..."
                time.sleep(1)
                
            
            #if show_deltas:
            #    for p in pulses:
            #        if last is not None:
            #            print p.timeStamp-last.timeStamp
            #        last = p

        try:
            pulses.pop(-1)
        except IndexError:
            pass

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
                    pass
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
