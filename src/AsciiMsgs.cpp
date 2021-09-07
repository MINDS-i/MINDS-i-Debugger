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


#include "AsciiMsgs.h"
#include "Arduino.h"
#include "MINDSiDebugger.h"
#include "Util.h"

uint8_t MINDSiDebugger::send(AsciiMsg_t msg)
{
    uint8_t* output = NULL;

    output = (uint8_t *)malloc(msg.ascii.len + 3 + 3);

    if (output == NULL) {
        return RETURN_CODE_ERR_ALLOC;
    }

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = msg.ascii.len + 3;

    // msg id
    output[3] = ASCII_ID;

    // data
    uint8_t index = 4;
    for (uint8_t i=0;i< msg.ascii.len;i++)
    {
        output[index] = msg.ascii.data[i];
        index++;
    }

    //checksum
    calc_checksum(output,msg.ascii.len + 4);

    Serial2.write(output,msg.ascii.len + 3 + 3);
    free(output);

    return RETURN_CODE_OK;

}

