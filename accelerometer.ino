#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();
char userInput;
int timeOut;
float time_divisor = 1000;
unsigned long currentTime = 0;
unsigned long startTime = 0;


void setup(void) {
  Serial.begin(9600);
    if (! mma.begin()) {
    Serial.println("Couldn't start");
    while (1);
  }
  
  mma.setRange(MMA8451_RANGE_4_G);
}

void loop() {


// Wait for keyboard input
  if(Serial.available()> 0){

    userInput = Serial.read();

    if(userInput){

      timeOut = userInput - '0';
      startTime = millis();

      while (millis() - startTime < userInput){
        // Get a new sensor event using Arduino_Sensor library
        sensors_event_t event;
        mma.getEvent(&event);
        currentTime = millis();
        // Display the results (acceleration is measured in m/s^2)
        /*
          Serial.print(currentTime/time_divisor, 3);Serial.print(",");
          Serial.print(event.acceleration.x); Serial.print(",");
          Serial.print(event.acceleration.y); Serial.print(",");
          Serial.println(event.acceleration.z);
        */
        
        Serial.println(currentTime/time_divisor, 3);
        Serial.println(event.acceleration.x);
        Serial.println(event.acceleration.y);
        Serial.println(event.acceleration.z);      
      }
    }
  }
  

  
}




// Other ways to interact with the sensor:

/*  
  mma.read();
  Serial.print(mma.x); Serial.print(",");
  Serial.print(mma.y); Serial.print(",");
  Serial.println(mma.z); 
*/

/*
  sensor_t sensor;
  mma.getSensor(&sensor);
  Serial.println(sensor.name);
  Serial.println(sensor.version);
  Serial.print(sensor.max_value); Serial.print("to"); Serial.println(sensor.min_value);
*/
