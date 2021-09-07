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

#ifndef OrientationMsgs_h
#define OrientationMsgs_h

#include "Arduino.h"

# define ORIENTATION_MSG_ID 0x20
# define ORIENTATION_MSG_LEN 6

typedef struct {
	int16_t heading;
	int16_t roll;
	int16_t pitch;
}OrientationMsg_t;

#endif
