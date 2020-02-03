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

LiquidCrystal_I2C lcd(I2C_ADDR,
                      En_pin,Rw_pin,Rs_pin,D4_pin,D5_pin,D6_pin,D7_pin,
                      BACKLIGHT_PIN, POSITIVE);

void setup() {
  lcd.begin(20,4);        // 20 columns by 4 rows on display

  lcd.setBacklight(HIGH); // Turn on backlight, LOW for off

  lcd.setCursor ( 0, 0 );            // go to the top left corner
  lcd.print("robotic-controls.com"); // write this string on the top row
  lcd.setCursor ( 0, 1 );            // go to the 2nd row
  lcd.print("  HD44780 / LCD2004 "); // pad string with spaces for centering
  lcd.setCursor ( 0, 2 );            // go to the third row
  lcd.print("  20x4 i2c display  "); // pad with spaces for centering
  lcd.setCursor ( 0, 3 );            // go to the fourth row
  lcd.print("Test increment: ");
}

int n = 1; // a global variable to track number of display refreshes

void loop() {
  lcd.setCursor (16,3);         // go to col 16 of the last row
  lcd.print(n++,DEC);           // update the display with a new number
                                // - overwrites previous characters
                                // - be sure new number is more digits
  delay(500);                   // wait half a second before another update
}
