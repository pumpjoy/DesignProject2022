#Unmodified Code of Keyboard obtained from https://forum.arduino.cc/t/adafruit-tft-touchscreen-keypad-for-touchscreen/347024/4
#include <Adafruit_GFX.h> // Hardware-specific library
#include <MCUFRIEND_kbv.h>
MCUFRIEND_kbv tft;

/****************************
  KEYBOARD SETUP
 ***************************/
#define BLACK 0x0000
const char Mobile_KB[3][13] PROGMEM = {
    {0, 13, 10, 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'},
    {1, 12, 9, 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'},
    {3, 10, 7, 'Z', 'X', 'C', 'V', 'B', 'N', 'M'},
};

void drawButton(int x, int y, int w, int h)
{
  // grey
  tft.fillRoundRect(x - 3, y + 3, w, h, 3, 0x8888); // Button Shading

  // white
  tft.fillRoundRect(x, y, w, h, 3, 0xffff); // outter button color

  // red
  tft.fillRoundRect(x + 1, y + 1, w - 1 * 2, h - 1 * 2, 3, 0xf800); // inner button color
}

void MakeKB_Button(const char type[][13])
{
  tft.setTextSize(2);
  tft.setTextColor(0xffff, 0xf0000);
  for (int y = 0; y < 3; y++)
  {
    int ShiftRight = 15 * pgm_read_byte(&(type[y][0]));
    for (int x = 3; x < 13; x++)
    {
      if (x >= pgm_read_byte(&(type[y][1])))
        break;

      drawButton(15 + (30 * (x - 3)) + ShiftRight, 100 + (30 * y), 20, 25); // this will draw the button on the screen by so many pixels
      tft.setCursor(20 + (30 * (x - 3)) + ShiftRight, 105 + (30 * y));
      tft.print(char(pgm_read_byte(&(type[y][x]))));
    }
  }
  // BackSpace
  drawButton(270, 160, 35, 25);
  tft.setCursor(276, 165);
  tft.print(F("BS"));
  // Spacebar
  drawButton(60, 190, 200, 25);
  tft.setCursor(105, 195);
  tft.print(F("SPACE BAR"));
}

void setup()
{
  Serial.begin(9600);
  uint16_t identifier = tft.readID();
  tft.reset();
  tft.begin(identifier);
  tft.fillScreen(BLACK);
  tft.setRotation(1);
  MakeKB_Button(Mobile_KB);
}

void loop()
{
}
