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

#ifndef MINDSiDebugger_h
#define MINDSiDebugger_h

#define ASCII_ID 0x90

#define RETURN_CODE_OK 1
#define RETURN_CODE_ERR_ALLOC 2

#include "Arduino.h"
#include "Util.h"
#include "AsciiMsgs.h"
#include "PositionMsgs.h"
#include "OrientationMsgs.h"
#include "NavigationMsgs.h"
#include "SensorMsgs.h"
#include "StateMsgs.h"
#include "RadioMsgs.h"
#include "VersionMsgs.h"

class MINDSiDebugger {
  public:
    MINDSiDebugger();
    MINDSiDebugger(long buad);
    uint8_t send(AsciiMsg_t msg);
    uint8_t send(RawPositionMsg_t msg);
    uint8_t send(ExtrapolatedPositionMsg_t msg);
    uint8_t send(OrientationMsg_t msg);
    uint8_t send(ControlMsg_t msg);
    uint8_t send(WaypointMsg_t msg);
    uint8_t send(ImuMsg_t msg);
    uint8_t send(SonarMsg_t msg);
    uint8_t send(BumperMsg_t msg);
    uint8_t send(StateMsg_t msg);
    uint8_t send(RadioMsg_t msg);
    uint8_t send(VersionMsg_t msg);
    int32_t lat_float_to_int32(float lat);
    int32_t lon_float_to_int32(float lon);
    uint16_t alt_float_to_uint16(float alt);
    int32_t frac_float_to_int32(float frac);

  private:
};

#endif
