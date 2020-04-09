#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>
int trans = 3;

//Servo ESC;


RF24 radio(7, 8); // CE, CSN
//const uint64_t addresses[2] = {0x0, 0x1};
void setup() {

//ESC.attach(3,1000,2000);
  
  //pinMode(trans, OUTPUT);
  
  radio.begin();
  radio.setChannel(45);
  radio.setAutoAck(false);
  radio.openWritingPipe(0xF0F0F0F0AA); // 00002
  //radio.openReadingPipe(1, addresses[0]); // 00001

  radio.setPALevel(RF24_PA_MAX);
  Serial.begin(9600);
  
}
int intArr = 0;
void loop() {
  
  
 radio.stopListening();
  
 // while (Serial.available()) {
    Serial.println(intArr);
    
    radio.write(&intArr, sizeof(intArr));
    if (intArr > 100) {
      intArr = 0;
    }
    else {
      intArr++;
    }
  delay (50);
}
