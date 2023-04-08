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

#ifndef Datatypes_h
#define Datatypes_h

#include "Arduino.h"
    
typedef struct {
    int16_t minutes;
    float frac;
} GpsAngle_t;

typedef struct {
    char data[256];
    uint8_t len;
} LenString_t;

#endif