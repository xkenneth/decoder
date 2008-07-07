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

database_connection = DataBase.Layer(configFile='zeoClient.cfg')

max_buffer_depth = 10

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
rop_identifier = Identifier(record_identifier='01',item_identifier='13')
bit_depth_identifier = Identifier(record_identifier='01',item_identifier='08')


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
            bit_depth_data_item = DataItem(identifier=bit_depth_identifier,value='%04.1f' % new_depth[0])
            depth_data_record = DataRecord([bit_depth_data_item])
            trans.write(depth_data_record)

    new_rop = None
    try:
        new_rop = grok.latestROP()
    except socket.error:
        print "MWDCommander comm error."
    
    ### ROP ###

    if new_rop is not None:
        try:
            rop_buffer.index(new_rop)
        except ValueError:
            rop_buffer.append(new_rop)
            print "Sending rop update ", new_rop[0], " @ ", new_rop[1]
            rop_data_item = DataItem(identifier=rop_identifier,value='%4.1f' % new_rop[0])
            rop_data_record = DataRecord([rop_data_item])
            trans.write(rop_data_record)

    ### INC ###

    new_inc = None
    try:
        inc = database_connection.slice('inclination',last=1)
        if len(inc) > 0:
            inclination_buffer.index(inc)
    except ValueError:
        new_inc = inc
        inclination_buffer.append(new_inc)
        
    if new_inc is not None:
        print "Inc Update: ", new_inc
        inclination_value_string = '%04.1f' % (180.0-new_inc[0].value*180/10000.0)
        inclination_identifier = Identifier(record_identifier='07',item_identifier='13')
        inclination_data_item = DataItem(identifier=inclination_identifier,value=inclination_value_string)
        mwd_data_record = DataRecord([inclination_data_item])
        trans.write(mwd_data_record)
    
    ### AZU ###
    new_azu = None
    try:
        azu = database_connection.slice('azimuth',last=1)
        if len(azu) > 0:
            azimuth_buffer.index(azu)
    except ValueError:
        new_azu = azu
        azimuth_buffer.append(new_azu)

    if new_azu is not None:
        azimuth_value_string = '%04.1f' % (new_azu[0].value*360.0/10000.0)
        print "Azi update: ",new_azu
        azimuth_identifier = Identifier(record_identifier='07',item_identifier='15')
        azimuth_data_item = DataItem(identifier=azimuth_identifier,value=azimuth_value_string)
        mwd_data_record = DataRecord([azimuth_data_item])
        trans.write(mwd_data_record)


    ### GR ###
    new_gr = None

    try:
        gamma_ray = database_connection.slice('gammaray',last=1)
        if len(gamma_ray) > 0:
            gamma_ray_buffer.index(gamma_ray)
    except ValueError:
        new_gr = gamma_ray
        gamma_ray_buffer.append(new_gr)
        
    if new_gr is not None:
        print "GR Update:",new_gr
        gamma_ray_value_string = '%04.1f' % (pow(10.0,(new_gr[0].value*2.0)/10000.0)*5.0)
        gamma_ray_identifier = Identifier(record_identifier='08',item_identifier='21')
        gamma_ray_data_item = DataItem(identifier=gamma_ray_identifier,value=gamma_ray_value_string)
        mwd_data_record = DataRecord([gamma_ray_data_item])
        trans.write(mwd_data_record)
            
    ### MANAGE BUFFERS ###
    depth_buffer = manage_buffer(depth_buffer)
    azimuth_buffer = manage_buffer(azimuth_buffer)
    gamma_ray_buffer = manage_buffer(gamma_ray_buffer)
    inclination_buffer = manage_buffer(inclination_buffer)
    rop_buffer = manage_buffer(rop_buffer)

    ### SLEEP ###
    time.sleep(1)
    
    
