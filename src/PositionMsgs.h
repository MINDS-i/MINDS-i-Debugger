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

#ifndef PositionMsgs_h
#define PositionMsgs_h

#include "Arduino.h"

# define RAW_POSITION_ID 0x10
# define RAW_POSITION_MSG_LEN 10
# define EXTRAPOLATED_POSITION_ID 0x11
# define EXTRAPLOATED_POSITION_MSG_LEN 10

typedef struct {
    int32_t latitude;
    int32_t longitude;
    uint16_t altitude;
}RawPositionMsg_t;

typedef struct {
    int32_t latitude;
    int32_t longitude;
    uint16_t altitude;
}ExtrapolatedPositionMsg_t;

#endif
