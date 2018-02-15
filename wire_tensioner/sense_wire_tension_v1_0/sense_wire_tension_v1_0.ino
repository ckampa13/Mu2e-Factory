// sense wire tension v1.0
// cole kampa -- kampa041@umn.edu
// arduino micro 

#include <Servo.h>
#include "HX711.h"

//---buttons---
//#define buttonOffPin 0
//#define buttonOnPin 1
//---actuator---
#define actuatorPin 9
//---load cell---
#define loadDAT 3
#define loadCLK 2
//---LEDs---
#define lowLED 5
#define goodLED 6
#define highLED 7

#define tension_good 80.0
#define tension_low 79.5
#define tension_high 81.5

#define min_tension_start 40.0
#define max_tension_start 65.0

//#define small_change 5.0 //number of grams before changing to fine tuning

//---initialize objects
Servo actuator;
HX711 load_cell;

//float calibration_factor = -11690.0; //determined using calibration arduino script

float tension_before = 0.0;
float tension_after = 0.0;

//float tension_good = 80.0;
//float tension_low = 70.0;
//float tension_high = 90.0;
// float tension_over = 90 //add functionality to overtension and relax

int position_last = 45;
//int position_hold;

char inByte;
String mode = "RESET";

bool tensioner_ready = false;


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
 
  actuator.attach(actuatorPin);
  actuator.write(position_last);

  //load_cell.set_scale();
  //load_cell.tare();
  
  //Serial.begin(9600);
  //Serial.println("wire tensioner v1.0:");

  digitalWrite(lowLED, HIGH);
  digitalWrite(goodLED, HIGH);
  digitalWrite(highLED, HIGH);
  delay(2000);
  digitalWrite(lowLED, LOW);
  digitalWrite(goodLED, LOW);
  digitalWrite(highLED, LOW);
}

void loop() {
 
  tension_before = load_cell.get_units(); //could add some number between get_units(##) to take an average of ## measurements 
  
  if (Serial.available()) {
    inByte = Serial.read();
    if (inByte == '0') {
      mode = "RESET";
    }
    if (inByte == '1') {
      mode = "TENSION";
      tensioner_ready = check_ready();
    }
  }

  if (mode == "RESET") {
    tensioner_ready = return_actuator(tension_before);
    position_last = 45;
  }
  if (mode == "TENSION") {
    if (tensioner_ready) {
      position_last = actuator_adjust(position_last,tension_before);  
    }
    else {
      tensioner_ready = check_ready();
    }
    //position_hold = actuator_adjust(position_last,tension_before);
    //position_last = position_hold;
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

  //****maybe move this delay into the loops for more control***
  delay(300);
}

bool check_ready() {
  if (current_tension < min_tension_start) {
    
  }
}

bool return_actuator(float current_tension) {
  bool tension_ready = false;
  if (current_tension < min_tension_start) {
    digitalWrite(lowLED, HIGH);
    digitalWrite(goodLED, LOW);
    digitalWrite(highLED, LOW);  
  }
  else if (current_tension > max_tension_start) {
    digitalWrite(lowLED, LOW);
    digitalWrite(goodLED, LOW);
    digitalWrite(highLED, HIGH);
  }
  else {
    digitalWrite(lowLED, LOW);
    digitalWrite(goodLED, HIGH);
    digitalWrite(highLED, LOW);
    tension_ready = true;
  }
  
  actuator.write(45);

  //return tension_ready;
  return false;
}

int actuator_adjust(int position_old, float tension){
  int position_new;
  //---check whether to extend or retract actuator based on tension
  /*
  if(tension < tension_good) {
    position_new = position_old + 1;
  }
  else if(tension > tension_good) {
    position_new = position_last - 1;
  }
  if(position_new < 45) {
    position_new = 45;
  }
  else if (position_new > 140) {
    position_new = 140;
  }
  //--set actuator to new position
  actuator.write(position_new);
  */
  //turn on proper LED
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
    //ADD BUZZER?
  }
  actuator.write(position_new);
  return position_new; //position_new becomes postion_last
}

