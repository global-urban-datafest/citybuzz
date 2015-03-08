/*
 CITYBUZZ
 Based on Arduino LiquidCrystal Library example code
 
  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 */

//Libraries
#include <stdio.h>
#include <LiquidCrystal.h>
#include <SPI.h>
//#include <SD.h>

// set pin numbers:
const int greenButton = 8;     // the number of the pushbutton pin
const int redButton = 7;     // the number of the pushbutton pin

int greenButtonState = 0; 
int redButtonState = 0; 
int result = 0;

//Question vars
char questionId[26];
char questionStr1[17];
char questionStr2[17];
   
//Semaphore
boolean ongoing = false;
  
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {

/*  
    //Initialize serial and wait for port to open:
  Serial.begin(9600); 
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
*/
  
  //Setup buttons
  pinMode(greenButton, INPUT);     
  pinMode(redButton, INPUT);     
  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("CITY BUZZ       ");
       
  //SD setup
  //SD.begin();
  //Serial.println("Begin arduino code");
  
  //REQUEST QUESTION TO SERVER
   result = system("/home/root/citybuzz/getQuestion.py > /home/root/citybuzz/question");
   //delay(500);
   if (result == 0) {
              
      //READ THE QUESTION
      FILE *fp;
      char resultStr[16];
      char * line = NULL;
      size_t len = 0;
      ssize_t read;

      fp = fopen("/home/root/citybuzz/question" , "r");
       if(fp == NULL) {
          //Error opening file
          lcd.setCursor(0, 1);
          lcd.print("System error   ");
       } else {          
         int i = 0;
         while (i < 3) {
            if (i == 0) {
              read = getline(&line, &len, fp);
              strncpy(questionId, line, 25);
              questionId[read - 1] = '\0';
            } else if (i == 1) {
              read = getline(&line, &len, fp);
              //lcd.setCursor(0, 0);
              //lcd.print(line);
              //delay(50);
              strncpy(questionStr1, line, 16);
              questionStr1[read - 1] = '\0';
              //delay(50);
            } else if (i == 2) {
              read = getline(&line, &len, fp);
//              lcd.setCursor(0, 1);
//              lcd.print(line2);
              strncpy(questionStr2, line, 16);
              questionStr2[read - 1] = '\0';
            }
            i++;
         }
         lcd.setCursor(0, 0);
         lcd.print(questionStr1);
         lcd.setCursor(0, 1);
         lcd.print(questionStr2);
         fclose(fp);
       }
      

   } else {
       lcd.setCursor(0, 1);
       lcd.print("Network error");
   }
}

void loop() {
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  //lcd.setCursor(0, 1);
  // print the number of seconds since reset:
  //lcd.print(millis()/1000);
  
  greenButtonState = digitalRead(greenButton);
  redButtonState = digitalRead(redButton);
  
  //GREEN BUTTON
  if (!ongoing) {
    if (greenButtonState == HIGH) {     
      ongoing = true;
      lcd.setCursor(0, 0);
      lcd.print("CITY BUZZ       ");
      lcd.setCursor(0, 1);
      // print the number of seconds since reset:
      lcd.print("Sending YES...  ");
      char command[170];
      strcpy(command, "/home/root/citybuzz/sendResponse.py ");
      strcat(command, questionId);
      strcat(command, " 1");
      result = system(command);
      //result = system("/home/root/citybuzz/sendResponse.py " + questionId + " 1");
      if (result == 0) {
            lcd.setCursor(0, 1);
            lcd.print("YES Sent!       ");
      } else {
            lcd.setCursor(0, 1);
            lcd.print("Network error   ");
      }
      delay(2000);               // wait for a second
      ongoing = false;
      lcd.clear();
      
    } else if (redButtonState == HIGH) {     
      ongoing = true;
      lcd.setCursor(0, 0);
      lcd.print("CITY BUZZ       ");
      lcd.setCursor(0, 1);
      // print the number of seconds since reset:
      lcd.print("Sending NO...   ");
      char command[170];
      strcpy(command, "/home/root/citybuzz/sendResponse.py ");
      strcat(command, questionId);
      strcat(command, " 0");
      result = system(command);
      //result = system("/home/root/citybuzz/sendResponse.py " + questionId + " 0");
      if (result == 0) {
            lcd.setCursor(0, 1);
            lcd.print("NO Sent!       ");
      } else {
            lcd.setCursor(0, 1);
            lcd.print("Network error   ");
      }
      delay(2000);               // wait for a second
      ongoing = false;
      lcd.clear();
    } 
    else {
         lcd.setCursor(0, 0);
         lcd.print(questionStr1);
         lcd.setCursor(0, 1);
         lcd.print(questionStr2);
    }
  }
}
