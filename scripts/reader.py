import argparse
import os.path
import time
import serial
import numpy as np
from struct import pack,unpack

alt_conv_factor = 3.2932160

crctable = \
    b"\x00\x00\x89\x11\x12\x23\x9b\x32\x24\x46\xad\x57\x36\x65\xbf\x74\
\x48\x8c\xc1\x9d\x5a\xaf\xd3\xbe\x6c\xca\xe5\xdb\x7e\xe9\xf7\xf8\
\x19\x09\x90\x18\x0b\x2a\x82\x3b\x3d\x4f\xb4\x5e\x2f\x6c\xa6\x7d\
\x51\x85\xd8\x94\x43\xa6\xca\xb7\x75\xc3\xfc\xd2\x67\xe0\xee\xf1\
\x32\x12\xbb\x03\x20\x31\xa9\x20\x16\x54\x9f\x45\x04\x77\x8d\x66\
\x7a\x9e\xf3\x8f\x68\xbd\xe1\xac\x5e\xd8\xd7\xc9\x4c\xfb\xc5\xea\
\x2b\x1b\xa2\x0a\x39\x38\xb0\x29\x0f\x5d\x86\x4c\x1d\x7e\x94\x6f\
\x63\x97\xea\x86\x71\xb4\xf8\xa5\x47\xd1\xce\xc0\x55\xf2\xdc\xe3\
\x64\x24\xed\x35\x76\x07\xff\x16\x40\x62\xc9\x73\x52\x41\xdb\x50\
\x2c\xa8\xa5\xb9\x3e\x8b\xb7\x9a\x08\xee\x81\xff\x1a\xcd\x93\xdc\
\x7d\x2d\xf4\x3c\x6f\x0e\xe6\x1f\x59\x6b\xd0\x7a\x4b\x48\xc2\x59\
\x35\xa1\xbc\xb0\x27\x82\xae\x93\x11\xe7\x98\xf6\x03\xc4\x8a\xd5\
\x56\x36\xdf\x27\x44\x15\xcd\x04\x72\x70\xfb\x61\x60\x53\xe9\x42\
\x1e\xba\x97\xab\x0c\x99\x85\x88\x3a\xfc\xb3\xed\x28\xdf\xa1\xce\
\x4f\x3f\xc6\x2e\x5d\x1c\xd4\x0d\x6b\x79\xe2\x68\x79\x5a\xf0\x4b\
\x07\xb3\x8e\xa2\x15\x90\x9c\x81\x23\xf5\xaa\xe4\x31\xd6\xb8\xc7\
\xc8\x48\x41\x59\xda\x6b\x53\x7a\xec\x0e\x65\x1f\xfe\x2d\x77\x3c\
\x80\xc4\x09\xd5\x92\xe7\x1b\xf6\xa4\x82\x2d\x93\xb6\xa1\x3f\xb0\
\xd1\x41\x58\x50\xc3\x62\x4a\x73\xf5\x07\x7c\x16\xe7\x24\x6e\x35\
\x99\xcd\x10\xdc\x8b\xee\x02\xff\xbd\x8b\x34\x9a\xaf\xa8\x26\xb9\
\xfa\x5a\x73\x4b\xe8\x79\x61\x68\xde\x1c\x57\x0d\xcc\x3f\x45\x2e\
\xb2\xd6\x3b\xc7\xa0\xf5\x29\xe4\x96\x90\x1f\x81\x84\xb3\x0d\xa2\
\xe3\x53\x6a\x42\xf1\x70\x78\x61\xc7\x15\x4e\x04\xd5\x36\x5c\x27\
\xab\xdf\x22\xce\xb9\xfc\x30\xed\x8f\x99\x06\x88\x9d\xba\x14\xab\
\xac\x6c\x25\x7d\xbe\x4f\x37\x5e\x88\x2a\x01\x3b\x9a\x09\x13\x18\
\xe4\xe0\x6d\xf1\xf6\xc3\x7f\xd2\xc0\xa6\x49\xb7\xd2\x85\x5b\x94\
\xb5\x65\x3c\x74\xa7\x46\x2e\x57\x91\x23\x18\x32\x83\x00\x0a\x11\
\xfd\xe9\x74\xf8\xef\xca\x66\xdb\xd9\xaf\x50\xbe\xcb\x8c\x42\x9d\
\x9e\x7e\x17\x6f\x8c\x5d\x05\x4c\xba\x38\x33\x29\xa8\x1b\x21\x0a\
\xd6\xf2\x5f\xe3\xc4\xd1\x4d\xc0\xf2\xb4\x7b\xa5\xe0\x97\x69\x86\
\x87\x77\x0e\x66\x95\x54\x1c\x45\xa3\x31\x2a\x20\xb1\x12\x38\x03\
\xcf\xfb\x46\xea\xdd\xd8\x54\xc9\xeb\xbd\x62\xac\xf9\x9e\x70\x8f"

def calc_crc(crc_buff):

    # start crc as 0x0001
    crc = np.frombuffer(b"\x01\x00",np.uint16)
    crc = crc[0]

    table = np.frombuffer(crctable,np.uint16)

    for x in crc_buff:
        index = (np.right_shift(crc,8) ^ x)
 #       print("{},{},{},{}".format(crc,x,index,table[index]))
        crc = (np.left_shift(crc,8) ^ table[index]) & 0xFFFF

    return crc

def gps_ang_to_float(min,frac):
    deg = np.int16(min/60.0)
    min_deg = (min-(deg*60.0)+frac/100000.0)/60.0
    return deg+min_deg;        

def outfile_name(args):
    if args.outfile != None:
        return args.outfile
    elif args.infile != None:
        return "decoded_" + args.infile
    else:
        return str(int(time.time())) + ".log"

def find_header(buf):
    header_bytes = 0
    loc = 0

    for x in buf:
        if header_bytes == 0 and x == int('0x51',16):
            header_bytes = 1
        elif header_bytes == 1 and x == int('0xAC',16):
            return loc - 1
        else:
            header_bytes = 0
        loc += 1    
    
    return -1

def check_for_msg(buf,header_loc):
    len_idx = header_loc + 2

    if len(buf) < header_loc + 6:
        # too short for a full msg
        return False
    elif len(buf) < header_loc + 3 + buf[len_idx]:
        return False
    
    return True

def process_msg(buf,header_loc,outfile):

    # extract msg components
    pkt_len = buf[header_loc+2]
    if pkt_len < 3:
        # Remove just the header and try again
        buf = buf[(header_loc+2):]
        return buf

    id = buf[header_loc+3]
    data = buf[(header_loc+4):(header_loc + 4 + pkt_len - 3)]
    crc_buff = buf[(header_loc+3):(header_loc+3+pkt_len-2)]
    crc_bytes = buf[(header_loc+3+pkt_len-2):(header_loc+3+pkt_len)]
    crc = np.left_shift(crc_bytes[0],8) + crc_bytes[1]

    # verify no msg corruption
    if crc == calc_crc(crc_buff):
        # process message by type
        if id == int('0x10',16): # Raw Position Msg type
            lat_min = unpack('h',pack('BB', data[0], data[1]))
            lat_frac = unpack('i',pack('BBBB', data[2], data[3], data[4], data[5]))
            lon_min = unpack('h',pack('BB', data[6], data[7]))
            lon_frac = unpack('i',pack('BBBB', data[8], data[9], data[10], data[11]))
            alt = unpack('H',pack('BB', data[12], data[13]))  
            print("Position (Raw) Msg: Lat = {:0.7f}, Lon = {:0.7f}, Alt = {:0.2f}\n".format(gps_ang_to_float(lat_min[0],lat_frac[0]), gps_ang_to_float(lon_min[0],lon_frac[0]), (alt[0]/alt_conv_factor)-900),end = '')
            outfile.write("{:d}:{:0.7f}:{:0.7f}:{:0.2f}\n".format(id, gps_ang_to_float(lat_min[0],lat_frac[0]), gps_ang_to_float(lon_min[0],lon_frac[0]), (alt[0]/alt_conv_factor)-900))
        elif id == int('0x11',16): #Extrapolated Position Msg type
            lat_min = unpack('h',pack('BB', data[0], data[1]))
            lat_frac = unpack('i',pack('BBBB', data[2], data[3], data[4], data[5]))
            lon_min = unpack('h',pack('BB', data[6], data[7]))
            lon_frac = unpack('i',pack('BBBB', data[8], data[9], data[10], data[11]))
            alt = unpack('H',pack('BB', data[12], data[13]))  
            print("Position (Extrapolated) Msg: Lat = {:0.7f}, Lon = {:0.7f}, Alt = {:0.2f}\n".format(gps_ang_to_float(lat_min[0],lat_frac[0]), gps_ang_to_float(lon_min[0],lon_frac[0]), (alt[0]/alt_conv_factor)-900),end = '')
            outfile.write("{:d}:{:0.7f}:{:0.7f}:{:0.2f}\n".format(id, gps_ang_to_float(lat_min[0],lat_frac[0]), gps_ang_to_float(lon_min[0],lon_frac[0]), (alt[0]/alt_conv_factor)-900))
        elif id == int('0x20',16): #Orientation Msg type
            heading = unpack('h',pack('BB', data[0], data[1]))
            roll = unpack('h',pack('BB', data[2], data[3]))
            pitch = unpack('h',pack('BB', data[4], data[5]))  
            print("Orientation Msg: Heading = {:0.2f}, Roll = {:0.2f}, Pitch = {:0.2f}\n".format(heading[0]/100.0, roll[0]/100.0, pitch[0]/100.0),end = '')                
            outfile.write("{:d}:{:0.2f}:{:0.2f}:{:0.2f}\n".format(id, heading[0]/100.0, roll[0]/100.0, pitch[0]/100.0))
        elif id == int('0x30',16): #Radio Msg type
            speed = unpack('h',pack('BB', data[0], data[1]))
            steering = unpack('b',pack('B', data[2]))
            print("Radio Msg: Speed = {:0.2f}, steering = {}\n".format(speed[0]/100.0, steering[0]),end = '')                
            outfile.write("{:d}:{:0.2f}:{}\n".format(id, speed[0]/100.0, steering[0]))
        elif id == int('0x40',16): #IMU Msg type
            euler_x = unpack('h',pack('BB', data[0], data[1]))
            euler_y = unpack('h',pack('BB', data[2], data[3]))
            euler_z = unpack('h',pack('BB', data[4], data[5]))
            acc_x = unpack('h',pack('BB', data[6], data[7]))
            acc_y = unpack('h',pack('BB', data[8], data[9]))
            acc_z = unpack('h',pack('BB', data[10], data[11]))
            gyro_x = unpack('h',pack('BB', data[12], data[13]))
            gyro_y = unpack('h',pack('BB', data[14], data[15]))
            gyro_z = unpack('h',pack('BB', data[16], data[17]))
            print("IMU Msg: Eul_x = {:f}, Eul_y = {:f}, Eul_z = {:f}, Acc_x = {:f}, Acc_y = {:f}, Acc_z = {:f}, Gyr_x = {:f}, Gyr_y = {:f}, Gyr_z = {:f}\n".format(euler_x[0]/10430.0,euler_y[0]/10430.0,euler_z[0]/10430.0,acc_x[0]/8192.0,acc_y[0]/8192.0,acc_z[0]/8192.0,gyro_x[0]/16.4,gyro_y[0]/16.4,gyro_z[0]/16.4),end = '')                
            outfile.write("{:d}:{:f}:{:f}:{:f}:{:f}:{:f}:{:f}:{:f}:{:f}:{:f}\n".format(id, euler_x[0]/10430.0,euler_y[0]/10430.0,euler_z[0]/10430.0,acc_x[0]/8192.0,acc_y[0]/8192.0,acc_z[0]/8192.0,gyro_x[0]/16.4,gyro_y[0]/16.4,gyro_z[0]/16.4))
        elif id == int('0x41',16): #Sonar Msg type
            ping1 = unpack('H',pack('BB', data[0], data[1]))
            ping2 = unpack('H',pack('BB', data[2], data[3]))
            ping3 = unpack('H',pack('BB', data[4], data[5]))
            ping4 = unpack('H',pack('BB', data[6], data[7]))
            ping5 = unpack('H',pack('BB', data[8], data[9]))
            print("Sonar Msg: ping1 = {:d}, ping2 = {:d}, ping3 = {:d}, ping4 = {:d}, ping5 = {:d}\n".format(ping1[0],ping2[0],ping3[0],ping4[0],ping5[0]),end = '')                
            outfile.write("{:d}:{:d}:{:d}:{:d}:{:d}:{:d}\n".format(id, ping1[0],ping2[0],ping3[0],ping4[0],ping5[0]))
        elif id == int('0x42',16): #Bumper Msg type
            left = unpack('B',pack('B', data[0]))
            right = unpack('B',pack('B', data[1]))
            print("Bumper Msg: left = {:d}, right = {:d}\n".format(left[0],right[0]))                
            outfile.write("{:d}:{:d}:{:d}\n".format(id,left[0],right[0]))
        elif id == int('0x60',16): #State Msg type
            apmState = unpack('b',pack('B', data[0]))
            driveState = unpack('b',pack('B', data[1]))
            autoState = unpack('b',pack('B', data[2]))
            autoFlag = unpack('b',pack('B', data[3]))
            voltage = unpack('b',pack('B', data[4]))
            amperage = unpack('b',pack('B', data[5]))
            groundSpeed = unpack('b',pack('B', data[6]))
            print("State Msg: apmState = {:d}, driveState = {:d}, autoState = {:d}, autoFlag = {:d}, voltage = {:0.2f}, amperage = {:0.2f}, groundSpeed = {:0.2f}\n".format(apmState[0], driveState[0], autoState[0], autoFlag[0], voltage[0]/10.0, amperage[0]/10.0, groundSpeed[0]/10.0),end = '')
            outfile.write("{:d}:{:d}:{:d}:{:d}:{:d}:{:0.2f}:{:0.2f}:{:0.2f}\n".format(id, apmState[0], driveState[0], autoState[0], autoFlag[0], voltage[0]/10.0, amperage[0]/10.0, groundSpeed[0]/10.0))
        elif id == int('0x70',16): #Configuration Msg type
            print("Configuration MSG recived (not defined)\n",end = '')                
            outfile.write("{:d}\n".format(id))
        elif id == int('0x80',16): #Control Msg type
            speed = unpack('h',pack('BB', data[0], data[1]))
            steering = unpack('B',pack('B', data[2]))
            print("Control Msg: Speed = {:0.2f}, steering = {}\n".format(speed[0]/100.0, steering[0]),end = '')
            outfile.write("{:d}:{:0.2f}:{}\n".format(id, speed[0]/100.0, steering[0]))
        elif id == int('0x81',16): #Waypoint Msg type
            latStart_min = unpack('h',pack('BB', data[0], data[1]))
            latStart_frac = unpack('i',pack('BBBB', data[2], data[3], data[4], data[5]))
            lonStart_min = unpack('h',pack('BB', data[6], data[7]))
            lonStart_frac = unpack('i',pack('BBBB', data[8], data[9], data[10], data[11]))
            latIntermediate_min = unpack('h',pack('BB', data[12], data[13]))
            latIntermediate_frac = unpack('i',pack('BBBB', data[14], data[15], data[16], data[17]))
            lonIntermediate_min = unpack('h',pack('BB', data[18], data[19]))
            lonIntermediate_frac = unpack('i',pack('BBBB', data[20], data[21], data[22], data[23]))
            latTarget_min = unpack('h',pack('BB', data[24], data[25]))
            latTarget_frac = unpack('i',pack('BBBB', data[26], data[27], data[28], data[29]))
            lonTarget_min = unpack('h',pack('BB', data[30], data3[1]))
            lonTarget_frac = unpack('i',pack('BBBB', data[32], data[33], data[34], data[35]))
            pathHeading = unpack('h',pack('BB', data[36], data[37]))
            print("Waypoint Msg: latStart = {:0.7f}, lonStart = {:0.7f}, latInter = {:0.7f}, lonInter = {:0.7f}, latTarget = {:0.7f}, lonTarget = {:0.7f}, pathHead = {:0.2f}\n".format(gps_ang_to_float(latStart_min[0],latStart_frac[0]), gps_ang_to_float(lonStart_min[0],lonStart_frac[0]), gps_ang_to_float(latIntermediate_min[0],latIntermediate_frac[0]), gps_ang_to_float(lonIntermediate_min[0],lonIntermediate_frac[0]), gps_ang_to_float(latTarget_min[0],latTarget_frac[0]), gps_ang_to_float(lonTarget_min[0],lonTarget_frac[0]), pathHeading[0]/100.0),end = '')
            outfile.write("{:d}:{:0.7f}:{:0.7f}:{:0.7f}:{:0.7f}:{:0.7f}:{:0.7f}:{:0.2f}\n".format(id, gps_ang_to_float(latStart_min[0],latStart_frac[0]), gps_ang_to_float(lonStart_min[0],lonStart_frac[0]), gps_ang_to_float(latIntermediate_min[0],latIntermediate_frac[0]), gps_ang_to_float(lonIntermediate_min[0],lonIntermediate_frac[0]), gps_ang_to_float(latTarget_min[0],latTarget_frac[0]), gps_ang_to_float(lonTarget_min[0],lonTarget_frac[0]), pathHeading[0]/100.0))
        elif id == int('0x90',16): #ASCII Msg type
            ascii = data[:pkt_len-3]
            print("ASCII Msg: {0!s}\n".format(ascii),end = '')                
            outfile.write("{:d}:{!s}}\n".format(id, ascii))
        elif id == int('0xA0',16): #Version Msg type
            debug_major = data[0]
            debug_minor = data[1]
            apm_major = data[2]
            apm_minor = data[3]
            print("Version Msg: debug_maj = {:d}, debug_min = {:d}, apm_major = {:d}, apm_minor = {:d}\n".format(debug_major,debug_minor,apm_major,apm_minor),end = '')                
            outfile.write("{:d}:{:d}:{:d}:{:d}:{:d}\n".format(id, debug_major,debug_minor,apm_major,apm_minor))
        else:
            print("Unknown Msg type recieved: %02x\n".format(id),end = '')

        outfile.flush()
    else:
        print("Error: CRC does not match recieved\n",end = '')
        # remove just the header and try again
        buf = buf[(header_loc+2):len(buf)]
        return buf

    # remove processed message from input buffer
    buf = buf[(header_loc+3+pkt_len):len(buf)]
    return buf

if __name__ == "__main__":
    # Gather arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', 
                        help='Input file with encoded log data.')
    parser.add_argument('-o', '--outfile', 
                        help='Optional - output file with decooded log data.')
    parser.add_argument('-p', '--port', 
                        help='Serial port path to read encoded data.')
    args = parser.parse_args()

    if args.infile != None and args.port != None:
        print("Error: Both input file (-i) and serial port (-p) cannot be specified simultaneously.")
        parser.print_help()
        exit()

    # Create output file for decoded data
    filename = outfile_name(args)
    try:
        outfile = open(filename, "x")
    except IOError:
        print("Error: Could not create output file - {}".format(args.outfile))
        exit()        

    # Live decoding (serial port)
    if args.infile != None:
        if not os.path.exists(args.infile):
            print("Error: Input file does not exist: {}".format(args.infile))
        print(args.infile)

        # Read and process live data
    
    # File decoding (file as input)
    elif args.port != None:
        # Configure and open serial port
        try:
            ser = serial.Serial(args.port, 115200, timeout=1)
        except serial.SerialException:
            print("Error: Could not open serial port - {}".format(args.port))
            exit()

        buf = bytes()
        while True:
            # Read and process data from file
            new_bytes = ser.read(80)
            read_size = len(new_bytes)

            if read_size + len(buf) < 512:
                buf += new_bytes
            else:
                print("Error: buffer overflow\n")

            header_loc = -1
            full_msg = False
            check_buff = True

            while check_buff:
                header_loc = find_header(buf)
                if header_loc >= 0:
                    full_msg = check_for_msg(buf,header_loc)
                    if full_msg:
                        buf = process_msg(buf,header_loc,outfile)
                    else:
                        check_buff = False
                else:                
                    # Garbage...toss all but last byte
                    buf = buf[(len(buf)-1):]
                    check_buff = False

    else:
        print("Error: Input file (-i) or serial port (-p) is required.")
        parser.print_help()
        
