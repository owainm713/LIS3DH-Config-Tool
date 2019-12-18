//LIS3DH-Arduino, program to practice using an LIS3DH accelerometer
// with Arduino

// Note the following connections are from an Arduino UNO to an
// LIS3DH on an Adafruit breakout board which has level shifting
// so 5V connections are ok. If you are not using a breakout board, alternate
// level shifting will be required if you are using a 5V logic microcontroller.
// Arduino SDA - LIS3DH SDA
// Arduino SCL - LIS3DH SCL
// 5V - LIS3DH SD0
// 5V - LIS3DH CS
// Arduino Gnd - LIS3DH Gnd
// Arduino Pin 9 - LIS3DH INT1
// Connect LED & resistor to LIS3DH Int to see when the interrupt occurs
// Interrupt is set to Active High

//created December 16, 2019
//modified December 16, 2019

#include <Wire.h>  // include i2c module

uint8_t addr = 0x19;  // i2c address of the LIS3DH
int intPin = 9;

int single_access_read(uint8_t regAddr){
  //single_access_read, function to read a single data register
  
  int reading = 0;    
  Wire.beginTransmission(addr);
  Wire.write(regAddr);
  Wire.endTransmission();
  delay(70);
  Wire.requestFrom(addr,1);
  while(Wire.available()){
    reading=Wire.read();    
  }
  return reading;   
}

void single_access_write(uint8_t regAddr, uint8_t regValue){
  //single_access_write, function to write to a single register 

  Wire.beginTransmission(addr);
  Wire.write(regAddr);
  Wire.write(regValue);
  Wire.endTransmission();
  return;  
}

void multiple_access_read(uint8_t regAddr, uint8_t numReg, int *data){
  //multiple_access_read, function to read a multiple data registers
  //data is a pointer pointing to an array to place the return data

  //cmdbit = 1 indicates  multiple reads of consecutive registers
  //cmdbit = 0 indicates  multiple reads of the same register
  uint8_t cmdBit = 0b1;  
  uint8_t cmd = (cmdBit<<7)+regAddr;  
    
  Wire.beginTransmission(addr);
  Wire.write(cmd);
  Wire.endTransmission();
  delay(70);
  Wire.requestFrom(addr,numReg);
  
  while(Wire.available()){
    *data=Wire.read();  //*data used, pointer rules
    //Serial.println(*data);  // for testing
    *(data++);    //incrementing the memory location *data points to, i.e. next array item
  }
  return;   
}

void multiple_access_write(uint8_t regAddr, uint8_t numReg, int data[]){
  //multiple_access_write, function to write to multiple data registers
  //data is an array with the values to write

  //cmdbit = 1 indicates  multiple reads of consecutive registers
  //cmdbit = 0 indicates  multiple reads of the same register
  uint8_t cmdBit = 0b1; 
  uint8_t cmd = (cmdBit<<7)+regAddr;

  Wire.beginTransmission(addr);
  Wire.write(cmd);
  for(int i=0; i<numReg; i++){
    Wire.write(data[i]);
  }
  Wire.endTransmission();
  return;  

}

int number_conversion(uint8_t lsb, uint8_t msb){
  //function to convert the raw LIS3DH output data from
  //2 unsigned integers to a single signed integer
  //Arduino handles the twos complement stuff automatically
  
  int x;  // variable to hold the converted value
  
  x = (msb<<8) + lsb;   
  x = x>>6;
    
  return x;  
}

void read_set_up(){
  // print off values in various control registers

  //CTRL_REG x6 Read

  int reading[6];
  multiple_access_read(0x20,6, reading);  //being an array "reading" is by default a pointer so "&" not required in front
  
  for(int i=0; i<6; i++){
    Serial.print(reading[i]);
    Serial.print(" ");
  }
  Serial.println(" "); 

  //INT1_CGF etc read
  Serial.print(single_access_read(0x30));
  Serial.print(" ");
  Serial.print(single_access_read(0x32));
  Serial.print(" ");
  Serial.println(single_access_read(0x33));

  //CLICK_CFG etc Read
  Serial.println(single_access_read(0x38));
  multiple_access_read(0x3A,4, reading);  
  
  for(int i=0; i<4; i++){
    Serial.print(reading[i]);
    Serial.print(" ");
  }
  Serial.println(" ");
}

void single_click_setup(){

  //set up control registers
  //CTRL_REG1 = 0x44
  //CTRL_REG2 = 0x00 High pass filter settings
  //CTRL_REG3 = 0x80 Interrupt setting - Click Interrupt
  //CTRL_REG4 = 0x80 BDU, +/- 2g
  //CTRL_REG5 = 0x00 Fifo, Latch interrupt settings
  //CTRL_REG6 = 0x00 More interrupt settings  

  int regData[]={0x44,0x00,0x80,0x80,0x00,0x00};
  multiple_access_write(0x20,6,regData);

  //CLICK_CFG = 0x10 - ZS
  //CLICK_THS = 0x44 - 1088mg
  //TIME_LIMIT = 0x06 - 120ms
  //TIME_LATENCY = 0x10 - 320ms
  //TIME_WINDOW = 0x00 - 0ms

  single_access_write(0x38, 0x10);
  int regData2[4] = {0x44, 0x06, 0x10,0x00};
  multiple_access_write(0x3A,4,regData2);
  
}

void setup() {
  // set up interrupt pin
  pinMode(intPin, INPUT);
  
  // set up i2c connection and serial connection
  Serial.begin(9600); // for testing
  Wire.begin(); 
  Serial.println(single_access_read(0x0F)); // check whoami register, should equal 0x33 or 51

  single_click_setup(); 
  read_set_up(); 

}

void loop() {
  // put your main code here, to run repeatedly:
  //uint8_t zH = single_access_read(0x2D);
  //uint8_t zL = single_access_read(0x2C);

  //Serial.println(number_conversion(zL, zH));

  //Print out CLICK_SRC register - Click Status  
  if(digitalRead(intPin) == 1){
    uint8_t intStatus = single_access_read(0x39);
    Serial.println(intStatus);    
  }

  delay(250);

}
