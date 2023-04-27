// This file was auto-generated. Any changes to this file may be overwritten.
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

#include "DebugMsgs.h" 
#include "Arduino.h"
#include "MINDSiDebugger.h"

uint8_t MINDSiDebugger::send(RawPositionMsg_t &msg)
{
    uint8_t output[RAW_POSITION_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = RAW_POSITION_MSG_LEN + 3;

    // msg id
    output[3] = RAW_POSITION_MSG_ID;

    // latitude
    output[4] = msg.latitude.minutes & 0xFF;
    output[5] = msg.latitude.minutes >> 8;
    output[6] = int32_t(round(msg.latitude.frac * 100000.0)) & 0xFF;
    output[7] = int32_t(round(msg.latitude.frac * 100000.0)) >> 8;
    output[8] = int32_t(round(msg.latitude.frac * 100000.0)) >> 16;
    output[9] = int32_t(round(msg.latitude.frac * 100000.0)) >> 24;

    // longitude
    output[10] = msg.longitude.minutes & 0xFF;
    output[11] = msg.longitude.minutes >> 8;
    output[12] = int32_t(round(msg.longitude.frac * 100000.0)) & 0xFF;
    output[13] = int32_t(round(msg.longitude.frac * 100000.0)) >> 8;
    output[14] = int32_t(round(msg.longitude.frac * 100000.0)) >> 16;
    output[15] = int32_t(round(msg.longitude.frac * 100000.0)) >> 24;

    // altitude
    output[16] = uint16_t(round((msg.altitude + 900.0) * 3.293216)) & 0xFF;
    output[17] = uint16_t(round((msg.altitude + 900.0) * 3.293216)) >> 8;

    // checksum
    calc_checksum(output, RAW_POSITION_MSG_LEN + 4);

    Serial2.write(output, RAW_POSITION_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedRawPositionMsg_t &msg)
{
    uint8_t output[STAMPED_RAW_POSITION_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_RAW_POSITION_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_RAW_POSITION_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // latitude
    output[8] = msg.latitude.minutes & 0xFF;
    output[9] = msg.latitude.minutes >> 8;
    output[10] = int32_t(round(msg.latitude.frac * 100000.0)) & 0xFF;
    output[11] = int32_t(round(msg.latitude.frac * 100000.0)) >> 8;
    output[12] = int32_t(round(msg.latitude.frac * 100000.0)) >> 16;
    output[13] = int32_t(round(msg.latitude.frac * 100000.0)) >> 24;

    // longitude
    output[14] = msg.longitude.minutes & 0xFF;
    output[15] = msg.longitude.minutes >> 8;
    output[16] = int32_t(round(msg.longitude.frac * 100000.0)) & 0xFF;
    output[17] = int32_t(round(msg.longitude.frac * 100000.0)) >> 8;
    output[18] = int32_t(round(msg.longitude.frac * 100000.0)) >> 16;
    output[19] = int32_t(round(msg.longitude.frac * 100000.0)) >> 24;

    // altitude
    output[20] = uint16_t(round((msg.altitude + 900.0) * 3.293216)) & 0xFF;
    output[21] = uint16_t(round((msg.altitude + 900.0) * 3.293216)) >> 8;

    // checksum
    calc_checksum(output, STAMPED_RAW_POSITION_MSG_LEN + 4);

    Serial2.write(output, STAMPED_RAW_POSITION_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(ExtrapolatedPositionMsg_t &msg)
{
    uint8_t output[EXTRAPOLATED_POSITION_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = EXTRAPOLATED_POSITION_MSG_LEN + 3;

    // msg id
    output[3] = EXTRAPOLATED_POSITION_MSG_ID;

    // latitude
    output[4] = msg.latitude.minutes & 0xFF;
    output[5] = msg.latitude.minutes >> 8;
    output[6] = int32_t(round(msg.latitude.frac * 100000.0)) & 0xFF;
    output[7] = int32_t(round(msg.latitude.frac * 100000.0)) >> 8;
    output[8] = int32_t(round(msg.latitude.frac * 100000.0)) >> 16;
    output[9] = int32_t(round(msg.latitude.frac * 100000.0)) >> 24;

    // longitude
    output[10] = msg.longitude.minutes & 0xFF;
    output[11] = msg.longitude.minutes >> 8;
    output[12] = int32_t(round(msg.longitude.frac * 100000.0)) & 0xFF;
    output[13] = int32_t(round(msg.longitude.frac * 100000.0)) >> 8;
    output[14] = int32_t(round(msg.longitude.frac * 100000.0)) >> 16;
    output[15] = int32_t(round(msg.longitude.frac * 100000.0)) >> 24;

    // altitude
    output[16] = uint16_t(round((msg.altitude + 900.0) * 3.293216)) & 0xFF;
    output[17] = uint16_t(round((msg.altitude + 900.0) * 3.293216)) >> 8;

    // checksum
    calc_checksum(output, EXTRAPOLATED_POSITION_MSG_LEN + 4);

    Serial2.write(output, EXTRAPOLATED_POSITION_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedExtrapolatedPositionMsg_t &msg)
{
    uint8_t output[STAMPED_EXTRAPOLATED_POSITION_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_EXTRAPOLATED_POSITION_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_EXTRAPOLATED_POSITION_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // latitude
    output[8] = msg.latitude.minutes & 0xFF;
    output[9] = msg.latitude.minutes >> 8;
    output[10] = int32_t(round(msg.latitude.frac * 100000.0)) & 0xFF;
    output[11] = int32_t(round(msg.latitude.frac * 100000.0)) >> 8;
    output[12] = int32_t(round(msg.latitude.frac * 100000.0)) >> 16;
    output[13] = int32_t(round(msg.latitude.frac * 100000.0)) >> 24;

    // longitude
    output[14] = msg.longitude.minutes & 0xFF;
    output[15] = msg.longitude.minutes >> 8;
    output[16] = int32_t(round(msg.longitude.frac * 100000.0)) & 0xFF;
    output[17] = int32_t(round(msg.longitude.frac * 100000.0)) >> 8;
    output[18] = int32_t(round(msg.longitude.frac * 100000.0)) >> 16;
    output[19] = int32_t(round(msg.longitude.frac * 100000.0)) >> 24;

    // altitude
    output[20] = uint16_t(round((msg.altitude + 900.0) * 3.293216)) & 0xFF;
    output[21] = uint16_t(round((msg.altitude + 900.0) * 3.293216)) >> 8;

    // checksum
    calc_checksum(output, STAMPED_EXTRAPOLATED_POSITION_MSG_LEN + 4);

    Serial2.write(output, STAMPED_EXTRAPOLATED_POSITION_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(OrientationMsg_t &msg)
{
    uint8_t output[ORIENTATION_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = ORIENTATION_MSG_LEN + 3;

    // msg id
    output[3] = ORIENTATION_MSG_ID;

    // heading
    output[4] = int16_t(round(msg.heading * 100.0)) & 0xFF;
    output[5] = int16_t(round(msg.heading * 100.0)) >> 8;

    // roll
    output[6] = int16_t(round(msg.roll * 100.0)) & 0xFF;
    output[7] = int16_t(round(msg.roll * 100.0)) >> 8;

    // pitch
    output[8] = int16_t(round(msg.pitch * 100.0)) & 0xFF;
    output[9] = int16_t(round(msg.pitch * 100.0)) >> 8;

    // checksum
    calc_checksum(output, ORIENTATION_MSG_LEN + 4);

    Serial2.write(output, ORIENTATION_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedOrientationMsg_t &msg)
{
    uint8_t output[STAMPED_ORIENTATION_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_ORIENTATION_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_ORIENTATION_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // heading
    output[8] = int16_t(round(msg.heading * 100.0)) & 0xFF;
    output[9] = int16_t(round(msg.heading * 100.0)) >> 8;

    // roll
    output[10] = int16_t(round(msg.roll * 100.0)) & 0xFF;
    output[11] = int16_t(round(msg.roll * 100.0)) >> 8;

    // pitch
    output[12] = int16_t(round(msg.pitch * 100.0)) & 0xFF;
    output[13] = int16_t(round(msg.pitch * 100.0)) >> 8;

    // checksum
    calc_checksum(output, STAMPED_ORIENTATION_MSG_LEN + 4);

    Serial2.write(output, STAMPED_ORIENTATION_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(RadioMsg_t &msg)
{
    uint8_t output[RADIO_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = RADIO_MSG_LEN + 3;

    // msg id
    output[3] = RADIO_MSG_ID;

    // speed
    output[4] = int16_t(round(msg.speed * 100.0)) & 0xFF;
    output[5] = int16_t(round(msg.speed * 100.0)) >> 8;

    // steering
    output[6] = msg.steering & 0xFF;

    // checksum
    calc_checksum(output, RADIO_MSG_LEN + 4);

    Serial2.write(output, RADIO_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedRadioMsg_t &msg)
{
    uint8_t output[STAMPED_RADIO_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_RADIO_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_RADIO_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // speed
    output[8] = int16_t(round(msg.speed * 100.0)) & 0xFF;
    output[9] = int16_t(round(msg.speed * 100.0)) >> 8;

    // steering
    output[10] = msg.steering & 0xFF;

    // checksum
    calc_checksum(output, STAMPED_RADIO_MSG_LEN + 4);

    Serial2.write(output, STAMPED_RADIO_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(ImuMsg_t &msg)
{
    uint8_t output[IMU_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = IMU_MSG_LEN + 3;

    // msg id
    output[3] = IMU_MSG_ID;

    // eulerX
    output[4] = int16_t(round(msg.eulerX * 10430.0)) & 0xFF;
    output[5] = int16_t(round(msg.eulerX * 10430.0)) >> 8;

    // eulerY
    output[6] = int16_t(round(msg.eulerY * 10430.0)) & 0xFF;
    output[7] = int16_t(round(msg.eulerY * 10430.0)) >> 8;

    // eulerZ
    output[8] = int16_t(round(msg.eulerZ * 10430.0)) & 0xFF;
    output[9] = int16_t(round(msg.eulerZ * 10430.0)) >> 8;

    // accX
    output[10] = int16_t(round(msg.accX * 8192.0)) & 0xFF;
    output[11] = int16_t(round(msg.accX * 8192.0)) >> 8;

    // accY
    output[12] = int16_t(round(msg.accY * 8192.0)) & 0xFF;
    output[13] = int16_t(round(msg.accY * 8192.0)) >> 8;

    // accZ
    output[14] = int16_t(round(msg.accZ * 8192.0)) & 0xFF;
    output[15] = int16_t(round(msg.accZ * 8192.0)) >> 8;

    // gyroX
    output[16] = int16_t(round(msg.gyroX * 16.4)) & 0xFF;
    output[17] = int16_t(round(msg.gyroX * 16.4)) >> 8;

    // gyroY
    output[18] = int16_t(round(msg.gyroY * 16.4)) & 0xFF;
    output[19] = int16_t(round(msg.gyroY * 16.4)) >> 8;

    // gyroZ
    output[20] = int16_t(round(msg.gyroZ * 16.4)) & 0xFF;
    output[21] = int16_t(round(msg.gyroZ * 16.4)) >> 8;

    // quaternionW
    output[22] = int16_t(round(msg.quaternionW * 16384.0)) & 0xFF;
    output[23] = int16_t(round(msg.quaternionW * 16384.0)) >> 8;

    // quaternionX
    output[24] = int16_t(round(msg.quaternionX * 16384.0)) & 0xFF;
    output[25] = int16_t(round(msg.quaternionX * 16384.0)) >> 8;

    // quaternionY
    output[26] = int16_t(round(msg.quaternionY * 16384.0)) & 0xFF;
    output[27] = int16_t(round(msg.quaternionY * 16384.0)) >> 8;

    // quaternionZ
    output[28] = int16_t(round(msg.quaternionZ * 16384.0)) & 0xFF;
    output[29] = int16_t(round(msg.quaternionZ * 16384.0)) >> 8;

    // checksum
    calc_checksum(output, IMU_MSG_LEN + 4);

    Serial2.write(output, IMU_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedImuMsg_t &msg)
{
    uint8_t output[STAMPED_IMU_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_IMU_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_IMU_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // eulerX
    output[8] = int16_t(round(msg.eulerX * 10430.0)) & 0xFF;
    output[9] = int16_t(round(msg.eulerX * 10430.0)) >> 8;

    // eulerY
    output[10] = int16_t(round(msg.eulerY * 10430.0)) & 0xFF;
    output[11] = int16_t(round(msg.eulerY * 10430.0)) >> 8;

    // eulerZ
    output[12] = int16_t(round(msg.eulerZ * 10430.0)) & 0xFF;
    output[13] = int16_t(round(msg.eulerZ * 10430.0)) >> 8;

    // accX
    output[14] = int16_t(round(msg.accX * 8192.0)) & 0xFF;
    output[15] = int16_t(round(msg.accX * 8192.0)) >> 8;

    // accY
    output[16] = int16_t(round(msg.accY * 8192.0)) & 0xFF;
    output[17] = int16_t(round(msg.accY * 8192.0)) >> 8;

    // accZ
    output[18] = int16_t(round(msg.accZ * 8192.0)) & 0xFF;
    output[19] = int16_t(round(msg.accZ * 8192.0)) >> 8;

    // gyroX
    output[20] = int16_t(round(msg.gyroX * 16.4)) & 0xFF;
    output[21] = int16_t(round(msg.gyroX * 16.4)) >> 8;

    // gyroY
    output[22] = int16_t(round(msg.gyroY * 16.4)) & 0xFF;
    output[23] = int16_t(round(msg.gyroY * 16.4)) >> 8;

    // gyroZ
    output[24] = int16_t(round(msg.gyroZ * 16.4)) & 0xFF;
    output[25] = int16_t(round(msg.gyroZ * 16.4)) >> 8;

    // quaternionW
    output[26] = int16_t(round(msg.quaternionW * 16384.0)) & 0xFF;
    output[27] = int16_t(round(msg.quaternionW * 16384.0)) >> 8;

    // quaternionX
    output[28] = int16_t(round(msg.quaternionX * 16384.0)) & 0xFF;
    output[29] = int16_t(round(msg.quaternionX * 16384.0)) >> 8;

    // quaternionY
    output[30] = int16_t(round(msg.quaternionY * 16384.0)) & 0xFF;
    output[31] = int16_t(round(msg.quaternionY * 16384.0)) >> 8;

    // quaternionZ
    output[32] = int16_t(round(msg.quaternionZ * 16384.0)) & 0xFF;
    output[33] = int16_t(round(msg.quaternionZ * 16384.0)) >> 8;

    // checksum
    calc_checksum(output, STAMPED_IMU_MSG_LEN + 4);

    Serial2.write(output, STAMPED_IMU_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(SonarMsg_t &msg)
{
    uint8_t output[SONAR_MSG_LEN + 3 + 3];

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

    // checksum
    calc_checksum(output, SONAR_MSG_LEN + 4);

    Serial2.write(output, SONAR_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedSonarMsg_t &msg)
{
    uint8_t output[STAMPED_SONAR_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_SONAR_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_SONAR_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // ping1
    output[8] = msg.ping1 & 0xFF;
    output[9] = msg.ping1 >> 8;

    // ping2
    output[10] = msg.ping2 & 0xFF;
    output[11] = msg.ping2 >> 8;

    // ping3
    output[12] = msg.ping3 & 0xFF;
    output[13] = msg.ping3 >> 8;

    // ping4
    output[14] = msg.ping4 & 0xFF;
    output[15] = msg.ping4 >> 8;

    // ping5
    output[16] = msg.ping5 & 0xFF;
    output[17] = msg.ping5 >> 8;

    // checksum
    calc_checksum(output, STAMPED_SONAR_MSG_LEN + 4);

    Serial2.write(output, STAMPED_SONAR_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(BumperMsg_t &msg)
{
    uint8_t output[BUMPER_MSG_LEN + 3 + 3];

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

    // checksum
    calc_checksum(output, BUMPER_MSG_LEN + 4);

    Serial2.write(output, BUMPER_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedBumperMsg_t &msg)
{
    uint8_t output[STAMPED_BUMPER_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_BUMPER_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_BUMPER_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // left
    output[8] = msg.left & 0xFF;

    // right
    output[9] = msg.right & 0xFF;

    // checksum
    calc_checksum(output, STAMPED_BUMPER_MSG_LEN + 4);

    Serial2.write(output, STAMPED_BUMPER_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StateMsg_t &msg)
{
    uint8_t output[STATE_MSG_LEN + 3 + 3];

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
    output[8] = uint8_t(round(msg.voltage * 10.0)) & 0xFF;

    // amperage
    output[9] = uint8_t(round(msg.amperage * 10.0)) & 0xFF;

    // groundSpeed
    output[10] = uint8_t(round(msg.groundSpeed * 10.0)) & 0xFF;

    // checksum
    calc_checksum(output, STATE_MSG_LEN + 4);

    Serial2.write(output, STATE_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedStateMsg_t &msg)
{
    uint8_t output[STAMPED_STATE_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_STATE_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_STATE_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // apmState
    output[8] = msg.apmState & 0xFF;

    // driveState
    output[9] = msg.driveState & 0xFF;

    // autoState
    output[10] = msg.autoState & 0xFF;

    // autoFlag
    output[11] = msg.autoFlag & 0xFF;

    // voltage
    output[12] = uint8_t(round(msg.voltage * 10.0)) & 0xFF;

    // amperage
    output[13] = uint8_t(round(msg.amperage * 10.0)) & 0xFF;

    // groundSpeed
    output[14] = uint8_t(round(msg.groundSpeed * 10.0)) & 0xFF;

    // checksum
    calc_checksum(output, STAMPED_STATE_MSG_LEN + 4);

    Serial2.write(output, STAMPED_STATE_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(ControlMsg_t &msg)
{
    uint8_t output[CONTROL_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = CONTROL_MSG_LEN + 3;

    // msg id
    output[3] = CONTROL_MSG_ID;

    // speed
    output[4] = int16_t(round(msg.speed * 100.0)) & 0xFF;
    output[5] = int16_t(round(msg.speed * 100.0)) >> 8;

    // steering
    output[6] = msg.steering & 0xFF;

    // checksum
    calc_checksum(output, CONTROL_MSG_LEN + 4);

    Serial2.write(output, CONTROL_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedControlMsg_t &msg)
{
    uint8_t output[STAMPED_CONTROL_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_CONTROL_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_CONTROL_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // speed
    output[8] = int16_t(round(msg.speed * 100.0)) & 0xFF;
    output[9] = int16_t(round(msg.speed * 100.0)) >> 8;

    // steering
    output[10] = msg.steering & 0xFF;

    // checksum
    calc_checksum(output, STAMPED_CONTROL_MSG_LEN + 4);

    Serial2.write(output, STAMPED_CONTROL_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(WaypointMsg_t &msg)
{
    uint8_t output[WAYPOINT_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = WAYPOINT_MSG_LEN + 3;

    // msg id
    output[3] = WAYPOINT_MSG_ID;

    // latStart
    output[4] = msg.latStart.minutes & 0xFF;
    output[5] = msg.latStart.minutes >> 8;
    output[6] = int32_t(round(msg.latStart.frac * 100000.0)) & 0xFF;
    output[7] = int32_t(round(msg.latStart.frac * 100000.0)) >> 8;
    output[8] = int32_t(round(msg.latStart.frac * 100000.0)) >> 16;
    output[9] = int32_t(round(msg.latStart.frac * 100000.0)) >> 24;

    // lonStart
    output[10] = msg.lonStart.minutes & 0xFF;
    output[11] = msg.lonStart.minutes >> 8;
    output[12] = int32_t(round(msg.lonStart.frac * 100000.0)) & 0xFF;
    output[13] = int32_t(round(msg.lonStart.frac * 100000.0)) >> 8;
    output[14] = int32_t(round(msg.lonStart.frac * 100000.0)) >> 16;
    output[15] = int32_t(round(msg.lonStart.frac * 100000.0)) >> 24;

    // latIntermediate
    output[16] = msg.latIntermediate.minutes & 0xFF;
    output[17] = msg.latIntermediate.minutes >> 8;
    output[18] = int32_t(round(msg.latIntermediate.frac * 100000.0)) & 0xFF;
    output[19] = int32_t(round(msg.latIntermediate.frac * 100000.0)) >> 8;
    output[20] = int32_t(round(msg.latIntermediate.frac * 100000.0)) >> 16;
    output[21] = int32_t(round(msg.latIntermediate.frac * 100000.0)) >> 24;

    // lonIntermediate
    output[22] = msg.lonIntermediate.minutes & 0xFF;
    output[23] = msg.lonIntermediate.minutes >> 8;
    output[24] = int32_t(round(msg.lonIntermediate.frac * 100000.0)) & 0xFF;
    output[25] = int32_t(round(msg.lonIntermediate.frac * 100000.0)) >> 8;
    output[26] = int32_t(round(msg.lonIntermediate.frac * 100000.0)) >> 16;
    output[27] = int32_t(round(msg.lonIntermediate.frac * 100000.0)) >> 24;

    // latTarget
    output[28] = msg.latTarget.minutes & 0xFF;
    output[29] = msg.latTarget.minutes >> 8;
    output[30] = int32_t(round(msg.latTarget.frac * 100000.0)) & 0xFF;
    output[31] = int32_t(round(msg.latTarget.frac * 100000.0)) >> 8;
    output[32] = int32_t(round(msg.latTarget.frac * 100000.0)) >> 16;
    output[33] = int32_t(round(msg.latTarget.frac * 100000.0)) >> 24;

    // lonTarget
    output[34] = msg.lonTarget.minutes & 0xFF;
    output[35] = msg.lonTarget.minutes >> 8;
    output[36] = int32_t(round(msg.lonTarget.frac * 100000.0)) & 0xFF;
    output[37] = int32_t(round(msg.lonTarget.frac * 100000.0)) >> 8;
    output[38] = int32_t(round(msg.lonTarget.frac * 100000.0)) >> 16;
    output[39] = int32_t(round(msg.lonTarget.frac * 100000.0)) >> 24;

    // pathHeading
    output[40] = int16_t(round(msg.pathHeading * 100.0)) & 0xFF;
    output[41] = int16_t(round(msg.pathHeading * 100.0)) >> 8;

    // checksum
    calc_checksum(output, WAYPOINT_MSG_LEN + 4);

    Serial2.write(output, WAYPOINT_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedWaypointMsg_t &msg)
{
    uint8_t output[STAMPED_WAYPOINT_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_WAYPOINT_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_WAYPOINT_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // latStart
    output[8] = msg.latStart.minutes & 0xFF;
    output[9] = msg.latStart.minutes >> 8;
    output[10] = int32_t(round(msg.latStart.frac * 100000.0)) & 0xFF;
    output[11] = int32_t(round(msg.latStart.frac * 100000.0)) >> 8;
    output[12] = int32_t(round(msg.latStart.frac * 100000.0)) >> 16;
    output[13] = int32_t(round(msg.latStart.frac * 100000.0)) >> 24;

    // lonStart
    output[14] = msg.lonStart.minutes & 0xFF;
    output[15] = msg.lonStart.minutes >> 8;
    output[16] = int32_t(round(msg.lonStart.frac * 100000.0)) & 0xFF;
    output[17] = int32_t(round(msg.lonStart.frac * 100000.0)) >> 8;
    output[18] = int32_t(round(msg.lonStart.frac * 100000.0)) >> 16;
    output[19] = int32_t(round(msg.lonStart.frac * 100000.0)) >> 24;

    // latIntermediate
    output[20] = msg.latIntermediate.minutes & 0xFF;
    output[21] = msg.latIntermediate.minutes >> 8;
    output[22] = int32_t(round(msg.latIntermediate.frac * 100000.0)) & 0xFF;
    output[23] = int32_t(round(msg.latIntermediate.frac * 100000.0)) >> 8;
    output[24] = int32_t(round(msg.latIntermediate.frac * 100000.0)) >> 16;
    output[25] = int32_t(round(msg.latIntermediate.frac * 100000.0)) >> 24;

    // lonIntermediate
    output[26] = msg.lonIntermediate.minutes & 0xFF;
    output[27] = msg.lonIntermediate.minutes >> 8;
    output[28] = int32_t(round(msg.lonIntermediate.frac * 100000.0)) & 0xFF;
    output[29] = int32_t(round(msg.lonIntermediate.frac * 100000.0)) >> 8;
    output[30] = int32_t(round(msg.lonIntermediate.frac * 100000.0)) >> 16;
    output[31] = int32_t(round(msg.lonIntermediate.frac * 100000.0)) >> 24;

    // latTarget
    output[32] = msg.latTarget.minutes & 0xFF;
    output[33] = msg.latTarget.minutes >> 8;
    output[34] = int32_t(round(msg.latTarget.frac * 100000.0)) & 0xFF;
    output[35] = int32_t(round(msg.latTarget.frac * 100000.0)) >> 8;
    output[36] = int32_t(round(msg.latTarget.frac * 100000.0)) >> 16;
    output[37] = int32_t(round(msg.latTarget.frac * 100000.0)) >> 24;

    // lonTarget
    output[38] = msg.lonTarget.minutes & 0xFF;
    output[39] = msg.lonTarget.minutes >> 8;
    output[40] = int32_t(round(msg.lonTarget.frac * 100000.0)) & 0xFF;
    output[41] = int32_t(round(msg.lonTarget.frac * 100000.0)) >> 8;
    output[42] = int32_t(round(msg.lonTarget.frac * 100000.0)) >> 16;
    output[43] = int32_t(round(msg.lonTarget.frac * 100000.0)) >> 24;

    // pathHeading
    output[44] = int16_t(round(msg.pathHeading * 100.0)) & 0xFF;
    output[45] = int16_t(round(msg.pathHeading * 100.0)) >> 8;

    // checksum
    calc_checksum(output, STAMPED_WAYPOINT_MSG_LEN + 4);

    Serial2.write(output, STAMPED_WAYPOINT_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(SteeringControllerMsg_t &msg)
{
    uint8_t output[STEERING_CONTROLLER_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STEERING_CONTROLLER_MSG_LEN + 3;

    // msg id
    output[3] = STEERING_CONTROLLER_MSG_ID;

    // scSteering
    output[4] = int16_t(round(msg.scSteering * 100.0)) & 0xFF;
    output[5] = int16_t(round(msg.scSteering * 100.0)) >> 8;

    // trueSteering
    output[6] = int16_t(round(msg.trueSteering * 100.0)) & 0xFF;
    output[7] = int16_t(round(msg.trueSteering * 100.0)) >> 8;

    // kCrosstrack
    output[8] = int16_t(round(msg.kCrosstrack * 1000.0)) & 0xFF;
    output[9] = int16_t(round(msg.kCrosstrack * 1000.0)) >> 8;

    // kYaw
    output[10] = int16_t(round(msg.kYaw * 1000.0)) & 0xFF;
    output[11] = int16_t(round(msg.kYaw * 1000.0)) >> 8;

    // headingError
    output[12] = int16_t(round(msg.headingError * 100.0)) & 0xFF;
    output[13] = int16_t(round(msg.headingError * 100.0)) >> 8;

    // crosstrackError
    output[14] = int16_t(round(msg.crosstrackError * 100.0)) & 0xFF;
    output[15] = int16_t(round(msg.crosstrackError * 100.0)) >> 8;

    // checksum
    calc_checksum(output, STEERING_CONTROLLER_MSG_LEN + 4);

    Serial2.write(output, STEERING_CONTROLLER_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedSteeringControllerMsg_t &msg)
{
    uint8_t output[STAMPED_STEERING_CONTROLLER_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_STEERING_CONTROLLER_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_STEERING_CONTROLLER_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // scSteering
    output[8] = int16_t(round(msg.scSteering * 100.0)) & 0xFF;
    output[9] = int16_t(round(msg.scSteering * 100.0)) >> 8;

    // trueSteering
    output[10] = int16_t(round(msg.trueSteering * 100.0)) & 0xFF;
    output[11] = int16_t(round(msg.trueSteering * 100.0)) >> 8;

    // kCrosstrack
    output[12] = int16_t(round(msg.kCrosstrack * 1000.0)) & 0xFF;
    output[13] = int16_t(round(msg.kCrosstrack * 1000.0)) >> 8;

    // kYaw
    output[14] = int16_t(round(msg.kYaw * 1000.0)) & 0xFF;
    output[15] = int16_t(round(msg.kYaw * 1000.0)) >> 8;

    // headingError
    output[16] = int16_t(round(msg.headingError * 100.0)) & 0xFF;
    output[17] = int16_t(round(msg.headingError * 100.0)) >> 8;

    // crosstrackError
    output[18] = int16_t(round(msg.crosstrackError * 100.0)) & 0xFF;
    output[19] = int16_t(round(msg.crosstrackError * 100.0)) >> 8;

    // checksum
    calc_checksum(output, STAMPED_STEERING_CONTROLLER_MSG_LEN + 4);

    Serial2.write(output, STAMPED_STEERING_CONTROLLER_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(VersionMsg_t &msg)
{
    uint8_t output[VERSION_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = VERSION_MSG_LEN + 3;

    // msg id
    output[3] = VERSION_MSG_ID;

    // debugMajor
    output[4] = msg.debugMajor & 0xFF;

    // debugMinor
    output[5] = msg.debugMinor & 0xFF;

    // apmMajor
    output[6] = msg.apmMajor & 0xFF;

    // apmMinor
    output[7] = msg.apmMinor & 0xFF;

    // checksum
    calc_checksum(output, VERSION_MSG_LEN + 4);

    Serial2.write(output, VERSION_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(StampedVersionMsg_t &msg)
{
    uint8_t output[STAMPED_VERSION_MSG_LEN + 3 + 3];

    // header bytes
    output[0] = 0x51;
    output[1] = 0xAC;

    // length
    output[2] = STAMPED_VERSION_MSG_LEN + 3;

    // msg id
    output[3] = STAMPED_VERSION_MSG_ID;

    // timestamp
    output[4] = msg.timestamp & 0xFF;
    output[5] = msg.timestamp >> 8;
    output[6] = msg.timestamp >> 16;
    output[7] = msg.timestamp >> 24;

    // debugMajor
    output[8] = msg.debugMajor & 0xFF;

    // debugMinor
    output[9] = msg.debugMinor & 0xFF;

    // apmMajor
    output[10] = msg.apmMajor & 0xFF;

    // apmMinor
    output[11] = msg.apmMinor & 0xFF;

    // checksum
    calc_checksum(output, STAMPED_VERSION_MSG_LEN + 4);

    Serial2.write(output, STAMPED_VERSION_MSG_LEN + 3 + 3);

    return RETURN_CODE_OK;
}

uint8_t MINDSiDebugger::send(AsciiMsg_t &msg)
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
    output[3] = ASCII_MSG_ID;

    // data
    uint8_t index = 4;
    for (uint8_t i=0; i< msg.ascii.len; i++)
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