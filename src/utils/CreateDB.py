from PyDrill import DataBase

d = DataBase.Layer('localhost',8050)

#if not d.verifyIntegrity():
#    print "Creating DataBase"
d.cleanSystem()
#    print "Done"
#else:
#    print "Database already created!"
    
