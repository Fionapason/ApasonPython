 /* ARDUINO CODE FOR EB 1 WHICH MEANS FOR ELECTRO DIALYSIS!!!
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
#define P_GEMS A0
#define P_SICK_1 A1
#define P_SICK_2 A2
#define P_SICK_3 A3
#define P_SICK_4 A4

#define P_SICK_15 A15

// MASSFLOW SENSORS
#define MF_1 A5
#define MF_2 A6
#define MF_3 A7
#define MF_4 A8

// CONDUCTIVITY SENSORS

#define C_MT_1 A9
#define C_MT_2 A10
#define C_MT_3 A11

// TEMPERATURE SENSORS

#define T_MT_1 A12
#define T_MT_2 A13
#define T_MT_3 A14


// LEVEL SWITCHES (INPUT PINS)

#define LS_1 22
#define LS_2 23
#define LS_3 24
#define LS_4 25
#define LS_5 26
#define LS_6 27
#define LS_7 28
#define LS_8 29
#define LS_9 30
#define LS_10 31
#define LS_11 32

// THREE WAY VALVES

#define TWV_1 38
#define TWV_2 39
#define TWV_3 40
#define TWV_4 41


// OPEN CLOSE VALVES

#define OCV_NC_1 44 // normally closed


// PUMP ON/OFF

//#define PUMP_1 48
//#define PUMP_2 49
//#define PUMP_3 50

// ED POLARITY
#define ED_POLARITY_Plus 50
#define ED_POLARITY_Minus 51

// Connection between ED and UF

#define UFConnection 52

void handshake();

void serialFlush(int bytesToFlush);

void inputSwitch(char input);

int readPressure_GEMS();
int readPressure_SICK_1();
int readPressure_SICK_2();
int readPressure_SICK_3();
int readPressure_SICK_4();

int readPressure_SICK_15();

int readMassflow_1();
int readMassflow_2();
int readMassflow_3();
int readMassflow_4();

int readConductivity_1();
int readConductivity_2();
int readConductivity_3();

int readTemperature_MT_1();
int readTemperature_MT_2();
int readTemperature_MT_3();


char check_LevelSwitch_1();
char check_LevelSwitch_2();
char check_LevelSwitch_3();
char check_LevelSwitch_4();
char check_LevelSwitch_5();
char check_LevelSwitch_6();
char check_LevelSwitch_7();
char check_LevelSwitch_8();
char check_LevelSwitch_9();
char check_LevelSwitch_10();
char check_LevelSwitch_11();


void set_HIGH_TWV_1(); 
void set_HIGH_TWV_2();
void set_HIGH_TWV_3();
void set_HIGH_TWV_4();

void set_LOW_TWV_1();
void set_LOW_TWV_2();
void set_LOW_TWV_3();
void set_LOW_TWV_4();

void OPEN_OCV_NC_1();

void CLOSE_OCV_NO_1();


void set_mcp_A();
void set_mcp_B();
void set_mcp_C();
void set_mcp_D();

void ED_Polarity_Pos();
void ED_Polarity_Neg();
void ED_Polarity_Off();

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
  pinMode(TWV_2, OUTPUT);
  pinMode(TWV_3, OUTPUT);
  pinMode(TWV_4, OUTPUT);

  pinMode(OCV_NC_1, OUTPUT);

  pinMode(ED_POLARITY_Plus, OUTPUT);
  pinMode(ED_POLARITY_Minus, OUTPUT);

  pinMode(UFConnection, INPUT);

  ED_Polarity_Off();

  CLOSE_OCV_NC_1();
  
  Serial.print('+');
   
}

void loop() {

     while (Serial.available() <= 0);
     
     char input = Serial.read();
    
     delay(2);
     
     int nextBytes = Serial.available();
    
     serialFlush(nextBytes);
    
     inputSwitch(input);
     
     nextBytes = Serial.available();
     serialFlush(nextBytes);
      
     Serial.write('\n');

}


// PRESSURE READ FUNCTIONS

int readPressure_GEMS(){
  return analogRead(P_GEMS);
}

int readPressure_SICK_1(){
  return analogRead(P_SICK_1);
}

int readPressure_SICK_2(){
  return analogRead(P_SICK_2);
}

int readPressure_SICK_3(){
  return analogRead(P_SICK_3);
}

int readPressure_SICK_4(){
  return analogRead(P_SICK_4);
}

int readPressure_SICK_15(){
  return analogRead(P_SICK_15);
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


// CONDUCTIVITY READ FUNCTIONS

int readConductivity_1(){
  return analogRead(C_MT_1);
}

int readConductivity_2(){
  return analogRead(C_MT_2);
}

int readConductivity_3(){
  return analogRead(C_MT_3);
}

// TEMPERATURE READ FUNCTIONS

int readTemperature_MT_1(){
  return analogRead(T_MT_1);
}

int readTemperature_MT_2(){
  return analogRead(T_MT_2);
}

int readTemperature_MT_3(){
  return analogRead(T_MT_3);
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

char check_LevelSwitch_5(){
  if (digitalRead(LS_5) == HIGH) {
    return '1';
  } else return '0';
}

char check_LevelSwitch_6(){
  if (digitalRead(LS_6) == HIGH) {
    return '1';
  } else return '0';
}

char check_LevelSwitch_7(){
  if (digitalRead(LS_7) == HIGH) {
    return '1';
  } else return '0';
}


char check_LevelSwitch_8(){
  if (digitalRead(LS_8) == HIGH) {
    return '1';
  } else return '0';
}

char check_LevelSwitch_9(){
  if (digitalRead(LS_9) == HIGH) {
    return '1';
  } else return '0';
}

char check_LevelSwitch_10(){
  if (digitalRead(LS_10) == HIGH) {
    return '1';
  } else return '0';
}

char check_LevelSwitch_11(){
  if (digitalRead(LS_11) == HIGH) {
    return '1';
  } else return '0';
}


// THREE WAY VALVE SET HIGH --> LOW LEVEL TRIGGER ON RELAY BOARD!!

void set_HIGH_TWV_1(){
  digitalWrite(TWV_1, LOW);
}
 
void set_HIGH_TWV_2(){
  digitalWrite(TWV_2, LOW);
}

void set_HIGH_TWV_3(){
  digitalWrite(TWV_3, LOW);
}

void set_HIGH_TWV_4(){
  digitalWrite(TWV_4, LOW);
}


// THREE WAY VALVE SET LOW

void set_LOW_TWV_1(){
  digitalWrite(TWV_1, HIGH);
}
 
void set_LOW_TWV_2(){
  digitalWrite(TWV_2, HIGH);
}

void set_LOW_TWV_3(){
  digitalWrite(TWV_3, HIGH);
}

void set_LOW_TWV_4(){
  digitalWrite(TWV_4, HIGH);
}


// OPEN OPEN CLOSE VALVES


void OPEN_OCV_NC_1(){
  digitalWrite(OCV_NC_1, LOW);
}


// CLOSE OPEN CLOSE VALVES

void CLOSE_OCV_NC_1(){
  digitalWrite(OCV_NC_1, HIGH);
}


// ED POLARITY IN POSITIVE DIRECTION

void ED_Polarity_Pos(){
  digitalWrite(ED_POLARITY_Plus, LOW);
  digitalWrite(ED_POLARITY_Minus, HIGH);
}

// ED POLARITY IN NEGATIVE DIRECTION

void ED_Polarity_Neg(){
  digitalWrite(ED_POLARITY_Plus, HIGH);
  digitalWrite(ED_POLARITY_Minus, LOW);
}

// ED POLARITY TURN OFF

void ED_Polarity_Off(){
  digitalWrite(ED_POLARITY_Plus, HIGH);
  digitalWrite(ED_POLARITY_Minus, HIGH);
}

// SET VOLTAGES ON MCP

void set_mcp_A(){
  
  while (Serial.available() <= 0){
    delay(5);
  }

  int voltage = Serial.parseInt();
  
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
        break;
    
    case 'a':
       Serial.println(readPressure_GEMS());
       break;
       
    case 'b':
      Serial.println(readPressure_SICK_1());
      break;
      
    case 'c':
      Serial.println(readPressure_SICK_2());
      break;
      
    case 'd':
      Serial.println(readPressure_SICK_3());
      break;
      
    case 'e':
      Serial.println(readPressure_SICK_4());
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

    
    case 'j':
      Serial.println(readConductivity_1());
      break;
      
    case 'k':
      Serial.println(readConductivity_2());
      break;
      
    case 'l':
      Serial.println(readConductivity_3());
      break;

    
    case 'm':
      Serial.println(readTemperature_MT_1());
      break;
      
    case 'n':
      Serial.println(readTemperature_MT_2());
      break;
      
    case 'o':
      Serial.println(readTemperature_MT_3());
      break;
    
    
    case 'p':
       Serial.println(readPressure_SICK_15());
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
      
    case 'u':
      Serial.write(check_LevelSwitch_5());
      break;
      
    case 'v':
      Serial.write(check_LevelSwitch_6());
      break;
      
    case 'w':
      Serial.write(check_LevelSwitch_7());
      break;
      
    case 'x':
      Serial.write(check_LevelSwitch_8());
      break;
      
    case 'y':
      Serial.write(check_LevelSwitch_9());
      break;
      
    case 'z':
      Serial.write(check_LevelSwitch_10());
      break;
      
    case 'A':
      Serial.write(check_LevelSwitch_11());
      break;


      
    case 'F':
      set_HIGH_TWV_1();
      Serial.write('+');
      break;
      
    case 'G':
      set_HIGH_TWV_2();
      Serial.write('+');
      break;
      
    case 'H':
      set_HIGH_TWV_3();
      Serial.write('+');
      break;
      
    case 'I':
      set_HIGH_TWV_4();
      Serial.write('+');
      break;



      
    case 'L':
      set_LOW_TWV_1();
      Serial.write('+');
      break;
      
    case 'M':
      set_LOW_TWV_2();
      Serial.write('+');
      break;
      
    case 'N':
      set_LOW_TWV_3();
      Serial.write('+');
      break;
      
    case 'O':
      set_LOW_TWV_4();
      Serial.write('+');
      break;



      
    case 'R':
      OPEN_OCV_NC_1();
      Serial.write('+');
      break;



      
    case 'V':
      CLOSE_OCV_NC_1();
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
    
    case '(':
      ED_Polarity_Pos();
      Serial.write('+');
      break;

    case ')':
       ED_Polarity_Neg();
       Serial.write('+');
       break;

     case '*':
      ED_Polarity_Off();
      Serial.write('+');
      break;

    case '[':
      Serial.print(digitalRead(UFConnection));

      break;
      
   default: Serial.write('-');
  }
}
