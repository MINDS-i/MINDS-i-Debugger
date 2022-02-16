# MINDS-i-Debugger
Code to assist with debugging MINDSi robots

This library contains code for providing logging and debugging msgs on a dedicated serial link.

## Usage

To be filled out.

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
| 0x10 | Raw Position | 
| 0x11 | Extrapolated Position | 
| 0x20 | Orientation | 
| 0x30 | Radio |
| 0x40 | IMU |
| 0x41 | Sonar |
| 0x42 | Bumper |
| 0x60 | State | 
| 0x70 | Configuration |
| 0x80 | Control |
| 0x81 | Waypoint |
| 0x90 | ASCII |
| 0xA0 | Version |

## Custom Data Types

```
typedef struct {
	char data[256];
	u8 len;
}LenString_t;

typedef struct {
  int16_t minutes;
  int32_t frac;
}GpsAngle_t;
```

## Message Definitions

#### Raw Position Message (0x10)

Positioning information being provided by the GPS sensor.

```
typedef struct {
	GpsAngle_t latitude;
	GpsAngle_t longitude;
	u16 altitude;
}RawPositionMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-5 | latitude_minutes | GPS reciever reported latitude (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 6-9 | latitude_frac | GPS reciever reported latitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 10-11 | longitude_minutes | GPS reciever reported longitude (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 12-15 | longitude_frac | GPS reciever reported longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 16-17 | altitude | GPS reciever reported altitude (meters). Map `0..(2^16-1) to - 900..19000`, resolution ~0.3m |

#### Extrapolated Position Message (0x11)

Position information created through calculation rather than sensed directly.

```
typedef struct {
	GpsAngle_t latitude;
	GpsAngle_t longitude;
	u16 altitude;
}ExtrapolatedPositionMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-5 | latitude_minutes | GPS reciever reported latitude (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 6-9 | latitude_frac | GPS reciever reported latitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 10-11 | longitude_minutes | GPS reciever reported longitude (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 12-15 | longitude_frac | GPS reciever reported longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 12-13 | altitude | Altitude extraploated between GPS readings (meters). Map `0..(2^16-1) to - 900..19000`, resolution ~0.3m |

#### Orientation Message (0x20)

Orientation information used for control puposes.

```
typedef struct {
	s16 heading;
	s16 roll;
	s16 pitch;
}OrientationMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-5 | heading | True heading (deg) * 100, range -18000..18000 representing -180.00 to 180.00 |
| 6-7 | roll | Roll (deg) * 100, range -18000..18000 representing -180.00 to 180.00 |
| 8-9 | pitch | Pitch (deg) * 100, range -18000..18000 representing -180.00 to 180.00 |

#### Radio Message (0x30)

Commands being sent by the radio controller.

```
typedef struct {
	s16 speed;
	u8 steering;
}RadioMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-5 | speed | Speed command from radio controller (mph) * 100 |
| 6 | steering | Steering value from radio controller |

#### IMU Message (0x40)

Measurement information being privided by the IMU sensor.

```
typedef struct {
	s16 euler_x;
	s16 euler_y;
	s16 euler_z;
	s16 acc_x;
	s16 acc_y;
	s16 acc_z;
	s16 gyro_x;
	s16 gyro_y;
	s16 gyro_z;	
}ImuMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-5 | euler_x | Euler angle on the X axis (rad)  * 10430, range -32767..32767 representing -pi to pi |
| 6-7 | euler_y | Euler angle on the Y axis (rad)  * 10430, range -32767..32767 representing -pi to pi |
| 8-9 | euler_z | Euler angle on the Z axis (rad)  * 10430, range -32767..32767 representing -pi to pi |
| 10-11 | acc_x | Acceleration on the X axis (g)  * 8192, range -32768..32767 representing -4 to 4 |
| 12-13 | acc_y | Acceleration angle on the Y axis (g)  * 8192, range -32768..32767 representing -4 to 4 |
| 14-15 | acc_z | Acceleration angle on the Z axis (g)  * 8192, range -32768..32767 representing -4 to 4 |
| 16-17 | gyro_x | Rotation rate on the X axis (deg/s)  * 16.4, range -32768..32767 representing -2000 to 2000 |
| 18-19 | gyro_y | Rotation rate angle on the Y axis (deg/s)  * 16.4, range -32768..32767 representing -2000 to 2000 |
| 20-21 | gyro_z | Rotation rate angle on the Z axis (deg/s)  * 16.4, range -32768..32767 representing -2000 to 2000 |

#### Sonar Message (0x41)

Measurement information being provided by the sonar ring.

```
typedef struct {
	u16 ping1;
	u16 ping2;
	u16 ping3;
	u16 ping4;
	u16 ping5;
}SonarMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-5 | ping1 | Echo time in microseconds |
| 6-7 | ping2 | Echo time in microseconds |
| 8-9 | ping3 | Echo time in microseconds |
| 10-11 | ping4 | Echo time in microseconds |
| 12-13 | ping5 | Echo time in microseconds |

#### Bumper Message (0x42)

TBD

#### State Message (0x60)

Current rover state information

```
typedef struct {
	u8 apmState;
	u8 driveState;
	u8 autoState;
	u8 autoFlag;
	u8 voltage;
	u8 amperage;
	u8 groundSpeed;
}StateMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4 | apmState | Maps [Invalid, Init, Self-test, Drive] to [0,1,2,3] |
| 5 | driveState | Maps [Invalid, Stop, Auto, Radio] to [0,1,2,3] |
| 6 | autoState | Maps [Invalid, Full, Avoid, Stalled] to [0,1,2,3] |
| 7 | autoFlag | Maps [None, Caution, Approach] to [0,1,2] |
| 8 | voltage | Current battery voltage * 10 (volts) |
| 9 | amperage | Current amperage draw on battery * 10 (amps) |
| 8 | groundSpeed | Current speed of rover * 10 (mph) |

#### Configuration Message (0x70)

TBD

#### Control Message (0x80)

Rover output control values.

```
typedef struct {
	s16 speed;
	u8 steering;
}ControlMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-5 | speed * 100 | speed setting sent to controller (mph) |
| 6 | steering | steering angle sent to controller (angle, 90 = no turn angle) |

#### Waypoint Message (0x81)

Variables used to calculate control for waypoint navigation.

```
typedef struct {
	GpsAngle_t latStart;
	GpsAngle_t lonStart;
	GpsAngle_t latIntermediate;
	GpsAngle_t lonIntermediate;
	GpsAngle_t latTarget;
	GpsAngle_t lonTarget;
	s16 pathHeading;
}WaypointMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-5 | latStart_minutes | Previous waypoint latitude used for creating path (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 6-9 | latStart_frac | Previous waypoint latitude used for creating path (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 10-11 | lonStart_minutes | Previous waypoint longitude used for creating path (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 12-15 | lonStart_frac | Previous waypoint longitude used for creating path (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 16-17 | latIntermediate_minutes | Temporary target latitude calculated by line gravity (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 18-21 | latIntermediate_frac | Temporary target latitude calculated by line gravity (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 22-23 | lonIntermediate_minutes | Temporary target longitude calculated by line gravity (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 24-27 | lonIntermediate_frac | Temporary target longitude calculated by line gravity (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 28-29 | latTarget_minutes | Current goal waypoint latitude.  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 30-33 | latTarget_frac | Current goal waypoint latitude. Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 34-35 | lonTarget_minutes | Current goal waypoint longitude (degrees and nondecimal minutes).  Specifically DDDMM of the DDDMM.MMMMM NMEA string |
| 36-39 | lonTarget_frac | Current goal waypoint longitude (decimal minutes). Specifically MMMMM of the DDDMM.MMMMM NMEA string |
| 40-41 | pathHeading | Desired heading * 100 deg, range -18000..18000 representing -180.00 to 180.00 |

#### ASCII Message (0x90)

A method for sending ASCII messages.  These should only be used for active debugging and should be removed before committing to the repository.

```
typedef struct {
	LenString_t ascii
}AsciiMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4-? | LenString_t | Struct of ASCII characters for temporary debugging msgs |

Example:
```
#ifdef M_DEBUG
	AsciiMsg_t msg;
	String tst = "ASCII MSG Here";
	msg.ascii.len = tst.length();
	tst.toCharArray(msg.ascii.data,tst.length()+1);
	debugger.send(msg);
#endif
```

#### Version Message (0xA0)

Version information

```
typedef struct {
	u8 debug_major
	u8 debug_minor
	u8 apm_major
	u8 apm_minor
}AsciiMsg_t;
```

| Byte Offset | Name | Description | 
| ------------ | ------------- | ------------- |
| 4 | debug_major | Major version of debug protocol |
| 5 | debug_minor | Minor version of debug protocol |
| 6 | apm_major | Major version of amp protocol |
| 7 | apm_minor | Minor version of amp protocol |
