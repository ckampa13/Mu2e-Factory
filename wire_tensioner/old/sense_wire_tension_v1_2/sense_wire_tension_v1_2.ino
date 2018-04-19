// sense wire tension v2.0
// cole kampa -- kampa041@umn.edu
// arduino micro

#include <Servo.h>
#include "HX711.h"

//---actuator data--- (send a pulse of certain width to send actuator to a given position (in degrees, using Servo library)
#define actuatorPin 9
//---load cell--- (this is to the load cell amplifier, match load cell colored wires to color labeled pins on load cell amp)
#define loadDAT 3
#define loadCLK 2
//---LEDs--- (replace resistors or get different LEDs to make them brighter)
#define lowLED 5
#define goodLED 6
#define highLED 7
//---buzzer---
#define buzzerPin 12
#define buzz_delay 200  //defines period of buzzer
#define freq 220        //sets tone of the buzzer when a measurement is bad

//---tension definitions---
#define tension_good 80.0
#define tension_low 79.5
#define tension_high 80.5

//---linear equation definitions--- following y = m*x + b
//****tension_plot.pdf****
//two solutions for the low tension linear regime and high tension linear regime (cut at 31.0 gf)
#define low_tension_m -0.2214
#define low_tension_b 129.36
#define high_tension_threshold 31.0 //specified minimum force by spring manufacturer, verified by consistency tests
#define high_tension_m -1.5997
#define high_tension_b 172.83

//---reversing button------------------------//
int startButton = 8;        // the number of the input pin
int state = HIGH;     // the current state of the output pin
int reading;          // the current reading from the input pin
int previous = LOW;   // the previous reading from the input pin
// the follow variables are long's because the time, measured in miliseconds, will quickly become a bigger number than can be stored in an int.
long time = 0;        // the last time the output pin was toggled
long debounce = 200;  // the debounce time, increase if the output flickers

//---initialize objects for actuator and load cell
Servo actuator;
HX711 load_cell;

//---other variable definitions
float tension_before = 0.0;
float tension_after = 0.0;
int position_last = 45;
char inByte;
String mode = "RESET";
//--------------------------------------//
void setup() {
  Serial.begin(9600);
  Serial.println("wire tensioner v1.0:");

  load_cell.begin(loadDAT, loadCLK);
  load_cell.set_scale(-11690.f);
  load_cell.tare();
  
  pinMode(lowLED, OUTPUT);
  pinMode(goodLED, OUTPUT);
  pinMode(highLED, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(startButton, INPUT);
 
  actuator.attach(actuatorPin);
  actuator.write(position_last);

  digitalWrite(lowLED, HIGH);
  digitalWrite(goodLED, HIGH);
  digitalWrite(highLED, HIGH);
  delay(2000);
  digitalWrite(lowLED, LOW);
  digitalWrite(goodLED, LOW);
  digitalWrite(highLED, LOW);
}
//--------------------------------------//
void loop() {
  tension_before = load_cell.get_units(); //could add some number between get_units(##) to take an average of ## measurements 
  //allow serial input for debugging
  if (Serial.available()) {
    inByte = Serial.read();
    if (inByte == '0') {
      mode = "RESET";
    }
    if (inByte == '1') {
      mode = "TENSION";
    }
  }
  //---mode change button---
  reading = digitalRead(startButton);
  // if the input just went from LOW and HIGH and we've waited long enough to ignore any noise on the circuit, toggle the output pin and remember the time
  if (reading == HIGH && previous == LOW && millis() - time > debounce) {
    if (mode == "RESET")
      mode = "TENSION";
    else
      mode = "RESET";
    time = millis();    
  }
  //the state measured in this loop becomes 'previous' for the next loop 
  previous = reading;
  
  if (mode == "RESET") {
    if (position_last != 45) {
      actuator.write(45);
      digitalWrite(lowLED, LOW);
      digitalWrite(goodLED, LOW);
      digitalWrite(highLED, LOW);
    }
    position_last = 45;
    delay(500); //can increase delay to save processing
  }
  if (mode == "TENSION") {
    position_last = actuator_adjust(position_last,tension_before);
    if (position_last >= 140) {
      mode = "RESET";
      //buzz 3 times based on frequency and duration defined above
      tone(buzzerPin,freq);
      delay(buzz_delay);
      noTone(buzzerPin);
      delay(buzz_delay);
      tone(buzzerPin,freq);
      delay(buzz_delay);
      noTone(buzzerPin);
      delay(buzz_delay);
      tone(buzzerPin,freq);
      delay(buzz_delay);
      noTone(buzzerPin);
    }
  }

  tension_after = load_cell.get_units();
  
  Serial.print("Tension: 1) ");
  Serial.print(tension_before);
  Serial.print("g, 2) ");
  Serial.print(tension_after);
  Serial.print("g; Mode: ");
  Serial.print(mode);
  Serial.print("; Position: ");
  Serial.println(position_last);

  delay(250);
}

//--------------------------------------//

int actuator_adjust(int position_old, float tension){
  int position_new;
  int delay_time = 800; //default delay for incrementing by 1
  float delta_tension;
  
  //new method for first time through based on linear equation definitions
  if (position_old == 45) {
    if (tension < high_tension_threshold) {
      position_new = floor(low_tension_m * tension + low_tension_b);
    }
    else {
      position_new = floor(high_tension_m * tension + high_tension_b);
    }
    delay_time = 4000; //5 s delay to start, adjust as necessary
  }
  //all other times, only increment +-1 and measure the tension again
  else {
    if(tension < tension_low) {
      position_new = position_old + 1;
      digitalWrite(lowLED, HIGH);
      digitalWrite(goodLED, LOW);
      digitalWrite(highLED, LOW);
    }
    else if (tension > tension_high) {
      position_new = position_old - 1;
      digitalWrite(lowLED, LOW);
      digitalWrite(goodLED, LOW);
      digitalWrite(highLED, HIGH);
    }
    else {
      position_new = position_old;
      digitalWrite(lowLED, LOW);
      digitalWrite(goodLED, HIGH);
      digitalWrite(highLED, LOW);
      delay_time = 50;
    }  
  }
  //adjust position if the motor trys to overrun the bounds (45 is full retraction, 140 is full extension)
  if(position_new < 45) {
    position_new = 45;
  }
  else if (position_new > 140) {
    position_new = 140;
  }
  actuator.write(position_new);
  delay(delay_time);
  return position_new; //position_new becomes postion_last
}
