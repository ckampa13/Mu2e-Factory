#include <PololuQik.h>
#include <SoftwareSerial.h>

//digital pins are connected from the arduino to the pololu
PololuQik2s9v1 qik(2, 3, 4); //(2-TX, 3-RX, 4-RESET)

//---speed control wheel/potentiometer-------//
float max_adc = 535.0; //check the serial monitor and note the adc value when the speed control wheel is pushed against the bolt stop: set max_adc to this value
int potpin = A0;       //attach the middle pin of the pot to the ADC input A0
//---reversing button------------------------//
int inPin = 9;        // the number of the input pin
int state = HIGH;     // the current state of the output pin
int reading;          // the current reading from the input pin
int previous = LOW;   // the previous reading from the input pin
// the follow variables are long's because the time, measured in miliseconds, will quickly become a bigger number than can be stored in an int.
long time = 0;        // the last time the output pin was toggled
long debounce = 200;  // the debounce time, increase if the output flickers

void setup()
{
  pinMode(inPin, INPUT); //for the reversing button
  Serial.begin(9600);
  Serial.println("qik 2s9v1 dual serial motor controller");
  qik.init(); //initialize pololu
}

void loop()
{
  //---motor speed control---   
  int adc = analogRead(potpin); //read the ADC input value (the pot adjusts this)
  float motorspeed = (adc)/max_adc*127; //set duty factor of the square wave. max_adc scales to get the top motor speed at the bolt stop
  if (motorspeed > 127.0) {
    motorspeed = 127.0;
  }
  //if motor turns on when the wheel is in the off postion, increase the value in the conditional
  if (motorspeed < 1.0) {
    motorspeed = 0.0;
  }
    
  //---reversal button---
  reading = digitalRead(inPin);
  // if the input just went from LOW and HIGH and we've waited long enough to ignore any noise on the circuit, toggle the output pin and remember the time
  if (reading == HIGH && previous == LOW && millis() - time > debounce) {
    if (state == HIGH)
      state = LOW;
    else
      state = HIGH;
    time = millis();    
  }
  //we arbitrarily select LOW for reverse and HIGH for forward. if low, multiply duty factor by -1 to reverse direction
  if (state == LOW) {
     motorspeed = -motorspeed;
  //the reversal button state measured in this loop becomes 'previous' for the next loop 
  previous = reading;
  }
  
  //send the motor speed to the pololu!
  qik.setM0Speed(motorspeed); 
   
  //now just print out some values to the serial moniter
  Serial.print("adc channel = " );
  Serial.print(adc);
  Serial.print("\t"); 
  Serial.print("motor speed = " );
  Serial.print(motorspeed);
  Serial.print("\n"); 

  delay(250);
}
