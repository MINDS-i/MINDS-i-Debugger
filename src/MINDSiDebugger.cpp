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

#include "Arduino.h"
#include "MINDSiDebugger.h"
#include "Util.h"

MINDSiDebugger::MINDSiDebugger()
{
    Serial2.begin(115200);
}

MINDSiDebugger::MINDSiDebugger(long baud)
{
    Serial2.begin(baud);
}

int32_t MINDSiDebugger::lat_float_to_int32(float lat)
{
  return (int32_t)(lat_conv_factor * lat);
}

int32_t MINDSiDebugger::lon_float_to_int32(float lon)
{
  return (int32_t)(lon_conv_factor * lon);
}

int32_t MINDSiDebugger::frac_float_to_int32(float frac)
{
  return (int32_t)(round(100000 * frac));
}

uint16_t MINDSiDebugger::alt_float_to_uint16(float alt)
{
  if (alt < -900)
    alt = -900;
  else if (alt > 19000)
    alt = 19000;

  return (uint16_t)(alt_conv_factor * (alt + 900));
}
