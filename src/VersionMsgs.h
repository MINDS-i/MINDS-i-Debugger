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

#ifndef VersionMsgs_h
#define VersionMsgs_h

#include "Arduino.h"

# define VERSION_MSG_ID 0x30
# define VERSION_MSG_LEN 4

typedef struct {
    uint8_t debug_major;
    uint8_t debug_minor;
    uint8_t apm_major;
    uint8_t apm_minor;
}VersionMsg_t;

#endif
