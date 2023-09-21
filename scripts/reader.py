#!/usr/bin/env python

import argparse
import numpy as np
from multiprocessing import Array, Process, RLock
import os.path
from rich.progress import Progress, TextColumn
import serial
import time

import data_decoder
import live_debug_plotter

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

DATARATE_WARNING = 40.0
BUFFER_WARNING = 200

ARRAY_FIELDS = [
    'bot_lat',
    'bot_lon',
    'bot_heading',
    'wp1_lat',
    'wp1_lon',
    'wp2_lat',
    'wp2_lon',
    'sc_steering_angle',
    'true_steering_angle',
    'path_heading',
    'heading_error',
    'crosstrack_error']
ARRAY_FIELD_TO_IDX = {field: idx for idx, field in enumerate(ARRAY_FIELDS)}

# runs on separate core
def update_plot(array, array_lock):
    debug_plotter = live_debug_plotter.DebugPlotter()
    while True:
        array_lock.acquire()
        bot_lat = array[ARRAY_FIELD_TO_IDX['bot_lat']]
        bot_lon = array[ARRAY_FIELD_TO_IDX['bot_lon']]
        bot_heading = array[ARRAY_FIELD_TO_IDX['bot_heading']]
        wp1_lat = array[ARRAY_FIELD_TO_IDX['wp1_lat']]
        wp1_lon = array[ARRAY_FIELD_TO_IDX['wp1_lon']]
        wp2_lat = array[ARRAY_FIELD_TO_IDX['wp2_lat']]
        wp2_lon = array[ARRAY_FIELD_TO_IDX['wp2_lon']]
        sc_steering_angle = array[ARRAY_FIELD_TO_IDX['sc_steering_angle']]
        true_steering_angle = array[ARRAY_FIELD_TO_IDX['true_steering_angle']]
        path_heading = array[ARRAY_FIELD_TO_IDX['path_heading']]
        heading_error = array[ARRAY_FIELD_TO_IDX['heading_error']]
        crosstrack_error = array[ARRAY_FIELD_TO_IDX['crosstrack_error']]
        array_lock.release()

        debug_plotter.update(
            bot_lat=bot_lat,
            bot_lon=bot_lon,
            bot_heading=bot_heading,
            wp1_lat=wp1_lat,
            wp1_lon=wp1_lon,
            wp2_lat=wp2_lat,
            wp2_lon=wp2_lon,
            sc_steering_angle=sc_steering_angle,
            true_steering_angle=true_steering_angle,
            path_heading=path_heading,
            heading_error=heading_error,
            crosstrack_error=crosstrack_error)

        time.sleep(0.1) # plot updates around 10 Hz

class Reader:
    def __init__(self, port, outfile, live_plotter=False):
        # Configure and open serial port
        self.ser = serial.Serial(port, 115200, timeout=1)

        self.decoder = data_decoder.DataDecoder(outfile)
        self.outfile = outfile

        self.live_plotter = live_plotter
        if self.live_plotter:
            self.array_lock = RLock()
            # initialize array to all zeroes
            self.array = Array('d', [0.0] * len(ARRAY_FIELD_TO_IDX), lock=self.array_lock)
            update_process = Process(target=update_plot, args=(self.array, self.array_lock))
            update_process.start()

    @staticmethod
    def calc_crc(crc_buff):
        # start crc as 0x0001
        crc = np.frombuffer(b"\x01\x00", np.uint16)
        crc = crc[0]

        table = np.frombuffer(crctable, np.uint16)

        for x in crc_buff:
            index = (np.right_shift(crc,8) ^ x)
            #print("{},{},{},{}".format(crc,x,index,table[index]))
            crc = (np.left_shift(crc,8) ^ table[index]) & 0xFFFF

        return crc

    @staticmethod
    def find_header(buf):
        header_bytes = 0
        loc = 0

        for x in buf:
            if header_bytes == 0 and x == int('0x51', 16):
                header_bytes = 1
            elif header_bytes == 1 and x == int('0xAC', 16):
                return loc - 1
            else:
                header_bytes = 0
            loc += 1

        return -1

    @staticmethod
    def check_for_msg(buf, header_loc):
        len_idx = header_loc + 2

        if len(buf) < header_loc + 6:
            # too short for a full msg
            return False
        elif len(buf) < header_loc + 3 + buf[len_idx]:
            return False

        return True

    def update_array(self, fields):
        # the array is shared between two separate processes
        self.array_lock.acquire()
        for field, value in fields:
            self.array[ARRAY_FIELD_TO_IDX[field]] = value
        self.array_lock.release()

    def process_msg(self, buf, header_loc):
        # extract msg components
        pkt_len = buf[header_loc + 2]
        if pkt_len < 3:
            # Remove just the header and try again
            buf = buf[(header_loc + 2):]
            return buf

        msg_id = buf[header_loc + 3]
        data = buf[(header_loc + 4):(header_loc + 4 + pkt_len - 3)]
        crc_buff = buf[(header_loc + 3):(header_loc + 3 + pkt_len - 2)]
        crc_bytes = buf[(header_loc + 3 + pkt_len - 2):(header_loc + 3 + pkt_len)]
        crc = np.left_shift(crc_bytes[0], 8) + crc_bytes[1]

        # verify no msg corruption
        if crc == Reader.calc_crc(crc_buff):
            msg_str, msg = self.decoder.decode_data(data, msg_id, pkt_len)

            if self.live_plotter:
                if msg_str.split('Stamped')[-1] == 'RawPosition': # RawPosition or StampedRawPosition
                    self.update_array([
                        ('bot_lat', msg.latitude),
                        ('bot_lon', msg.longitude)])
                elif msg_str.split('Stamped')[-1] == 'Orientation':  # Orientation or StampedOrientation
                    self.update_array([('bot_heading', msg.heading)])
                elif msg_str.split('Stamped')[-1] == 'SteeringController': # SteeringController or StampedSteeringController
                    self.update_array([
                        ('sc_steering_angle', msg.sc_steering),
                        ('true_steering_angle', msg.true_steering),
                        ('heading_error', msg.heading_error),
                        ('crosstrack_error', msg.crosstrack_error)])
                elif msg_str.split('Stamped')[-1] == 'Waypoint': # Waypoint or StampedWaypoint
                    assert isinstance(msg, data_decoder.Waypoint)
                    self.update_array([
                        ('wp1_lat', msg.lat_start),
                        ('wp1_lon', msg.lon_start),
                        ('wp2_lat', msg.lat_target),
                        ('wp2_lon', msg.lon_target),
                        ('path_heading', msg.path_heading)])
        else:
            print("Error: CRC does not match recieved")
            # remove just the header and try again
            buf = buf[(header_loc + 2):len(buf)]
            return buf

        # remove processed message from input buffer
        buf = buf[(header_loc + 3 + pkt_len):len(buf)]
        return buf

    def start(self):
        buf = bytes()
        # todo progress bar isn't really intended for this, maybe there's a better tool in the rich library
        with Progress(TextColumn('{task.description}')) as progress:
            task = progress.add_task('')
            warning_task = None
            prev_time = time.time()
            max_num_bytes_in_buffer = 0
            num_bytes_read = []
            num_bytes_in_buffer = []

            while True:
                # get number of bytes accumulated since last reading
                num_bytes_in_buffer.append(self.ser.in_waiting)

                # Read and process data from file
                new_bytes = self.ser.read(80)
                read_size = len(new_bytes)

                # set the progress bar with datarate/buffer information
                cur_time = time.time()
                num_bytes_read.append(read_size)
                if cur_time - prev_time > 1.0:
                    # only update status bar once per second (good window size for data as well)
                    processed_kbits = sum(num_bytes_read) / 125.0
                    processed_kbps = processed_kbits / (cur_time - prev_time)
                    max_num_bytes_in_buffer = max(max_num_bytes_in_buffer, max(num_bytes_in_buffer))
                    avg_bytes_in_buffer = round(sum(num_bytes_in_buffer) / len(num_bytes_in_buffer))

                    if processed_kbits > DATARATE_WARNING or avg_bytes_in_buffer > BUFFER_WARNING:
                        # handle any warnings
                        if warning_task is None:
                            warning_task = progress.add_task('')

                        warning_msg = ''
                        if processed_kbits > DATARATE_WARNING:
                            warning_msg = \
                                '[red]Warning: High datarate! The APM is likely '\
                                'bogged down which could cause unexpected behavior.'
                        elif avg_bytes_in_buffer > BUFFER_WARNING:
                            warning_msg = \
                                '[red]Read input buffer is too large. The Debug '\
                                'reader is likely unable to keep up.'
                        progress.update(warning_task, description=warning_msg)
                    else:
                        # no warnings (remove warning line)
                        if warning_task is not None:
                            progress.remove_task(warning_task)
                            warning_task = None

                    status_str = f"[green]Processing Bitrate: {processed_kbps:5.2f} kbps "\
                                 f"[blue]Input Buffer: {avg_bytes_in_buffer:3d} B (max: {max_num_bytes_in_buffer:3d} B)"
                    progress.update(task, description=status_str)

                    # clear the data for the next window
                    num_bytes_read = []
                    num_bytes_in_buffer = []

                    prev_time = cur_time

                if read_size + len(buf) < 512:
                    buf += new_bytes
                else:
                    print("Error: buffer overflow")

                header_loc = -1
                full_msg = False
                check_buff = True

                while check_buff:
                    header_loc = Reader.find_header(buf)
                    if header_loc >= 0:
                        full_msg = Reader.check_for_msg(buf, header_loc)
                        if full_msg:
                            buf = self.process_msg(buf, header_loc)
                        else:
                            check_buff = False
                    else:
                        # Garbage...toss all but last byte
                        buf = buf[(len(buf) - 1):]
                        check_buff = False

def outfile_name(args):
    if args.outfile != None:
        return args.outfile
    elif args.infile != None:
        return "decoded_" + args.infile
    else:
        return str(int(time.time())) + ".log"


if __name__ == "__main__":
    # Gather arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', 
                        help='Input file with encoded log data.')
    parser.add_argument('-o', '--outfile', 
                        help='Optional - output file with decooded log data.')
    parser.add_argument('-p', '--port', 
                        help='Serial port path to read encoded data.')
    parser.add_argument('-l', '--live-plotter', action='store_true',
                        help='Flag to enable live plotting')
    args = parser.parse_args()

    if args.infile != None and args.port != None:
        print("Error: Both input file (-i) and serial port (-p) cannot be specified simultaneously.")
        parser.print_help()
        exit()

    filename = outfile_name(args)
    try:
        if args.infile != None:
            # File decoding (file as input)
            if not os.path.exists(args.infile):
                print("Error: Input file does not exist: {}".format(args.infile))
            print(args.infile)

            # Read and process logged data
            with open(args.infile, 'r') as f:
                for line in f.readlines():
                    msg_type, msg = data_decoder.read_log_dataline(dataline=line, print_line=True)
        elif args.port != None:
            # Create output file for decoded data
            with open(filename, 'x') as outfile:
                # Live decoding (serial port)
                try:
                    reader = Reader(port=args.port, outfile=outfile, live_plotter=args.live_plotter)
                    reader.start()
                except serial.SerialException:
                    print("Error: Could not open serial port - {}".format(args.port))
                    exit()
        else:
            print("Error: Input file (-i) or serial port (-p) is required.")
            parser.print_help()
            exit()
    except IOError:
        print("Error: Could not create output file - {}".format(args.outfile))
        exit()        
