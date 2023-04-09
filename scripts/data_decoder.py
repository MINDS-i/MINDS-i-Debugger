# This file was auto-generated. Any changes to this file may be overwritten.

from dataclasses import dataclass
from struct import pack, unpack

@dataclass(frozen=True)
class GpsAngle:
    minutes: int
    frac: float

@dataclass(frozen=True)
class LenString:
    data: list
    len: int

@dataclass(frozen=True)
class RawPosition:
    latitude: float
    longitude: float
    altitude: float

@dataclass(frozen=True)
class StampedRawPosition:
    timestamp: float
    latitude: float
    longitude: float
    altitude: float

@dataclass(frozen=True)
class ExtrapolatedPosition:
    latitude: float
    longitude: float
    altitude: float

@dataclass(frozen=True)
class StampedExtrapolatedPosition:
    timestamp: float
    latitude: float
    longitude: float
    altitude: float

@dataclass(frozen=True)
class Orientation:
    heading: float
    roll: float
    pitch: float

@dataclass(frozen=True)
class StampedOrientation:
    timestamp: float
    heading: float
    roll: float
    pitch: float

@dataclass(frozen=True)
class Radio:
    speed: float
    steering: int

@dataclass(frozen=True)
class StampedRadio:
    timestamp: float
    speed: float
    steering: int

@dataclass(frozen=True)
class Imu:
    euler_x: float
    euler_y: float
    euler_z: float
    acc_x: float
    acc_y: float
    acc_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float
    quaternion_w: float
    quaternion_x: float
    quaternion_y: float
    quaternion_z: float

@dataclass(frozen=True)
class StampedImu:
    timestamp: float
    euler_x: float
    euler_y: float
    euler_z: float
    acc_x: float
    acc_y: float
    acc_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float
    quaternion_w: float
    quaternion_x: float
    quaternion_y: float
    quaternion_z: float

@dataclass(frozen=True)
class Sonar:
    ping1: int
    ping2: int
    ping3: int
    ping4: int
    ping5: int

@dataclass(frozen=True)
class StampedSonar:
    timestamp: float
    ping1: int
    ping2: int
    ping3: int
    ping4: int
    ping5: int

@dataclass(frozen=True)
class Bumper:
    left: int
    right: int

@dataclass(frozen=True)
class StampedBumper:
    timestamp: float
    left: int
    right: int

@dataclass(frozen=True)
class State:
    apmState: int
    driveState: int
    autoState: int
    autoFlag: int
    voltage: float
    amperage: float
    groundSpeed: float

@dataclass(frozen=True)
class StampedState:
    timestamp: float
    apmState: int
    driveState: int
    autoState: int
    autoFlag: int
    voltage: float
    amperage: float
    groundSpeed: float

@dataclass(frozen=True)
class Control:
    speed: float
    steering: int
    sc_steering: float
    true_steering: float
    k_crosstrack: float
    k_yaw: float
    heading_error: float
    crosstrack_error: float

@dataclass(frozen=True)
class StampedControl:
    timestamp: float
    speed: float
    steering: int
    sc_steering: float
    true_steering: float
    k_crosstrack: float
    k_yaw: float
    heading_error: float
    crosstrack_error: float

@dataclass(frozen=True)
class Waypoint:
    lat_start: float
    lon_start: float
    lat_intermediate: float
    lon_intermediate: float
    lat_target: float
    lon_target: float
    path_heading: float

@dataclass(frozen=True)
class StampedWaypoint:
    timestamp: float
    lat_start: float
    lon_start: float
    lat_intermediate: float
    lon_intermediate: float
    lat_target: float
    lon_target: float
    path_heading: float

@dataclass(frozen=True)
class Version:
    debug_major: int
    debug_minor: int
    apm_major: int
    apm_minor: int

@dataclass(frozen=True)
class StampedVersion:
    timestamp: float
    debug_major: int
    debug_minor: int
    apm_major: int
    apm_minor: int

@dataclass(frozen=True)
class Ascii:
    ascii: str

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
                f"RawPosition",
                f"latitude = {gps_angle_to_float(latitude_minutes, latitude_frac):.7f}",
                f"longitude = {gps_angle_to_float(longitude_minutes, longitude_frac):.7f}",
                f"altitude = {altitude:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{gps_angle_to_float(latitude_minutes, latitude_frac):.7f}:"\
                f"{gps_angle_to_float(longitude_minutes, longitude_frac):.7f}:"\
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
                f"StampedRawPosition",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"latitude = {gps_angle_to_float(latitude_minutes, latitude_frac):.7f}",
                f"longitude = {gps_angle_to_float(longitude_minutes, longitude_frac):.7f}",
                f"altitude = {altitude:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{gps_angle_to_float(latitude_minutes, latitude_frac):.7f}:"\
                f"{gps_angle_to_float(longitude_minutes, longitude_frac):.7f}:"\
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
                f"ExtrapolatedPosition",
                f"latitude = {gps_angle_to_float(latitude_minutes, latitude_frac):.7f}",
                f"longitude = {gps_angle_to_float(longitude_minutes, longitude_frac):.7f}",
                f"altitude = {altitude:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{gps_angle_to_float(latitude_minutes, latitude_frac):.7f}:"\
                f"{gps_angle_to_float(longitude_minutes, longitude_frac):.7f}:"\
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
                f"StampedExtrapolatedPosition",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"latitude = {gps_angle_to_float(latitude_minutes, latitude_frac):.7f}",
                f"longitude = {gps_angle_to_float(longitude_minutes, longitude_frac):.7f}",
                f"altitude = {altitude:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{gps_angle_to_float(latitude_minutes, latitude_frac):.7f}:"\
                f"{gps_angle_to_float(longitude_minutes, longitude_frac):.7f}:"\
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
                f"Orientation",
                f"heading = {heading:.2f}",
                f"roll = {roll:.2f}",
                f"pitch = {pitch:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{heading:.2f}:"\
                f"{roll:.2f}:"\
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
                f"StampedOrientation",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"heading = {heading:.2f}",
                f"roll = {roll:.2f}",
                f"pitch = {pitch:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{heading:.2f}:"\
                f"{roll:.2f}:"\
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
                f"Radio",
                f"speed = {speed:.2f}",
                f"steering = {steering:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{speed:.2f}:"\
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
                f"StampedRadio",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"speed = {speed:.2f}",
                f"steering = {steering:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{speed:.2f}:"\
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
                f"Imu",
                f"euler_x = {euler_x:.2f}",
                f"euler_y = {euler_y:.2f}",
                f"euler_z = {euler_z:.2f}",
                f"acc_x = {acc_x:.2f}",
                f"acc_y = {acc_y:.2f}",
                f"acc_z = {acc_z:.2f}",
                f"gyro_x = {gyro_x:.2f}",
                f"gyro_y = {gyro_y:.2f}",
                f"gyro_z = {gyro_z:.2f}",
                f"quaternion_w = {quaternion_w:.2f}",
                f"quaternion_x = {quaternion_x:.2f}",
                f"quaternion_y = {quaternion_y:.2f}",
                f"quaternion_z = {quaternion_z:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{euler_x:.2f}:"\
                f"{euler_y:.2f}:"\
                f"{euler_z:.2f}:"\
                f"{acc_x:.2f}:"\
                f"{acc_y:.2f}:"\
                f"{acc_z:.2f}:"\
                f"{gyro_x:.2f}:"\
                f"{gyro_y:.2f}:"\
                f"{gyro_z:.2f}:"\
                f"{quaternion_w:.2f}:"\
                f"{quaternion_x:.2f}:"\
                f"{quaternion_y:.2f}:"\
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
                f"StampedImu",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"euler_x = {euler_x:.2f}",
                f"euler_y = {euler_y:.2f}",
                f"euler_z = {euler_z:.2f}",
                f"acc_x = {acc_x:.2f}",
                f"acc_y = {acc_y:.2f}",
                f"acc_z = {acc_z:.2f}",
                f"gyro_x = {gyro_x:.2f}",
                f"gyro_y = {gyro_y:.2f}",
                f"gyro_z = {gyro_z:.2f}",
                f"quaternion_w = {quaternion_w:.2f}",
                f"quaternion_x = {quaternion_x:.2f}",
                f"quaternion_y = {quaternion_y:.2f}",
                f"quaternion_z = {quaternion_z:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{euler_x:.2f}:"\
                f"{euler_y:.2f}:"\
                f"{euler_z:.2f}:"\
                f"{acc_x:.2f}:"\
                f"{acc_y:.2f}:"\
                f"{acc_z:.2f}:"\
                f"{gyro_x:.2f}:"\
                f"{gyro_y:.2f}:"\
                f"{gyro_z:.2f}:"\
                f"{quaternion_w:.2f}:"\
                f"{quaternion_x:.2f}:"\
                f"{quaternion_y:.2f}:"\
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
                f"Sonar",
                f"ping1 = {ping1:d}",
                f"ping2 = {ping2:d}",
                f"ping3 = {ping3:d}",
                f"ping4 = {ping4:d}",
                f"ping5 = {ping5:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ping1:d}:"\
                f"{ping2:d}:"\
                f"{ping3:d}:"\
                f"{ping4:d}:"\
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
                f"StampedSonar",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"ping1 = {ping1:d}",
                f"ping2 = {ping2:d}",
                f"ping3 = {ping3:d}",
                f"ping4 = {ping4:d}",
                f"ping5 = {ping5:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{ping1:d}:"\
                f"{ping2:d}:"\
                f"{ping3:d}:"\
                f"{ping4:d}:"\
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
                f"Bumper",
                f"left = {left:d}",
                f"right = {right:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{left:d}:"\
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
                f"StampedBumper",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"left = {left:d}",
                f"right = {right:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{left:d}:"\
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
                f"State",
                f"apmState = {apmState:d}",
                f"driveState = {driveState:d}",
                f"autoState = {autoState:d}",
                f"autoFlag = {autoFlag:d}",
                f"voltage = {voltage:f}",
                f"amperage = {amperage:f}",
                f"groundSpeed = {groundSpeed:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{apmState:d}:"\
                f"{driveState:d}:"\
                f"{autoState:d}:"\
                f"{autoFlag:d}:"\
                f"{voltage:f}:"\
                f"{amperage:f}:"\
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
                f"StampedState",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"apmState = {apmState:d}",
                f"driveState = {driveState:d}",
                f"autoState = {autoState:d}",
                f"autoFlag = {autoFlag:d}",
                f"voltage = {voltage:f}",
                f"amperage = {amperage:f}",
                f"groundSpeed = {groundSpeed:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{apmState:d}:"\
                f"{driveState:d}:"\
                f"{autoState:d}:"\
                f"{autoFlag:d}:"\
                f"{voltage:f}:"\
                f"{amperage:f}:"\
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
                f"Control",
                f"speed = {speed:.2f}",
                f"steering = {steering:d}",
                f"sc_steering = {sc_steering:.2f}",
                f"true_steering = {true_steering:.2f}",
                f"k_crosstrack = {k_crosstrack:.4f}",
                f"k_yaw = {k_yaw:.4f}",
                f"heading_error = {heading_error:.2f}",
                f"crosstrack_error = {crosstrack_error:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{speed:.2f}:"\
                f"{steering:d}:"\
                f"{sc_steering:.2f}:"\
                f"{true_steering:.2f}:"\
                f"{k_crosstrack:.4f}:"\
                f"{k_yaw:.4f}:"\
                f"{heading_error:.2f}:"\
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
                f"StampedControl",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"speed = {speed:.2f}",
                f"steering = {steering:d}",
                f"sc_steering = {sc_steering:.2f}",
                f"true_steering = {true_steering:.2f}",
                f"k_crosstrack = {k_crosstrack:.4f}",
                f"k_yaw = {k_yaw:.4f}",
                f"heading_error = {heading_error:.2f}",
                f"crosstrack_error = {crosstrack_error:.2f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{speed:.2f}:"\
                f"{steering:d}:"\
                f"{sc_steering:.2f}:"\
                f"{true_steering:.2f}:"\
                f"{k_crosstrack:.4f}:"\
                f"{k_yaw:.4f}:"\
                f"{heading_error:.2f}:"\
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
                f"Waypoint",
                f"lat_start = {gps_angle_to_float(lat_start_minutes, lat_start_frac):.7f}",
                f"lon_start = {gps_angle_to_float(lon_start_minutes, lon_start_frac):.7f}",
                f"lat_intermediate = {gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac):.7f}",
                f"lon_intermediate = {gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac):.7f}",
                f"lat_target = {gps_angle_to_float(lat_target_minutes, lat_target_frac):.7f}",
                f"lon_target = {gps_angle_to_float(lon_target_minutes, lon_target_frac):.7f}",
                f"path_heading = {path_heading:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{gps_angle_to_float(lat_start_minutes, lat_start_frac):.7f}:"\
                f"{gps_angle_to_float(lon_start_minutes, lon_start_frac):.7f}:"\
                f"{gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac):.7f}:"\
                f"{gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac):.7f}:"\
                f"{gps_angle_to_float(lat_target_minutes, lat_target_frac):.7f}:"\
                f"{gps_angle_to_float(lon_target_minutes, lon_target_frac):.7f}:"\
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
                f"StampedWaypoint",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"lat_start = {gps_angle_to_float(lat_start_minutes, lat_start_frac):.7f}",
                f"lon_start = {gps_angle_to_float(lon_start_minutes, lon_start_frac):.7f}",
                f"lat_intermediate = {gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac):.7f}",
                f"lon_intermediate = {gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac):.7f}",
                f"lat_target = {gps_angle_to_float(lat_target_minutes, lat_target_frac):.7f}",
                f"lon_target = {gps_angle_to_float(lon_target_minutes, lon_target_frac):.7f}",
                f"path_heading = {path_heading:f}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{gps_angle_to_float(lat_start_minutes, lat_start_frac):.7f}:"\
                f"{gps_angle_to_float(lon_start_minutes, lon_start_frac):.7f}:"\
                f"{gps_angle_to_float(lat_intermediate_minutes, lat_intermediate_frac):.7f}:"\
                f"{gps_angle_to_float(lon_intermediate_minutes, lon_intermediate_frac):.7f}:"\
                f"{gps_angle_to_float(lat_target_minutes, lat_target_frac):.7f}:"\
                f"{gps_angle_to_float(lon_target_minutes, lon_target_frac):.7f}:"\
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
                f"Version",
                f"debug_major = {debug_major:d}",
                f"debug_minor = {debug_minor:d}",
                f"apm_major = {apm_major:d}",
                f"apm_minor = {apm_minor:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{debug_major:d}:"\
                f"{debug_minor:d}:"\
                f"{apm_major:d}:"\
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
                f"StampedVersion",
                f"timestamp = {ms_to_s(timestamp):.3f}",
                f"debug_major = {debug_major:d}",
                f"debug_minor = {debug_minor:d}",
                f"apm_major = {apm_major:d}",
                f"apm_minor = {apm_minor:d}")
            self.outfile.write(
                f"{msg_id:d}:"\
                f"{ms_to_s(timestamp):.3f}:"\
                f"{debug_major:d}:"\
                f"{debug_minor:d}:"\
                f"{apm_major:d}:"\
                f"{apm_minor:d}\n")
            return ('StampedVersion',
                    StampedVersion(
                        ms_to_s(timestamp),
                        debug_major,
                        debug_minor,
                        apm_major,
                        apm_minor))
        elif msg_id == int('0x90', 16): # AsciiMsg_t
            ascii = data[:pkt_len - 3]
            print('Ascii: {0!s}'.format(ascii.decode()))
            self.outfile.write("{:d}:{!s}\n".format(msg_id, ascii.decode()))
            return ('Ascii', Ascii(ascii.decode()))
        else:
            print(f'Unknown Msg type recieved: {msg_id:d}')
            return ('Unknown', None)
        
        self.outfile.flush()

def read_log_dataline(dataline, print_line=False):
    data = dataline.strip().split(':')
    if int(data[0]) == int('0x10', 16): # RawPositionMsg_t
        if print_line:
            print(
                f"RawPosition",
                f"latitude = {float(data[1]):.7f}",
                f"longitude = {float(data[2]):.7f}",
                f"altitude = {float(data[3]):f}")
        return ('RawPosition',
                RawPosition(
                    float(data[1]), # latitude
                    float(data[2]), # longitude
                    float(data[3]))) # altitude
    elif int(data[0]) == int('0x1A', 16): # StampedRawPositionMsg_t
        if print_line:
            print(
                f"StampedRawPosition",
                f"timestamp = {float(data[1]):.3f}",
                f"latitude = {float(data[2]):.7f}",
                f"longitude = {float(data[3]):.7f}",
                f"altitude = {float(data[4]):f}")
        return ('StampedRawPosition',
                StampedRawPosition(
                    float(data[1]), # timestamp
                    float(data[2]), # latitude
                    float(data[3]), # longitude
                    float(data[4]))) # altitude
    elif int(data[0]) == int('0x11', 16): # ExtrapolatedPositionMsg_t
        if print_line:
            print(
                f"ExtrapolatedPosition",
                f"latitude = {float(data[1]):.7f}",
                f"longitude = {float(data[2]):.7f}",
                f"altitude = {float(data[3]):f}")
        return ('ExtrapolatedPosition',
                ExtrapolatedPosition(
                    float(data[1]), # latitude
                    float(data[2]), # longitude
                    float(data[3]))) # altitude
    elif int(data[0]) == int('0x1B', 16): # StampedExtrapolatedPositionMsg_t
        if print_line:
            print(
                f"StampedExtrapolatedPosition",
                f"timestamp = {float(data[1]):.3f}",
                f"latitude = {float(data[2]):.7f}",
                f"longitude = {float(data[3]):.7f}",
                f"altitude = {float(data[4]):f}")
        return ('StampedExtrapolatedPosition',
                StampedExtrapolatedPosition(
                    float(data[1]), # timestamp
                    float(data[2]), # latitude
                    float(data[3]), # longitude
                    float(data[4]))) # altitude
    elif int(data[0]) == int('0x20', 16): # OrientationMsg_t
        if print_line:
            print(
                f"Orientation",
                f"heading = {float(data[1]):.2f}",
                f"roll = {float(data[2]):.2f}",
                f"pitch = {float(data[3]):.2f}")
        return ('Orientation',
                Orientation(
                    float(data[1]), # heading
                    float(data[2]), # roll
                    float(data[3]))) # pitch
    elif int(data[0]) == int('0x2A', 16): # StampedOrientationMsg_t
        if print_line:
            print(
                f"StampedOrientation",
                f"timestamp = {float(data[1]):.3f}",
                f"heading = {float(data[2]):.2f}",
                f"roll = {float(data[3]):.2f}",
                f"pitch = {float(data[4]):.2f}")
        return ('StampedOrientation',
                StampedOrientation(
                    float(data[1]), # timestamp
                    float(data[2]), # heading
                    float(data[3]), # roll
                    float(data[4]))) # pitch
    elif int(data[0]) == int('0x30', 16): # RadioMsg_t
        if print_line:
            print(
                f"Radio",
                f"speed = {float(data[1]):.2f}",
                f"steering = {int(data[2]):d}")
        return ('Radio',
                Radio(
                    float(data[1]), # speed
                    int(data[2]))) # steering
    elif int(data[0]) == int('0x3A', 16): # StampedRadioMsg_t
        if print_line:
            print(
                f"StampedRadio",
                f"timestamp = {float(data[1]):.3f}",
                f"speed = {float(data[2]):.2f}",
                f"steering = {int(data[3]):d}")
        return ('StampedRadio',
                StampedRadio(
                    float(data[1]), # timestamp
                    float(data[2]), # speed
                    int(data[3]))) # steering
    elif int(data[0]) == int('0x40', 16): # ImuMsg_t
        if print_line:
            print(
                f"Imu",
                f"euler_x = {float(data[1]):.2f}",
                f"euler_y = {float(data[2]):.2f}",
                f"euler_z = {float(data[3]):.2f}",
                f"acc_x = {float(data[4]):.2f}",
                f"acc_y = {float(data[5]):.2f}",
                f"acc_z = {float(data[6]):.2f}",
                f"gyro_x = {float(data[7]):.2f}",
                f"gyro_y = {float(data[8]):.2f}",
                f"gyro_z = {float(data[9]):.2f}",
                f"quaternion_w = {float(data[10]):.2f}",
                f"quaternion_x = {float(data[11]):.2f}",
                f"quaternion_y = {float(data[12]):.2f}",
                f"quaternion_z = {float(data[13]):.2f}")
        return ('Imu',
                Imu(
                    float(data[1]), # euler_x
                    float(data[2]), # euler_y
                    float(data[3]), # euler_z
                    float(data[4]), # acc_x
                    float(data[5]), # acc_y
                    float(data[6]), # acc_z
                    float(data[7]), # gyro_x
                    float(data[8]), # gyro_y
                    float(data[9]), # gyro_z
                    float(data[10]), # quaternion_w
                    float(data[11]), # quaternion_x
                    float(data[12]), # quaternion_y
                    float(data[13]))) # quaternion_z
    elif int(data[0]) == int('0x4A', 16): # StampedImuMsg_t
        if print_line:
            print(
                f"StampedImu",
                f"timestamp = {float(data[1]):.3f}",
                f"euler_x = {float(data[2]):.2f}",
                f"euler_y = {float(data[3]):.2f}",
                f"euler_z = {float(data[4]):.2f}",
                f"acc_x = {float(data[5]):.2f}",
                f"acc_y = {float(data[6]):.2f}",
                f"acc_z = {float(data[7]):.2f}",
                f"gyro_x = {float(data[8]):.2f}",
                f"gyro_y = {float(data[9]):.2f}",
                f"gyro_z = {float(data[10]):.2f}",
                f"quaternion_w = {float(data[11]):.2f}",
                f"quaternion_x = {float(data[12]):.2f}",
                f"quaternion_y = {float(data[13]):.2f}",
                f"quaternion_z = {float(data[14]):.2f}")
        return ('StampedImu',
                StampedImu(
                    float(data[1]), # timestamp
                    float(data[2]), # euler_x
                    float(data[3]), # euler_y
                    float(data[4]), # euler_z
                    float(data[5]), # acc_x
                    float(data[6]), # acc_y
                    float(data[7]), # acc_z
                    float(data[8]), # gyro_x
                    float(data[9]), # gyro_y
                    float(data[10]), # gyro_z
                    float(data[11]), # quaternion_w
                    float(data[12]), # quaternion_x
                    float(data[13]), # quaternion_y
                    float(data[14]))) # quaternion_z
    elif int(data[0]) == int('0x41', 16): # SonarMsg_t
        if print_line:
            print(
                f"Sonar",
                f"ping1 = {int(data[1]):d}",
                f"ping2 = {int(data[2]):d}",
                f"ping3 = {int(data[3]):d}",
                f"ping4 = {int(data[4]):d}",
                f"ping5 = {int(data[5]):d}")
        return ('Sonar',
                Sonar(
                    int(data[1]), # ping1
                    int(data[2]), # ping2
                    int(data[3]), # ping3
                    int(data[4]), # ping4
                    int(data[5]))) # ping5
    elif int(data[0]) == int('0x4B', 16): # StampedSonarMsg_t
        if print_line:
            print(
                f"StampedSonar",
                f"timestamp = {float(data[1]):.3f}",
                f"ping1 = {int(data[2]):d}",
                f"ping2 = {int(data[3]):d}",
                f"ping3 = {int(data[4]):d}",
                f"ping4 = {int(data[5]):d}",
                f"ping5 = {int(data[6]):d}")
        return ('StampedSonar',
                StampedSonar(
                    float(data[1]), # timestamp
                    int(data[2]), # ping1
                    int(data[3]), # ping2
                    int(data[4]), # ping3
                    int(data[5]), # ping4
                    int(data[6]))) # ping5
    elif int(data[0]) == int('0x42', 16): # BumperMsg_t
        if print_line:
            print(
                f"Bumper",
                f"left = {int(data[1]):d}",
                f"right = {int(data[2]):d}")
        return ('Bumper',
                Bumper(
                    int(data[1]), # left
                    int(data[2]))) # right
    elif int(data[0]) == int('0x4C', 16): # StampedBumperMsg_t
        if print_line:
            print(
                f"StampedBumper",
                f"timestamp = {float(data[1]):.3f}",
                f"left = {int(data[2]):d}",
                f"right = {int(data[3]):d}")
        return ('StampedBumper',
                StampedBumper(
                    float(data[1]), # timestamp
                    int(data[2]), # left
                    int(data[3]))) # right
    elif int(data[0]) == int('0x60', 16): # StateMsg_t
        if print_line:
            print(
                f"State",
                f"apmState = {int(data[1]):d}",
                f"driveState = {int(data[2]):d}",
                f"autoState = {int(data[3]):d}",
                f"autoFlag = {int(data[4]):d}",
                f"voltage = {float(data[5]):f}",
                f"amperage = {float(data[6]):f}",
                f"groundSpeed = {float(data[7]):f}")
        return ('State',
                State(
                    int(data[1]), # apmState
                    int(data[2]), # driveState
                    int(data[3]), # autoState
                    int(data[4]), # autoFlag
                    float(data[5]), # voltage
                    float(data[6]), # amperage
                    float(data[7]))) # groundSpeed
    elif int(data[0]) == int('0x6A', 16): # StampedStateMsg_t
        if print_line:
            print(
                f"StampedState",
                f"timestamp = {float(data[1]):.3f}",
                f"apmState = {int(data[2]):d}",
                f"driveState = {int(data[3]):d}",
                f"autoState = {int(data[4]):d}",
                f"autoFlag = {int(data[5]):d}",
                f"voltage = {float(data[6]):f}",
                f"amperage = {float(data[7]):f}",
                f"groundSpeed = {float(data[8]):f}")
        return ('StampedState',
                StampedState(
                    float(data[1]), # timestamp
                    int(data[2]), # apmState
                    int(data[3]), # driveState
                    int(data[4]), # autoState
                    int(data[5]), # autoFlag
                    float(data[6]), # voltage
                    float(data[7]), # amperage
                    float(data[8]))) # groundSpeed
    elif int(data[0]) == int('0x80', 16): # ControlMsg_t
        if print_line:
            print(
                f"Control",
                f"speed = {float(data[1]):.2f}",
                f"steering = {int(data[2]):d}",
                f"sc_steering = {float(data[3]):.2f}",
                f"true_steering = {float(data[4]):.2f}",
                f"k_crosstrack = {float(data[5]):.4f}",
                f"k_yaw = {float(data[6]):.4f}",
                f"heading_error = {float(data[7]):.2f}",
                f"crosstrack_error = {float(data[8]):.2f}")
        return ('Control',
                Control(
                    float(data[1]), # speed
                    int(data[2]), # steering
                    float(data[3]), # sc_steering
                    float(data[4]), # true_steering
                    float(data[5]), # k_crosstrack
                    float(data[6]), # k_yaw
                    float(data[7]), # heading_error
                    float(data[8]))) # crosstrack_error
    elif int(data[0]) == int('0x8A', 16): # StampedControlMsg_t
        if print_line:
            print(
                f"StampedControl",
                f"timestamp = {float(data[1]):.3f}",
                f"speed = {float(data[2]):.2f}",
                f"steering = {int(data[3]):d}",
                f"sc_steering = {float(data[4]):.2f}",
                f"true_steering = {float(data[5]):.2f}",
                f"k_crosstrack = {float(data[6]):.4f}",
                f"k_yaw = {float(data[7]):.4f}",
                f"heading_error = {float(data[8]):.2f}",
                f"crosstrack_error = {float(data[9]):.2f}")
        return ('StampedControl',
                StampedControl(
                    float(data[1]), # timestamp
                    float(data[2]), # speed
                    int(data[3]), # steering
                    float(data[4]), # sc_steering
                    float(data[5]), # true_steering
                    float(data[6]), # k_crosstrack
                    float(data[7]), # k_yaw
                    float(data[8]), # heading_error
                    float(data[9]))) # crosstrack_error
    elif int(data[0]) == int('0x81', 16): # WaypointMsg_t
        if print_line:
            print(
                f"Waypoint",
                f"lat_start = {float(data[1]):.7f}",
                f"lon_start = {float(data[2]):.7f}",
                f"lat_intermediate = {float(data[3]):.7f}",
                f"lon_intermediate = {float(data[4]):.7f}",
                f"lat_target = {float(data[5]):.7f}",
                f"lon_target = {float(data[6]):.7f}",
                f"path_heading = {float(data[7]):f}")
        return ('Waypoint',
                Waypoint(
                    float(data[1]), # lat_start
                    float(data[2]), # lon_start
                    float(data[3]), # lat_intermediate
                    float(data[4]), # lon_intermediate
                    float(data[5]), # lat_target
                    float(data[6]), # lon_target
                    float(data[7]))) # path_heading
    elif int(data[0]) == int('0x8B', 16): # StampedWaypointMsg_t
        if print_line:
            print(
                f"StampedWaypoint",
                f"timestamp = {float(data[1]):.3f}",
                f"lat_start = {float(data[2]):.7f}",
                f"lon_start = {float(data[3]):.7f}",
                f"lat_intermediate = {float(data[4]):.7f}",
                f"lon_intermediate = {float(data[5]):.7f}",
                f"lat_target = {float(data[6]):.7f}",
                f"lon_target = {float(data[7]):.7f}",
                f"path_heading = {float(data[8]):f}")
        return ('StampedWaypoint',
                StampedWaypoint(
                    float(data[1]), # timestamp
                    float(data[2]), # lat_start
                    float(data[3]), # lon_start
                    float(data[4]), # lat_intermediate
                    float(data[5]), # lon_intermediate
                    float(data[6]), # lat_target
                    float(data[7]), # lon_target
                    float(data[8]))) # path_heading
    elif int(data[0]) == int('0xA0', 16): # VersionMsg_t
        if print_line:
            print(
                f"Version",
                f"debug_major = {int(data[1]):d}",
                f"debug_minor = {int(data[2]):d}",
                f"apm_major = {int(data[3]):d}",
                f"apm_minor = {int(data[4]):d}")
        return ('Version',
                Version(
                    int(data[1]), # debug_major
                    int(data[2]), # debug_minor
                    int(data[3]), # apm_major
                    int(data[4]))) # apm_minor
    elif int(data[0]) == int('0xAA', 16): # StampedVersionMsg_t
        if print_line:
            print(
                f"StampedVersion",
                f"timestamp = {float(data[1]):.3f}",
                f"debug_major = {int(data[2]):d}",
                f"debug_minor = {int(data[3]):d}",
                f"apm_major = {int(data[4]):d}",
                f"apm_minor = {int(data[5]):d}")
        return ('StampedVersion',
                StampedVersion(
                    float(data[1]), # timestamp
                    int(data[2]), # debug_major
                    int(data[3]), # debug_minor
                    int(data[4]), # apm_major
                    int(data[5]))) # apm_minor
    elif int(data[0]) == int('0x90', 16): # AsciiMsg_t
        if print_line:
            print("Ascii", f"ascii = {':'.join(data[1:])}")
        return ('Ascii', Ascii(':'.join(data[1:])))
    else:
        print(f'Unknown Msg type read: {int(data[0]):d}')
        return ('Unknown', None)