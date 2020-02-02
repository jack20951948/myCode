#include <SPI.h>
#include <MFRC522.h>     // 引用程式庫

#define RST_PIN      A0        // 讀卡機的重置腳位
#define SS_PIN       10        // 晶片選擇腳位

#define SERIAL_BAUDRATE 9600
#define CLK_PIN 2 // 定義連接腳位
#define DT_PIN 3
#define SW_PIN 4

#define interruptA 0 // UNO腳位2是interrupt 0，其他板子請見官方網頁

volatile long count = 0;
unsigned long t = 0;

MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件

void setup() {
  Serial.begin(SERIAL_BAUDRATE);
  // 當狀態下降時，代表旋轉編碼器被轉動了
  attachInterrupt(interruptA, rotaryEncoderChanged, FALLING);
  pinMode(CLK_PIN, INPUT_PULLUP); // 輸入模式並啟用內建上拉電阻
  pinMode(DT_PIN, INPUT_PULLUP);
  pinMode(SW_PIN, INPUT_PULLUP);

  Serial.print("Begin! Now state:");
  Serial.println(count);
  //Serial.begin(9600);
  Serial.println("RFID reader is ready!");

  SPI.begin();
  mfrc522.PCD_Init();   // 初始化MFRC522讀卡機模組
}

void loop() {
    // 確認是否有新卡片
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
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
      }
      Serial.println();

      mfrc522.PICC_HaltA();  // 讓卡片進入停止模式
    } 

    if(digitalRead(SW_PIN) == LOW){ // 按下開關，輸出值
     Serial.print("Output! Now state:");
     Serial.println(count);
     delay(300);
    }
}

void rotaryEncoderChanged(){ // when CLK_PIN is FALLING
  unsigned long temp = millis();
  if(temp - t < 200) // 去彈跳
    return;
  t = temp;
 
  // DT_PIN的狀態代表正轉或逆轉
  count += digitalRead(DT_PIN) == HIGH ? 1 : -1;
  
  if(count == 4){ // 大於state 3，設爲state 0
     count = 0; 
     delay(300);
  }

  if(count == -1){ // 小於state 0，設爲state 3
     count = 3; 
     delay(300);
  }
  
  Serial.print("Now state:");
  Serial.println(count);
}
