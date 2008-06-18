from PyDrill import DataBase
import time
import mx.DateTime

db = DataBase.Layer('localhost',8050)

while(1): #forever
    try:
        db.conn.sync()

        t = mx.DateTime.now()
        
        print "Bucket Status:"

        for k in db.root.keys():
            print k,":",len(db.root[k])

        print "Time to retrive:",mx.DateTime.now()-t,
        print "@ ", mx.DateTime.now()

        time.sleep(1)
    except KeyboardInterrupt:
        print "Exiting"
        db.disconnect()
        #shutdown code
        break

print "Clean Exit"
        
    
