/*
SPI Connection Tabl

| StretchSense  | Arduino Uno                   |
|---------------|-------------------------------|
| GND           | GND                           |
| 3V#           | 3.3V                          |
| CLK           | 13 (SCK)                      |
| MOSI          | 11 (MOSI)                     |
| MISO          | 12 (MISO)                     |
| NSS           | 10 (or another digital pin)   |
*/

/**************************************************************************/
// Module and Variables
/**************************************************************************/

// the StretchSense circuit [16FGV1.0] communicates using SPI
#include <SPI.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

// DE sensors variables
float live_capacitance[10]    = {0,0,0,0,0,0,0,0,0,0};
int mapped_capacitance[10]    = {0,0,0,0,0,0,0,0,0,0};
float highest_capacitance[10] = {0,0,0,0,0,0,0,0,0,0};
float lowest_capacitance[10]  = {0,0,0,0,0,0,0,0,0,0};

// Flags
int calibration = false;

// For the Stretsense
//const int InterruptPin = 6;
const int chipSelectPin = 10;
const int powerPin = 9;

/**************************************************************************/
// DEFINITIONS
/**************************************************************************/
// Data package options
#define DATA                0x00  // 16FGV1.0 data packet
#define CONFIG              0x01  // 16FGV1.0 configuration command
// ODR - Output Data Rate
#define RATE_OFF            0x00
#define RATE_25HZ           0x01
#define RATE_50HZ           0x02
#define RATE_100HZ          0x03
#define RATE_166HZ          0x04
#define RATE_200HZ          0x05
#define RATE_250HZ          0x06
#define RATE_500HZ          0x07
#define RATE_1kHZ           0x08
// INT - Interrupt Mode
#define INTERRUPT_DISABLED  0x00
#define INTERRUPT_ENABLED   0x01
// TRG - Trigger Mode
#define TRIGGER_DISABLED    0x00
#define TRIGGER_ENABLED     0x01
// FILTER - Filter Mode
#define FILTER_1PT          0x01
#define FILTER_2PT          0x02
#define FILTER_4PT          0x04
#define FILTER_8PT          0x08
#define FILTER_16PT         0x10
#define FILTER_32PT         0x20
#define FILTER_64PT         0x40
#define FILTER_128PT        0x80
#define FILTER_255PT        0xFF
// RES - Resolution Mode
// NOTE: resolution changes your sampling range
#define RESOLUTION_1pF      0x00
#define RESOLUTION_100fF    0x01
#define RESOLUTION_10fF     0x02
#define RESOLUTION_1fF      0x03
// Config Transfer
#define PADDING             0x00

// Configuration Setup
// MODIFY THESE PARAMETERS TO CHANGE CIRCUIT FUNCTION
int   ODR_MODE        = RATE_500HZ;
int   INTERRUPT_MODE  = INTERRUPT_DISABLED;
int   TRIGGER_MODE    = TRIGGER_DISABLED;
int   FILTER_MODE     = FILTER_32PT;
int   RESOLUTION_MODE = RESOLUTION_1pF;

// SPI Configuration
SPISettings SPI_settings(2000000, MSBFIRST, SPI_MODE1); 
// Default scaling factor
int CapacitanceScalingFactor = 0; //Default value
int RawData[20];

// For testing if the board is still on
unsigned long previousMillis = 0;
unsigned long interval = 2000;

// =====================================================
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  //Serial.flush();
  //Stretchsense
  //Initialise SPI port
  SPI.begin();
  SPI.beginTransaction(SPI_settings);
  pinMode(chipSelectPin, OUTPUT);
  pinMode(powerPin, OUTPUT);
  digitalWrite(powerPin, HIGH);
  //Configure 16FGV1.0:
  writeConfiguration();
  //Get capacitance scaling factor
  CapacitanceScalingFactor = getCapacitanceScalingFactor(RESOLUTION_MODE);
  // give the circuit time to set up:
  delay(50);
}

// =====================================================
void loop() {
  // Read sensors
  StretchSenseLoop();
  //calibrateDESensors();
  //sendJsonData();
  // live csapacitance

  // // Test if stretchsense board is still active and not spitting out empty values
  // unsigned long currentMillis = millis();
  
  // if(currentMillis - previousMillis > interval){
  //   previousMillis = currentMillis;
  //   if(isArrayempty(live_capacitance)){
  //     digitalWrite(powerPin, LOW);
  //     delay(200);
  //     digitalWrite(powerPin, HIGH);
  //   }
  // }

  // Print to serial
  sendSerialData();
}

// =====================================================
void sendSerialData() {
  // Serial.print("<");  // Start character
  // Serial.print(millis()); // This will print the timestamp
  // Serial.print(",");
  
  /*for(int i=0; i<10; i++) {    // i index should be <10 for full serial bus, but since only 8 are used right now it has been changed
    //Serial.print("ch");
    //Serial.print(i);
    //Serial.print(":");
    //Serial.print (lowest_capacitance[i]);
    //Serial.print (",");
    //Serial.print (highest_capacitance[i]);
    //mapped_capacitance[i] = map(live_capacitance[i], lowest_capacitance[i], highest_capacitance[i], 0, 100);
    Serial.print(calibrationCurve(live_capacitance[i]));
    if(i < 9) {
      Serial.print(",");
    }
  }
  // Serial.print(">");*/
  Serial.print(calibrationCurve(live_capacitance[9]));
  Serial.println();
}

// =====================================================
void sendJsonData() {
  StaticJsonDocument<200> doc;  // Static JSON document of 200 bytes
  doc["ms"] = millis();  // adding the timestamp
  for (int i = 0; i < 10; i++) {
    String key = "c" + String(i);
    doc[key] = calibrationCurve(live_capacitance[i]);
  }
  serializeJson(doc, Serial);  // Serialize and send the JSON object to Serial
  Serial.println();
}

// =====================================================
float calibrationCurve(float capacitance) {
    float calibrated = 0;
    // insert calibration equation here
    calibrated = capacitance;
    return calibrated;
}

// =====================================================
void calibrateDESensors() {
  /* Initialize maximum and minimum capacitance for each finger */             
  if (calibration == false){
    for (int i=0; i<10; i++){   
      lowest_capacitance[i] = live_capacitance[i]-1;  
      highest_capacitance[i] = live_capacitance[i]+1; 
      calibration = true;
    }
  }
  /* Modify maximum and minimum capacitance for each finger based on reading */ 
  else{
    for (int i=0; i<10; i++){   
      if (live_capacitance[i] <= lowest_capacitance[i]){
        lowest_capacitance[i] = live_capacitance[i];
      }
      if (live_capacitance[i] >= highest_capacitance[i]){
        highest_capacitance[i] = live_capacitance[i];
      }
    }
  }
} 

// =====================================================
void writeConfiguration() {
  // 16FGV1.0 requires a configuration package to start streaming data
  // Set the chip select low to select the device:
  digitalWrite(chipSelectPin, LOW);
  SPI.transfer(CONFIG);                 //  Select Config Package
  SPI.transfer(ODR_MODE);               //  Set output data rate
  SPI.transfer(INTERRUPT_MODE);         //  Set interrupt mode
  SPI.transfer(TRIGGER_MODE);           //  Set trigger mode
  SPI.transfer(FILTER_MODE);            //  Set filter
  SPI.transfer(RESOLUTION_MODE);        //  Set Resolution
  for (int i=0;i<16;i++){
    SPI.transfer(PADDING);              //  Pad out the remaining configuration package
  }
  // take the chip select high to de-select:
  digitalWrite(chipSelectPin, HIGH);
}

// =====================================================
void readCapacitance(int raw[]) {
  // 16FGV1.0 transmits data in the form of 10, 16bit capacitance values
  // Set the chip select low to select the device:
  digitalWrite(chipSelectPin, LOW);
  SPI.transfer(DATA);                   //  Select Data Package
  SPI.transfer(PADDING);                //  Get Sequence Number
  for (int i=0; i<20; i++){
    raw[i] =  SPI.transfer(PADDING);    //  Pad out the remaining configuration package
  }
  // take the chip select high to de-select:
  digitalWrite(chipSelectPin, HIGH);
}

// =====================================================
int getCapacitanceScalingFactor (int Resolution_Config) {
  switch(Resolution_Config){
    case (RESOLUTION_1pF):
      return 1;  
    break;
    case (RESOLUTION_100fF):
      return 10;  
    break;
    case (RESOLUTION_10fF):
      return 100;  
    break;
    case (RESOLUTION_1fF):
      return 1000;  
    break;
  }
  return 1;
}

// =====================================================
float extractCapacitance(int raw[], int channel) {
  float capacitance = 0;
  capacitance = (raw[2*channel])*256+raw[2*channel+1];
  capacitance /= CapacitanceScalingFactor;
  return capacitance;
}

// =====================================================
void StretchSenseLoop () {
  float capacitance = 0;
  // Read the sensor Data
  readCapacitance(RawData);
  // convert the raw data to capacitance:
  for (int i=0; i<10; i++){
    live_capacitance[i] = (RawData[2*i] << 8) + RawData[2*i + 1];  // Combine two bytes into a single 16-bit value
    live_capacitance[i] /= CapacitanceScalingFactor;
    //capacitance = extractCapacitance(RawData,i);
    //if(i<10){
    //  live_capacitance[i] = capacitance;
    //}
  }
}

// =====================================================
bool isArrayempty (float array[10]) {
  float sum = 0.0;
  // Sum array
  for(int i=0; i<10; i++){
    sum += array[i];
  }

  // Only if all elements are 0, return true
  if(sum == 0.0){
    return true;
  }
  return false;
}
