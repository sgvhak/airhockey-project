#
# begin license header
#
# This file is part of Pixy CMUcam5 or "Pixy" for short
#
# All Pixy source code is provided under the terms of the
# GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
# Those wishing to use Pixy source code, software and/or
# technologies under different licensing terms should contact us at
# cmucam@cs.cmu.edu. Such licensing terms are available for
# all portions of the Pixy codebase presented here.
#
# end license header
#

#
#  Pixy.h - Library for interfacing with Pixy.
#  Created by Scott Robinson, October 22, 2013.
#  Released into the public domain.
#

import SPI

PIXY_SYNC_BYTE       =      0x5a
PIXY_SYNC_BYTE_DATA  =      0x5b
PIXY_OUTBUF_SIZE     =      6

class LinkSPI:
    def __init__(self):
        self.outBuf = []
        SPI.setClockDivider(SPI.SPI_CLOCK_DIV16);
        SPI.begin();

    def getWord(self):
        """ returns uint16_t """
        # ordering is different because Pixy is sending 16 bits through SPI
        # instead of 2 bytes in a 16-bit word as with I2C
        out = 0

        if len(self.outBuf) > 0:
            w = SPI.transfer(PIXY_SYNC_BYTE_DATA)
            out = self.outBuf.pop(0)
        else:
            w = SPI.transfer(PIXY_SYNC_BYTE)

        w = w << 8
        c = SPI.transfer(out)
        w = w | c

        return w

    def getByte(self):
        """ return uint8_t """
        return SPI.transfer(0x00);

    def send(self, data):
        """ 
        data array of bytes
        return int8_t 
        """
        if len(data) > PIXY_OUTBUF_SIZE or len(self.outBuf) != 0:
            return -1

        self.outBuf = data
        return len(self.outBuf)

