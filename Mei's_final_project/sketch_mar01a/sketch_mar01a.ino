#include "LedControl.h"
// Arduino Pin 7 to DIN, 6 to Clk, 5 to LOAD, no.of devices is 1
LedControl lc=LedControl(7,6,5,1);
  int sec=0;
  int tensec,minn;
void setup()
{
 // Initialize the MAX7219 device
  lc.shutdown(0,false);   // Enable display
  lc.setIntensity(0,10);  // Set brightness level (0 is min, 15 is max)
  lc.clearDisplay(0);     // Clear display register
}
void loop()
{ 
  for(int sec;sec<10;sec++){
    if(tensec==6 & sec ==4){
    tensec=0;
    sec=0;
    minn++;
   }
   lc.setDigit(0,0,sec,false); 
   lc.setDigit(0,1,tensec,false); 
   lc.setDigit(0,2,minn,false); 
   delay(659);
  }
  tensec++;    
}
