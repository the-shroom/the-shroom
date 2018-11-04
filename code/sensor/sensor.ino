// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"
#include "name.h"
#define DHTPIN 2     // what digital pin we're connected to

// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.

// TODO: better interface/abstractions
// TODO: PID control

DHT dht(DHTPIN, DHTTYPE);

bool toggle = false;

int OP_SET = 1;



class ConrolTarget{
  public:
    float target;
    float range;

    float calcTarget(float measure){
      float upper = this->target * (1.0 + this->range);
      float lower = this->target * (1.0 - this->range);

      if (measure > upper){
        return 1;
      } else if (lower > measure){
        return -1;
      } else {
        return 0.0;
      }
    }
};

ConrolTarget humidity_control;
ConrolTarget temperature_control;

logAction humidity    = {0,String("humidity")};
logAction temperature = {0,String("temperature")};

void setup() {
  
  dht.begin();

  ControlRelay fans = {1, "fans", 1};
  ControlRelay fogger = {1, "fogger", 1};
  ControlRelay peltier_warm = {1, "peltier_warm", 1};
  ControlRelay peltier_cool = {1, "peltier_cool", 1};

  temperature_control.target = 20;
  temperature_control.range = 0.02;
  
  humidity_control.target = 80;
  humidity_control.range = 0.02;
  
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  digitalWrite(3,HIGH);
  digitalWrite(4,HIGH); 
  digitalWrite(5,HIGH);
  digitalWrite(6,HIGH);
  
//  test switch
//  digitalWrite(3, LOW);
//  delay(1000);
//  digitalWrite(3, HIGH);
  
  

  Serial.begin(9600);
  Serial.println("Start moisture farming! Shroom on!");
  Serial.print(humidity.name);
  Serial.print(", ");
  Serial.println(temperature.name);
  
}

void loop() {
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  
  humidity.value    = dht.readHumidity();
  temperature.value = dht.readTemperature();

  printDebug(humidity);
  printDebug(temperature);
  Serial.print("\n");
//  logAction temperature

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity.value) || isnan(humidity.value) ) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

}

int printDebug(logAction logaction){
  Serial.print(logaction.value);
  Serial.print(", ");
}



void serialEvent(){
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)

  while (Serial.available()) {
    // get the new byte:
    int opcode = (int) Serial.read();
    int port   = (int) Serial.read();
    int output = (int) Serial.read();
    Serial.print("Setting port ");
    Serial.print(port);
    Serial.print(" to ");
    Serial.println(output);
    
    if (opcode == OP_SET){
      if (output > 0){
        output = LOW;
      } else {
        output = HIGH;
      }
      digitalWrite(port,output); 
    }
     
    digitalWrite(LED_BUILTIN, LOW);
      
  }
}
