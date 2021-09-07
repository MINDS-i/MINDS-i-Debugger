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

#ifndef StateMsgs_h
#define StateMsgs_h

#include "Arduino.h"

# define STATE_MSG_ID 0x60
# define STATE_MSG_LEN 7

typedef struct {
    uint8_t apmState;
    uint8_t driveState;
    uint8_t autoState;
    uint8_t autoFlag;
    uint8_t voltage;
    uint8_t amperage;
    uint8_t groundSpeed;
}StateMsg_t;

#endif
