/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 70; // variable to store the servo position
//float pos = 140.0;
int full_ext = 40;
int full_ret = 140;
char inByte;

void setup() {
  Serial.begin(9600);
  Serial.println("Ready!");
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
if (Serial.available() > 0) { // we only want the code to do stuff when we send it an instruction character via serial (USB)
    inByte = Serial.read();  
    if(inByte == '0') {
      pos -= 1;
      //pos -= 0.5;
    }
    if(inByte == '1') {
      pos += 1;
      //pos += 0.5;
    }
    Serial.println(pos);
    myservo.write(pos);
}
//myservo.write(pos);
delay(100);
}
/*
}
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    Serial.println(pos);
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(100);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    Serial.println(pos);
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(100);                       // waits 15ms for the servo to reach the position
  }
}
*/
