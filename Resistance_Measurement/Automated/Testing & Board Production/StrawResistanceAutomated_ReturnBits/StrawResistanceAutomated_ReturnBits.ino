//   Update: 8/22/2017 removing voltage calculation...only returns a float between 0 and 1023.0.
//   This way the Arduino code should never have to change on a board, once a final version is decided.
//
//   Serial string to read all: arbrcrdrerfrgrhrirjrkrlrmrnrorpr
//

//Global Variables
//const float Vard= 4.991;
//const float Vard= 5.028;
const int num_meas = 100;
//                   234567   234567   234567   234567
int dig_vals[16] = {B000000, B000100, B100000, B100100,    B010010, B010110, B110010, B110110,    B001001, B001101, B101001, B101101,    B011011, B011111, B111011, B111111};

int analog_read[num_meas][6];
//int adc_max[6];
int adc_max;
long adc_total;
float adc_avg;
//float volt_max[6];
float final_volt[6];
//float Vout= 0;
int inByte = 97;
int current_selection = 97;
int rawADC = 0;

// Send serial value 'y' for actual averaging of data, 'z' for giving maximum voltage value, corresponding to minimum resistance...setting default to averaging, but should always declare in python script.
char avg_method = 'y';

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  Serial.println("Ready!"); // print "Ready" once
  // initialize the Digital (Select) pins:
  for (int thisPin = 2; thisPin <= 7; thisPin++) {
    pinMode(thisPin, OUTPUT);
    
  }
}

void loop() {
  // read the sensor:
  if (Serial.available() > 0) {
    //inByte = Serial.parseInt();
    inByte = Serial.read();
    if(inByte-97 >= 0 && inByte-97 < 16) {    //If letter is a-p, switch digital values
      digitalSwitch(dig_vals[inByte-97]);
      current_selection = inByte; 
    }
    if(inByte == 'r') { //using r for 'read'
      readVoltage(avg_method);
    }
    if(inByte == 'y' || inByte == 'z') { //y=avg z=max
      avg_method = inByte;
    }
  }

/*
  //TESTING DIG SWITCHING
  for (int i = 2; i <= 7; i++) {
    if(bitRead(PORTD,i) == HIGH) {
      Serial.print("1");
    }
    else {
      Serial.print("0");
    }
  }
  Serial.print('\n');
*/

  //serial print to be read by python script
  //readVoltage();
  delay(25);
}

// Setting digital outputs for select channels on MUXs
void digitalSwitch(int dig) {
  digitalWrite(2, HIGH && (dig & B100000));
  digitalWrite(3, HIGH && (dig & B010000));
  digitalWrite(4, HIGH && (dig & B001000));
  digitalWrite(5, HIGH && (dig & B000100));
  digitalWrite(6, HIGH && (dig & B000010));
  digitalWrite(7, HIGH && (dig & B000001));
  //delay(250);
  delay(10);
}



void readVoltage(char avg_method) {
  for (int j = 0; j < 6; j++) {
    for (int i = 0; i < num_meas; i++) {
      analog_read[i][j] = 0;
    }

    final_volt[j] = 0; 
    
  }

  int i = 0;
  while(i < num_meas) {
    for (int j = 0; j < 6; j++) {
      //analogRead returns integer in range 0 to 1023
      //rawADC = analogRead(j);
      //Vout = (rawADC * Vard)/1024.0;
      //analog_read[i][j] = Vout;
      //analog_read[i][j] = rawADC;
      analog_read[i][j] = analogRead(j);

      /*
      //TESTING
      Serial.print("M");
      Serial.print(i);
      Serial.print(" ");
      */
      /*
      Serial.print("A");
      Serial.print(j);
      Serial.print(": ");
      Serial.print(analog_read[i][j]*Vard/1024.0);
      Serial.print(" V \n");
      */
    }
    i++;

    //1 ms delay between measurements
    delay(1);
  }

  if (avg_method == 'y') {
    //Find average value
    for (int j = 0; j < 6; j++) {
      adc_total = 0;
      for (int i = 0; i < num_meas; i++) {
        adc_total += analog_read[i][j];
      }
      adc_avg = adc_total/num_meas;
      
      //final_volt[j] = adc_avg * Vard / 1023.0;
      final_volt[j] = adc_avg;
    }
  }
  else if (avg_method == 'z') {
    //Find maximum values for Voltage...corresponds to minimum resistance!

    /*
    for (int j = 0; j < 6; j++) {
      adc_max[j] = 0;
    }
    */
    
    for (int j = 0; j < 6; j++) {
      adc_max = 0;
      for (int i = 0; i < num_meas; i++) {
        if (analog_read[i][j] > adc_max) {
        //if (analog_read[i][j] > adc_max[j]) {
          adc_max = analog_read[i][j];
          //adc_max[j] = analog_read[i][j];
        }
      }

      //final_volt[j] = adc_max * Vard / 1023.0;
      final_volt[j] = adc_max;
    }
  }

  //SERIAL OUTPUT
  //Serial.print("S");
  Serial.print(char(current_selection));
  Serial.print(", ");
  
  for (int j = 0; j < 6; j++){
    //volt_max[j] = adc_max[j] * Vard / 1023.0;
    Serial.print(final_volt[j]);
    if ( j != 5 ) {
      Serial.print(", ");
    }
    else {
      Serial.print("\n");
    }
    /*
    //TESTING
    Serial.print("A");
    Serial.print(j);
    Serial.print(": ");
    Serial.print(volt_max[j]);
    Serial.print(" V \n");
    */
  }
}


