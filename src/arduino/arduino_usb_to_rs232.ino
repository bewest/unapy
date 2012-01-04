//Relays RS232 from USB serial to software serial ports on arduino
//RX on pin 2, TX on pin 3

#include <SoftwareSerial.h>

SoftwareSerial mySerial(2,3);

void setup()
{
    //Init arduino built-in serial at 9600bps
    Serial.begin(9600);
    pinMode(0,INPUT);
    pinMode(1,OUTPUT);
  //  Serial.println("Serial Init");
  
    //Init software serial at 9600bps
    mySerial.begin(9600);
    //Serial.println("SoftSerial Init");
  
    //Debug LED
    const int ledPin = 13;
    pinMode(ledPin,OUTPUT);
    digitalWrite(ledPin, HIGH);  
}

void loop()
{
  if(mySerial.available())
  {
    Serial.write(mySerial.read()); 
  }
  
  if(Serial.available())
  {
    mySerial.write(Serial.read());
  }
}
