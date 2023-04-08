# This file was auto-generated. Any changes to this file may be overwritten.

from collections import namedtuple
from struct import pack, unpack

RawPosition = namedtuple('RawPosition',
    ['latitude',
     'longitude',
     'altitude'])

StampedRawPosition = namedtuple('StampedRawPosition',
    ['timestamp',
     'latitude',
     'longitude',
     'altitude'])

ExtrapolatedPosition = namedtuple('ExtrapolatedPosition',
    ['latitude',
     'longitude',
     'altitude'])

StampedExtrapolatedPosition = namedtuple('StampedExtrapolatedPosition',
    ['timestamp',
     'latitude',
     'longitude',
     'altitude'])

Orientation = namedtuple('Orientation',
    ['heading',
     'roll',
     'pitch'])

StampedOrientation = namedtuple('StampedOrientation',
    ['timestamp',
     'heading',
     'roll',
     'pitch'])

Radio = namedtuple('Radio',
    ['speed',
     'steering'])

StampedRadio = namedtuple('StampedRadio',
    ['timestamp',
     'speed',
     'steering'])

Imu = namedtuple('Imu',
    ['euler_x',
     'euler_y',
     'euler_z',
     'acc_x',
     'acc_y',
     'acc_z',
     'gyro_x',
     'gyro_y',
     'gyro_z',
     'quaternion_w',
     'quaternion_x',
     'quaternion_y',
     'quaternion_z'])

StampedImu = namedtuple('StampedImu',
    ['timestamp',
     'euler_x',
     'euler_y',
     'euler_z',
     'acc_x',
     'acc_y',
     'acc_z',
     'gyro_x',
     'gyro_y',
     'gyro_z',
     'quaternion_w',
     'quaternion_x',
     'quaternion_y',
     'quaternion_z'])

Sonar = namedtuple('Sonar',
    ['ping1',
     'ping2',
     'ping3',
     'ping4',
     'ping5'])

StampedSonar = namedtuple('StampedSonar',
    ['timestamp',
     'ping1',
     'ping2',
     'ping3',
     'ping4',
     'ping5'])

Bumper = namedtuple('Bumper',
    ['left',
     'right'])

StampedBumper = namedtuple('StampedBumper',
    ['timestamp',
     'left',
     'right'])

State = namedtuple('State',
    ['apmState',
     'driveState',
     'autoState',
     'autoFlag',
     'voltage',
     'amperage',
     'groundSpeed'])

StampedState = namedtuple('StampedState',
    ['timestamp',
     'apmState',
     'driveState',
     'autoState',
     'autoFlag',
     'voltage',
     'amperage',
     'groundSpeed'])

Control = namedtuple('Control',
    ['speed',
     'steering',
     'sc_steering',
     'true_steering',
     'k_crosstrack',
     'k_yaw',
     'heading_error',
     'crosstrack_error'])

StampedControl = namedtuple('StampedControl',
    ['timestamp',
     'speed',
     'steering',
     'sc_steering',
     'true_steering',
     'k_crosstrack',
     'k_yaw',
     'heading_error',
     'crosstrack_error'])

Waypoint = namedtuple('Waypoint',
    ['lat_start',
     'lon_start',
     'lat_intermediate',
     'lon_intermediate',
     'lat_target',
     'lon_target',
     'path_heading'])

StampedWaypoint = namedtuple('StampedWaypoint',
    ['timestamp',
     'lat_start',
     'lon_start',
     'lat_intermediate',
     'lon_intermediate',
     'lat_target',
     'lon_target',
     'path_heading'])

Version = namedtuple('Version',
    ['debug_major',
     'debug_minor',
     'apm_major',
     'apm_minor'])

StampedVersion = namedtuple('StampedVersion',
    ['timestamp',
     'debug_major',
     'debug_minor',
     'apm_major',
     'apm_minor'])

Ascii = namedtuple('Ascii', ['ascii'])

def gps_angle_to_float(min, frac):
    deg = min / 60.0
    min_deg = (min - (deg * 60.0) + frac) / 60.0
    return deg + min_deg;        

def ms_to_s(ms):
    return ms / 1000.0

class DataDecoder:
    def __init__(self, outfile):
        self.outfile = outfile
        
    def decode_data(self, data, msg_id, pkt_len):
        if msg_id == int('0x10', 16): # RawPositionMsg_t
            latitude_minutes = unpack('h', pack('BB', data[0], data[1]))[0]
            latitude_frac = unpack('i', pack('BBBB', data[2], data[3], data[4], data[5]))[0] / 100000.0
            longitude_minutes = unpack('h', pack('BB', data[6], data[7]))[0]
            longitude_frac = unpack('i', pack('BBBB', data[8], data[9], data[10], data[11]))[0] / 100000.0
            altitude = unpack('H', pack('BB', data[12], data[13]))[0] / 3.293216 - 900.0
            print(
                f"RawPosition"\
                f" latitude = {gps_angle_to_float(latitude_minutes, latitude_frac):.7f}"\
                f" longitude = {gps_angle_to_float(longitude_minutes, longitude_frac):.7f}"\
                f" altitude = {altitude:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{gps_angle_to_float(latitude_minutes, latitude_frac):.7f}"\
                f"{gps_angle_to_float(longitude_minutes, longitude_frac):.7f}"\
                f"{altitude:f}\n")
            return ('RawPosition',
                    RawPosition(
                        gps_angle_to_float(latitude_minutes, latitude_frac),
                        gps_angle_to_float(longitude_minutes, longitude_frac),
                        altitude))
        elif msg_id == int('0x1A', 16): # StampedRawPositionMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            latitude_minutes = unpack('h', pack('BB', data[4], data[5]))[0]
            latitude_frac = unpack('i', pack('BBBB', data[6], data[7], data[8], data[9]))[0] / 100000.0
            longitude_minutes = unpack('h', pack('BB', data[10], data[11]))[0]
            longitude_frac = unpack('i', pack('BBBB', data[12], data[13], data[14], data[15]))[0] / 100000.0
            altitude = unpack('H', pack('BB', data[16], data[17]))[0] / 3.293216 - 900.0
            print(
                f"StampedRawPosition"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" latitude = {gps_angle_to_float(latitude_minutes, latitude_frac):.7f}"\
                f" longitude = {gps_angle_to_float(longitude_minutes, longitude_frac):.7f}"\
                f" altitude = {altitude:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{gps_angle_to_float(latitude_minutes, latitude_frac):.7f}"\
                f"{gps_angle_to_float(longitude_minutes, longitude_frac):.7f}"\
                f"{altitude:f}\n")
            return ('StampedRawPosition',
                    StampedRawPosition(
                        ms_to_s(timestamp),
                        gps_angle_to_float(latitude_minutes, latitude_frac),
                        gps_angle_to_float(longitude_minutes, longitude_frac),
                        altitude))
        elif msg_id == int('0x11', 16): # ExtrapolatedPositionMsg_t
            latitude_minutes = unpack('h', pack('BB', data[0], data[1]))[0]
            latitude_frac = unpack('i', pack('BBBB', data[2], data[3], data[4], data[5]))[0] / 100000.0
            longitude_minutes = unpack('h', pack('BB', data[6], data[7]))[0]
            longitude_frac = unpack('i', pack('BBBB', data[8], data[9], data[10], data[11]))[0] / 100000.0
            altitude = unpack('H', pack('BB', data[12], data[13]))[0] / 3.293216 - 900.0
            print(
                f"ExtrapolatedPosition"\
                f" latitude = {gps_angle_to_float(latitude_minutes, latitude_frac):.7f}"\
                f" longitude = {gps_angle_to_float(longitude_minutes, longitude_frac):.7f}"\
                f" altitude = {altitude:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{gps_angle_to_float(latitude_minutes, latitude_frac):.7f}"\
                f"{gps_angle_to_float(longitude_minutes, longitude_frac):.7f}"\
                f"{altitude:f}\n")
            return ('ExtrapolatedPosition',
                    ExtrapolatedPosition(
                        gps_angle_to_float(latitude_minutes, latitude_frac),
                        gps_angle_to_float(longitude_minutes, longitude_frac),
                        altitude))
        elif msg_id == int('0x1B', 16): # StampedExtrapolatedPositionMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            latitude_minutes = unpack('h', pack('BB', data[4], data[5]))[0]
            latitude_frac = unpack('i', pack('BBBB', data[6], data[7], data[8], data[9]))[0] / 100000.0
            longitude_minutes = unpack('h', pack('BB', data[10], data[11]))[0]
            longitude_frac = unpack('i', pack('BBBB', data[12], data[13], data[14], data[15]))[0] / 100000.0
            altitude = unpack('H', pack('BB', data[16], data[17]))[0] / 3.293216 - 900.0
            print(
                f"StampedExtrapolatedPosition"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" latitude = {gps_angle_to_float(latitude_minutes, latitude_frac):.7f}"\
                f" longitude = {gps_angle_to_float(longitude_minutes, longitude_frac):.7f}"\
                f" altitude = {altitude:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{gps_angle_to_float(latitude_minutes, latitude_frac):.7f}"\
                f"{gps_angle_to_float(longitude_minutes, longitude_frac):.7f}"\
                f"{altitude:f}\n")
            return ('StampedExtrapolatedPosition',
                    StampedExtrapolatedPosition(
                        ms_to_s(timestamp),
                        gps_angle_to_float(latitude_minutes, latitude_frac),
                        gps_angle_to_float(longitude_minutes, longitude_frac),
                        altitude))
        elif msg_id == int('0x20', 16): # OrientationMsg_t
            heading = unpack('h', pack('BB', data[0], data[1]))[0] / 100.0
            roll = unpack('h', pack('BB', data[2], data[3]))[0] / 100.0
            pitch = unpack('h', pack('BB', data[4], data[5]))[0] / 100.0
            print(
                f"Orientation"\
                f" heading = {heading:.2f}"\
                f" roll = {roll:.2f}"\
                f" pitch = {pitch:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{heading:.2f}"\
                f"{roll:.2f}"\
                f"{pitch:.2f}\n")
            return ('Orientation',
                    Orientation(
                        heading,
                        roll,
                        pitch))
        elif msg_id == int('0x2A', 16): # StampedOrientationMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            heading = unpack('h', pack('BB', data[4], data[5]))[0] / 100.0
            roll = unpack('h', pack('BB', data[6], data[7]))[0] / 100.0
            pitch = unpack('h', pack('BB', data[8], data[9]))[0] / 100.0
            print(
                f"StampedOrientation"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" heading = {heading:.2f}"\
                f" roll = {roll:.2f}"\
                f" pitch = {pitch:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{heading:.2f}"\
                f"{roll:.2f}"\
                f"{pitch:.2f}\n")
            return ('StampedOrientation',
                    StampedOrientation(
                        ms_to_s(timestamp),
                        heading,
                        roll,
                        pitch))
        elif msg_id == int('0x30', 16): # RadioMsg_t
            speed = unpack('h', pack('BB', data[0], data[1]))[0] / 100.0
            steering = unpack('B', pack('B', data[2]))[0]
            print(
                f"Radio"\
                f" speed = {speed:.2f}"\
                f" steering = {steering:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{speed:.2f}"\
                f"{steering:d}\n")
            return ('Radio',
                    Radio(
                        speed,
                        steering))
        elif msg_id == int('0x3A', 16): # StampedRadioMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            speed = unpack('h', pack('BB', data[4], data[5]))[0] / 100.0
            steering = unpack('B', pack('B', data[6]))[0]
            print(
                f"StampedRadio"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" speed = {speed:.2f}"\
                f" steering = {steering:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{speed:.2f}"\
                f"{steering:d}\n")
            return ('StampedRadio',
                    StampedRadio(
                        ms_to_s(timestamp),
                        speed,
                        steering))
        elif msg_id == int('0x40', 16): # ImuMsg_t
            euler_x = unpack('h', pack('BB', data[0], data[1]))[0] / 10430.0
            euler_y = unpack('h', pack('BB', data[2], data[3]))[0] / 10430.0
            euler_z = unpack('h', pack('BB', data[4], data[5]))[0] / 10430.0
            acc_x = unpack('h', pack('BB', data[6], data[7]))[0] / 8192.0
            acc_y = unpack('h', pack('BB', data[8], data[9]))[0] / 8192.0
            acc_z = unpack('h', pack('BB', data[10], data[11]))[0] / 8192.0
            gyro_x = unpack('h', pack('BB', data[12], data[13]))[0] / 16.4
            gyro_y = unpack('h', pack('BB', data[14], data[15]))[0] / 16.4
            gyro_z = unpack('h', pack('BB', data[16], data[17]))[0] / 16.4
            quaternion_w = unpack('h', pack('BB', data[18], data[19]))[0] / 16384.0
            quaternion_x = unpack('h', pack('BB', data[20], data[21]))[0] / 16384.0
            quaternion_y = unpack('h', pack('BB', data[22], data[23]))[0] / 16384.0
            quaternion_z = unpack('h', pack('BB', data[24], data[25]))[0] / 16384.0
            print(
                f"Imu"\
                f" euler_x = {euler_x:.2f}"\
                f" euler_y = {euler_y:.2f}"\
                f" euler_z = {euler_z:.2f}"\
                f" acc_x = {acc_x:.2f}"\
                f" acc_y = {acc_y:.2f}"\
                f" acc_z = {acc_z:.2f}"\
                f" gyro_x = {gyro_x:.2f}"\
                f" gyro_y = {gyro_y:.2f}"\
                f" gyro_z = {gyro_z:.2f}"\
                f" quaternion_w = {quaternion_w:.2f}"\
                f" quaternion_x = {quaternion_x:.2f}"\
                f" quaternion_y = {quaternion_y:.2f}"\
                f" quaternion_z = {quaternion_z:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{euler_x:.2f}"\
                f"{euler_y:.2f}"\
                f"{euler_z:.2f}"\
                f"{acc_x:.2f}"\
                f"{acc_y:.2f}"\
                f"{acc_z:.2f}"\
                f"{gyro_x:.2f}"\
                f"{gyro_y:.2f}"\
                f"{gyro_z:.2f}"\
                f"{quaternion_w:.2f}"\
                f"{quaternion_x:.2f}"\
                f"{quaternion_y:.2f}"\
                f"{quaternion_z:.2f}\n")
            return ('Imu',
                    Imu(
                        euler_x,
                        euler_y,
                        euler_z,
                        acc_x,
                        acc_y,
                        acc_z,
                        gyro_x,
                        gyro_y,
                        gyro_z,
                        quaternion_w,
                        quaternion_x,
                        quaternion_y,
                        quaternion_z))
        elif msg_id == int('0x4A', 16): # StampedImuMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            euler_x = unpack('h', pack('BB', data[4], data[5]))[0] / 10430.0
            euler_y = unpack('h', pack('BB', data[6], data[7]))[0] / 10430.0
            euler_z = unpack('h', pack('BB', data[8], data[9]))[0] / 10430.0
            acc_x = unpack('h', pack('BB', data[10], data[11]))[0] / 8192.0
            acc_y = unpack('h', pack('BB', data[12], data[13]))[0] / 8192.0
            acc_z = unpack('h', pack('BB', data[14], data[15]))[0] / 8192.0
            gyro_x = unpack('h', pack('BB', data[16], data[17]))[0] / 16.4
            gyro_y = unpack('h', pack('BB', data[18], data[19]))[0] / 16.4
            gyro_z = unpack('h', pack('BB', data[20], data[21]))[0] / 16.4
            quaternion_w = unpack('h', pack('BB', data[22], data[23]))[0] / 16384.0
            quaternion_x = unpack('h', pack('BB', data[24], data[25]))[0] / 16384.0
            quaternion_y = unpack('h', pack('BB', data[26], data[27]))[0] / 16384.0
            quaternion_z = unpack('h', pack('BB', data[28], data[29]))[0] / 16384.0
            print(
                f"StampedImu"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" euler_x = {euler_x:.2f}"\
                f" euler_y = {euler_y:.2f}"\
                f" euler_z = {euler_z:.2f}"\
                f" acc_x = {acc_x:.2f}"\
                f" acc_y = {acc_y:.2f}"\
                f" acc_z = {acc_z:.2f}"\
                f" gyro_x = {gyro_x:.2f}"\
                f" gyro_y = {gyro_y:.2f}"\
                f" gyro_z = {gyro_z:.2f}"\
                f" quaternion_w = {quaternion_w:.2f}"\
                f" quaternion_x = {quaternion_x:.2f}"\
                f" quaternion_y = {quaternion_y:.2f}"\
                f" quaternion_z = {quaternion_z:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{euler_x:.2f}"\
                f"{euler_y:.2f}"\
                f"{euler_z:.2f}"\
                f"{acc_x:.2f}"\
                f"{acc_y:.2f}"\
                f"{acc_z:.2f}"\
                f"{gyro_x:.2f}"\
                f"{gyro_y:.2f}"\
                f"{gyro_z:.2f}"\
                f"{quaternion_w:.2f}"\
                f"{quaternion_x:.2f}"\
                f"{quaternion_y:.2f}"\
                f"{quaternion_z:.2f}\n")
            return ('StampedImu',
                    StampedImu(
                        ms_to_s(timestamp),
                        euler_x,
                        euler_y,
                        euler_z,
                        acc_x,
                        acc_y,
                        acc_z,
                        gyro_x,
                        gyro_y,
                        gyro_z,
                        quaternion_w,
                        quaternion_x,
                        quaternion_y,
                        quaternion_z))
        elif msg_id == int('0x41', 16): # SonarMsg_t
            ping1 = unpack('h', pack('BB', data[0], data[1]))[0]
            ping2 = unpack('h', pack('BB', data[2], data[3]))[0]
            ping3 = unpack('h', pack('BB', data[4], data[5]))[0]
            ping4 = unpack('h', pack('BB', data[6], data[7]))[0]
            ping5 = unpack('h', pack('BB', data[8], data[9]))[0]
            print(
                f"Sonar"\
                f" ping1 = {ping1:d}"\
                f" ping2 = {ping2:d}"\
                f" ping3 = {ping3:d}"\
                f" ping4 = {ping4:d}"\
                f" ping5 = {ping5:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ping1:d}"\
                f"{ping2:d}"\
                f"{ping3:d}"\
                f"{ping4:d}"\
                f"{ping5:d}\n")
            return ('Sonar',
                    Sonar(
                        ping1,
                        ping2,
                        ping3,
                        ping4,
                        ping5))
        elif msg_id == int('0x4B', 16): # StampedSonarMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            ping1 = unpack('h', pack('BB', data[4], data[5]))[0]
            ping2 = unpack('h', pack('BB', data[6], data[7]))[0]
            ping3 = unpack('h', pack('BB', data[8], data[9]))[0]
            ping4 = unpack('h', pack('BB', data[10], data[11]))[0]
            ping5 = unpack('h', pack('BB', data[12], data[13]))[0]
            print(
                f"StampedSonar"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" ping1 = {ping1:d}"\
                f" ping2 = {ping2:d}"\
                f" ping3 = {ping3:d}"\
                f" ping4 = {ping4:d}"\
                f" ping5 = {ping5:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{ping1:d}"\
                f"{ping2:d}"\
                f"{ping3:d}"\
                f"{ping4:d}"\
                f"{ping5:d}\n")
            return ('StampedSonar',
                    StampedSonar(
                        ms_to_s(timestamp),
                        ping1,
                        ping2,
                        ping3,
                        ping4,
                        ping5))
        elif msg_id == int('0x42', 16): # BumperMsg_t
            left = unpack('b', pack('B', data[0]))[0]
            right = unpack('b', pack('B', data[1]))[0]
            print(
                f"Bumper"\
                f" left = {left:d}"\
                f" right = {right:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{left:d}"\
                f"{right:d}\n")
            return ('Bumper',
                    Bumper(
                        left,
                        right))
        elif msg_id == int('0x4C', 16): # StampedBumperMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            left = unpack('b', pack('B', data[4]))[0]
            right = unpack('b', pack('B', data[5]))[0]
            print(
                f"StampedBumper"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" left = {left:d}"\
                f" right = {right:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{left:d}"\
                f"{right:d}\n")
            return ('StampedBumper',
                    StampedBumper(
                        ms_to_s(timestamp),
                        left,
                        right))
        elif msg_id == int('0x60', 16): # StateMsg_t
            apmState = unpack('B', pack('B', data[0]))[0]
            driveState = unpack('B', pack('B', data[1]))[0]
            autoState = unpack('B', pack('B', data[2]))[0]
            autoFlag = unpack('B', pack('B', data[3]))[0]
            voltage = unpack('B', pack('B', data[4]))[0] / 10.0
            amperage = unpack('B', pack('B', data[5]))[0] / 10.0
            groundSpeed = unpack('B', pack('B', data[6]))[0] / 10.0
            print(
                f"State"\
                f" apmState = {apmState:d}"\
                f" driveState = {driveState:d}"\
                f" autoState = {autoState:d}"\
                f" autoFlag = {autoFlag:d}"\
                f" voltage = {voltage:f}"\
                f" amperage = {amperage:f}"\
                f" groundSpeed = {groundSpeed:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{apmState:d}"\
                f"{driveState:d}"\
                f"{autoState:d}"\
                f"{autoFlag:d}"\
                f"{voltage:f}"\
                f"{amperage:f}"\
                f"{groundSpeed:f}\n")
            return ('State',
                    State(
                        apmState,
                        driveState,
                        autoState,
                        autoFlag,
                        voltage,
                        amperage,
                        groundSpeed))
        elif msg_id == int('0x6A', 16): # StampedStateMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            apmState = unpack('B', pack('B', data[4]))[0]
            driveState = unpack('B', pack('B', data[5]))[0]
            autoState = unpack('B', pack('B', data[6]))[0]
            autoFlag = unpack('B', pack('B', data[7]))[0]
            voltage = unpack('B', pack('B', data[8]))[0] / 10.0
            amperage = unpack('B', pack('B', data[9]))[0] / 10.0
            groundSpeed = unpack('B', pack('B', data[10]))[0] / 10.0
            print(
                f"StampedState"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" apmState = {apmState:d}"\
                f" driveState = {driveState:d}"\
                f" autoState = {autoState:d}"\
                f" autoFlag = {autoFlag:d}"\
                f" voltage = {voltage:f}"\
                f" amperage = {amperage:f}"\
                f" groundSpeed = {groundSpeed:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{apmState:d}"\
                f"{driveState:d}"\
                f"{autoState:d}"\
                f"{autoFlag:d}"\
                f"{voltage:f}"\
                f"{amperage:f}"\
                f"{groundSpeed:f}\n")
            return ('StampedState',
                    StampedState(
                        ms_to_s(timestamp),
                        apmState,
                        driveState,
                        autoState,
                        autoFlag,
                        voltage,
                        amperage,
                        groundSpeed))
        elif msg_id == int('0x80', 16): # ControlMsg_t
            speed = unpack('h', pack('BB', data[0], data[1]))[0] / 100.0
            steering = unpack('B', pack('B', data[2]))[0]
            sc_steering = unpack('h', pack('BB', data[3], data[4]))[0] / 100.0
            true_steering = unpack('h', pack('BB', data[5], data[6]))[0] / 100.0
            k_crosstrack = unpack('h', pack('BB', data[7], data[8]))[0] / 1000.0
            k_yaw = unpack('h', pack('BB', data[9], data[10]))[0] / 1000.0
            heading_error = unpack('h', pack('BB', data[11], data[12]))[0] / 100.0
            crosstrack_error = unpack('h', pack('BB', data[13], data[14]))[0] / 100.0
            print(
                f"Control"\
                f" speed = {speed:.2f}"\
                f" steering = {steering:d}"\
                f" sc_steering = {sc_steering:.2f}"\
                f" true_steering = {true_steering:.2f}"\
                f" k_crosstrack = {k_crosstrack:.4f}"\
                f" k_yaw = {k_yaw:.4f}"\
                f" heading_error = {heading_error:.2f}"\
                f" crosstrack_error = {crosstrack_error:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{speed:.2f}"\
                f"{steering:d}"\
                f"{sc_steering:.2f}"\
                f"{true_steering:.2f}"\
                f"{k_crosstrack:.4f}"\
                f"{k_yaw:.4f}"\
                f"{heading_error:.2f}"\
                f"{crosstrack_error:.2f}\n")
            return ('Control',
                    Control(
                        speed,
                        steering,
                        sc_steering,
                        true_steering,
                        k_crosstrack,
                        k_yaw,
                        heading_error,
                        crosstrack_error))
        elif msg_id == int('0x8A', 16): # StampedControlMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            speed = unpack('h', pack('BB', data[4], data[5]))[0] / 100.0
            steering = unpack('B', pack('B', data[6]))[0]
            sc_steering = unpack('h', pack('BB', data[7], data[8]))[0] / 100.0
            true_steering = unpack('h', pack('BB', data[9], data[10]))[0] / 100.0
            k_crosstrack = unpack('h', pack('BB', data[11], data[12]))[0] / 1000.0
            k_yaw = unpack('h', pack('BB', data[13], data[14]))[0] / 1000.0
            heading_error = unpack('h', pack('BB', data[15], data[16]))[0] / 100.0
            crosstrack_error = unpack('h', pack('BB', data[17], data[18]))[0] / 100.0
            print(
                f"StampedControl"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" speed = {speed:.2f}"\
                f" steering = {steering:d}"\
                f" sc_steering = {sc_steering:.2f}"\
                f" true_steering = {true_steering:.2f}"\
                f" k_crosstrack = {k_crosstrack:.4f}"\
                f" k_yaw = {k_yaw:.4f}"\
                f" heading_error = {heading_error:.2f}"\
                f" crosstrack_error = {crosstrack_error:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{speed:.2f}"\
                f"{steering:d}"\
                f"{sc_steering:.2f}"\
                f"{true_steering:.2f}"\
                f"{k_crosstrack:.4f}"\
                f"{k_yaw:.4f}"\
                f"{heading_error:.2f}"\
                f"{crosstrack_error:.2f}\n")
            return ('StampedControl',
                    StampedControl(
                        ms_to_s(timestamp),
                        speed,
                        steering,
                        sc_steering,
                        true_steering,
                        k_crosstrack,
                        k_yaw,
                        heading_error,
                        crosstrack_error))
        elif msg_id == int('0x81', 16): # WaypointMsg_t
            lat_start_minutes = unpack('h', pack('BB', data[0], data[1]))[0]
            lat_start_frac = unpack('i', pack('BBBB', data[2], data[3], data[4], data[5]))[0] / 100000.0
            lon_start_minutes = unpack('h', pack('BB', data[6], data[7]))[0]
            lon_start_frac = unpack('i', pack('BBBB', data[8], data[9], data[10], data[11]))[0] / 100000.0
            lat_intermediate_minutes = unpack('h', pack('BB', data[12], data[13]))[0]
            lat_intermediate_frac = unpack('i', pack('BBBB', data[14], data[15], data[16], data[17]))[0] / 100000.0
            lon_intermediate_minutes = unpack('h', pack('BB', data[18], data[19]))[0]
            lon_intermediate_frac = unpack('i', pack('BBBB', data[20], data[21], data[22], data[23]))[0] / 100000.0
            lat_target_minutes = unpack('h', pack('BB', data[24], data[25]))[0]
            lat_target_frac = unpack('i', pack('BBBB', data[26], data[27], data[28], data[29]))[0] / 100000.0
            lon_target_minutes = unpack('h', pack('BB', data[30], data[31]))[0]
            lon_target_frac = unpack('i', pack('BBBB', data[32], data[33], data[34], data[35]))[0] / 100000.0
            path_heading = unpack('h', pack('BB', data[36], data[37]))[0] / 100.0
            print(
                f"Waypoint"\
                f" lat_start = {gps_angle_to_float(lat_start_minutes, lat_start_frac):.7f}"\
                f" lon_start = {gps_angle_to_float(lon_start_minutes, lon_start_frac):.7f}"\
                f" lat_intermediate = {gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac):.7f}"\
                f" lon_intermediate = {gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac):.7f}"\
                f" lat_target = {gps_angle_to_float(lat_target_minutes, lat_target_frac):.7f}"\
                f" lon_target = {gps_angle_to_float(lon_target_minutes, lon_target_frac):.7f}"\
                f" path_heading = {path_heading:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{gps_angle_to_float(lat_start_minutes, lat_start_frac):.7f}"\
                f"{gps_angle_to_float(lon_start_minutes, lon_start_frac):.7f}"\
                f"{gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac):.7f}"\
                f"{gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac):.7f}"\
                f"{gps_angle_to_float(lat_target_minutes, lat_target_frac):.7f}"\
                f"{gps_angle_to_float(lon_target_minutes, lon_target_frac):.7f}"\
                f"{path_heading:f}\n")
            return ('Waypoint',
                    Waypoint(
                        gps_angle_to_float(lat_start_minutes, lat_start_frac),
                        gps_angle_to_float(lon_start_minutes, lon_start_frac),
                        gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac),
                        gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac),
                        gps_angle_to_float(lat_target_minutes, lat_target_frac),
                        gps_angle_to_float(lon_target_minutes, lon_target_frac),
                        path_heading))
        elif msg_id == int('0x8B', 16): # StampedWaypointMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            lat_start_minutes = unpack('h', pack('BB', data[4], data[5]))[0]
            lat_start_frac = unpack('i', pack('BBBB', data[6], data[7], data[8], data[9]))[0] / 100000.0
            lon_start_minutes = unpack('h', pack('BB', data[10], data[11]))[0]
            lon_start_frac = unpack('i', pack('BBBB', data[12], data[13], data[14], data[15]))[0] / 100000.0
            lat_intermediate_minutes = unpack('h', pack('BB', data[16], data[17]))[0]
            lat_intermediate_frac = unpack('i', pack('BBBB', data[18], data[19], data[20], data[21]))[0] / 100000.0
            lon_intermediate_minutes = unpack('h', pack('BB', data[22], data[23]))[0]
            lon_intermediate_frac = unpack('i', pack('BBBB', data[24], data[25], data[26], data[27]))[0] / 100000.0
            lat_target_minutes = unpack('h', pack('BB', data[28], data[29]))[0]
            lat_target_frac = unpack('i', pack('BBBB', data[30], data[31], data[32], data[33]))[0] / 100000.0
            lon_target_minutes = unpack('h', pack('BB', data[34], data[35]))[0]
            lon_target_frac = unpack('i', pack('BBBB', data[36], data[37], data[38], data[39]))[0] / 100000.0
            path_heading = unpack('h', pack('BB', data[40], data[41]))[0] / 100.0
            print(
                f"StampedWaypoint"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" lat_start = {gps_angle_to_float(lat_start_minutes, lat_start_frac):.7f}"\
                f" lon_start = {gps_angle_to_float(lon_start_minutes, lon_start_frac):.7f}"\
                f" lat_intermediate = {gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac):.7f}"\
                f" lon_intermediate = {gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac):.7f}"\
                f" lat_target = {gps_angle_to_float(lat_target_minutes, lat_target_frac):.7f}"\
                f" lon_target = {gps_angle_to_float(lon_target_minutes, lon_target_frac):.7f}"\
                f" path_heading = {path_heading:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{gps_angle_to_float(lat_start_minutes, lat_start_frac):.7f}"\
                f"{gps_angle_to_float(lon_start_minutes, lon_start_frac):.7f}"\
                f"{gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac):.7f}"\
                f"{gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac):.7f}"\
                f"{gps_angle_to_float(lat_target_minutes, lat_target_frac):.7f}"\
                f"{gps_angle_to_float(lon_target_minutes, lon_target_frac):.7f}"\
                f"{path_heading:f}\n")
            return ('StampedWaypoint',
                    StampedWaypoint(
                        ms_to_s(timestamp),
                        gps_angle_to_float(lat_start_minutes, lat_start_frac),
                        gps_angle_to_float(lon_start_minutes, lon_start_frac),
                        gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac),
                        gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac),
                        gps_angle_to_float(lat_target_minutes, lat_target_frac),
                        gps_angle_to_float(lon_target_minutes, lon_target_frac),
                        path_heading))
        elif msg_id == int('0xA0', 16): # VersionMsg_t
            debug_major = unpack('B', pack('B', data[0]))[0]
            debug_minor = unpack('B', pack('B', data[1]))[0]
            apm_major = unpack('B', pack('B', data[2]))[0]
            apm_minor = unpack('B', pack('B', data[3]))[0]
            print(
                f"Version"\
                f" debug_major = {debug_major:d}"\
                f" debug_minor = {debug_minor:d}"\
                f" apm_major = {apm_major:d}"\
                f" apm_minor = {apm_minor:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{debug_major:d}"\
                f"{debug_minor:d}"\
                f"{apm_major:d}"\
                f"{apm_minor:d}\n")
            return ('Version',
                    Version(
                        debug_major,
                        debug_minor,
                        apm_major,
                        apm_minor))
        elif msg_id == int('0xAA', 16): # StampedVersionMsg_t
            timestamp = unpack('I', pack('BBBB', data[0], data[1], data[2], data[3]))[0]
            debug_major = unpack('B', pack('B', data[4]))[0]
            debug_minor = unpack('B', pack('B', data[5]))[0]
            apm_major = unpack('B', pack('B', data[6]))[0]
            apm_minor = unpack('B', pack('B', data[7]))[0]
            print(
                f"StampedVersion"\
                f" timestamp = {ms_to_s(timestamp):.3f}"\
                f" debug_major = {debug_major:d}"\
                f" debug_minor = {debug_minor:d}"\
                f" apm_major = {apm_major:d}"\
                f" apm_minor = {apm_minor:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}"\
                f"{debug_major:d}"\
                f"{debug_minor:d}"\
                f"{apm_major:d}"\
                f"{apm_minor:d}\n")
            return ('StampedVersion',
                    StampedVersion(
                        ms_to_s(timestamp),
                        debug_major,
                        debug_minor,
                        apm_major,
                        apm_minor))
        elif msg_id == int('0x90',16): # AsciiMsg_t
            ascii = data[:pkt_len - 3]
            print('Ascii: {0!s}'.format(ascii.decode()))
            self.outfile.write("{:d}:{!s}\n".format(msg_id, ascii.decode()))
            return ('Ascii', Ascii(ascii))
        else:
            print(f"Unknown Msg type recieved: {msg_id:d}")
        
        self.outfile.flush()