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

int count = 0;
unsigned long t = 0;

String currentID;
int role = 999;
int roleA = 0;
int roleB = 1;

String print_list = "";

MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件

void setup() {
  randomSeed(analogRead(0));
  pinMode(7, OUTPUT); digitalWrite(7, LOW);

  // NOTE: SOME PRINTERS NEED 9600 BAUD instead of 19200, check test page.
  mySerial.begin(9600);  // Initialize SoftwareSerial
  //Serial1.begin(19200); // Use this instead if using hardware serial
  printer.begin();        // Init printer (same regardless of serial type)
  Serial.begin(SERIAL_BAUDRATE);
  // 當狀態下降時，代表旋轉編碼器被轉動了
  Serial.print("Begin! Now state:");
  print_list += "Begin! Now state: ";

  Serial.println(count);
  print_list += String(count) + "\n";

  Serial.println("RFID reader is ready!");

  SPI.begin();
  mfrc522.PCD_Init();   // 初始化MFRC522讀卡機模組 
}

void loop() {
    readRFID();

    
}

void readRFID(){
      // 確認是否有新卡片
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {

      currentID = "";

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
      print_list += "currentID: " + String(currentID) + "\n";

      checkIdentity(currentID);
      
      mfrc522.PICC_HaltA();  // 讓卡片進入停止模式

      readEncoder(); 
      printOut(print_list);
    } 
}

void checkIdentity(String currentID){
  if (currentID == "912112428"){
      role = roleA;
      Serial.print("Last role: ");
      Serial.println(role);
      print_list += "Last role: " + String(role) + "\n";
  }
  else if (currentID == "9015113522"){
      role = roleB;
      Serial.print("Last role: ");
      Serial.println(role);
      print_list += "Last role: " + String(role) + "\n";
  }
  else{
    Serial.println("Loggin deny!");
  }
}

void readEncoder(){
     Serial.print("change from role ");
     print_list += "change from role ";
     count = random(0,4);

     if (currentID == "912112428"){
      Serial.print(roleA);
      print_list += String(roleA);
      roleA = count;
    }
     else if (currentID == "9015113522"){
      Serial.print(roleB);
      print_list += String(roleB);
      roleB = count;
    }

    Serial.print(" to ");
    Serial.println(count);
    Serial.print("\nNow role: ");
    Serial.println(count);

    print_list += " to " + String(count) + "\nNow role: " + String(count);

    role = 999;
    currentID = "";
    mfrc522.PICC_HaltA();  // 讓卡片進入停止模式
    delay(100);
    Serial.println("### readEncoder Out ###");
}

void printOut(String print_data){
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
}