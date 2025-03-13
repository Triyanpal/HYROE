#include <HX711.h>

// Tedea Huntleigh Load Cell Calibration
// Arduino Uno Pinout:
// E+ - 5V
// E- - GND
// S+ - A0
// S- - A1
// +S - A2
// -S - A3

// Calibration parameters
float LOADCELL_OFFSET = 0.0;   // Offset value
float LOADCELL_SCALE = 100.0;    // Scale value

// Known weight for calibration (replace with your own value)
const float KNOWN_WEIGHT = 1.183;  // Known weight in kilograms

void setup() {
  Serial.begin(9600);
  
  // Print the calibration parameters
  Serial.println("Load Cell Calibration Parameters:");
  Serial.print("Offset: ");
  Serial.println(LOADCELL_OFFSET);
  Serial.print("Scale: ");
  Serial.println(LOADCELL_SCALE);
  
  // Calibrate the load cell
  calibrateLoadCell();
}

void loop() {
  // Read the load cell value
  float value = readLoadCell();

  // Apply calibration
  float calibratedValue = (value - LOADCELL_OFFSET) / LOADCELL_SCALE;
  // Serial.print("calibrated = ");
  // Serial.println(calibratedValue);
  // Check if LOADCELL_SCALE is not zero or close to zero
  // if (LOADCELL_SCALE > 0.005) {
  //   // Convert calibrated value to load in kilograms
  //   float load = calibratedValue * LOADCELL_SCALE;
    
  //   // Print the load value
  //   Serial.print("Load: ");
  //   Serial.print(load);
  //   Serial.println(" N");
  // } else {
  //   // Print an error message if LOADCELL_SCALE is zero or close to zero
  //   Serial.println("Error: Load cell not calibrated properly.");
  // }
  
  // Delay for stability
  delay(800);
}

void calibrateLoadCell() {
  Serial.println("Calibrating Load Cell...");
  Serial.println("Please place the known weight on the load cell.");
  Serial.println("Press any key to start calibration.");
  
  // Wait for user input to start calibration
  while (!Serial.available()) {
    // Wait for user input
  }
  Serial.read();  // Clear the input buffer
  
  // Read the load cell value with the known weight
  float value = readLoadCell();
  
  // Calculate the calibration parameters
  LOADCELL_SCALE = KNOWN_WEIGHT / (value);
  
  // Print the calibration results
  Serial.println("Calibration completed!");
  Serial.print("Offset: ");
  Serial.println(LOADCELL_OFFSET);
  Serial.print("Scale: ");
  Serial.println(LOADCELL_SCALE);
}

float readLoadCell() {
  // float value = readLoadCell();
  // float calibratedValue = (value - LOADCELL_OFFSET) / LOADCELL_SCALE;
  // Read the voltage across the load cell
  // int sensePositive = analogRead(A2);
  // int senseNegative = analogRead(A3);
  float loadcellvalue = ((9.81 * analogRead(A0))-10000)/100;
  // int signalNegative = analogRead(A1);

  // float Loadresult = loadcellvalue - calibratedValue;

  // Serial.println(sensePositive);
  // Serial.println(senseNegative);
  Serial.print("Load cell reading = ");
  Serial.println(loadcellvalue);
  // Serial.println(signalNegative);

  // Serial.println("Load");
  // Serial.print(Loadresult);


  // // Calculate the differential voltage
  // int differentialVoltage = sensePositive - senseNegative;
  
  // // Adjust the voltage with the signal terminals
  // int adjustedVoltage = differentialVoltage - (signalPositive - signalNegative);
  
  // // Return the adjusted voltage
  // return adjustedVoltage;
  return 0;
}
