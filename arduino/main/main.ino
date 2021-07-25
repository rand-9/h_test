// Include the libraries:
#include <Adafruit_Sensor.h>
#include <DHT.h>
// Set DHT pin:
#define DHTPIN 2
#define DHTTYPE DHT22   // DHT 22  (AM2302) sensor temperature

#include "DFRobot_EC.h"
#include "DFRobot_PH.h"
#include <EEPROM.h>

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
    pinMode(pump_pin, OUTPUT);  // pin pump
    pinMode(fwater_pin, OUTPUT);  // pin water add pump
    pinMode(nutA_pin, OUTPUT);  // pin water add A
    pinMode(nutB_pin, OUTPUT);  // pin water add B
    pinMode(air_pin, OUTPUT);  // pin air pump
    pinMode(phd_pin, OUTPUT);  // pin ph down
    dht.begin();
    ec.begin();
    //Serial.println("Starting Arduino Uno...");
}

void loop() {

    if (Serial.available() > 0) {
    incomingByte = Serial.readString(); // read the incoming byte:

        // main pump
        if (incomingByte == "pon") {
            digitalWrite(pump_pin, HIGH);           
        delay(500);//Wait for a second
        }

        else if(incomingByte == "pof") {
            digitalWrite(pump_pin, LOW);
            delay(500);//Wait for a second
            }

        // fresh water
        else if(incomingByte == "won") {
            digitalWrite(fwater_pin, HIGH);
            delay(500);
        }

        else if(incomingByte == "wof") {
            digitalWrite(fwater_pin, LOW);
            delay(500);
        }
  
        // air pump
        else if(incomingByte == "aon") {
            digitalWrite(air_pin, HIGH);
            delay(500);
        }

        else if(incomingByte == "aof") {
            digitalWrite(air_pin, LOW);
            delay(500);
        }

        // nutrien B
        else if(incomingByte == "a") {
            digitalWrite(nutA_pin, HIGH);
            delay(pump_time); // Wait for a second
            digitalWrite(nutA_pin, LOW);
            delay(500);
        }

        // nutrient A
        else if(incomingByte == "b") {
            digitalWrite(nutB_pin, HIGH);
            delay(pump_time); // Wait for a second
            digitalWrite(nutB_pin, LOW);
            delay(500);
        }

        // dropper PH
        else if(incomingByte == "phd") {
            digitalWrite(phd_pin, HIGH);
            delay(ph_down_time);
            digitalWrite(phd_pin, LOW);
            delay(500);
        }

        // Temperature
        else if(incomingByte == "tmp") {
            delay(250);
            float t = dht.readTemperature(); // Read the temperature as Celsius:
            delay(500);
            //Serial.print("Temperature: ");
            Serial.print(t);
            delay(250);
        }

        // humidity
        else if(incomingByte == "hum") {
            delay(250);
            float h = dht.readHumidity();// Read the humidity in %:
            delay(500);
            //Serial.print("Humidity: ");
            Serial.print(h);
            delay(250);
        }

        // Conductivity EC
        else if(incomingByte == "ec") {
            delay(250);
            voltage1 = analogRead(EC_PIN)/1024.0*5000;  // read the voltage
            ecValue =  ec.readEC(voltage1,temperature);
            delay(500);
            Serial.print(ecValue,2);
            delay(250);
        }

        // PH
        else if(incomingByte == "ph") {
            delay(250);
            voltage2 = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
            phValue =  ph.readPH(voltage2,temperature);
            delay(500);
            Serial.print(phValue,2);
            delay(250);
        }

        // Top water sensor
        else if(incomingByte == "twa") {
            delay(250);
            twaterValue = digitalRead(tswitch_pin);
            delay(500);
            Serial.print(twaterValue,2);
            delay(250);
        }

    }

}
