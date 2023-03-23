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

    // steer controller
	output[7] = msg.sc_steering & 0xFF;
	output[8] = msg.sc_steering >> 8;

    // true steer
	output[9] = msg.true_steering & 0xFF;
	output[10] = msg.true_steering >> 8;

    // k_crosstrack
	output[11] = msg.k_crosstrack & 0xFF;
	output[12] = msg.k_crosstrack >> 8;

    // k_yaw
	output[13] = msg.k_yaw & 0xFF;
	output[14] = msg.k_yaw >> 8;

    // heading
	output[15] = msg.heading_error & 0xFF;
	output[16] = msg.heading_error >> 8;

    // heading error
	output[17] = msg.crosstrack_error & 0xFF;
	output[18] = msg.crosstrack_error >> 8;
	
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
	output[4] = msg.latStart.minutes & 0xFF;
	output[5] = msg.latStart.minutes >> 8;
	output[6] = msg.latStart.frac & 0xFF;
	output[7] = msg.latStart.frac >> 8;
	output[8] = msg.latStart.frac >> 16;
	output[9] = msg.latStart.frac >> 24;

    // lon start (generally previously achived waypoint)
	output[10] = msg.lonStart.minutes & 0xFF;
	output[11] = msg.lonStart.minutes >> 8;
	output[12] = msg.lonStart.frac & 0xFF;
	output[13] = msg.lonStart.frac >> 8;
	output[14] = msg.lonStart.frac >> 16;
	output[15] = msg.lonStart.frac >> 24;

    // lat intermediate (generally produced by line-gravity)
	output[16] = msg.latIntermediate.minutes & 0xFF;
	output[17] = msg.latIntermediate.minutes >> 8;
	output[18] = msg.latIntermediate.frac & 0xFF;
	output[19] = msg.latIntermediate.frac >> 8;
	output[20] = msg.latIntermediate.frac >> 16;
	output[21] = msg.latIntermediate.frac >> 24;

    // lon start (generally produced by line-gravity)
	output[22] = msg.lonIntermediate.minutes & 0xFF;
	output[23] = msg.lonIntermediate.minutes >> 8;
	output[24] = msg.lonIntermediate.frac & 0xFF;
	output[25] = msg.lonIntermediate.frac >> 8;
	output[26] = msg.lonIntermediate.frac >> 16;
	output[27] = msg.lonIntermediate.frac >> 24;

    // lat start (generally the next waypoint)
	output[28] = msg.latTarget.minutes & 0xFF;
	output[29] = msg.latTarget.minutes >> 8;
	output[30] = msg.latTarget.frac & 0xFF;
	output[31] = msg.latTarget.frac >> 8;
	output[32] = msg.latTarget.frac >> 16;
	output[33] = msg.latTarget.frac >> 24;

    // lon start (generally the next waypoint)
	output[34] = msg.lonTarget.minutes & 0xFF;
	output[35] = msg.lonTarget.minutes >> 8;
	output[36] = msg.lonTarget.frac & 0xFF;
	output[37] = msg.lonTarget.frac >> 8;
	output[38] = msg.lonTarget.frac >> 16;
	output[39] = msg.lonTarget.frac >> 24;

    // path(desired) heading
	output[40] = msg.pathHeading & 0xFF;
	output[41] = msg.pathHeading >> 8;

    //checksum
    calc_checksum(output,WAYPOINT_MSG_LEN + 4);

    Serial2.write(output,WAYPOINT_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}
