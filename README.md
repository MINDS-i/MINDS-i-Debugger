# MINDS-i-Debugger
Code to assist with debugging MINDSi robots

This library contains code for providing logging and debugging msgs on a dedicated serial link.

## Usage

### Sending Messages

In the main program file include the required debugger headers.

``` cpp
#include <MINDSiDebugger.h>
#include <DebugMsgs.h>
#include <Util.h>
```

Create a debugger instance

``` cpp
#ifdef M_DEBUG
  #include "MINDSiDebugger.h"
  MINDSiDebugger debugger;
#endif
```

Create a message and send it anywhere you want to send a message (sending messages in fast running loops can slow down the loop and hinder performance)


``` cpp
#ifdef M_DEBUG
	// Logger Msg
	RawPositionMsg_t msg;
	GPS_ANGLE loc_lat = location.angLatitude();
	GPS_ANGLE loc_lon = location.angLongitude();
	msg.latitude.minutes = loc_lat.minutes;
	msg.latitude.frac = loc_lat.frac;
	msg.longitude.minutes = loc_lon.minutes;
	msg.longitude.frac = loc_lon.frac;
	msg.altitude = 0.0;
	debugger.send(msg);
#endif
```

### Receiving Messages

Receive messages by running the reader (specifying port and output file). Optionally, a live view of the robot can be viewed by secifying the live plotter flag (see the usage output)

```
./scripts/reader.py -h
```

## Creating/Modifying Debug Messages

The debug messages are auto generated using the message generation script. Editing the [debug_msgs.yaml](./msg_generation/debug_msgs.yaml) file and re-running the message generation script will allow you to create and modify debug messages.

### YAML configuration file

All debug messages are described in the follwing way:

#### Built In Types

These are the native types and sizes and associated with the target platform

``` yaml
'char': 1
'int8_t': 1
'uint8_t': 1
'int16_t': 2
'uint16_t': 2
'int32_t': 4
'uint32_t': 4
'float': 4
```

#### Custom Types

These the custom types that messages can use to describe more complicated fields

``` yaml
<custom_type_name>:
    # list of fields
    - name: <field_name>
        struct_type: <struct_type> # can be custom type or built in type
        cast_type: <cast_type> # optional - built in integer type to cast the value to before sending (needed for float struct types)
        mod_factor: <value> # optional - value to scale the field by before casting to <cast_type>
        mod_offset: <value> # optional - value to add to the field (occurs before <mod_factor> if specified) before casting to <cast_type>
        description: <string> # optional - description of the field for this README
```

#### Debug Messages

These are debug messages that can be sent from the platform

``` yaml
  - name: <debug_msg_name>:
    id: <hex_msg_id> # a unique (checked at generation time) hex identifier
    description: '<string>' # description of the message for this README
    fields:
      # list of fields
      - name: <field_name>
        struct_type: <struct_type> # can be custom type or built in type
        cast_type: <cast_type> # optional - built in integer type to cast the value to before sending (needed for float struct types)
        mod_factor: <value> # optional - value to scale the field by before casting to <cast_type>
        mod_offset: <value> # optional - value to add to the field (occurs before <mod_factor> if specified) before casting to <cast_type>
            interpret: # optional - usually used for custom types
                type: <python_type> # type hint for the python reader to display the message field
                func: <func> # function to create a value from this type (custom functions can be defined in the template for data_decoder.py)
        num_format: <string> # optional - python f string format string to format the field (usually to specify digits or alignment)
        description: <string> # optional - description of the field for this README
```

### Generating the debug messages

Run the message generation script once you've edited the configuration file. By default a stamped message will be created for each message type, but this can be disabled (see the usage output)

```
./msg_generation/generate_debug_msgs.py -h
```

## Packet Structure

| Header_1 | Header_2 | Length | Type | Message-dependent | Checksum_1 | Checksum_2 | 
| ------------ | ------------- | ------------ | ------------- | ------------ | ------------- | ------------ |
| 0x51 | 0xAC | len | id | data_bytes.. | cs_1 | cs_2 |

## Checksum Calculation

Checksums are calculated over the bytes following the length field (see "Packet Structure") up to but not including the checksum fields. 

The checksum can be calculated using the following pseudo code:

``` js
const uint16_t crctable[256] =
{
    0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
    0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
    0x0919, 0x1890, 0x2A0B, 0x3B82, 0x4F3D, 0x5EB4, 0x6C2F, 0x7DA6,
    0x8551, 0x94D8, 0xA643, 0xB7CA, 0xC375, 0xD2FC, 0xE067, 0xF1EE,
    0x1232, 0x03BB, 0x3120, 0x20A9, 0x5416, 0x459F, 0x7704, 0x668D,
    0x9E7A, 0x8FF3, 0xBD68, 0xACE1, 0xD85E, 0xC9D7, 0xFB4C, 0xEAC5,
    0x1B2B, 0x0AA2, 0x3839, 0x29B0, 0x5D0F, 0x4C86, 0x7E1D, 0x6F94,
    0x9763, 0x86EA, 0xB471, 0xA5F8, 0xD147, 0xC0CE, 0xF255, 0xE3DC,
    0x2464, 0x35ED, 0x0776, 0x16FF, 0x6240, 0x73C9, 0x4152, 0x50DB,
    0xA82C, 0xB9A5, 0x8B3E, 0x9AB7, 0xEE08, 0xFF81, 0xCD1A, 0xDC93,
    0x2D7D, 0x3CF4, 0x0E6F, 0x1FE6, 0x6B59, 0x7AD0, 0x484B, 0x59C2,
    0xA135, 0xB0BC, 0x8227, 0x93AE, 0xE711, 0xF698, 0xC403, 0xD58A,
    0x3656, 0x27DF, 0x1544, 0x04CD, 0x7072, 0x61FB, 0x5360, 0x42E9,
    0xBA1E, 0xAB97, 0x990C, 0x8885, 0xFC3A, 0xEDB3, 0xDF28, 0xCEA1,
    0x3F4F, 0x2EC6, 0x1C5D, 0x0DD4, 0x796B, 0x68E2, 0x5A79, 0x4BF0,
    0xB307, 0xA28E, 0x9015, 0x819C, 0xF523, 0xE4AA, 0xD631, 0xC7B8,
    0x48C8, 0x5941, 0x6BDA, 0x7A53, 0x0EEC, 0x1F65, 0x2DFE, 0x3C77,
    0xC480, 0xD509, 0xE792, 0xF61B, 0x82A4, 0x932D, 0xA1B6, 0xB03F,
    0x41D1, 0x5058, 0x62C3, 0x734A, 0x07F5, 0x167C, 0x24E7, 0x356E,
    0xCD99, 0xDC10, 0xEE8B, 0xFF02, 0x8BBD, 0x9A34, 0xA8AF, 0xB926,
    0x5AFA, 0x4B73, 0x79E8, 0x6861, 0x1CDE, 0x0D57, 0x3FCC, 0x2E45,
    0xD6B2, 0xC73B, 0xF5A0, 0xE429, 0x9096, 0x811F, 0xB384, 0xA20D,
    0x53E3, 0x426A, 0x70F1, 0x6178, 0x15C7, 0x044E, 0x36D5, 0x275C,
    0xDFAB, 0xCE22, 0xFCB9, 0xED30, 0x998F, 0x8806, 0xBA9D, 0xAB14,
    0x6CAC, 0x7D25, 0x4FBE, 0x5E37, 0x2A88, 0x3B01, 0x099A, 0x1813,
    0xE0E4, 0xF16D, 0xC3F6, 0xD27F, 0xA6C0, 0xB749, 0x85D2, 0x945B,
    0x65B5, 0x743C, 0x46A7, 0x572E, 0x2391, 0x3218, 0x0083, 0x110A,
    0xE9FD, 0xF874, 0xCAEF, 0xDB66, 0xAFD9, 0xBE50, 0x8CCB, 0x9D42,
    0x7E9E, 0x6F17, 0x5D8C, 0x4C05, 0x38BA, 0x2933, 0x1BA8, 0x0A21,
    0xF2D6, 0xE35F, 0xD1C4, 0xC04D, 0xB4F2, 0xA57B, 0x97E0, 0x8669,
    0x7787, 0x660E, 0x5495, 0x451C, 0x31A3, 0x202A, 0x12B1, 0x0338,
    0xFBCF, 0xEA46, 0xD8DD, 0xC954, 0xBDEB, 0xAC62, 0x9EF9, 0x8F70
};

crc = 0x0001

for ( each byteValue between length and checksum fields)
{
 	crc = (crc << 8) ^ crctable[((crc >> 8) ^ byteValue)];
}
```

## Message Types

List of available message types.

| Type ID | Name | 
| ------------ | ------------- |
| 0x10 | RawPositionMsg_t |
| 0x1A | StampedRawPositionMsg_t |
| 0x11 | ExtrapolatedPositionMsg_t |
| 0x1B | StampedExtrapolatedPositionMsg_t |
| 0x20 | OrientationMsg_t |
| 0x2A | StampedOrientationMsg_t |
| 0x30 | RadioMsg_t |
| 0x3A | StampedRadioMsg_t |
| 0x40 | ImuMsg_t |
| 0x4A | StampedImuMsg_t |
| 0x41 | SonarMsg_t |
| 0x4B | StampedSonarMsg_t |
| 0x42 | BumperMsg_t |
| 0x4C | StampedBumperMsg_t |
| 0x60 | StateMsg_t |
| 0x6A | StampedStateMsg_t |
| 0x80 | ControlMsg_t |
| 0x8A | StampedControlMsg_t |
| 0x81 | WaypointMsg_t |
| 0x8B | StampedWaypointMsg_t |
| 0x82 | ControlMsg_t |
| 0x8C | StampedControlMsg_t |
| 0xA0 | VersionMsg_t |
| 0xAA | StampedVersionMsg_t |
| 0x90 | AsciiMsg_t |

## Custom Data Types

``` cpp
typedef struct {
    int16_t minutes;
    float frac;
} GpsAngle_t;

typedef struct {
    char data[256];
    uint8_t len;
} LenString_t;
```

## Message Definitions

#### RawPosition Message (0x10)

Positioning information being provided by the GPS sensor.

``` cpp
typedef struct {
    GpsAngle_t latitude;
    GpsAngle_t longitude;
    float altitude;
} RawPositionMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | latitude.minutes | -32768..32767 | 1 | GPS reciever reported latitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 6-9 | latitude.frac | -21474.8..21474.8 | 1e-05 | GPS reciever reported latitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 10-11 | longitude.minutes | -32768..32767 | 1 | GPS reciever reported longitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 12-15 | longitude.frac | -21474.8..21474.8 | 1e-05 | GPS reciever reported longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 16-17 | altitude | -900.0..19000.3 | 0.304 | GPS reciever reported altitude (m) |

#### StampedRawPosition Message (0x1A)

Positioning information being provided by the GPS sensor.

``` cpp
typedef struct {
    uint32_t timestamp;
    GpsAngle_t latitude;
    GpsAngle_t longitude;
    float altitude;
} StampedRawPositionMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | latitude.minutes | -32768..32767 | 1 | GPS reciever reported latitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 10-13 | latitude.frac | -21474.8..21474.8 | 1e-05 | GPS reciever reported latitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 14-15 | longitude.minutes | -32768..32767 | 1 | GPS reciever reported longitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 16-19 | longitude.frac | -21474.8..21474.8 | 1e-05 | GPS reciever reported longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 20-21 | altitude | -900.0..19000.3 | 0.304 | GPS reciever reported altitude (m) |

#### ExtrapolatedPosition Message (0x11)

Position information created through calculation rather than sensed directly.

``` cpp
typedef struct {
    GpsAngle_t latitude;
    GpsAngle_t longitude;
    float altitude;
} ExtrapolatedPositionMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | latitude.minutes | -32768..32767 | 1 | GPS reciever reported latitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 6-9 | latitude.frac | -21474.8..21474.8 | 1e-05 | GPS reciever reported latitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 10-11 | longitude.minutes | -32768..32767 | 1 | GPS reciever reported longitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 12-15 | longitude.frac | -21474.8..21474.8 | 1e-05 | GPS reciever reported longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 16-17 | altitude | -900.0..19000.3 | 0.304 | Altitude extraploated between GPS readings (m) |

#### StampedExtrapolatedPosition Message (0x1B)

Position information created through calculation rather than sensed directly.

``` cpp
typedef struct {
    uint32_t timestamp;
    GpsAngle_t latitude;
    GpsAngle_t longitude;
    float altitude;
} StampedExtrapolatedPositionMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | latitude.minutes | -32768..32767 | 1 | GPS reciever reported latitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 10-13 | latitude.frac | -21474.8..21474.8 | 1e-05 | GPS reciever reported latitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 14-15 | longitude.minutes | -32768..32767 | 1 | GPS reciever reported longitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 16-19 | longitude.frac | -21474.8..21474.8 | 1e-05 | GPS reciever reported longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 20-21 | altitude | -900.0..19000.3 | 0.304 | Altitude extraploated between GPS readings (m) |

#### Orientation Message (0x20)

Orientation information used for control puposes.

``` cpp
typedef struct {
    float heading;
    float roll;
    float pitch;
} OrientationMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | heading | -327.68..327.67 | 0.01 | Heading (deg) |
| 6-7 | roll | -327.68..327.67 | 0.01 | Roll (deg) |
| 8-9 | pitch | -327.68..327.67 | 0.01 | Pitch (deg) |

#### StampedOrientation Message (0x2A)

Orientation information used for control puposes.

``` cpp
typedef struct {
    uint32_t timestamp;
    float heading;
    float roll;
    float pitch;
} StampedOrientationMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | heading | -327.68..327.67 | 0.01 | Heading (deg) |
| 10-11 | roll | -327.68..327.67 | 0.01 | Roll (deg) |
| 12-13 | pitch | -327.68..327.67 | 0.01 | Pitch (deg) |

#### Radio Message (0x30)

Commands being sent by the radio controller.

``` cpp
typedef struct {
    float speed;
    uint8_t steering;
} RadioMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | speed | -327.68..327.67 | 0.01 | Speed command from radio controller (mph) |
| 6 | steering | 0..256 | 1 | TBD |

#### StampedRadio Message (0x3A)

Commands being sent by the radio controller.

``` cpp
typedef struct {
    uint32_t timestamp;
    float speed;
    uint8_t steering;
} StampedRadioMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | speed | -327.68..327.67 | 0.01 | Speed command from radio controller (mph) |
| 10 | steering | 0..256 | 1 | TBD |

#### Imu Message (0x40)

Measurement information being privided by the IMU sensor.

``` cpp
typedef struct {
    float eulerX;
    float eulerY;
    float eulerZ;
    float accX;
    float accY;
    float accZ;
    float gyroX;
    float gyroY;
    float gyroZ;
    float quaternionW;
    float quaternionX;
    float quaternionY;
    float quaternionZ;
} ImuMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | euler_x | -3.14171..3.14161 | 9.59e-05 | Euler angle on the X axis (rad) |
| 6-7 | euler_y | -3.14171..3.14161 | 9.59e-05 | Euler angle on the Y axis (rad) |
| 8-9 | euler_z | -3.14171..3.14161 | 9.59e-05 | Euler angle on the Z axis (rad) |
| 10-11 | acc_x | -4.0..3.99988 | 0.000122 | Acceleration on the X axis (g) |
| 12-13 | acc_y | -4.0..3.99988 | 0.000122 | Acceleration on the Y axis (g) |
| 14-15 | acc_z | -4.0..3.99988 | 0.000122 | Acceleration on the Z axis (g) |
| 16-17 | gyro_x | -1998.05..1997.99 | 0.061 | Rotation rate on the X axis (deg/s) |
| 18-19 | gyro_y | -1998.05..1997.99 | 0.061 | Rotation rate on the Y axis (deg/s) |
| 20-21 | gyro_z | -1998.05..1997.99 | 0.061 | Rotation rate on the Z axis (deg/s) |
| 22-23 | quaternion_w | -2.0..1.99994 | 6.1e-05 | W value of the quaternion matrix |
| 24-25 | quaternion_x | -2.0..1.99994 | 6.1e-05 | X value of the quaternion matrix |
| 26-27 | quaternion_y | -2.0..1.99994 | 6.1e-05 | Y value of the quaternion matrix |
| 28-29 | quaternion_z | -2.0..1.99994 | 6.1e-05 | Z value of the quaternion matrix |

#### StampedImu Message (0x4A)

Measurement information being privided by the IMU sensor.

``` cpp
typedef struct {
    uint32_t timestamp;
    float eulerX;
    float eulerY;
    float eulerZ;
    float accX;
    float accY;
    float accZ;
    float gyroX;
    float gyroY;
    float gyroZ;
    float quaternionW;
    float quaternionX;
    float quaternionY;
    float quaternionZ;
} StampedImuMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | euler_x | -3.14171..3.14161 | 9.59e-05 | Euler angle on the X axis (rad) |
| 10-11 | euler_y | -3.14171..3.14161 | 9.59e-05 | Euler angle on the Y axis (rad) |
| 12-13 | euler_z | -3.14171..3.14161 | 9.59e-05 | Euler angle on the Z axis (rad) |
| 14-15 | acc_x | -4.0..3.99988 | 0.000122 | Acceleration on the X axis (g) |
| 16-17 | acc_y | -4.0..3.99988 | 0.000122 | Acceleration on the Y axis (g) |
| 18-19 | acc_z | -4.0..3.99988 | 0.000122 | Acceleration on the Z axis (g) |
| 20-21 | gyro_x | -1998.05..1997.99 | 0.061 | Rotation rate on the X axis (deg/s) |
| 22-23 | gyro_y | -1998.05..1997.99 | 0.061 | Rotation rate on the Y axis (deg/s) |
| 24-25 | gyro_z | -1998.05..1997.99 | 0.061 | Rotation rate on the Z axis (deg/s) |
| 26-27 | quaternion_w | -2.0..1.99994 | 6.1e-05 | W value of the quaternion matrix |
| 28-29 | quaternion_x | -2.0..1.99994 | 6.1e-05 | X value of the quaternion matrix |
| 30-31 | quaternion_y | -2.0..1.99994 | 6.1e-05 | Y value of the quaternion matrix |
| 32-33 | quaternion_z | -2.0..1.99994 | 6.1e-05 | Z value of the quaternion matrix |

#### Sonar Message (0x41)

Measurement information being provided by the sonar ring.

``` cpp
typedef struct {
    int16_t ping1;
    int16_t ping2;
    int16_t ping3;
    int16_t ping4;
    int16_t ping5;
} SonarMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | ping1 | -32768..32767 | 1 | Echo time in microseconds |
| 6-7 | ping2 | -32768..32767 | 1 | Echo time in microseconds |
| 8-9 | ping3 | -32768..32767 | 1 | Echo time in microseconds |
| 10-11 | ping4 | -32768..32767 | 1 | Echo time in microseconds |
| 12-13 | ping5 | -32768..32767 | 1 | Echo time in microseconds |

#### StampedSonar Message (0x4B)

Measurement information being provided by the sonar ring.

``` cpp
typedef struct {
    uint32_t timestamp;
    int16_t ping1;
    int16_t ping2;
    int16_t ping3;
    int16_t ping4;
    int16_t ping5;
} StampedSonarMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | ping1 | -32768..32767 | 1 | Echo time in microseconds |
| 10-11 | ping2 | -32768..32767 | 1 | Echo time in microseconds |
| 12-13 | ping3 | -32768..32767 | 1 | Echo time in microseconds |
| 14-15 | ping4 | -32768..32767 | 1 | Echo time in microseconds |
| 16-17 | ping5 | -32768..32767 | 1 | Echo time in microseconds |

#### Bumper Message (0x42)

Measurement information being provided by the bump sensors.

``` cpp
typedef struct {
    int8_t left;
    int8_t right;
} BumperMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4 | left | -128..127 | 1 | TBD |
| 5 | right | -128..127 | 1 | TBD |

#### StampedBumper Message (0x4C)

Measurement information being provided by the bump sensors.

``` cpp
typedef struct {
    uint32_t timestamp;
    int8_t left;
    int8_t right;
} StampedBumperMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8 | left | -128..127 | 1 | TBD |
| 9 | right | -128..127 | 1 | TBD |

#### State Message (0x60)

Current rover state information.

``` cpp
typedef struct {
    uint8_t apmState;
    uint8_t driveState;
    uint8_t autoState;
    uint8_t autoFlag;
    float voltage;
    float amperage;
    float groundSpeed;
} StateMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4 | apmState | 0..256 | 1 | Maps [Invalid, Init, Self-test, Drive] to [0, 1, 2, 3] |
| 5 | driveState | 0..256 | 1 | Maps [Invalid, Stop, Auto, Radio] to [0, 1, 2, 3] |
| 6 | autoState | 0..256 | 1 | Maps [Invalid, Full, Avoid, Stalled] to [0, 1, 2, 3] |
| 7 | autoFlag | 0..256 | 1 | Maps [None, Caution, Approach] to [0, 1, 2] |
| 8 | voltage | 0.0..25.6 | 0.1 | Current battery voltage (volts) |
| 9 | amperage | 0.0..25.6 | 0.1 | Current amperage draw on battery (amps) |
| 10 | groundSpeed | 0.0..25.6 | 0.1 | Current speed of rover (mph) |

#### StampedState Message (0x6A)

Current rover state information.

``` cpp
typedef struct {
    uint32_t timestamp;
    uint8_t apmState;
    uint8_t driveState;
    uint8_t autoState;
    uint8_t autoFlag;
    float voltage;
    float amperage;
    float groundSpeed;
} StampedStateMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8 | apmState | 0..256 | 1 | Maps [Invalid, Init, Self-test, Drive] to [0, 1, 2, 3] |
| 9 | driveState | 0..256 | 1 | Maps [Invalid, Stop, Auto, Radio] to [0, 1, 2, 3] |
| 10 | autoState | 0..256 | 1 | Maps [Invalid, Full, Avoid, Stalled] to [0, 1, 2, 3] |
| 11 | autoFlag | 0..256 | 1 | Maps [None, Caution, Approach] to [0, 1, 2] |
| 12 | voltage | 0.0..25.6 | 0.1 | Current battery voltage (volts) |
| 13 | amperage | 0.0..25.6 | 0.1 | Current amperage draw on battery (amps) |
| 14 | groundSpeed | 0.0..25.6 | 0.1 | Current speed of rover (mph) |

#### Control Message (0x80)

Rover output control values.

``` cpp
typedef struct {
    float speed;
    uint8_t steering;
} ControlMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | speed | -327.68..327.67 | 0.01 | Speed setting sent to controller (mph) |
| 6 | steering | 0..256 | 1 | Steering angle sent to controller (centered at 90 degrees) |

#### StampedControl Message (0x8A)

Rover output control values.

``` cpp
typedef struct {
    uint32_t timestamp;
    float speed;
    uint8_t steering;
} StampedControlMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | speed | -327.68..327.67 | 0.01 | Speed setting sent to controller (mph) |
| 10 | steering | 0..256 | 1 | Steering angle sent to controller (centered at 90 degrees) |

#### Waypoint Message (0x81)

Variables used to calculate control for waypoint navigation.

``` cpp
typedef struct {
    GpsAngle_t latStart;
    GpsAngle_t lonStart;
    GpsAngle_t latIntermediate;
    GpsAngle_t lonIntermediate;
    GpsAngle_t latTarget;
    GpsAngle_t lonTarget;
    float pathHeading;
} WaypointMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | lat_start.minutes | -32768..32767 | 1 | Previous waypoint latitude used for creating path (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 6-9 | lat_start.frac | -21474.8..21474.8 | 1e-05 | Previous waypoint latitude used for creating path (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 10-11 | lon_start.minutes | -32768..32767 | 1 | Previous waypoint longitude used for creating path (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 12-15 | lon_start.frac | -21474.8..21474.8 | 1e-05 | Previous waypoint longitude used for creating path (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 16-17 | lat_intermediate.minutes | -32768..32767 | 1 | Temporary target latitude calculated by line gravity (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 18-21 | lat_intermediate.frac | -21474.8..21474.8 | 1e-05 | Temporary target latitude calculated by line gravity (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 22-23 | lon_intermediate.minutes | -32768..32767 | 1 | Temporary target longitude calculated by line gravity (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 24-27 | lon_intermediate.frac | -21474.8..21474.8 | 1e-05 | Temporary target longitude calculated by line gravity (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 28-29 | lat_target.minutes | -32768..32767 | 1 | Current goal waypoint latitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 30-33 | lat_target.frac | -21474.8..21474.8 | 1e-05 | Current goal waypoint latitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 34-35 | lon_target.minutes | -32768..32767 | 1 | Current goal waypoint longitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 36-39 | lon_target.frac | -21474.8..21474.8 | 1e-05 | Current goal waypoint longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 40-41 | path_heading | -327.68..327.67 | 0.01 | Desired heading (deg) |

#### StampedWaypoint Message (0x8B)

Variables used to calculate control for waypoint navigation.

``` cpp
typedef struct {
    uint32_t timestamp;
    GpsAngle_t latStart;
    GpsAngle_t lonStart;
    GpsAngle_t latIntermediate;
    GpsAngle_t lonIntermediate;
    GpsAngle_t latTarget;
    GpsAngle_t lonTarget;
    float pathHeading;
} StampedWaypointMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | lat_start.minutes | -32768..32767 | 1 | Previous waypoint latitude used for creating path (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 10-13 | lat_start.frac | -21474.8..21474.8 | 1e-05 | Previous waypoint latitude used for creating path (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 14-15 | lon_start.minutes | -32768..32767 | 1 | Previous waypoint longitude used for creating path (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 16-19 | lon_start.frac | -21474.8..21474.8 | 1e-05 | Previous waypoint longitude used for creating path (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 20-21 | lat_intermediate.minutes | -32768..32767 | 1 | Temporary target latitude calculated by line gravity (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 22-25 | lat_intermediate.frac | -21474.8..21474.8 | 1e-05 | Temporary target latitude calculated by line gravity (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 26-27 | lon_intermediate.minutes | -32768..32767 | 1 | Temporary target longitude calculated by line gravity (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 28-31 | lon_intermediate.frac | -21474.8..21474.8 | 1e-05 | Temporary target longitude calculated by line gravity (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 32-33 | lat_target.minutes | -32768..32767 | 1 | Current goal waypoint latitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 34-37 | lat_target.frac | -21474.8..21474.8 | 1e-05 | Current goal waypoint latitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 38-39 | lon_target.minutes | -32768..32767 | 1 | Current goal waypoint longitude (degrees and nondecimal minutes). Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 40-43 | lon_target.frac | -21474.8..21474.8 | 1e-05 | Current goal waypoint longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 44-45 | path_heading | -327.68..327.67 | 0.01 | Desired heading (deg) |

#### Control Message (0x82)

Debug output for steering controller

``` cpp
typedef struct {
    float scSteering;
    float trueSteering;
    float kCrosstrack;
    float kYaw;
    float headingError;
    float crosstrackError;
} ControlMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-5 | sc_steering | -327.68..327.67 | 0.01 | Steering controller output angle (deg) (ccw: + cw: -) |
| 6-7 | true_steering | -327.68..327.67 | 0.01 | Platform specific steering angle (deg) (centered at 90 degrees) |
| 8-9 | k_crosstrack | -32.768..32.767 | 0.001 | Crosstrack error gain value |
| 10-11 | k_yaw | -32.768..32.767 | 0.001 | Yaw error gain value |
| 12-13 | heading_error | -327.68..327.67 | 0.01 | Heading error (deg) |
| 14-15 | crosstrack_error | -327.68..327.67 | 0.01 | Crosstrack error (m) |

#### StampedControl Message (0x8C)

Debug output for steering controller

``` cpp
typedef struct {
    uint32_t timestamp;
    float scSteering;
    float trueSteering;
    float kCrosstrack;
    float kYaw;
    float headingError;
    float crosstrackError;
} StampedControlMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8-9 | sc_steering | -327.68..327.67 | 0.01 | Steering controller output angle (deg) (ccw: + cw: -) |
| 10-11 | true_steering | -327.68..327.67 | 0.01 | Platform specific steering angle (deg) (centered at 90 degrees) |
| 12-13 | k_crosstrack | -32.768..32.767 | 0.001 | Crosstrack error gain value |
| 14-15 | k_yaw | -32.768..32.767 | 0.001 | Yaw error gain value |
| 16-17 | heading_error | -327.68..327.67 | 0.01 | Heading error (deg) |
| 18-19 | crosstrack_error | -327.68..327.67 | 0.01 | Crosstrack error (m) |

#### Version Message (0xA0)

Version information.

``` cpp
typedef struct {
    uint8_t debugMajor;
    uint8_t debugMinor;
    uint8_t apmMajor;
    uint8_t apmMinor;
} VersionMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4 | debug_major | 0..256 | 1 | Major version of debug protocol |
| 5 | debug_minor | 0..256 | 1 | Minor version of debug protocol |
| 6 | apm_major | 0..256 | 1 | Major version of APM protocol |
| 7 | apm_minor | 0..256 | 1 | Minor version of APM protocol |

#### StampedVersion Message (0xAA)

Version information.

``` cpp
typedef struct {
    uint32_t timestamp;
    uint8_t debugMajor;
    uint8_t debugMinor;
    uint8_t apmMajor;
    uint8_t apmMinor;
} StampedVersionMsg_t;
```

| Byte Offset | Name | Range | Resolution | Description |
| ------------ | ------------- | ------------- | ------------- | ------------- |
| 4-7 | timestamp | 0..4294967296 | 1 | Arduino time (ms) when the message was created |
| 8 | debug_major | 0..256 | 1 | Major version of debug protocol |
| 9 | debug_minor | 0..256 | 1 | Minor version of debug protocol |
| 10 | apm_major | 0..256 | 1 | Major version of APM protocol |
| 11 | apm_minor | 0..256 | 1 | Minor version of APM protocol |


#### Ascii Message (0x90)

A method for sending ASCII messages. These should only be used for active debugging and should be removed before committing to the repository.

``` cpp
typedef struct {
	LenString_t ascii
} AsciiMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-? | LenString_t | Struct of ASCII characters for temporary debugging msgs |

Example:
``` cpp
#ifdef M_DEBUG
	AsciiMsg_t msg;
	String tst = "ASCII MSG Here";
	msg.ascii.len = tst.length();
	tst.toCharArray(msg.ascii.data, tst.length() + 1);
	debugger.send(msg);
#endif
```