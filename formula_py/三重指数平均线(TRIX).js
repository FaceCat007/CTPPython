CONST N=12;CONST M=9;

MTR:=EMA(EMA(EMA(CLOSE,N),N),N); 
TRIX:(MTR-REF(MTR,1))/REF(MTR,1)*100; 
MATRIX:MA(TRIX,M);