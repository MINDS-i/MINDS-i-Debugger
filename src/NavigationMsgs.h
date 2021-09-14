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

#ifndef NavigationMsgs_h
#define NavigationMsgs_h

#include "Arduino.h"
#include "Util.h"

# define CONTROL_MSG_ID 0x80
# define CONTROL_MSG_LEN 3
# define WAYPOINT_MSG_ID 0x81
# define WAYPOINT_MSG_LEN 38

typedef struct {
    int16_t speed;
    uint8_t steering;
}ControlMsg_t;

typedef struct {
    GpsAngle_t latStart;
    GpsAngle_t lonStart;
    GpsAngle_t latIntermediate;
    GpsAngle_t lonIntermediate;
    GpsAngle_t latTarget;
    GpsAngle_t lonTarget;
    int16_t pathHeading;
}WaypointMsg_t;

#endif
