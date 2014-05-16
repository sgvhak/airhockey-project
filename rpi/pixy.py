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

PIXY_MAXIMUM_ARRAYSIZE =    130
PIXY_START_WORD        =    0xaa55
PIXY_START_WORDX       =    0x55aa
PIXY_DEFAULT_ADDR      =    0x54  # I2C
BLOCK_LEN              =    5

def serial_print(msg):
    print msg

def print_block(block):
    (signature, x, y, width, height) = block
    serial_print("sig: %d x: %d y: %d width: %d height: %d" % (signature, x, y, width, height));


class Pixy:
    def __init__(self, link, addr=PIXY_DEFAULT_ADDR):
        self.link = link
        self.blocks = []
        self.skipStart = False # boolean
        self.link.init(addr)

    def getBlocks(self, maxBlocks=1000):
        """ returns uint16_t """
        if not self.skipStart:
            if not self._getStart():
                return 0
        else:
            self.skipStart = False

        while len(self.blocks) < maxBlocks and len(self.blocks) < PIXY_MAXIMUM_ARRAYSIZE:
            checksum = self.link.getWord()
            if checksum == PIXY_START_WORD: # start of next frame
                self.skipStart = True
                return len(self.blocks)
            elif checksum == 0:
                return len(self.blocks)

            block = []
            for ii in range(BLOCK_LEN):
                block.append(self.link.getWord())

            trialsum = sum(block)

            if (checksum == trialsum):
                self.blocks.append(block)
            else:
                serial_print("cs error")

            w = self.link.getWord()

            if w != PIXY_START_WORD:
                return len(self.blocks)
                

    def _short_to_bytes(v):
        """ return array [msb, lsb] """
        return [ (v >> 8) & 0xff, v & 0xff ]

    def setServos(self, s0, s1):
        """ 
        s0 uint16_t
        s1 uint16_6
        returns int8_t
        """
        def msb(v):
            return (v >> 8) & 0xff
        def lsb(v):
            return v & 0xff
        # TODO check if shoft should be written msb first or lsb first
        outBuf = [ 0x00, 0xff ] + self._short_to_bytes(s0) + self._short_to_bytes(s1)
        self.link.send(outBuf)

    def _getStart(self):
        lastw = 0xffff
        while (True):
            w = self.link.getWord()
            if w == 0 and lastw == 0:
                self._delay_microsec(10)
                return False
            elif w == PIXY_START_WORD and lastw == PIXY_START_WORD:
                return True
            elif w == PIXY_START_WORDX:
                serial_print("reorder")
                self.link.getByte() # resync

            lastw = w

    def _delay_microsec(self, durationMs):
        # TODO sleep duration
        pass


