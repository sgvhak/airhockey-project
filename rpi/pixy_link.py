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
    """SPI communication module that conforms to link interface expected by pixy comm module"""

    def __init__(self):
        pass

    def init(self, addr):
        """Perform link initialization
        :param addr: unused """
        self.outBuf = []
        SPI.setClockDivider(SPI.SPI_CLOCK_DIV16)
        SPI.begin()

    def getWord(self):
        """Read two bytes of data from the stream.  Write a byte of data if pending.
        :returns: uint16_t word of data received from peer"""
        # ordering is different because Pixy is sending 16 bits through SPI
        # instead of 2 bytes in a 16-bit word as with I2C
        out = 0

        if len(self.outBuf) > 0:
            w = SPI.transfer(PIXY_SYNC_BYTE_DATA)
            out = self.outBuf.pop(0)
        else:
            w = SPI.transfer(PIXY_SYNC_BYTE)

        # Notice that wireline ordering is MSB first
        w = w << 8
        c = SPI.transfer(out)
        w = w | c

        return w

    def getByte(self):
        """Read a single byte of data. Used to align stream. 
        :returns: byte received uint8_t """
        return SPI.transfer(0x00)   # write a dummy byte so we can receive a byte

    def send(self, data):
        """Load a buffer of data that will be sent as getWord is called.
        :param data: array of bytes
        :returns: number of bytes queued or -1 if error
        """
        if len(data) > PIXY_OUTBUF_SIZE or len(self.outBuf) != 0:
            return -1

        self.outBuf = data
        return len(self.outBuf)

