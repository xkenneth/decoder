import socket
import os
from PyDrill import Services
from PyDrill.Objects import Pulse
from mx.DateTime import *
from Ft.Xml import MarkupWriter
import mx
import time
import select

class LabVIEWWrapper:

   def __init__(self,port=8002,configFile=None,messages=False,**kw):

      self.port = port
      self.messages = messages
      self.configFile = configFile
      self.quit = False
      
      self.lvsocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
      
      try:
         self.lvsocket.bind ( ( '', self.port ) )
         print "Wrapper started on port: ", self.port
      except KeyError:                       
         raise ValueError('Value: WrapperPort has not been defined in the config file!')
      
      self.lvsocket.listen ( 1 )

      #self.lvsocket.settimeout(1)
      self.lvsocket.setblocking(0)

   def close(self):
      self.lvsocket.close()

   def serve(self):
      
      try:
         #print ready
         channel, details = self.lvsocket.accept()
         #print channel, type(channel), "Channel!"
         #print details, type(details)
         data = channel.recv(4096)
      except Exception, e:
         #print e
         #print "Sleeping!"
         return None
      
      #print 'Opened a connection with', details
      #print 'Recieved', data

      newData = data.split('\n')
         #print "!",newData
         #print len(newData)
      timeStamps = []
      for d in newData:
         if d:
            timeStamp = mx.DateTime.DateTimeFrom(d)
            timeStamps.append(timeStamp)
         #print "Recieved TimeStamp", timeStamp
         
      pulses = []
      for tS in timeStamps:
         try:
               #print "Trying to recreate pulse!"
            p = Pulse.Pulse(timeStamp=tS)
            pulses.append(p)
               #print "Done Recreating Pulse!"
         except Exception, e:
            print e

         
      #print "Sending ok!"
      channel.send('OK')
      channel.close()
      
      return pulses



if __name__ == '__main__':
   from PyDrill import DataBase
   
   try:
      d = DataBase.Layer(configFile='zeoClient.cfg')
      configFile = 'config.xml'
      glue = LabVIEWWrapper()
      x = 0

      logFile = file('pulseLog.xml','w')
      
      writer = MarkupWriter(logFile,indent=u'yes')
      writer.startDocument()
      writer.startElement(u'Pulses')
      
      while(1):
         pulses = glue.serve()
         if pulses:
            print "Got: ", len(pulses)
            print pulses
            for p in pulses:
               try:
                  d.newData(p)
                  p.writeToXml(writer)
               except ValueError, e:
                  print e
                  
            x += len(pulses)
            print x," Total Pulses Recieved"
            #print pulses
            time.sleep(0.5)
         else:
            time.sleep(.1)

   except KeyboardInterrupt:
      print "Closing"
      writer.endElement(u'Pulses')
      writer.endDocument()
      logFile.close()
      print "Exited Gracefully"

      
