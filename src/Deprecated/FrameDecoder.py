import sys
import getopt
from PyDrill import DataBase
from PyDrill.Decoders.TwoOfFive import FrameDecoder
from PyDrill.Generation.TwoOfFive import Symbols, Frames
from ZODB import FileStorage, DB
import mx.DateTime
import time

optlist, args = getopt.getopt(sys.argv[1:],'',['readonly','reset','today','server=','showdeltas'])

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

    decoder = FrameDecoder.FrameDecoder()
    decoder.addSymbols(symbols=Symbols.generateSymbols(),identifiers=Symbols.generateIdentifiers())
    decoder.addFrames(frames=Frames.generate())
    symbols = []
    key = 'symbol'

    while(1):
        if len(symbols) == 0:
            #print "Retrieving symbols..."
            
            #print "Last Key: ",root['lastKey']

            try:
                if root['lastKey'] is None:
                    symbols = database_connection.slice(key=key,first=10)
                else:
                    symbols = database_connection.slice(key=key,begin=root['lastKey'],first=10)
                
                root['lastKey'] = symbols[-1].timeStamp

                symbols.pop(-1)

            except KeyError:

                print "No Symbols Yet Available..sleeping"

                time.sleep(1)
                
            #print len(symbols),"Retrieved..."

                

            

        while(1):

            try:
                p = symbols.pop(0)
            except IndexError:
                break

            print p

            new_data = decoder.decode(p)

            if new_data is not None:
                print new_data
                tool_data = new_data.decompose()
                print tool_data
                if not readonly:
                    try:
                        database_connection.newData(new_data)
                    except ValueError, e:
                        print e

                for td in tool_data:
                    try:
                        database_connection.newData(td)
                    except ValueError, e:
                        print e

        time.sleep(.25)

except KeyboardInterrupt:
    print "Exiting"
    print "Last Key Saved As:",root['lastKey']

    transaction.commit()
    print "Clean Exit"
