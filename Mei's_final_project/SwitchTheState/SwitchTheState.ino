#define SERIAL_BAUDRATE 115200
#define CLK_PIN 2 // 定義連接腳位
#define DT_PIN 3
#define SW_PIN 4

#define interruptA 0 // UNO腳位2是interrupt 0，其他板子請見官方網頁

volatile long count = 0;
unsigned long t = 0;

void setup() {
  Serial.begin(SERIAL_BAUDRATE);
  // 當狀態下降時，代表旋轉編碼器被轉動了
  attachInterrupt(interruptA, rotaryEncoderChanged, FALLING);
  pinMode(CLK_PIN, INPUT_PULLUP); // 輸入模式並啟用內建上拉電阻
  pinMode(DT_PIN, INPUT_PULLUP);
  pinMode(SW_PIN, INPUT_PULLUP);

  Serial.print("Begin! Now state:");
  Serial.println(count);
}
void loop() {
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
