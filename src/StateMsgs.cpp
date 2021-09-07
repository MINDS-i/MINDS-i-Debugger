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

#include "StateMsgs.h"
#include "Arduino.h"
#include "MINDSiDebugger.h"
#include "Util.h"

uint8_t MINDSiDebugger::send(StateMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(STATE_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STATE_MSG_LEN + 3;

    // msg id
    output[3] = STATE_MSG_ID;

    // apmState
	output[4] = msg.apmState & 0xFF;
	
    // driveState
	output[5] = msg.driveState & 0xFF;

    // autoState
	output[6] = msg.autoState & 0xFF;

    // autoFlag
	output[7] = msg.autoFlag & 0xFF;

    // voltage
	output[8] = msg.voltage & 0xFF;

    // amperage
	output[9] = msg.amperage & 0xFF;

    // groundSpeed
	output[10] = msg.groundSpeed & 0xFF;

    //checksum
    calc_checksum(output,STATE_MSG_LEN + 4);

    Serial2.write(output,STATE_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}

