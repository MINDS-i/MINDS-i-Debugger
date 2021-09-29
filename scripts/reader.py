import argparse
import os.path
import time
import serial
import numpy as np

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
    deg = np.uint16(min/60.0)
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
            lat_min = data[0] | np.left_shift(data[1],8)
            lat_frac = data[2] | np.left_shift(data[3],8) | np.left_shift(data[4],16) | np.left_shift(data[5],24)
            lon_min = data[6] | np.left_shift(data[7],8)
            lon_frac = data[8] | np.left_shift(data[9],8) | np.left_shift(data[10],16) | np.left_shift(data[11],24)
            alt = data[12] | np.left_shift(data[13],8)  
            print("Position (Raw) Msg: Lat = {:0.7f}, Lon = {:0.7f}, Alt = {:0.2f}\n".format(gps_ang_to_float(lat_min,lat_frac), gps_ang_to_float(lon_min,lon_frac), (alt/alt_conv_factor)-900),end = '')
            outfile.write("{:d}:{:0.7f}:{:0.7f}:{:0.2f}\n".format(id, gps_ang_to_float(lat_min,lat_frac), gps_ang_to_float(lon_min,lon_frac), (alt/alt_conv_factor)-900))
        elif id == int('0x11',16): #Extrapolated Position Msg type
            lat_min = data[0] | np.left_shift(data[1],8)
            lat_frac = data[2] | np.left_shift(data[3],8) | np.left_shift(data[4],16) | np.left_shift(data[5],24)
            lon_min = data[6] | np.left_shift(data[7],8)
            lon_frac = data[8] | np.left_shift(data[9],8) | np.left_shift(data[10],16) | np.left_shift(data[11],24)
            alt = data[12] | np.left_shift(data[13],8)  
            print("Position (Extrapolated) Msg: Lat = {:0.7f}, Lon = {:0.7f}, Alt = {:0.2f}\n".format(gps_ang_to_float(lat_min,lat_frac), gps_ang_to_float(lon_min,lon_frac), (alt/alt_conv_factor)-900),end = '')
            outfile.write("{:d}:{:0.7f}:{:0.7f}:{:0.2f}\n".format(id, gps_ang_to_float(lat_min,lat_frac), gps_ang_to_float(lon_min,lon_frac), (alt/alt_conv_factor)-900))
        elif id == int('0x20',16): #Orientation Msg type
            heading = data[0] | np.left_shift(data[1],8)
            roll = data[2] | np.left_shift(data[3],8)
            pitch = data[4] | np.left_shift(data[5],8)  
            print("Orientation Msg: Heading = {:0.2f}, Roll = {:0.2f}, Pitch = {:0.2f}\n".format(heading/100.0, roll/100.0, pitch/100.0),end = '')                
            outfile.write("{:d}:{:0.2f}:{:0.2f}:{:0.2f}\n".format(id, heading/100.0, roll/100.0, pitch/100.0))
        elif id == int('0x30',16): #Radio Msg type
            speed = data[0] | np.left_shift(data[1],8)
            steering = data[2]
            print("Radio Msg: Speed = {:0.2f}, steering = {}\n".format(speed/100.0, steering),end = '')                
            outfile.write("{:d}:{:0.2f}:{}\n".format(id, speed/100.0, steering))
        elif id == int('0x40',16): #IMU Msg type
            euler_x = data[0] | np.left_shift(data[1],8)
            euler_y = data[2] | np.left_shift(data[3],8)
            euler_z = data[4] | np.left_shift(data[5],8)
            acc_x = data[6] | np.left_shift(data[7],8)
            acc_y = data[8] | np.left_shift(data[9],8)
            acc_z = data[10] | np.left_shift(data[11],8)
            gyro_x = data[12] | np.left_shift(data[13],8)
            gyro_y = data[14] | np.left_shift(data[15],8)
            gyro_z = data[16] | np.left_shift(data[17],8)
            print("IMU Msg: Eul_x = {:f}, Eul_y = {:f}, Eul_z = {:f}, Acc_x = {:f}, Acc_y = {:f}, Acc_z = {:f}, Gyr_x = {:f}, Gyr_y = {:f}, Gyr_z = {:f}\n".format(euler_x/10430.0,euler_y/10430.0,euler_z/10430.0,acc_x/8192.0,acc_y/8192.0,acc_z/8192.0,gyro_x/16.4,gyro_y/16.4,gyro_z/16.4),end = '')                
            outfile.write("{:d}:{:f}:{:f}:{:f}:{:f}:{:f}:{:f}:{:f}:{:f}:{:f}\n".format(id, euler_x/10430.0,euler_y/10430.0,euler_z/10430.0,acc_x/8192.0,acc_y/8192.0,acc_z/8192.0,gyro_x/16.4,gyro_y/16.4,gyro_z/16.4))
        elif id == int('0x41',16): #Sonar Msg type
            ping1 = data[0] | np.left_shift(data[1],8)
            ping2 = data[2] | np.left_shift(data[3],8)
            ping3 = data[4] | np.left_shift(data[5],8)
            ping4 = data[6] | np.left_shift(data[7],8)
            ping5 = data[8] | np.left_shift(data[9],8)
            print("Sonar Msg: ping1 = {:d}, ping2 = {:d}, ping3 = {:d}, ping4 = {:d}, ping5 = {:d}\n".format(ping1,ping2,ping3,ping4,ping5),end = '')                
            outfile.write("{:d}:{:d}:{:d}:{:d}:{:d}:{:d}\n".format(id, ping1,ping2,ping3,ping4,ping5))
        elif id == int('0x42',16): #Bumper Msg type
            left = data[0]
            right = data[1]
            print("Bumper Msg: left = {:d}, right = {:d}\n".format(left,right))                
            outfile.write("{:d}:{:d}:{:d}\n".format(id,left,right))
        elif id == int('0x60',16): #State Msg type
            apmState = data[0]
            driveState = data[1]
            autoState = data[2]
            autoFlag = data[3]
            voltage = data[4]
            amperage = data[5]
            groundSpeed = data[6]
            print("State Msg: apmState = {:d}, driveState = {:d}, autoState = {:d}, autoFlag = {:d}, voltage = {:0.2f}, amperage = {:0.2f}, groundSpeed = {:0.2f}\n".format(apmState, driveState, autoState, autoFlag, voltage/10.0, amperage/10.0, groundSpeed/10.0),end = '')
            outfile.write("{:d}:{:d}:{:d}:{:d}:{:d}:{:0.2f}:{:0.2f}:{:0.2f}\n".format(id, apmState, driveState, autoState, autoFlag, voltage/10.0, amperage/10.0, groundSpeed/10.0))
        elif id == int('0x70',16): #Configuration Msg type
            print("Configuration MSG recived (not defined)\n",end = '')                
            outfile.write("{:d}\n".format(id))
        elif id == int('0x80',16): #Control Msg type
            speed = data[0] | np.left_shift(data[1],8)
            steering = data[2]
            print("Control Msg: Speed = {:0.2f}, steering = {}\n".format(speed/100.0, steering),end = '')
            outfile.write("{:d}:{:0.2f}:{}\n".format(id, speed/100.0, steering))
        elif id == int('0x81',16): #Waypoint Msg type
            latStart_min = data[0] | np.left_shift(data[1],8)
            latStart_frac = data[2] | np.left_shift(data[3],8) | np.left_shift(data[4],16) | np.left_shift(data[5],24)
            lonStart_min = data[6] | np.left_shift(data[7],8)
            lonStart_frac = data[8] | np.left_shift(data[9],8) | np.left_shift(data[10],16) | np.left_shift(data[11],24)
            latIntermediate_min = data[12] | np.left_shift(data[13],8)
            latIntermediate_frac = data[14] | np.left_shift(data[15],8) | np.left_shift(data[16],16) | np.left_shift(data[17],24)
            lonIntermediate_min = data[18] | np.left_shift(data[19],8)
            lonIntermediate_frac = data[20] | np.left_shift(data[21],8) | np.left_shift(data[22],16) | np.left_shift(data[23],24)
            latTarget_min = data[24] | np.left_shift(data[25],8)
            latTarget_frac = data[26] | np.left_shift(data[27],8) | np.left_shift(data[28],16) | np.left_shift(data[29],24)
            lonTarget_min = data[30] | np.left_shift(data[31],8)
            lonTarget_frac = data[32] | np.left_shift(data[33],8) | np.left_shift(data[34],16) | np.left_shift(data[35],24)
            pathHeading = data[36] | np.left_shift(data[37],8)
            print("Waypoint Msg: latStart = {:0.7f}, lonStart = {:0.7f}, latInter = {:0.7f}, lonInter = {:0.7f}, latTarget = {:0.7f}, lonTarget = {:0.7f}, pathHead = {:0.2f}\n".format(gps_ang_to_float(latStart_min,latStart_frac), gps_ang_to_float(lonStart_min,lonStart_frac), gps_ang_to_float(latIntermediate_min,latIntermediate_frac), gps_ang_to_float(lonIntermediate_min,lonIntermediate_frac), gps_ang_to_float(latTarget_min,latTarget_frac), gps_ang_to_float(lonTarget_min,lonTarget_frac), pathHeading/100.0),end = '')
            outfile.write("{:d}:{:0.7f}:{:0.7f}:{:0.7f}:{:0.7f}:{:0.7f}:{:0.7f}:{:0.2f}\n".format(id, gps_ang_to_float(latStart_min,latStart_frac), gps_ang_to_float(lonStart_min,lonStart_frac), gps_ang_to_float(latIntermediate_min,latIntermediate_frac), gps_ang_to_float(lonIntermediate_min,lonIntermediate_frac), gps_ang_to_float(latTarget_min,latTarget_frac), gps_ang_to_float(lonTarget_min,lonTarget_frac), pathHeading/100.0))
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
        
