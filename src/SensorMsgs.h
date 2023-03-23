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

#ifndef SensorMsgs_h
#define SensorMsgs_h

#include "Arduino.h"

# define IMU_MSG_ID 0x40
# define IMU_MSG_LEN 30
# define SONAR_MSG_ID 0x41
# define SONAR_MSG_LEN 10
# define BUMPER_MSG_ID 0x42
# define BUMPER_MSG_LEN 2

typedef struct {
    unsigned long ms;
    int16_t euler_x;
    int16_t euler_y;
    int16_t euler_z;
    int16_t acc_x;
    int16_t acc_y;
    int16_t acc_z;
    int16_t gyro_x;
    int16_t gyro_y;
    int16_t gyro_z;
    int16_t quaternion_w;
    int16_t quaternion_x;
    int16_t quaternion_y;
    int16_t quaternion_z;
}ImuMsg_t;

typedef struct {
    int16_t ping1;
    int16_t ping2;
    int16_t ping3;
    int16_t ping4;
    int16_t ping5;
}SonarMsg_t;

typedef struct {
    int8_t left;
    int8_t right;
}BumperMsg_t;

#endif
