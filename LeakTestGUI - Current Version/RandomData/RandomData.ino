// print random numbers to serial - example from arduino website

long randNumber0;long randNumber1;long randNumber;

void setup(){
  Serial.begin(115200);

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  randomSeed(analogRead(0));
}

void loop() {
  // print a random number from 0 to 299
  randNumber0 = random(5);
  randNumber1 = random(300);
  Serial.print(randNumber0);Serial.print("\t");Serial.print(randNumber1);
  Serial.println();
  // print a random number from 10 to 19
  //randNumber = random(10, 20);
  //Serial.println(randNumber);

  delay(50);
}
