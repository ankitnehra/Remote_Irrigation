
const int sensorPin =A0;
int soilMoisture;
double moisturePC;
int moistureInt;
const int ledPin = 13;
int incomingByte;
int on = 36;
int off = 37;

void setup() {
  // put your setup code here, to run once++
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
}

void loop() {
  // put your main code here, to   run repeatedly:
  
  //moisturelevel of soil as read by the sensor
  soilMoisture = analogRead(sensorPin);

  //Convert the analog read to voltage
  moisturePC = soilMoisture*(100.0/925.0);

  moistureInt = (int)moisturePC;

  if (moistureInt <100)
    Serial.print(moistureInt);

  delay(5000);
  
  /*Listen from the wifi to turn off the engine
   * if raspberry asks to shut down
   *  shut it down
   * else if raspberry asks to turn it on
   *  turn it on
   * 
   */
   if (Serial.available() > 0) {
      incomingByte = Serial.read();
      if (incomingByte ==off)
        digitalWrite(ledPin, LOW);
      if(incomingByte==on)
        digitalWrite(ledPin, HIGH);
   }

}
