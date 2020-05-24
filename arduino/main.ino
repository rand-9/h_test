String incomingByte = "";

void setup() {

Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
pinMode(13, OUTPUT);

}

void loop() {

if (Serial.available() > 0) {

incomingByte = Serial.readString(); // read the incoming byte:

// Serial.print(" I received:");

//Serial.println(incomingByte);

if (incomingByte == "pon") {
  
//Set the LED pin to HIGH. This gives power to the LED and turns it on
    digitalWrite(13, HIGH);
//Wait for a second
    delay(1000);
}

else if(incomingByte == "pof") {

//Set the LED pin to LOW. This turns it off
    digitalWrite(13, LOW);
//Wait for a second
    delay(1000);
}
    
else {
    digitalWrite (13, HIGH);
    delay(400);
    digitalWrite (13, LOW);
    delay(400);

}




}
}
