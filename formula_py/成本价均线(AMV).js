CONST M1=5;CONST M2=13;CONST M3=34;CONST M4=60;

AMOV:=VOL*(OPEN+CLOSE)/2;
AMV1:SUM(AMOV,M1)/SUM(VOL,M1); 
AMV2:SUM(AMOV,M2)/SUM(VOL,M2); 
AMV3:SUM(AMOV,M3)/SUM(VOL,M3);
AMV4:SUM(AMOV,M4)/SUM(VOL,M4);