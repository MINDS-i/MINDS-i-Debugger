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

#include "SensorMsgs.h"
#include "Arduino.h"
#include "MINDSiDebugger.h"
#include "Util.h"

uint8_t MINDSiDebugger::send(ImuMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(IMU_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = IMU_MSG_LEN + 3;

    // msg id
    output[3] = IMU_MSG_ID;

    // euler x
	output[4] = msg.euler_x & 0xFF;
	output[5] = msg.euler_x >> 8;

    // euler y
	output[6] = msg.euler_y & 0xFF;
	output[7] = msg.euler_y >> 8;

    // euler z
	output[8] = msg.euler_z & 0xFF;
	output[9] = msg.euler_z >> 8;

    // acc x
	output[10] = msg.acc_x & 0xFF;
	output[11] = msg.acc_x >> 8;

    // acc y
	output[12] = msg.acc_y & 0xFF;
	output[13] = msg.acc_y >> 8;

    // acc z
	output[14] = msg.acc_z & 0xFF;
	output[15] = msg.acc_z >> 8;

    // gyro x
	output[16] = msg.gyro_x & 0xFF;
	output[17] = msg.gyro_x >> 8;

    // gyro y
	output[18] = msg.gyro_y & 0xFF;
	output[19] = msg.gyro_y >> 8;

    // gyro z
	output[20] = msg.gyro_z & 0xFF;
	output[21] = msg.gyro_z >> 8;

    //checksum
    calc_checksum(output,IMU_MSG_LEN + 4);

    Serial2.write(output,IMU_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}

uint8_t MINDSiDebugger::send(SonarMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(SONAR_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = SONAR_MSG_LEN + 3;

    // msg id
    output[3] = SONAR_MSG_ID;

    // ping1
	output[4] = msg.ping1 & 0xFF;
	output[5] = msg.ping1 >> 8;

    // ping2
	output[6] = msg.ping2 & 0xFF;
	output[7] = msg.ping2 >> 8;

    // ping3
	output[8] = msg.ping3 & 0xFF;
	output[9] = msg.ping3 >> 8;

    // ping4
	output[10] = msg.ping4 & 0xFF;
	output[11] = msg.ping4 >> 8;

    // ping5
	output[12] = msg.ping5 & 0xFF;
	output[13] = msg.ping5 >> 8;

    //checksum
    calc_checksum(output,SONAR_MSG_LEN + 4);

    Serial2.write(output,SONAR_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}

uint8_t MINDSiDebugger::send(BumperMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(BUMPER_MSG_LEN + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = BUMPER_MSG_LEN + 3;

    // msg id
    output[3] = BUMPER_MSG_ID;

    // left
	output[4] = msg.left & 0xFF;

    // right
	output[5] = msg.right & 0xFF;

    //checksum
    calc_checksum(output,BUMPER_MSG_LEN + 4);

    Serial2.write(output,BUMPER_MSG_LEN + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}
