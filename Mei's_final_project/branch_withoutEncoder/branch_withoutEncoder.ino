#include <SPI.h>
#include <MFRC522.h>     // 引用程式庫

#define LED1  3
#define LED2  4
#define LED3  8
#define LED4  9
#define LED5  A1

#define RST_PIN      A0        // 讀卡機的重置腳位
#define SS_PIN       10        // 晶片選擇腳位

#define SERIAL_BAUDRATE 9600
#define CLK_PIN 2 // 定義連接腳位
#define DT_PIN 3
#define SW_PIN 4

#define interruptA 0 // UNO腳位2是interrupt 0，其他板子請見官方網頁

#include "Adafruit_Thermal.h"
#include "logo.h"
#include "adaqrcode.h"

// Here's the new syntax when using SoftwareSerial (e.g. Arduino Uno) ----
// If using hardware serial instead, comment out or remove these lines:

#include "SoftwareSerial.h"
#define TX_PIN 6 // Arduino transmit  GREEN WIRE  labeled RX on printer
#define RX_PIN 5 // Arduino receive   YRLLOW WIRE   labeled TX on printer

SoftwareSerial mySerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);     // Pass addr to printer constructor

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define I2C_ADDR    0x27  // Define I2C Address where the PCF8574A is
                          // Address can be changed by soldering A0, A1, or A2
                          // Default is 0x27

// map the pin configuration of LCD backpack for the LiquidCristal class
#define BACKLIGHT_PIN 3
#define En_pin  2
#define Rw_pin  1
#define Rs_pin  0
#define D4_pin  4
#define D5_pin  5
#define D6_pin  6
#define D7_pin  7

#define Enter  2
#define Return  7

LiquidCrystal_I2C lcd(I2C_ADDR,
                      En_pin,Rw_pin,Rs_pin,D4_pin,D5_pin,D6_pin,D7_pin,
                      BACKLIGHT_PIN, POSITIVE);

String todays_date = "22 MAY 2020";
String exchange_rate = "1 : 0.00128";

int randomRole = 0;
unsigned long t = 0;

String currentID;
int role = 999;
int roleA = 0;
int roleB = 1;
int roleC = 2;

int home_flag = 0;
int stranger_flag = 0;

MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件

void setup() {
  randomSeed(analogRead(1));
  pinMode(LED1, OUTPUT); digitalWrite(LED1, HIGH);
  pinMode(LED2, OUTPUT); digitalWrite(LED2, LOW);
  pinMode(LED3, OUTPUT); digitalWrite(LED3, LOW);
  pinMode(LED4, OUTPUT); digitalWrite(LED4, LOW);
  pinMode(LED5, OUTPUT); digitalWrite(LED5, LOW);

  pinMode(Enter, INPUT_PULLUP);
  pinMode(Return, INPUT_PULLUP);

  // NOTE: SOME PRINTERS NEED 9600 BAUD instead of 19200, check test page.
  mySerial.begin(9600);  // Initialize SoftwareSerial
  //Serial1.begin(19200); // Use this instead if using hardware serial
  printer.begin();        // Init printer (same regardless of serial type)
  Serial.begin(SERIAL_BAUDRATE);
  // 當狀態下降時，代表旋轉編碼器被轉動了
  Serial.print("Begin!\n");

  Serial.println("RFID reader is ready!");

  SPI.begin();
  mfrc522.PCD_Init();   // 初始化MFRC522讀卡機模組 

  ///////////////////LCD///////////////////
  lcd.begin(20,4);        // 20 columns by 4 rows on display
  lcd.setBacklight(HIGH); // Turn on backlight, LOW for off
}

void loop() {
  if (home_flag == 0){
    status_sign('a');
    lcd.clear();
    lcd.setCursor ( 0, 1 );            // go to the 2nd row
    lcd.print("Welcome! Please scan"); // pad string with spaces for centering
    lcd.setCursor ( 0, 2 );            // go to the third row
    lcd.print("   your passport!"); // pad with spaces for centering
    home_flag = 1;
  }
  readRFID();
}

void readRFID(){
      // 確認是否有新卡片
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      home_flag = 0;
      stranger_flag = 0;
      currentID = "";
      lcd.clear();
      lcd.setCursor ( 0, 1 );
      lcd.print("    Loading");
      delay(500);
      for( int i = 11; i < 16 ; i++ ){
        lcd.setCursor ( i, 1 );
        lcd.print(".");
        delay(500);
      }
      delay(2000);

      byte *id = mfrc522.uid.uidByte;   // 取得卡片的UID
      byte idSize = mfrc522.uid.size;   // 取得UID的長度

      Serial.print("PICC type: ");      // 顯示卡片類型
      // 根據卡片回應的SAK值（mfrc522.uid.sak）判斷卡片類型
      MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
      Serial.println(mfrc522.PICC_GetTypeName(piccType));

      Serial.print("UID Size: ");       // 顯示卡片的UID長度值
      Serial.println(idSize);
 
      for (byte i = 0; i < idSize; i++) {  // 逐一顯示UID碼
        Serial.print("id[");
        Serial.print(i);
        Serial.print("]: ");
        Serial.println(id[i], HEX);       // 以16進位顯示UID值
        currentID += id[i];
      }
      Serial.println();
      Serial.print("currentID: #A");
      Serial.println(currentID);

      status_sign('b');
      lcd.clear();
      lcd.setCursor ( 0, 0 );
      lcd.print("  ID: #A");
      lcd.setCursor ( 8, 0 );
      lcd.print(currentID);
      lcd.setCursor ( 0, 3 );
      lcd.print("   Return/Comfirm");

      checkIdentity(currentID);
      
      mfrc522.PICC_HaltA();  // 讓卡片進入停止模式

      while (digitalRead(Enter) == HIGH){
        if (digitalRead(Return) == LOW or stranger_flag == 1){
          return ;
        }
      }
      while (digitalRead(Enter) == LOW){}

      lcd.clear();
      lcd.setCursor ( 0, 1 );
      lcd.print("Please look at the");
      lcd.setCursor ( 0, 2 );
      lcd.print("camera!");
      delay(2000);

      
      for( int j = 0; j < 3; j++ ){
        lcd.clear();
        lcd.setCursor ( 0, 1 );
        lcd.print("   Verifying");
        delay(500);
        for( int i = 12; i < 17 ; i++ ){
          lcd.setCursor ( i, 1 );
          lcd.print(".");
          delay(500);
        }
      }
      delay(500);

      changeRole(); 
      printOut(todays_date, exchange_rate, currentID, role, randomRole);
    } 
}

void checkIdentity(String currentID){
  if (currentID == "912112428"){
      role = roleA;
      Serial.print("Last role: ");
      Serial.println(role);

      //lcd.setCursor ( 0, 1 );
      //lcd.print("Now role: ");
      //lcd.setCursor ( 10, 1 );
      //lcd.print(role);
  }
  else if (currentID == "9015113522"){
      role = roleB;
      Serial.print("Last role: ");
      Serial.println(role);

      //lcd.setCursor ( 0, 1 );
      //lcd.print("Now role: ");
      //lcd.setCursor ( 10, 1 );
      //lcd.print(role);
      //lcd.setCursor ( 0, 2 );
      //lcd.print(" ");
  }
  else if (currentID == "24512017399"){
      role = roleC;
      Serial.print("Last role: ");
      Serial.println(role);
  }
  else{
    stranger_flag = 1;
    Serial.println("Loggin deny!");
    lcd.clear();
    lcd.setCursor ( 0, 0 );
    lcd.print("Login denied!");
    lcd.setCursor ( 0, 1 );
    lcd.print("Please contact Mei");
    lcd.setCursor ( 0, 2 );
    lcd.print("if you need the");
    lcd.setCursor ( 0, 3 );
    lcd.print("authority!");
    delay(5000);
  }
}

void changeRole(){
     status_sign('c');
     Serial.print("Change from role ");

     lcd.clear();
     lcd.setCursor ( 0, 0 );
     lcd.print(" Verification pass!");
     lcd.setCursor ( 0, 1 );
     lcd.print("Switch to zone #");
     
     getRandomRole();
     lcd.setCursor ( 16, 1 );
     lcd.print(randomRole);
     lcd.setCursor ( 0, 2 );
     lcd.print("   Return/Comfirm");

     while (digitalRead(Enter) == HIGH){
       if (digitalRead(Return) == LOW){
          getRandomRole();
          lcd.setCursor ( 16, 1 );
          lcd.print(randomRole);
          lcd.setCursor ( 0, 2 );
          lcd.print("   Return/Comfirm");
          delay(500);
       }
     }

     if (currentID == "912112428"){
      Serial.print(roleA);
      roleA = randomRole;
    }
     else if (currentID == "9015113522"){
      Serial.print(roleB);
      roleB = randomRole;
    }
     else if (currentID == "24512017399"){
      Serial.print(roleC);
      roleC = randomRole;
     }

    Serial.print(" to ");
    Serial.println(randomRole);
    Serial.print("\nNow role: ");
    Serial.println(randomRole);

    mfrc522.PICC_HaltA();  // 讓卡片進入停止模式
    delay(100);

    for( int j = 0; j < 3; j++ ){
      lcd.clear();
      lcd.setCursor ( 0, 1 );
      lcd.print("Switching to zone #"); 
      lcd.setCursor ( 19, 1 );
      lcd.print(randomRole); 
      lcd.setCursor ( 0, 2 );
      lcd.print("  please wait"); 
      delay(500);
      for( int i = 13; i < 18 ; i++ ){
        lcd.setCursor ( i, 2 );
        lcd.print(".");
        delay(500);
      }
    }
    Serial.println("### changeRole Out ###");
    delay(1000);
}

void printOut(String todays_date, String exchange_rate, String currentID, int role, int randomRole){
  lcd.clear();
  lcd.setCursor ( 0, 1 );
  lcd.print("  Switch complete!"); 
  delay(2000);
  lcd.setCursor ( 0, 2 );
  delay(500);
  status_sign('d');
  lcd.print("  List printing"); 
  delay(500);
  for( int i = 15; i < 18 ; i++ ){
    lcd.setCursor ( i, 2 );
    lcd.print(".");
    delay(500);
  }
  delay(2000);

  ///////////////////////////////////////////////////////////////////////
  printer.justify('C');

  printer.doubleHeightOn();
  printer.println(F("TIME UNIT EXCHANGER"));
  printer.doubleHeightOff();

  printer.feed(1);

  printer.boldOn();
  printer.print(F("Date: "));
  printer.println(todays_date);
  printer.boldOff();

  printer.feed(1);

  printer.underlineOn();
  printer.println(F("INFORMATION"));
  printer.underlineOff();

  printer.feed(1);

  printer.print(F("Personal ID Number:#A"));
  printer.println(currentID);
  printer.print(F("Passport Number:"));
  printer.println(currentID.toInt() + 1144);
  printer.print(F("Zone:"));
  printer.println(role);

  printer.feed(1);

  printer.setSize('L');
  printer.print(F("SWITCH TO ZONE "));
  printer.println(randomRole);
  printer.setSize('S');
  printer.inverseOn();
  printer.print(F("exchange rate"));
  printer.inverseOff();
  printer.print(F(" "));
  printer.println(exchange_rate);
  printer.print(F("Current zone "));
  printer.println(randomRole);

  printer.feed(1);

  printer.underlineOn();
  printer.println(F("MORE DETAILS"));
  printer.underlineOff();
  printer.setBarcodeHeight(100);
  // Print UPC line on product barcodes:
  printer.printBarcode("123456789123", UPC_A);

  printer.feed(1);

  printer.printBitmap(adalogo_width, adalogo_height, adalogo_data);

  printer.feed(1);

  printer.printBitmap(adaqrcode_width, adaqrcode_height, adaqrcode_data);
  printer.feed(1);
  printer.println(F("www.itueo.com"));

  // printer.println(print_data);
  
  printer.feed(2);

  printer.sleep();      // Tell printer to sleep
  delay(3000L);         // Sleep for 3 seconds
  printer.wake();       // MUST wake() before printing again, even if reset
  printer.setDefault(); // Restore printer to defaults

  role = 999;
  currentID = "";

  status_sign('e');
  lcd.clear();
  lcd.setCursor ( 0, 1 );
  lcd.print("Print out complete!");
  delay(3000);
}

void getRandomRole(){
  randomRole = random(0,4);
  if (currentID == "912112428"){
    while (randomRole == roleA){
      randomRole = random(0,4);
    }
  }
  else if (currentID == "9015113522"){
    while (randomRole == roleB){
      randomRole = random(0,4);
    }
  }
  else if (currentID == "24512017399"){
    while (randomRole == roleC){
      randomRole = random(0,4);
    }
  }
}

void status_sign(char sign){
  switch(sign){
    case 'a':
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, LOW);
      digitalWrite(LED4, LOW);
      digitalWrite(LED5, LOW);
      break;
    case 'b':
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, HIGH);
      digitalWrite(LED3, LOW);
      digitalWrite(LED4, LOW);
      digitalWrite(LED5, LOW);
      break;
    case 'c':
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, HIGH);
      digitalWrite(LED4, LOW);
      digitalWrite(LED5, LOW);
      break;
    case 'd':
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, LOW);
      digitalWrite(LED4, HIGH);
      digitalWrite(LED5, LOW);
      break;
    case 'e':
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, LOW);
      digitalWrite(LED4, LOW);
      digitalWrite(LED5, HIGH);
      break;
  }
}