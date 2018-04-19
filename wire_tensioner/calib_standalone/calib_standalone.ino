// load cell calibration
//     cole kampa     ,      jack popa
// <kampa041@umn.edu> , <popax014@umn.edu>

#include "HX711.h"

//load cell
#define loadDAT  7
#define loadCLK  6
#define ref_mass 49.9495
//others
#define LED 4
#define buzzerPin 13
//#define buzz_delay 200
//#define freq 220
//#define buzz_delay_bad 500
//#define freq_bad 320

char user_input;
String mode = "WAIT";
String last_mode;

float calibration_factor = 11880.0;

HX711 scale(loadDAT, loadCLK);

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 calibration sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");
  Serial.println("Press + or a to increase calibration factor");
  Serial.println("Press - or z to decrease calibration factor");

  pinMode(buzzerPin, OUTPUT);
  
  scale.set_scale(calibration_factor);
  scale.tare();	//Reset the scale to 0

  long zero_factor = scale.read_average(); //Get a baseline reading 
  Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);
}

void loop() {
  if (Serial.available()) {
    user_input = Serial.read();
    if (user_input == '0') {
      mode = "WAIT";
    }
    if (user_input == '1') {
      mode = "TARE";
    }
    if (user_input == '2') {
      mode = "SET";
    }
  }
  last_mode = mode;
  if (mode == "TARE") {
    scale.tare();
    tone(buzzerPin,freq);
    delay(buzz_delay);
    noTone(buzzerPin);
    mode = "WAIT";
  }
  else if (mode == "SET") {
    calibration_factor = adjust_calib(calibration_factor);
    scale.set_scale(calibration_factor);
    mode = "WAIT";
  }

  Serial.print("Reading: ");
  Serial.print(scale.get_units(), 4);
  Serial.print(" g, calibration_factor: "); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  Serial.print(calibration_factor);
  Serial.print(", Mode: ");
  Serial.println(last_mode);
  
  delay(500);
}

float adjust_calib(float old_calib){
  int i = 0;
  float new_calib = old_calib;
  scale.set_scale(new_calib);
  float step_size;
  float meas = scale.get_units();
  float dif = meas - ref_mass;
  step_size = set_step(dif);
  while(abs(dif)>0.005){
    i += 1;
    if(dif > 0.0){
      new_calib += step_size;
    }
    else{
      new_calib -= step_size;
    }
    scale.set_scale(new_calib);
    meas = scale.get_units();
    dif = meas - ref_mass;
    //see function below: set_step() decides how large of a step to make based on how far off the calibration factor is
    step_size = set_step(dif);
    //testing prints
    if(i%50 == 0) {
      Serial.print("Reading: ");
      Serial.print(meas, 4);
      Serial.print(" g, calibration_factor: "); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
      Serial.print(new_calib);
      Serial.println(", Mode: SET");
      Serial.print("dif: ");
      Serial.print(dif, 4);
      Serial.print(", step: ");
      Serial.print(step_size);
      Serial.print(", loops: ");
      Serial.println(i);
    }
    //if we loop through more than 150 times, something is wrong. return the original calibration factor and buzz at the user 3 times
    if(i>150) {
      tone(buzzerPin,freq_bad);
      pinMode(LED,HIGH);
      delay(buzz_delay_bad);
      noTone(buzzerPin);
      pinMode(LED,LOW);
      delay(buzz_delay_bad);
      tone(buzzerPin,freq_bad);
      pinMode(LED,HIGH);
      delay(buzz_delay_bad);
      noTone(buzzerPin);
      pinMode(LED,LOW);
      delay(buzz_delay_bad);
      tone(buzzerPin,freq_bad);
      pinMode(LED,HIGH);
      delay(buzz_delay_bad);
      noTone(buzzerPin);
      pinMode(LED,LOW);
      return old_calib;
    }
  }
  //good calibration factor...buzz once and return the new calibration factor
  tone(buzzerPin,freq);
  pinMode(LED,HIGH);
  delay(buzz_delay);
  noTone(buzzerPin);
  pinMode(LED,LOW);
  return new_calib;
}

float set_step(float difference) {
  if(abs(difference)>10.0){
    return 1000.0;
  }
  else if(abs(difference)>1.0){
    return 100.0;
    //return 50.0;
  }
  else if(abs(difference)>0.1) {
    return 10.0;
  }
  else if(abs(difference)>0.01){
    return 1.0;
  }
  else {
    return 0.1;
  }
}
