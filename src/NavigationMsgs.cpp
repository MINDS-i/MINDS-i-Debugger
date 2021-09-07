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

#include "NavigationMsgs.h" 
#include "Arduino.h"
#include "MINDSiDebugger.h"
#include "Util.h"

uint8_t MINDSiDebugger::send(ControlMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(CONTROL_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = CONTROL_MSG_LEN + 3;

    // msg id
    output[3] = CONTROL_MSG_ID;

    // speed
	output[4] = msg.speed & 0xFF;
	output[5] = msg.speed >> 8;
	
    // steering
	output[6] = msg.steering & 0xFF;
	
    //checksum
    calc_checksum(output,CONTROL_MSG_LEN + 4);

    Serial2.write(output,CONTROL_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}

uint8_t MINDSiDebugger::send(WaypointMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(WAYPOINT_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = WAYPOINT_MSG_LEN + 3;

    // msg id
    output[3] = WAYPOINT_MSG_ID;

    // lat start (generally previously achived waypoint)
	output[4] = msg.latStart & 0xFF;
	output[5] = msg.latStart >> 8;
	output[6] = msg.latStart >> 16;
	output[7] = msg.latStart >> 24;

    // lon start (generally previously achived waypoint)
	output[8] = msg.lonStart & 0xFF;
	output[9] = msg.lonStart >> 8;
	output[10] = msg.lonStart >> 16;
	output[11] = msg.lonStart >> 24;

    // lat intermediate (generally produced by line-gravity)
	output[12] = msg.latIntermediate & 0xFF;
	output[13] = msg.latIntermediate >> 8;
	output[14] = msg.latIntermediate >> 16;
	output[15] = msg.latIntermediate >> 24;

    // lon start (generally produced by line-gravity)
	output[16] = msg.lonIntermediate & 0xFF;
	output[17] = msg.lonIntermediate >> 8;
	output[18] = msg.lonIntermediate >> 16;
	output[19] = msg.lonIntermediate >> 24;

    // lat start (generally the next waypoint)
	output[20] = msg.latTarget & 0xFF;
	output[21] = msg.latTarget >> 8;
	output[22] = msg.latTarget >> 16;
	output[23] = msg.latTarget >> 24;

    // lon start (generally the next waypoint)
	output[24] = msg.lonTarget & 0xFF;
	output[25] = msg.lonTarget >> 8;
	output[26] = msg.lonTarget >> 16;
	output[27] = msg.lonTarget >> 24;

    // path(desired) heading
	output[28] = msg.pathHeading & 0xFF;
	output[29] = msg.pathHeading >> 8;

    //checksum
    calc_checksum(output,WAYPOINT_MSG_LEN + 4);

    Serial2.write(output,WAYPOINT_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}
