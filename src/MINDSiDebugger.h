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

#ifndef MINDSiDebugger_h
#define MINDSiDebugger_h

#define RETURN_CODE_OK 1
#define RETURN_CODE_ERR_ALLOC 2

#include "Arduino.h"
#include "Util.h"
#include "DebugMsgs.h"

class MINDSiDebugger {
  public:
    MINDSiDebugger();
    MINDSiDebugger(long buad);
    uint8_t send(RawPositionMsg_t &msg);
    uint8_t send(StampedRawPositionMsg_t &msg);
    uint8_t send(ExtrapolatedPositionMsg_t &msg);
    uint8_t send(StampedExtrapolatedPositionMsg_t &msg);
    uint8_t send(OrientationMsg_t &msg);
    uint8_t send(StampedOrientationMsg_t &msg);
    uint8_t send(RadioMsg_t &msg);
    uint8_t send(StampedRadioMsg_t &msg);
    uint8_t send(ImuMsg_t &msg);
    uint8_t send(StampedImuMsg_t &msg);
    uint8_t send(SonarMsg_t &msg);
    uint8_t send(StampedSonarMsg_t &msg);
    uint8_t send(BumperMsg_t &msg);
    uint8_t send(StampedBumperMsg_t &msg);
    uint8_t send(StateMsg_t &msg);
    uint8_t send(StampedStateMsg_t &msg);
    uint8_t send(ControlMsg_t &msg);
    uint8_t send(StampedControlMsg_t &msg);
    uint8_t send(WaypointMsg_t &msg);
    uint8_t send(StampedWaypointMsg_t &msg);
    uint8_t send(ControlMsg_t &msg);
    uint8_t send(StampedControlMsg_t &msg);
    uint8_t send(VersionMsg_t &msg);
    uint8_t send(StampedVersionMsg_t &msg);
    uint8_t send(AsciiMsg_t &msg);
  
  private:
};

#endif