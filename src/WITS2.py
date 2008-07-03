import sys
import getopt
import serial
import time
import pdb
import socket

from PyWITS.Transmitter import Transmitter
from PyWITS.Receiver import Receiver
from PyWITS.Objects.Identifier import Identifier
from PyWITS.Objects.DataItem import DataItem
from PyWITS.Objects.DataRecord import DataRecord

from PyDrill import DataBase

import xmlrpclib

import mx.DateTime

grok = xmlrpclib.Server('http://localhost:8080/MWDCommander')

optlist, args = getopt.getopt(sys.argv[1:], '', ['baud=','timeout='])

baud = 9600
timeout = 0.25

try:
    device = args[0]
except IndexError:
    raise ValueError('Device must be specified!')

for opt in optlist:
    if opt[0] == '--baud':
        baud = int(opt[1])

ser = serial.Serial(device,baud,timeout=timeout)

trans = Transmitter(ser)
rec = Receiver(ser)

#database_connection = DataBase.Layer(configFile='zeoClient.cfg')

max_buffer_depth = 50

def manage_buffer(buffer):
    if len(buffer) > max_buffer_depth:
        for i in range(len(buffer) - max_buffer_depth):
            buffer.pop(0)

    return buffer

gamma_ray_buffer = []
azimuth_buffer = []
inclination_buffer = []
depth_buffer = []
rop_buffer = []

#WITS0 definitions
#hole depth
hole_depth_identifier = Identifier(record_identifier='01',item_identifier='10')




while(1): #FOREVER!!!!!!
    ### DEPTH ###
    
    new_depth = None
    
    try:
        new_depth = grok.latestDepth()
    except socket.error:
        print "MWDCommander comm error."
    
    if new_depth is not None:
        try:
            depth_buffer.index(new_depth)
        except ValueError:
            depth_buffer.append(new_depth)
            #send it out the WITS port
            print "Sending depth update ",new_depth[0]," @ ",new_depth[1]
            hole_depth_data_item = DataItem(identifier=hole_depth_identifier,value='%04.1f' % new_depth[0])
            depth_data_record = DataRecord([hole_depth_data_item])
            trans.write(depth_data_record)
    

    ### ROP ###

    ### MANAGE BUFFERS ###
    depth_buffer = manage_buffer(depth_buffer)
    azimuth_buffer = manage_buffer(azimuth_buffer)
    gamma_ray_buffer = manage_buffer(gamma_ray_buffer)
    inclination_buffer = manage_buffer(inclination_buffer)
    rop_buffer = manage_buffer(rop_buffer)

    ### SLEEP ###
    time.sleep(1)
    
    
