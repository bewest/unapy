#include <SoftwareSerial.h>
//Relays RS232 from USB to software serial ports on arduino
//rx on pin 2, tx on pin 3
//
//Initialization Commands: 
//":#;0x0D" - Reset Arduino
//":<RATE>;0x0D" - Set software serial with baudrate: <RATE> 0 = 1200, 1=2400, 2=4800 ... 6=38400, 7=57600, 8=115200
//":?;0x0D" - Request baudrate response from Arduino
//":!;0x0D" - Confirm intention

SoftwareSerial mySerial(2,3);

byte buffer[4]; //current command buffer
unsigned short int buffer_position; //current state of buffer position
byte pending_command; //interpreted and executed on confirmCommand()
byte request_confirmation_sent; //did the arduino request confirmation of a pending command?

void setup()
{
  //Initialize variables
  
  byte buffer[4] = {0x00, 0x00, 0x00, 0x00}; //current command buffer
  unsigned short int buffer_position = 0; //current state of buffer position
  byte pending_command = 0x00; //interpreted and executed on confirmCommand()
  byte request_confirmation_sent = 0; //did the arduino request confirmation of a pending command?

  //Init arduino built-in serial
    Serial.begin(9600);
    pinMode(0,INPUT);
    pinMode(1,OUTPUT);
    
    //Init software serial - actually, only do this when told the bitrate by the incoming port
    //setSoftwareSerialBaudrate(38400);
  
    //Debug LED
    const int ledPin = 13;
    pinMode(ledPin,OUTPUT);
    digitalWrite(ledPin, HIGH);  
}

void setSoftwareSerialBaudrate(unsigned int baudrate)
{
    mySerial.begin(baudrate); 
}

void loop()
{
  if(mySerial.available())
  { 
    Serial.write(mySerial.read()); 
  }
  
  if(Serial.available())
  {
    byte read_byte = Serial.read();
    
    //if ':' then read_colon_into_buffer()
    //if buffer_position != 0 then read_noncolon_into_buffer
    //else (b/c bp = 0 and not a colon) just echo the read_byte out to myserial
    
    if (read_byte == ':') read_colon_into_buffer();
    else if (buffer_position != 0) read_non_colon_into_buffer(read_byte);
    else {
      mySerial.write(read_byte);
    }
  }
}

void read_colon_into_buffer()
{
  if (buffer_position != 0) flush_buffer();

  // Note: buffer_postion = 0 b/c set by flush_buffer if not 0
  
  buffer[0] = ':';
  
  buffer_position = 1;
}

void read_non_colon_into_buffer(byte read_byte)
{
  buffer[buffer_position] = read_byte;
  buffer_position++;
  if (buffer_position == 5) interpret_buffered_command();
  
  
}

void interpret_buffered_command()
{
  if(buffer[0]==':' && buffer[2]==';' && buffer[3]==0x0D)
  {
    if(pending_command != 0x00 && buffer[1] != '!')
    {
     //What happens if two commands get sent without a confirmation in between? Assume pending command was meant for myserial and write it out.
     mySerial.write(':');
     mySerial.write(pending_command);
     mySerial.write(';');
     mySerial.write(0x0D);
     pending_command = 0x00;
    }
    
    switch(buffer[1]){
     case '0': //0-8 set common baudrates
     case '1':
     case '2':
     case '3':
     case '4':
     case '5':
     case '6':
     case '7':     
     case '8':
     case '#': //reset arduino
     case '?': //request current baudrate
       //valid command entered, so set pending_command and ask for confirmation
       pending_command = buffer[1];
       buffer_position = 0; //do not flush_buffer(), as this will result in echoing command to myserial! set position to 0 instead.
       send_confirm_command_request();
       break;
     case '!':
        //only execute command if confirmed in response to request, otherwise assume confirmation command is meant for myserial
       if (request_confirmation_sent == 1) {
         confirm_command();
         request_confirmation_sent = 0;
       }
       else {
        flush_buffer(); 
       }
       break;
     default:
       //invalid command entered, so flush buffer and carry on
       flush_buffer(); //send invalid command to serial port
    } 
  }
  else {
   //What happens if buffer is not even in the right syntax?
   //flush it! 
   flush_buffer();
  }
}

void send_confirm_command_request()
{
   Serial.print(":???;\r");
   request_confirmation_sent = 1;
}

void confirm_command()
{
     switch(pending_command){
     case '0':
       setSoftwareSerialBaudrate(1200);
       break;
     case '1':
       setSoftwareSerialBaudrate(2400);
       break;
     case '2':
       setSoftwareSerialBaudrate(4800);
       break;
     case '3':
       setSoftwareSerialBaudrate(9600);
       break;
     case '4':
       setSoftwareSerialBaudrate(14400);
       break;
     case '5':
       setSoftwareSerialBaudrate(19200);   
       break;
     case '6':
       setSoftwareSerialBaudrate(38400);
       break;
     case '7':
       setSoftwareSerialBaudrate(57600);
       break;
     case '8':
       setSoftwareSerialBaudrate(115200);
       break;
     case '#':
       reset_arduino();
       break;
     }
     
     pending_command = 0x00;
}

void reset_arduino()
{
  //in principle, this should just call setup() then continue loop()
  setup();
}

//If buffer contains no valid commands, or is reset, send contents up to buffer_position to software serial 
void flush_buffer()
{
  //Write out everything in the buffer to mySerial
  for(int i = 0; i < buffer_position; i++){
    mySerial.write(buffer[i]);
  }
  
  //Set the buffer position back to 0
  buffer_position = 0;
}
