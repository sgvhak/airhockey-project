#include <SPI.h>  
#include <Pixy.h>

Pixy pixy;

void setup()
{

  Serial.begin(9600);
  Serial.print("Starting...\n");
}

void loop()
{ 
  static int i = 0;
  int j;
  uint16_t blocks;
  char buf[32]; 
  
  blocks = pixy.getBlocks();
  
  if (blocks)
  {
        sprintf(buf, "  block %d: ", 0);
        Serial.print(buf); 
        pixy.blocks[0].print();
  }  
}

