#include <Adafruit_MCP4728.h>
#include <Wire.h>

// INPUT
#define PRESSURE_SENSOR A0
#define MASSFLOW_SENSOR A1

Adafruit_MCP4728 mcp;

/* SETUP FUNCTION */
void setup() {
  // Start the serial connection with the controller
  Serial.begin(115200);
  handshake();
  analogReference(DEFAULT);

  if(!mcp.begin()){
   Serial.println("Failed to find MCP4728 chip");
   while (1) {
      delay(10);
    }
  }
  Serial.println("MCP4728 Found!");
  
  delay(5);
  // INTERNAL2V56
}

/* MAIN FUNCTION */
void loop(){
  //Wait for Input from ComMgr
  handleInput();
  delay(5);
}

void handshake(){
  // initialize the handshake with MATLAB
  Serial.print('a');
  char a = 'b';

  // handshake has to come back from the serial port
  while (a != 'a') {
    a = Serial.read();
    /* Maintain the pump object already here */
    //delay(5);
  }
  Serial.flush();
  Serial.print('d');
}

void handleInput(){
  // Check for Input
  
  if (Serial.available()>0){

    // Read the Input, store in a string
    char input =  Serial.read();
    
    delay(2);
    int nextBytes = Serial.available();

      if (input == 'v'){
        Serial.print(analogRead(PRESSURE_SENSOR));
      }
      else if (input == 'c') {
        Serial.print('a');
      }
      else if (input == 'i') {
        Serial.print(analogRead(MASSFLOW_SENSOR));
      }
      else if (input == 'm') {
        
        Serial.print("enter a number from 0 to 4096");
        
        int voltage = Serial.parseInt();

        
        
        delay(5);

        char ready = Serial.read();
        
        
        
        if(ready == 'r') {
          if(mcp.setChannelValue(MCP4728_CHANNEL_A, voltage)){
            Serial.print("SUCCESS!");
          } 
        }
        
      }
      else{
      Serial.print('0');
      }

      
    Serial.print('\n');
    serialFlush(nextBytes);
  }
}

void serialFlush(int bytesToFlush){
  while(bytesToFlush-- > 0) {
    char t = Serial.read();
    delay(1);
  }
} 