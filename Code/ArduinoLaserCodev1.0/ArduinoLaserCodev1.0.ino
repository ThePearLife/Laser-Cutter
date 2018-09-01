//ArduinoLaserCodev1.0
//Code to control laser cutter using Arduino
//Anant Kanungo
//08/23/2018


int datapin = 2; 
int clockpin = 3;
int latchpin = 4;
byte data = 0;

void setup() {
  pinMode(datapin, OUTPUT);
  pinMode(clockpin, OUTPUT);  
  pinMode(latchpin, OUTPUT);
}

void loop() {
  int i;
  for(i=0;i<1000;i++){
    
    shiftWrite(0, HIGH);
    shiftWrite(4, HIGH);
    shiftWrite(2, LOW);
    shiftWrite(5, LOW);
    delay(20);
    shiftWrite(1, HIGH);
    shiftWrite(6, HIGH);
    shiftWrite(0, LOW);
    shiftWrite(4, LOW);
    delay(20);
    shiftWrite(3, HIGH);
    shiftWrite(7, HIGH);
    shiftWrite(1, LOW);
    shiftWrite(6, LOW);
    delay(20);
    shiftWrite(2, HIGH);
    shiftWrite(5, HIGH);
    shiftWrite(3, LOW);
    shiftWrite(7, LOW);
    delay(2 l0);
    
  }

}

void shiftWrite(int desiredPin, boolean desiredState)
{
  bitWrite(data,desiredPin,desiredState);
  shiftOut(datapin, clockpin, MSBFIRST, data);
  digitalWrite(latchpin, HIGH);
  digitalWrite(latchpin, LOW);
}
