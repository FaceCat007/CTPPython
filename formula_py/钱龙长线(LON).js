﻿LC := REF(CLOSE,1);
VID := SUM(VOL,2)/(((HHV(HIGH,2)-LLV(LOW,2)))*100);
RC := (CLOSE-LC)*VID;
LONG := SUM(RC,0);
DIFF := SMA(LONG,10,1);
DEA := SMA(LONG,20,1);
LON : DIFF-DEA;
LONMA : MA(LON,10);
LONT : LON, COLORSTICK;