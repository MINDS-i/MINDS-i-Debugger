// This file was auto-generated. Any changes to this file may be overwritten.
/* Copyright 2021 MINDS-i, INC.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

#ifndef DebugMsgs_h
#define DebugMsgs_h

#include "Datatypes.h"
#include "Arduino.h"
    
# define RAW_POSITION_MSG_ID 0x10
# define RAW_POSITION_MSG_LEN 14
# define STAMPED_RAW_POSITION_MSG_ID 0x1A
# define STAMPED_RAW_POSITION_MSG_LEN 18
# define EXTRAPOLATED_POSITION_MSG_ID 0x11
# define EXTRAPOLATED_POSITION_MSG_LEN 14
# define STAMPED_EXTRAPOLATED_POSITION_MSG_ID 0x1B
# define STAMPED_EXTRAPOLATED_POSITION_MSG_LEN 18
# define ORIENTATION_MSG_ID 0x20
# define ORIENTATION_MSG_LEN 6
# define STAMPED_ORIENTATION_MSG_ID 0x2A
# define STAMPED_ORIENTATION_MSG_LEN 10
# define RADIO_MSG_ID 0x30
# define RADIO_MSG_LEN 3
# define STAMPED_RADIO_MSG_ID 0x3A
# define STAMPED_RADIO_MSG_LEN 7
# define IMU_MSG_ID 0x40
# define IMU_MSG_LEN 26
# define STAMPED_IMU_MSG_ID 0x4A
# define STAMPED_IMU_MSG_LEN 30
# define SONAR_MSG_ID 0x41
# define SONAR_MSG_LEN 10
# define STAMPED_SONAR_MSG_ID 0x4B
# define STAMPED_SONAR_MSG_LEN 14
# define BUMPER_MSG_ID 0x42
# define BUMPER_MSG_LEN 2
# define STAMPED_BUMPER_MSG_ID 0x4C
# define STAMPED_BUMPER_MSG_LEN 6
# define STATE_MSG_ID 0x60
# define STATE_MSG_LEN 7
# define STAMPED_STATE_MSG_ID 0x6A
# define STAMPED_STATE_MSG_LEN 11
# define CONTROL_MSG_ID 0x80
# define CONTROL_MSG_LEN 3
# define STAMPED_CONTROL_MSG_ID 0x8A
# define STAMPED_CONTROL_MSG_LEN 7
# define WAYPOINT_MSG_ID 0x81
# define WAYPOINT_MSG_LEN 38
# define STAMPED_WAYPOINT_MSG_ID 0x8B
# define STAMPED_WAYPOINT_MSG_LEN 42
# define STEERING_CONTROLLER_MSG_ID 0x82
# define STEERING_CONTROLLER_MSG_LEN 36
# define STAMPED_STEERING_CONTROLLER_MSG_ID 0x8C
# define STAMPED_STEERING_CONTROLLER_MSG_LEN 40
# define VERSION_MSG_ID 0xA0
# define VERSION_MSG_LEN 4
# define STAMPED_VERSION_MSG_ID 0xAA
# define STAMPED_VERSION_MSG_LEN 8
# define ASCII_MSG_ID 0x90

typedef struct {
    GpsAngle_t latitude;
    GpsAngle_t longitude;
    float altitude;
} RawPositionMsg_t;

typedef struct {
    uint32_t timestamp;
    GpsAngle_t latitude;
    GpsAngle_t longitude;
    float altitude;
} StampedRawPositionMsg_t;

typedef struct {
    GpsAngle_t latitude;
    GpsAngle_t longitude;
    float altitude;
} ExtrapolatedPositionMsg_t;

typedef struct {
    uint32_t timestamp;
    GpsAngle_t latitude;
    GpsAngle_t longitude;
    float altitude;
} StampedExtrapolatedPositionMsg_t;

typedef struct {
    float heading;
    float roll;
    float pitch;
} OrientationMsg_t;

typedef struct {
    uint32_t timestamp;
    float heading;
    float roll;
    float pitch;
} StampedOrientationMsg_t;

typedef struct {
    float speed;
    uint8_t steering;
} RadioMsg_t;

typedef struct {
    uint32_t timestamp;
    float speed;
    uint8_t steering;
} StampedRadioMsg_t;

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

typedef struct {
    int16_t ping1;
    int16_t ping2;
    int16_t ping3;
    int16_t ping4;
    int16_t ping5;
} SonarMsg_t;

typedef struct {
    uint32_t timestamp;
    int16_t ping1;
    int16_t ping2;
    int16_t ping3;
    int16_t ping4;
    int16_t ping5;
} StampedSonarMsg_t;

typedef struct {
    int8_t left;
    int8_t right;
} BumperMsg_t;

typedef struct {
    uint32_t timestamp;
    int8_t left;
    int8_t right;
} StampedBumperMsg_t;

typedef struct {
    uint8_t apmState;
    uint8_t driveState;
    uint8_t autoState;
    uint8_t autoFlag;
    float voltage;
    float amperage;
    float groundSpeed;
} StateMsg_t;

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

typedef struct {
    float speed;
    uint8_t steering;
} ControlMsg_t;

typedef struct {
    uint32_t timestamp;
    float speed;
    uint8_t steering;
} StampedControlMsg_t;

typedef struct {
    GpsAngle_t latStart;
    GpsAngle_t lonStart;
    GpsAngle_t latIntermediate;
    GpsAngle_t lonIntermediate;
    GpsAngle_t latTarget;
    GpsAngle_t lonTarget;
    float pathHeading;
} WaypointMsg_t;

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

typedef struct {
    float scSteering;
    float trueSteering;
    float kCrosstrack;
    float kYaw;
    float headingError;
    float crosstrackError;
    GpsAngle_t goalPt1Lat;
    GpsAngle_t goalPt1Lon;
    GpsAngle_t goalPt2Lat;
    GpsAngle_t goalPt2Lon;
} SteeringControllerMsg_t;

typedef struct {
    uint32_t timestamp;
    float scSteering;
    float trueSteering;
    float kCrosstrack;
    float kYaw;
    float headingError;
    float crosstrackError;
    GpsAngle_t goalPt1Lat;
    GpsAngle_t goalPt1Lon;
    GpsAngle_t goalPt2Lat;
    GpsAngle_t goalPt2Lon;
} StampedSteeringControllerMsg_t;

typedef struct {
    uint8_t debugMajor;
    uint8_t debugMinor;
    uint8_t apmMajor;
    uint8_t apmMinor;
} VersionMsg_t;

typedef struct {
    uint32_t timestamp;
    uint8_t debugMajor;
    uint8_t debugMinor;
    uint8_t apmMajor;
    uint8_t apmMinor;
} StampedVersionMsg_t;

typedef struct {
    LenString_t ascii;
} AsciiMsg_t;

#endif