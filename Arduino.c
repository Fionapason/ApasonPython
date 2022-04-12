/*
 * ARDUINO CODE FOR EB 2 AS IN UF
 */

#include <Adafruit_MCP4728.h>

/* https://github.com/adafruit/Adafruit_MCP4728 YOU
HAVE TO DOWNLOAD THIS LIBRARY AS A ZIP FILE AND ADD
IT IN YOUR ARDUINO IDE IF YOU WANT TO RECOMPILE

ALSO DOWNLOAD AND ADD TO LIBRARY: 
https://github.com/adafruit/Adafruit_BusIO */

#include <Wire.h>

// ANALOG OUT
Adafruit_MCP4728 mcp;

// PRESSURE SENSORS
#define P_SICK_1 A1
#define P_SICK_2 A2
#define P_SICK_3 A3


// MASSFLOW SENSORS
#define MF_1 A5
#define MF_2 A6
#define MF_3 A7
#define MF_4 A8

// LEVEL SWITCHES (INPUT PINS)

#define LS_1 22
#define LS_2 23
#define LS_3 24
#define LS_4 25


// THREE WAY VALVES

#define TWV_1 38


// OPEN CLOSE VALVES

#define OCV_NO_3 46 // normally open
#define OCV_NC_4 47 // normally closed

// PUMP ON/OFF

#define PUMP_1 48
#define PUMP_2 49

void handshake();

void serialFlush(int bytesToFlush);

void inputSwitch(char input);

int readPressure_SICK_1();
int readPressure_SICK_2();
int readPressure_SICK_3();

int readMassflow_1();
int readMassflow_2();
int readMassflow_3();
int readMassflow_4();



char check_LevelSwitch_1();
char check_LevelSwitch_2();
char check_LevelSwitch_3();
char check_LevelSwitch_4();


void set_HIGH_TWV_1(); 

void set_LOW_TWV_1();



void OPEN_OCV_NO_3();
void OPEN_OCV_NC_4();

void CLOSE_OCV_NO_3();
void CLOSE_OCV_NC_4();

void PUMP_1_ON();
void PUMP_1_OFF();

void PUMP_2_ON();
void PUMP_2_OFF();


void set_mcp_A();
void set_mcp_B();
void set_mcp_C();
void set_mcp_D();


void setup() {
  
  Serial.begin(115200);

  //initialize DAC
  mcp.begin();
  
  //secure serial connection
  handshake();
  
  //set analog Reference voltage
  analogReference(DEFAULT);

  //initialize digital output pins
  pinMode(TWV_1, OUTPUT);

  pinMode(OCV_NO_3  , OUTPUT);
  pinMode(OCV_NC_4  , OUTPUT);

  pinMode(PUMP_1, OUTPUT);
  pinMode(PUMP_2, OUTPUT);

  digitalWrite(48,HIGH);

  
  Serial.println("I AM DONE! \n");
   
}

void loop() {

 while (Serial.available() <= 0);
 
 char input = Serial.read();
 
 int nextBytes = Serial.available();

 serialFlush(nextBytes);

 inputSwitch(input);
 
 nextBytes = Serial.available();
 serialFlush(nextBytes);
  
 // Serial.write('\n');

}


// PRESSURE READ FUNCTIONS

int readPressure_SICK_1(){
  return analogRead(P_SICK_1);
}

int readPressure_SICK_2(){
  return analogRead(P_SICK_2);
}

int readPressure_SICK_3(){
  return analogRead(P_SICK_3);
}


// MASSFLOW READ FUNCTIONS

int readMassflow_1(){
  return analogRead(MF_1);
}

int readMassflow_2(){
  return analogRead(MF_2);
}

int readMassflow_3(){
  return analogRead(MF_3);
}

int readMassflow_4(){
  return analogRead(MF_4);
}



// LEVEL SWITCH CHECK FUNCTIONS
// RETURN 1 IF THE CIRCUIT IS CLOSED, 0 IF IT'S OPENED

char check_LevelSwitch_1(){
  if (digitalRead(LS_1) == HIGH) {
    return '1';
  } else return '0';
}

char check_LevelSwitch_2(){
  if (digitalRead(LS_2) == HIGH) {
    return '1';
  } else return '0';
}

char check_LevelSwitch_3(){
  if (digitalRead(LS_3) == HIGH) {
    return '1';
  } else return '0';
}

char check_LevelSwitch_4(){
  if (digitalRead(LS_4) == HIGH) {
    return '1';
  } else return '0';
}



// THREE WAY VALVE SET HIGH --> LOW LEVEL TRIGGER ON RELAY BOARD!!

void set_HIGH_TWV_1(){
  digitalWrite(TWV_1, LOW);
}
 


// THREE WAY VALVE SET LOW

void set_LOW_TWV_1(){
  digitalWrite(TWV_1, HIGH);
}
 


// OPEN OPEN CLOSE VALVES


void OPEN_OCV_NO_3(){
  digitalWrite(OCV_NO_3, HIGH);
}
void OPEN_OCV_NC_4(){
  digitalWrite(OCV_NC_4, LOW);
}

// CLOSE OPEN CLOSE VALVES

void CLOSE_OCV_NO_3(){
  digitalWrite(OCV_NO_3, LOW);
}
void CLOSE_OCV_NC_4(){
  digitalWrite(OCV_NC_4, HIGH);
}

// PUMP ON

void PUMP_1_ON(){
  digitalWrite(PUMP_1, HIGH);
}
void PUMP_2_ON(){
  digitalWrite(PUMP_2, HIGH);
}

// PUMP OFF

void PUMP_1_OFF(){
  digitalWrite(PUMP_1, LOW);
}
void PUMP_2_OFF(){
  digitalWrite(PUMP_2, LOW);
}

// SET VOLTAGES ON MCP

void set_mcp_A(){
  
  while (Serial.available() <= 0){
    delay(5);
  }

  int voltage = Serial.readString().toInt();
  
  delay(10);

  mcp.setChannelValue(MCP4728_CHANNEL_A, voltage);

}

void set_mcp_B(){
  
  while (Serial.available() <= 0){
    delay(5);
  }

  int voltage = Serial.parseInt();
  
  delay(10);

  mcp.setChannelValue(MCP4728_CHANNEL_B, voltage);
}

void set_mcp_C(){
  
  while (Serial.available() <= 0){
    delay(5);
  }

  int voltage = Serial.parseInt();
  
  delay(10);

  mcp.setChannelValue(MCP4728_CHANNEL_C, voltage);
}


void set_mcp_D(){
  
  while (Serial.available() <= 0){
    delay(5);
  }

  int voltage = Serial.parseInt();
  
  delay(10);

  mcp.setChannelValue(MCP4728_CHANNEL_D, voltage);
}

// HANDSHAKE

void handshake() {
  // initialize the handshake with MATLAB
  Serial.print('a');
  char a = 'b';
  // handshake has to come back from the serial port
  while (a != 'a') {
    a = Serial.read();
    delay(500);
  }
  
}

//FLUSH LEFT OVER BYTES

void serialFlush(int bytesToFlush){
  while(bytesToFlush-- > 0) {
    char t = Serial.read();
    delay(1);
  }
}

void inputSwitch(char input){
  switch(input) {
   // ONLY FOR HANDSHAKE
    case '+':
       Serial.write('a');

    
    case 'b':
      Serial.println(readPressure_SICK_1());
      break;
    case 'c':
      Serial.println(readPressure_SICK_2());
      break;
    case 'd':
      Serial.println(readPressure_SICK_3());
      break;

    case 'f':
      Serial.println(readMassflow_1());
      break;
    case 'g':
      Serial.println(readMassflow_2());
      break;
    case 'h':
      Serial.println(readMassflow_3());
      break;
    case 'i':
      Serial.println(readMassflow_4());
      break;
    
    
    case 'q':
      Serial.write(check_LevelSwitch_1());
      
      break;
    case 'r':
      Serial.write(check_LevelSwitch_2());

      break;
    case 's':
      Serial.write(check_LevelSwitch_3());

      break;
    case 't':
      Serial.write(check_LevelSwitch_4());

      break;

      
    case 'F':
      set_HIGH_TWV_1();
      Serial.write('+');
      break;


      
    case 'L':
      set_LOW_TWV_1();
      Serial.write('+');

      break;

      
 
    case 'T':
      OPEN_OCV_NO_3();
      Serial.write('+');

      break;
    case 'U':
      OPEN_OCV_NC_4();
      Serial.write('+');

      break;


      

    case 'X':
      CLOSE_OCV_NO_3();
      Serial.write('+');

      break;
    case 'Y':
      CLOSE_OCV_NC_4();
      Serial.write('+');

      break;


      
    case '!':
      set_mcp_A();
      Serial.write('+');
      
      break;
    case '@':
      set_mcp_B();
      Serial.write('+');

      break;
    case '#':
      set_mcp_C();
      Serial.write('+');

      break;
    case '$':
      set_mcp_D();
      Serial.write('+');

      break;

      
    case '%':
      PUMP_1_ON();
      Serial.write('+');
      break;
    case '^':
      PUMP_1_OFF();
      Serial.write('+');

      break;


      
    case '&':
      PUMP_2_ON();
      Serial.write('+');

      break;
    case '*':
      PUMP_2_OFF();
      Serial.write('+');

      break;
      
   default: Serial.write('-');
  }
}