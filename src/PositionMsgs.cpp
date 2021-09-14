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

#include "PositionMsgs.h"
#include "Arduino.h"
#include "MINDSiDebugger.h"

uint8_t MINDSiDebugger::send(RawPositionMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(RAW_POSITION_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = RAW_POSITION_MSG_LEN + 3;

    // msg id
    output[3] = RAW_POSITION_ID;

    // lat
	output[4] = msg.latitude.minutes & 0xFF;
	output[5] = msg.latitude.minutes >> 8;
	output[6] = msg.latitude.frac & 0xFF;
	output[7] = msg.latitude.frac >> 8;
	output[8] = msg.latitude.frac >> 16;
	output[9] = msg.latitude.frac >> 24;

    // lon
	output[10] = msg.longitude.minutes & 0xFF;
	output[11] = msg.longitude.minutes >> 8;
	output[12] = msg.longitude.frac & 0xFF;
	output[13] = msg.longitude.frac >> 8;
	output[14] = msg.longitude.frac >> 16;
	output[15] = msg.longitude.frac >> 24;

    // alt
	output[16] = msg.altitude & 0xFF;
	output[17] = msg.altitude >> 8;

    //checksum
    calc_checksum(output,RAW_POSITION_MSG_LEN + 4);

    Serial2.write(output,RAW_POSITION_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}

uint8_t MINDSiDebugger::send(ExtrapolatedPositionMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(EXTRAPLOATED_POSITION_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = EXTRAPLOATED_POSITION_MSG_LEN + 3;

    // msg id
    output[3] = EXTRAPOLATED_POSITION_ID;

    // lat
	output[4] = msg.latitude.minutes & 0xFF;
	output[5] = msg.latitude.minutes >> 8;
	output[6] = msg.latitude.frac & 0xFF;
	output[7] = msg.latitude.frac >> 8;
	output[8] = msg.latitude.frac >> 16;
	output[9] = msg.latitude.frac >> 24;

    // lon
	output[10] = msg.longitude.minutes & 0xFF;
	output[11] = msg.longitude.minutes >> 8;
	output[12] = msg.longitude.frac & 0xFF;
	output[13] = msg.longitude.frac >> 8;
	output[14] = msg.longitude.frac >> 16;
	output[15] = msg.longitude.frac >> 24;

    // alt
	output[16] = msg.altitude & 0xFF;
	output[17] = msg.altitude >> 8;

    //checksum
    calc_checksum(output,EXTRAPLOATED_POSITION_MSG_LEN + 4);

    Serial2.write(output,EXTRAPLOATED_POSITION_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}
