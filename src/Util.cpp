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

#include "Arduino.h"
#include "Util.h"

void calc_checksum(uint8_t* ogi_cmd, uint8_t len){
    uint16_t crc = 0x0001;

    for (uint8_t i = 3; i < len; i++)
    {
 	    crc = (crc << 8) ^ crctable[((crc >> 8) ^ ogi_cmd[i])];
    }

    ogi_cmd[len+1] = (uint8_t)crc; 
    ogi_cmd[len] = (uint8_t)(crc >> 8);
}
