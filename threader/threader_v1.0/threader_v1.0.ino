#include <PololuQik.h>

//updates by cole kampa <kampa041@umn.edu>

//jason bono
//version 2 adds a button reversing the motor

/*
Required connections between Arduino and qik 2s9v1:

      Arduino   qik 2s9v1
-------------------------
           5V - VCC
          GND - GND
Digital Pin 2 - TX
Digital Pin 3 - RX
Digital Pin 4 - RESET
*/

#include <SoftwareSerial.h>
#include <PololuQik.h>

PololuQik2s9v1 qik(2, 3, 4);

int potpin = A0; //attach the middle pin of the pot to the ADC input A0

//---added for the on/off switch----------
int onPin = 10;         // the number of the input pin for the motor on button

//---added for the reversing switch----------
int revPin = 9;         // the number of the input pin for reversing button
int rev_state = HIGH;      // the current state of the output pin
int rev_reading;           // the current reading from the input pin
int rev_previous = LOW;    // the previous reading from the input pin

// the follow variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long time = 0;         // the last time the output pin was toggled
long debounce = 200;   // the debounce time, increase if the output flickers
//---------------------------------------

void setup()
{
    // initialize digital pin 13 as an output.
  //pinMode(13, OUTPUT); //output to the pololu
  pinMode(revPin, INPUT); //for the reversing button
  pinMode(onPin, INPUT); //for the motor on button
  
  //Serial.begin(115200);
  Serial.println("qik 2s9v1 dual serial motor controller");
  
  qik.init();
  
  Serial.print("Firmware version: ");
  //Serial.write(qik.getFirmwareVersion());
  Serial.println();
}

void loop()
{
//  digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(200);              // wait for a second
//  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
//  delay(200);   

  
  
  int adc = analogRead(potpin); //read the ADC input value (the pot adjusts this)
  //float motorspeed = ((1023 - adc)/1023.0)*127; //set duty factor of the square wave between 0 and 100
  float motorspeed = (adc / 1023.0) * 100
  
  
    
  //===========================added for the putton
  rev_reading = digitalRead(revPin);
    // if the input just went from LOW and HIGH and we've waited long enough
  // to ignore any noise on the circuit, toggle the output pin and remember
  // the time
  if (rev_reading == HIGH && rev_previous == LOW && millis() - time > debounce) {
    if (rev_state == HIGH)
      rev_state = LOW;
    else
      rev_state = HIGH;

    time = millis();    
  }

  //digitalWrite(outPin, state);
  //if (rev_state == HIGH) {
//
//}
  if (rev_state == LOW) {
     motorspeed = -motorspeed;
}
  


  rev_previous = rev_reading;
  //-------------------------------------------------

  
  
  if(digitalRead(onPin) == HIGH){
    qik.setM0Speed(motorspeed);
}
  else:
    qik.setM0Speed(0.0);
}
   
  //now just print out some values to the serial moniter
  Serial.print("adc channel = " );
  Serial.print(adc);
  Serial.print("\t"); 
  Serial.print("motor speed = " );
  Serial.print(motorspeed);
  Serial.print("\n"); 
 
 
 
 
 //qik.setM1Speed(127);  
 /*
  for (int i = 0; i <= 127; i++)
  {
    qik.setM0Speed(i);
    delay(5);
  }

  for (int i = 127; i >= -127; i--)
  {
    qik.setM0Speed(i);
    delay(5);
  }

  for (int i = -127; i <= 0; i++)
  {
    qik.setM0Speed(i);
    delay(5);
  }

  for (int i = 0; i <= 127; i++)
  {
    qik.setM1Speed(i);
    delay(5);
  }

  for (int i = 127; i >= -127; i--)
  {
    qik.setM1Speed(i);
    delay(5);
  }

  for (int i = -127; i <= 0; i++)
  {
    qik.setM1Speed(i);
    delay(5);
  }
  
  */
  
}
