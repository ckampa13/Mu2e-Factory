//Global Variables
const float Vard= 5.0;
const int num_meas = 100;

int dig_vals[16] = {B000000, B000100, B100000, B100100,    B010010, B010110, B110010, B110110,    B001001, B001101, B101001, B101101,    B011011, B011111, B111011, B111111};

int analog_read[num_meas][6];
int adc_max[6];
float volt_max[6];

float Vout= 0;
int inByte = 0;
int current_selection = 0;
int rawADC = 0;

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  // initialize the Digital (Select) pins:
  for (int thisPin = 2; thisPin <= 7; thisPin++) {
    pinMode(thisPin, OUTPUT);
    
  }
}

void loop() {
  // read the sensor:
  if (Serial.available() > 0) {
    inByte = Serial.parseInt();
    if(inByte >= 0 && inByte < 16) {
      digitalSwitch(dig_vals[inByte]);
      current_selection = inByte; 
    }
    if(inByte == 69) {
      readVoltage();
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
  delay(250);
}

// Setting digital outputs for select channels on MUXs
void digitalSwitch(int dig) {
  digitalWrite(2, HIGH && (dig & B100000));
  digitalWrite(3, HIGH && (dig & B010000));
  digitalWrite(4, HIGH && (dig & B001000));
  digitalWrite(5, HIGH && (dig & B000100));
  digitalWrite(6, HIGH && (dig & B000010));
  digitalWrite(7, HIGH && (dig & B000001));
  delay(500);
}



void readVoltage() {
  for (int i = 0; i < num_meas; i++) {
    for (int j = 0; j < 6; j++) {
      analog_read[i][j] = 0;
    }
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
    delay(10);
  }

  //Find maximum values for Voltage...corresponds to minimum resistance!
  for (int j = 0; j < 6; j++) {
    adc_max[j] = 0;
  }
  for (int i = 0; i < num_meas; i++) {
    for (int j = 0; j < 6; j++) {
      if (analog_read[i][j] > adc_max[j]) {
        adc_max[j] = analog_read[i][j];
      }
    }
  }

  //SERIAL OUTPUT
  Serial.print("(S");
  Serial.print(current_selection);
  Serial.print(": ");
  
  for (int j = 0; j < 6; j++){
    volt_max[j] = adc_max[j] * Vard / 1023.0;
    Serial.print(volt_max[j]);
    if ( j != 5 ) {
      Serial.print(", ");
    }
    else {
      Serial.print(")\n");
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

