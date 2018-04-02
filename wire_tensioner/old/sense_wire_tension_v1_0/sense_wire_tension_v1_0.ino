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
//---buzzer---
#define buzzerPin 12

#define tension_good 80.0
#define tension_low 79.5
#define tension_high 80.5

//looping through spring and pulling only measures 1/2 the actual tension that the spring will give, so we set limits to half the actual values (40-70gf)
#define min_pull_tension 20.0
#define max_pull_tension 35.0
#define min_tension_start 35.0
#define max_tension_start 75.0

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
  pinMode(buzzerPin, OUTPUT);
 
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
    }
  }

  if (mode == "RESET") {
    tensioner_ready = return_actuator(tension_before);
    position_last = 45;
  }
  if (mode == "TENSION") {
    if (tensioner_ready == true) {
      position_last = actuator_adjust(position_last,tension_before);  
    }
    else {
      mode == "RESET";
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
  //delay(1000); //FOR TESTING ONLY
}

bool return_actuator(float current_tension) {
  bool tension_ready = false;
  //let user know when pull tension is in a good range
  if (current_tension > min_pull_tension && current_tension < max_pull_tension) {
    tone(buzzerPin,440);  
  }
  else {
    noTone(buzzerPin);
  }

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
    tension_ready = true; //this is really the only important line of this entire conditional...the rest is just lights. could simplify to a one line conditional.
  }

  actuator.write(45);
  //return tension_ready;
  delay(500); //increase this number to save processing power
  return tension_ready;
}

int actuator_adjust(int position_old, float tension){
  int position_new;
  float delta_position;
  float delta_tension;
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
  delta_tension = abs(tension_good - tension);
  if (delta_tension > 10.0) {
    delta_position = 1.5*delta_tension; //positive if we need to increase tension (retract arm), negative to decrease
  }
  else {
    delta_position = 1;
  }
  delta_position = floor(delta_position);
  //position_new = position_old + delta_position;
  if(tension < tension_low) {
    position_new = position_old + delta_position;
    digitalWrite(lowLED, HIGH);
    digitalWrite(goodLED, LOW);
    digitalWrite(highLED, LOW);
    //delay(50*abs(delta_position));
  }
  else if (tension > tension_high) {
    position_new = position_old - delta_position;
    digitalWrite(lowLED, LOW);
    digitalWrite(goodLED, LOW);
    digitalWrite(highLED, HIGH);
    //delay(50*abs(delta_position));
  }
  else {
    position_new = position_old;
    //delta_position = 10; //for the delay
    digitalWrite(lowLED, LOW);
    digitalWrite(goodLED, HIGH);
    digitalWrite(highLED, LOW);
    delay(50); // change to change how often we see the tension...low number will help us see initial fluctuations in tension once desired tension range is met
    //ADD BUZZER?
  }
  if(position_new < 45) {
    position_new = 45;
  }
  else if (position_new > 140) {
    position_new = 140;
  }
  actuator.write(position_new);
  //delay(50*abs(delta_position));
  if (delta_position == 1) {
    delay(750);
  }
  else {
    delay(2000);
  }
  return position_new; //position_new becomes postion_last
}

//--CALIBRATION FUNCTION HERE---
//bool calibrate () {
//}
