// Include the libraries:
#include <Adafruit_Sensor.h>
#include <DHT.h>
// Set DHT pin:
#define DHTPIN 2
#define DHTTYPE DHT22   // DHT 22  (AM2302) sensor temperature

#include "DFRobot_EC.h"
#include <EEPROM.h>

#define EC_PIN A1

float voltage,ecValue,temperature = 25;
DFRobot_EC ec;

String incomingByte = "";
DHT dht = DHT(DHTPIN, DHTTYPE);

int pump_time = 2000;


void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(3, OUTPUT);  // pin pump
  pinMode(4, OUTPUT);  // pin water add pump
  pinMode(5, OUTPUT);  // pin water add A
  pinMode(6, OUTPUT);  // pin water add B
  dht.begin();// Setup sensor:
  ec.begin();
  //Serial.println("Starting Arduino Uno...");
}

void loop() {

if (Serial.available() > 0) {

  incomingByte = Serial.readString(); // read the incoming byte:


  if (incomingByte == "pon") {
    
  //Set the LED pin to HIGH. This gives power to the LED and turns it on
      digitalWrite(3, HIGH);           
      delay(500);//Wait for a second
  }

  else if(incomingByte == "pof") {

  //Set the LED pin to LOW. This turns it off
      digitalWrite(3, LOW);
      delay(500);//Wait for a second
  }


  else if(incomingByte == "won") {

  //Set the LED pin to LOW. This turns it off
      digitalWrite(4, HIGH);
      //delay(pump_time);//Wait for a second
      //digitalWrite(4, LOW);
      delay(500);
  }


    else if(incomingByte == "wof") {

  //Set the LED pin to LOW. This turns it off
      digitalWrite(4, LOW);
      delay(500);
  }


  else if(incomingByte == "b") {
      digitalWrite(5, HIGH);
      delay(pump_time);//Wait for a second
      digitalWrite(5, LOW);
      delay(500);
  }


  else if(incomingByte == "a") {
      digitalWrite(6, HIGH);
      delay(pump_time);//Wait for a second
      digitalWrite(6, LOW);
      delay(500);
  }

  else if(incomingByte == "tmp") {
      delay(250);
      float t = dht.readTemperature(); // Read the temperature as Celsius:
      delay(500);
      //Serial.print("Temperature: ");
      Serial.print(t);
      delay(250);
  }


  else if(incomingByte == "hum") {
      delay(250);
      float h = dht.readHumidity();// Read the humidity in %:
      delay(500);
      //Serial.print("Humidity: ");
      Serial.print(h);
      delay(250);
  }

  else if(incomingByte == "ec") {
      delay(250);
      voltage = analogRead(EC_PIN)/1024.0*5000;  // read the voltage
      ecValue =  ec.readEC(voltage,temperature);
      delay(500);
      //Serial.print("Conductivity: ");
      Serial.print(ecValue,2);
      delay(250);
  }

    

}
}
