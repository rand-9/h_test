// Include the libraries
#include <Adafruit_Sensor.h>
#include <DHT.h>

#include "DFRobot_EC.h"
#include "DFRobot_PH.h"
#include <EEPROM.h>

// Set DHT pin
#define DHTPIN 2
#define DHTTYPE DHT22   // DHT 22  (AM2302) sensor temperature

// Set DFRobot pins
#define EC_PIN A1
#define PH_PIN A2

// pin assignment
const int pump_pin = 3;
const int fwater_pin = 4;
const int nutA_pin = 5;
const int nutB_pin = 6;
const int tswitch_pin = 7;
const int phd_pin = 8;
const int air_pin = 9;
const int power_dht = 10;

// time variables
int pump_time = 2000;
int ph_down_time = 1000;

// calibration values
float voltage1 = 25;
float ecValue = 25;
float voltage2 = 25;
float phValue = 25;
float temperature = 25;
float twaterValue = 0;

DFRobot_EC ec;
DFRobot_PH ph;

String incomingByte = "";
DHT dht = DHT(DHTPIN, DHTTYPE);


void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(tswitch_pin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(pump_pin, OUTPUT);  // pin pump
  pinMode(fwater_pin, OUTPUT);  // pin water add pump
  pinMode(nutA_pin, OUTPUT);  // pin water add A
  pinMode(nutB_pin, OUTPUT);  // pin water add B
  pinMode(air_pin, OUTPUT);  // pin air pump
  pinMode(phd_pin, OUTPUT);  // pin ph down
  pinMode(power_dht, OUTPUT);  // pin ph down
  delay(500);
  digitalWrite(power_dht, HIGH);
  delay(500);
  dht.begin();
  ec.begin();
}

void loop() {

  // If something appears on serial
  if (Serial.available() > 0) {

    incomingByte = Serial.readString(); // read the incoming byte

    // Main water pump ON
    if (incomingByte == "pon") {
      digitalWrite(pump_pin, HIGH);           
      delay(500);
    }

    // Main water pump OFF
    else if(incomingByte == "pof") {
      digitalWrite(pump_pin, LOW);
      delay(500);
    }

    // Fresh water pump ON
    else if(incomingByte == "won") {
      digitalWrite(fwater_pin, HIGH);
      delay(500);
    }

    // Fresh water pump OFF
    else if(incomingByte == "wof") {
      digitalWrite(fwater_pin, LOW);
      delay(500);
    }

    // Air pump ON
    else if(incomingByte == "aon") {
      digitalWrite(air_pin, HIGH);
      delay(500);
    }

    // Air pump OFF
    else if(incomingByte == "aof") {
      digitalWrite(air_pin, LOW);
      delay(500);
    }

    // Nutrien A pump
    else if(incomingByte == "a") {
      digitalWrite(nutA_pin, HIGH);
      delay(pump_time); // Wait for a second
      digitalWrite(nutA_pin, LOW);
      delay(500);
    }

    // Nutrient B pump
    else if(incomingByte == "b") {
      digitalWrite(nutB_pin, HIGH);
      delay(pump_time); // Wait for a second
      digitalWrite(nutB_pin, LOW);
      delay(500);
    }

    // Down PH pump
    else if(incomingByte == "phd") {
      digitalWrite(phd_pin, HIGH);
      delay(ph_down_time);
      digitalWrite(phd_pin, LOW);
      delay(500);
    }

    // Temperature
    else if(incomingByte == "tmp") {
      delay(1000);
      float t = dht.readTemperature(); // Read the temperature as Celsius:
      delay(1000);
      //Serial.print("Temperature: ");
      Serial.print(t);
      delay(250);
    }

    // Humidity
    else if(incomingByte == "hum") {
      delay(1000);
      float h = dht.readHumidity();// Read the humidity in %:
      delay(1000);
      //Serial.print("Humidity: ");
      Serial.print(h);
      delay(250);
    }

    // Conductivity EC
    else if(incomingByte == "ec") {
      delay(500);
      voltage1 = analogRead(EC_PIN)/1024.0*5000;  // read the voltage
      ecValue =  ec.readEC(voltage1,temperature);
      delay(500);
      Serial.print(ecValue,2);
      delay(250);
    }

    // PH
    else if(incomingByte == "ph") {
      delay(500);
      voltage2 = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
      phValue =  ph.readPH(voltage2,temperature);
      delay(500);
      Serial.print(phValue,2);
      delay(250);
    }

    // Top water sensor
    else if(incomingByte == "twa") {
      delay(500);
      twaterValue = digitalRead(tswitch_pin);
      delay(500);
      Serial.print(twaterValue,2);
      delay(250);
    }

    // Test
    else if(incomingByte == "h") {
      delay(250);
      Serial.println("hiImArduino");
      delay(250);
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(2000);                       
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
      delay(2000);
      delay(250);    
    }

  }

}
