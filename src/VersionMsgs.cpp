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

#include "VersionMsgs.h"
#include "Arduino.h"
#include "MINDSiDebugger.h"
#include "Util.h"

uint8_t MINDSiDebugger::send(VersionMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(VERSION_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = VERSION_MSG_LEN + 3;

    // msg id
    output[3] = VERSION_MSG_ID;

    // debug_major
	output[4] = msg.debug_major & 0xFF;
	
    // debug_minor
	output[5] = msg.debug_minor & 0xFF;

    // apm_major
	output[6] = msg.apm_major & 0xFF;
	
    // apm_minor
	output[7] = msg.apm_minor & 0xFF;

    //checksum
    calc_checksum(output,VERSION_MSG_LEN + 4);

    Serial2.write(output,VERSION_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}

