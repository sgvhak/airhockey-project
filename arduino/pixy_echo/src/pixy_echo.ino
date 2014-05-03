#include <SPI.h>  
#include <Pixy.h>

Pixy pixy;

#define MAX_NUM_BLOCKS 1

void setup() {

  Serial.begin(9600);
}

void loop() { 
    char buf[32]; 
    uint16_t blocks = pixy.getBlocks();

    if (blocks) {
        for (int bidx = 0; bidx < min(blocks, MAX_NUM_BLOCKS); bidx++) {
            Block b = pixy.blocks[bidx];
            sprintf(buf, "%d,%d,%d,%d,%d,%d\n", bidx, b.signature, b.x, b.y, b.width, b.height);
            Serial.print(buf);
        }
    }  
}

