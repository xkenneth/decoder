import sys
import getopt
import serial
import time

from PyWITS.Transmitter import Transmitter
from PyWITS.Receiver import Receiver
from PyWITS.Objects.Identifier import Identifier
from PyWITS.Objects.DataItem import DataItem
from PyWITS.Objects.DataRecord import DataRecord

from PyDrill import DataBase

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

count = 0.0

try:
    while(1):
        #collect the data points
        
        #gamma ray
        try:
            gamma_ray = database_connection.slice('gammaray',last=1)
            print "Retrieved:",gamma_ray
            print gamma_ray[0].value
            gamma_ray_value_string = '%04.1f' % (pow(10.0,(gamma_ray[0].value*2.0)/10000.0)*5.0)
            print gamma_ray_value_string

            gamma_ray_identifier = Identifier(record_identifier='08',item_identifier='21')
            gamma_ray_data_item = DataItem(identifier=gamma_ray_identifier,value=gamma_ray_value_string)
            
            mwd_data_record = DataRecord([gamma_ray_data_item])

            trans.write(mwd_data_record)
            
        except KeyError, e:
            print e
            pass

        #azimuth
        try:
            azimuth = database_connection.slice('azimuth',last=1)
            print "Retrieved:",azimuth
            print azimuth[0].value
            azimuth_value_string = '%04.1f' % (azimuth[0].value*360.0/10000.0)
            print azimuth_value_string

            azimuth_identifier = Identifier(record_identifier='07',item_identifier='15')
            azimuth_data_item = DataItem(identifier=azimuth_identifier,value=azimuth_value_string)
            
            mwd_data_record = DataRecord([azimuth_data_item])

            trans.write(mwd_data_record)
            
        except KeyError, e:
            print e
            pass
        
        
        #inclination
        try:
            inclination = database_connection.slice('inclination',last=1)
            print "Retrieved:",inclination
            print inclination[0].value
            inclination_value_string = '%04.1f' % (180.0-inclination[0].value*180/10000.0)
            print inclination_value_string

            inclination_identifier = Identifier(record_identifier='07',item_identifier='13')
            inclination_data_item = DataItem(identifier=inclination_identifier,value=inclination_value_string)
            
            mwd_data_record = DataRecord([inclination_data_item])

            trans.write(mwd_data_record)
            
        except KeyError, e:
            print e
            pass        

        #depth
        #bit depth
        bit_depth_identifier = Identifier(record_identifier='01',item_identifier='08')
        bit_depth_data_item = DataItem(identifier=bit_depth_identifier,value='%04.1f' % count)
        
        #hole depth
        hole_depth_identifier = Identifier(record_identifier='01',item_identifier='10')
        hole_depth_data_item = DataItem(identifier=hole_depth_identifier,value='%04.1f' % count)
        
        #rop
        rop_identifier = Identifier(record_identifier='01',item_identifier='13')
        rop_data_item = DataItem(identifier=rop_identifier,value='28000')
        

        depth_data_record = DataRecord([bit_depth_data_item,hole_depth_data_item,rop_data_item])

        trans.write(depth_data_record)

        #sleep
        count += 0.1
        time.sleep(1)
except KeyboardInterrupt:
    pass
    

# #gamma ray
# inclination_identifier = Identifier(record_identifier='07',item_identifier='13')
# inclination_data_item = DataItem(identifier=inclination_identifier,value='00.0')

# azimuth_identifier = Identifier(record_identifier='07',item_identifier='15')
# azimuth_data_item = DataItem(identifier=azimuth_identifier,value='00.0')

# test_data_record = DataRecord(data_items=[inclination_data_item,azimuth_data_item])

# test_data_record2 = DataRecord([gamma_ray_data_item])

# test_data_record3 = DataRecord([bit_depth_data_item,hole_depth_data_item,rop_data_item])

# x = 0
# count1 = 738.21
# count2 = 1128.21
# count3 = 143.21

# try:
#     while(1):
#         #print '%04.1f' % x
#         inclination_data_item.value = '%04.1i' % x
#         azimuth_data_item.value = '%04.1i' % (2*x)
#         gamma_ray_data_item.value = '%04.1i' % (3*x)
#         bit_depth_data_item.value = '%05.2f' % (count1+x)
#         hole_depth_data_item.value = '%05.2f' % (count2+x)
#         rop_data_item.value = '%05.2f' % (count3+x)
        
        

#         x += 1
#         print "Writing"
#         trans.write(test_data_record)
#         trans.write(test_data_record2)
#         trans.write(test_data_record3)
#         #print "Reading"
#         #rec.read()
#         time.sleep(1)
        
# except KeyboardInterrupt:
#     pass
