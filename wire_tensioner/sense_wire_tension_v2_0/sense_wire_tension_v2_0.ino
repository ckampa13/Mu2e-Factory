#include "HX711.h"

//Declare pin functions on Arduino Micro
//--stepper motor--
#define stp 12
#define dir 9
#define MS1 8
#define MS2 11
#define EN  10

#define reset_steps 2500
#define reset_time 20000 //ms

//--load cell--
#define loadDAT 7
#define loadCLK 6

//--extras--
#define buzzerPin 13
//#define button 5
#define LED 4
#define mode_switch 3
#define button 2

//MAYBE GET RID OF THESE?
#define largest_step 100
#define large_step 50
#define medium_step 10
#define small_step 1

#define dur_start 50
#define dur_good 200
#define freq_good 220
#define dur_bad 400
#define freq_bad 320

//Declare variables for functions
//--adjustable--
//int buzz_delay = 200; //buzz duration/delay
//int freq = 220;       //buzzer tone

int stepper_steps[] = {1,10,50,100}; //0 small, 1 medium, 2 large, 3 largest
float tension_cutoff[] = {20.0,70.0,75.0,79.5,80.0};

///GET RID OF THESE
float tension_good = 80.5;
float tension_low = 80.0;
float tension_high = 81.0;

float calib_factor = 11880.0;

char user_input;
int x;
int y;
int dir_state;
//float tension_before;
//float tension_after;
float tension;
String mode = "RESET";

int button_state = 0;
int switch_state;

// notes for song
const int a = 440;
const int f = 349;
const int cH = 523;

//--initialize load cell object
HX711 load_cell;

//-----------MAIN FUNCTIONS-----------//
void setup() {
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(mode_switch, INPUT);
  //pinMode(button, INPUT_PULLUP);
  pinMode(button, INPUT);
  //attachInterrupt(digitalPinToInterrupt(button), ButtonPress, HIGH);
  attachInterrupt(digitalPinToInterrupt(button), ButtonPress, RISING);
  
  // send the stepper back to the extended position, in case it was retracted when it last turned off
  ResetStepper(reset_steps);

  load_cell.begin(loadDAT, loadCLK);
  load_cell.set_scale(calib_factor);
  load_cell.tare();
  
  // initiate serial connection (usb)
  Serial.begin(9600); //Open Serial connection for debugging
  Serial.println("Begin motor control");

  // let the user know we are ready to go!
  digitalWrite(LED, HIGH);
  tone(buzzerPin, freq_good);
  delay(250);
  digitalWrite(LED, LOW);
  noTone(buzzerPin);
  button_state = 0;
}

void loop() {
  //---NORMAL OPERATION---
  //button_state = digitalRead(button);
  if(button_state){
    switch_state = digitalRead(mode_switch);
    if(switch_state){
      calib_factor = CalibrationMode(calib_factor);
      load_cell.set_scale(calib_factor);
    }
    else TensionMode();
    button_state = 0;
  }
  //---TESTING---
  while(Serial.available()){
    user_input = Serial.read(); //Read user input and trigger appropriate function
    if (user_input == '0') ResetStepper(reset_steps);
    else if (user_input == '1') TensionMode();
    else if (user_input == '2'){ 
      calib_factor = CalibrationMode(calib_factor);
      load_cell.set_scale(calib_factor);
    }
  }
  
  tension = load_cell.get_units();
  Serial.print("Tension: ");
  Serial.print(tension);
  Serial.print("g, Time(ms): ");
  Serial.println(millis());

  delay(250);
}
//------------------------------------//


//-----STEPPER SETTINGS-----//
void MotorPower(int i){
  if(i==0) digitalWrite(EN,HIGH);  //off state
  else digitalWrite(EN,LOW);       //on state
}

void SetMotorDir(String d){
  if (d == "PULL") digitalWrite(dir,LOW);
  else if (d == "PUSH") digitalWrite(dir,HIGH);
}

//input integer refers to denominator of fraction step: e.g. 1 = 1/1 full step, 2 = 1/2 full step
void SetMotorStep(int s){
  if(s == 1){
    digitalWrite(MS1,LOW);
    digitalWrite(MS2,LOW);
  }
  else if(s == 2){
    digitalWrite(MS1,HIGH);
    digitalWrite(MS2,LOW);
  }
  else if(s == 4){
    digitalWrite(MS1,LOW);
    digitalWrite(MS2,HIGH);
  }
  else if(s == 8){
    digitalWrite(MS1,HIGH);
    digitalWrite(MS2,HIGH);
  }
}
//--------------------------//

//--------PERIPHERALS-------//
// button interrupt
void ButtonPress(){
  button_state = 1;
}

// simple flashing LED + buzzing
void BuzzLight(int dur, int freq, int num){
  for(x=0; x<num; x++){
    tone(buzzerPin,freq);
    digitalWrite(LED,HIGH);
    delay(dur);
    noTone(buzzerPin);
    digitalWrite(LED,LOW);
    delay(dur);
  }
}
//--------------------------//


//--------TENSIONING--------//
void TensionMode(){
  BuzzLight(dur_start, freq_good, 2);
  long start_time = millis();
  int i = 0;
  int j = 0;
  float tension = load_cell.get_units();
  //set motor things
  MotorPower(1); // enable motor!
  SetMotorDir("PULL");
  button_state = 0;
  while(tension < tension_cutoff[4]-0.05 && i != -1){
    SetMotorStep(1);
    i = PullTension(largest_step, -1.0, tension_cutoff[0], i);
    i = PullTension(large_step, tension_cutoff[0], tension_cutoff[1], i);
    SetMotorStep(2);
    i = PullTension(medium_step, tension_cutoff[1], tension_cutoff[2], i);
    i = PullTension(small_step, tension_cutoff[2], tension_cutoff[3], i);
    SetMotorStep(8);
    i = PullTension(small_step, tension_cutoff[3], tension_cutoff[4], i);
    tension = load_cell.get_units();
  }
  MotorPower(0); // disable motor, once at tension
  if(i == -1){
    BuzzLight(dur_bad,freq_bad,3 );
    ResetStepper(reset_steps);
    return;
  }
  //ImperialMarch();
  BuzzLight(dur_good,freq_good,1);
  //give final info on wire
  digitalWrite(LED,HIGH);
  tension = load_cell.get_units();
  Serial.print("FINAL TENSION: ");
  Serial.print(tension);
  Serial.print("gf,STEPS: ");
  Serial.print(i);
  Serial.print(", TIME: ");
  Serial.println(millis()-start_time);
  //---HOLD MODE---
  button_state = 0;
  while (!button_state){
    tension = load_cell.get_units();
    if (tension > 81.0 || tension < 79.0){
      digitalWrite(LED,LOW);
      BuzzLight(dur_bad,freq_bad,1);
    }
    Serial.print("Tension: ");
    Serial.print(tension);
    Serial.print("g, Time(ms): ");
    Serial.print(millis());
    Serial.println(", Mode: HOLD");
    delay(500);
  }
  //set stepper back to initial position...add a few just for good measure (maybe +3 or +5)
  digitalWrite(LED,LOW);
  ResetStepper(i+3); //should send back to start position...added a few as a safety guard
  button_state = 0;
  return;
}

void ResetStepper(int steps){
  MotorPower(1);
  SetMotorDir("PUSH");
  SetMotorStep(1);
  MotorStep(steps);
  MotorPower(0);
  BuzzLight(dur_start, freq_good, 2);
}

float PullTension(int steps, float min_tension, float max_tension, int past_steps){
  long t_start = millis();
  int i = past_steps;
  int j = 0;
  float tension = load_cell.get_units();
  while(tension >= min_tension && tension < max_tension){
    if(i > reset_steps  || (millis()-t_start)>reset_time || button_state || i == -1) return -1;
    MotorStep(steps);
    i += steps;
    delay(10);
    tension = load_cell.get_units();
    if(j%5==0){
      Serial.print("Tension: ");
      Serial.print(tension);
      Serial.print("g, Time(ms): ");
      Serial.print(millis());
      Serial.print(", Steps: ");
      Serial.println(i);
    }
    j++;
  }
  return(i);
}

void MotorStep(int steps){
  for(x= 1; x<=steps; x++){  //Loop the stepping enough times for motion to be visible
    digitalWrite(stp,HIGH); //Trigger one step
    delay(1);
    digitalWrite(stp,LOW); //Pull step pin low so it can be triggered again
    delay(1);
  }  
}
//--------------------------//


//--------CALIBRATION--------//
//delay 200ms while taring too make sure we don't read the bounce of the button
//don't forget to pass the new calib factor!
//also must tare at the end
float CalibrationMode(float calib_old){
  float calib_new = calib_old;
  
  Serial.print("(Calib Factor) New: ");
  Serial.print(calib_new);
  Serial.print(", Old: ");
  Serial.println(calib_old);
  return calib_new;
}

//---------MUZAK----------//
void ImperialMarch(){
  beep(a, 250);
  beep(a, 250);    
  beep(a, 250);
  beep(f, 175);
  beep(cH, 75);  
  beep(a, 250);
  beep(f, 175);
  beep(cH, 75);
  beep(a, 325);
  /*
  beep(a, 500);
  beep(a, 500);    
  beep(a, 500);
  beep(f, 350);
  beep(cH, 150);  
  beep(a, 500);
  beep(f, 350);
  beep(cH, 150);
  beep(a, 650);
  */
}

void beep(int note, int duration){
  //Play tone on buzzerPin
  tone(buzzerPin, note, duration);
 
  //Blink LED
  digitalWrite(LED, HIGH);
  delay(duration);
  digitalWrite(LED, LOW);
 
  //Stop tone on buzzerPin
  noTone(buzzerPin);
 
  delay(50);
 
  //Increment counter
  //counter++;
}
