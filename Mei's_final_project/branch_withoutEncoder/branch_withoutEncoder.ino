#include <SPI.h>
#include <MFRC522.h>     // 引用程式庫

#define RST_PIN      A0        // 讀卡機的重置腳位
#define SS_PIN       10        // 晶片選擇腳位

#define SERIAL_BAUDRATE 9600
#define CLK_PIN 2 // 定義連接腳位
#define DT_PIN 3
#define SW_PIN 4

#define interruptA 0 // UNO腳位2是interrupt 0，其他板子請見官方網頁

#include "Adafruit_Thermal.h"
#include "adalogo.h"
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

int randomRole = 0;
unsigned long t = 0;

String currentID;
int role = 999;
int roleA = 0;
int roleB = 1;

int home_flag = 0;
int stranger_flag = 0;

String print_list = "";
String print_list_checkID = "";
String print_list_change = "";

MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件

void setup() {
  randomSeed(analogRead(1));
  pinMode(7, OUTPUT); digitalWrite(7, LOW);

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
    lcd.clear();
    lcd.setCursor ( 0, 0 );            // go to the top left corner
    lcd.print("    Mei's project   "); // write this string on the top row
    lcd.setCursor ( 0, 1 );            // go to the 2nd row
    lcd.print("RFID reader's ready!"); // pad string with spaces for centering
    lcd.setCursor ( 0, 2 );            // go to the third row
    lcd.print("Please swipe the    "); // pad with spaces for centering
    lcd.setCursor ( 0, 3 );            // go to the fourth row
    lcd.print("card to activate!...");
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
      print_list = "";
      print_list_checkID = "";
      lcd.clear();
      lcd.setCursor ( 0, 0 );
      lcd.print("Loading");
      delay(500);
      for( int i = 7; i < 13 ; i++ ){
        lcd.setCursor ( i, 0 );
        lcd.print(".");
        delay(500);
      }

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
      Serial.print("currentID: ");
      Serial.println(currentID);

      lcd.clear();
      lcd.setCursor ( 0, 0 );
      lcd.print("currentID: ");
      lcd.setCursor ( 11, 0 );
      lcd.print(currentID);
      lcd.setCursor ( 0, 3 );
      lcd.print("Comfirm       Return");

      print_list += "currentID: " + String(currentID) + "\n";

      checkIdentity(currentID);
      
      mfrc522.PICC_HaltA();  // 讓卡片進入停止模式

      while (digitalRead(Enter) == HIGH){
        if (digitalRead(Return) == LOW or stranger_flag == 1){
          return ;
        }
      }
      while (digitalRead(Enter) == LOW){}
      changeRole(); 
      printOut(print_list + print_list_checkID + print_list_change);
    } 
}

void checkIdentity(String currentID){
  if (currentID == "912112428"){
      role = roleA;
      Serial.print("Last role: ");
      Serial.println(role);

      lcd.setCursor ( 0, 1 );
      lcd.print("Now role: ");
      lcd.setCursor ( 10, 1 );
      lcd.print(role);

      print_list_checkID += "Last role: " + String(role) + "\n";
  }
  else if (currentID == "9015113522"){
      role = roleB;
      Serial.print("Last role: ");
      Serial.println(role);

      lcd.setCursor ( 0, 1 );
      lcd.print("Now role: ");
      lcd.setCursor ( 10, 1 );
      lcd.print(role);
      lcd.setCursor ( 0, 2 );
      lcd.print(" ");

      print_list_checkID += "Last role: " + String(role) + "\n";
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
     Serial.print("Change from role ");
     lcd.setCursor ( 0, 2 );
     lcd.print("Change to role ");

     print_list_change += "Change from role ";

     getRandomRole();
     lcd.setCursor ( 15, 2 );
     lcd.print(randomRole);
     lcd.setCursor ( 0, 3 );
     lcd.print("Comfirm the change? ");

     while (digitalRead(Enter) == HIGH){
       if (digitalRead(Return) == LOW){
          getRandomRole();
          lcd.setCursor ( 15, 2 );
          lcd.print(randomRole);
          lcd.setCursor ( 0, 3 );
          lcd.print("Comfirm the change?");
          delay(500);
       }
     }

     if (currentID == "912112428"){
      Serial.print(roleA);
      print_list_change += String(roleA);
      roleA = randomRole;
    }
     else if (currentID == "9015113522"){
      Serial.print(roleB);
      print_list_change += String(roleB);
      roleB = randomRole;
    }

    Serial.print(" to ");
    Serial.println(randomRole);
    Serial.print("\nNow role: ");
    Serial.println(randomRole);

    print_list_change += " to " + String(randomRole) + "\nNow role: " + String(randomRole);

    role = 999;
    currentID = "";
    mfrc522.PICC_HaltA();  // 讓卡片進入停止模式
    delay(100);
    Serial.println("### changeRole Out ###");
}

void printOut(String print_data){
  lcd.clear();
  lcd.setCursor ( 0, 0 );
  lcd.print("Processing"); 
  delay(500);
  for( int i = 10; i < 20 ; i++ ){
    lcd.setCursor ( i, 0 );
    lcd.print(".");
    delay(500);
  }
  delay(2000);
  lcd.setCursor ( 0, 1 );
  lcd.print("updating your data");
  delay(500);
  for( int i = 18; i < 20 ; i++ ){
    lcd.setCursor ( i, 1 );
    lcd.print(".");
    delay(500);
  }
  delay(2000);
  lcd.setCursor ( 0, 2 ); 
  lcd.print("Connecting to your");
  lcd.setCursor ( 0, 3 );
  lcd.print("printer"); 
  delay(500);
  for( int i = 7; i < 16 ; i++ ){
    lcd.setCursor ( i, 3 );
    lcd.print(".");
    delay(500);
  }
  delay(2000);

  printer.println(F("Print It!"));

  printer.println(print_data);

  printer.justify('C');
  printer.println(F("##### End #####"));
  
  printer.feed(2);

  printer.sleep();      // Tell printer to sleep
  delay(3000L);         // Sleep for 3 seconds
  printer.wake();       // MUST wake() before printing again, even if reset
  printer.setDefault(); // Restore printer to defaults

  print_list = "";
  print_list_checkID = "";
  print_list_change = "";

  lcd.clear();
  lcd.setCursor ( 0, 0 );
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
}