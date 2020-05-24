// Include the libraries:
#include <Adafruit_Sensor.h>
#include <DHT.h>
// Set DHT pin:
#define DHTPIN 11
#define DHTTYPE DHT22   // DHT 22  (AM2302) sensor temperature


String incomingByte = "";
DHT dht = DHT(DHTPIN, DHTTYPE);


void setup() {

Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
pinMode(12, OUTPUT);  // pin pump
dht.begin();// Setup sensor:
}

void loop() {

if (Serial.available() > 0) {

incomingByte = Serial.readString(); // read the incoming byte:

// Serial.print(" I received:");

//Serial.println(incomingByte);

if (incomingByte == "pon") {
  
//Set the LED pin to HIGH. This gives power to the LED and turns it on
    digitalWrite(12, HIGH);           
    delay(500);//Wait for a second
}

else if(incomingByte == "pof") {

//Set the LED pin to LOW. This turns it off
    digitalWrite(12, LOW);
    delay(500);//Wait for a second
}


else if(incomingByte == "tmp") {
  delay(250);
  float t = dht.readTemperature(); // Read the temperature as Celsius:
  delay(500);
  Serial.print("Temperature: ");
  Serial.print(t);
  delay(250);
}


else if(incomingByte == "hum") {
   delay(250);
   float h = dht.readHumidity();// Read the humidity in %:
   delay(500);
   Serial.print("Humidity: ");
   Serial.print(h);
   delay(250);
}

    


}
}
