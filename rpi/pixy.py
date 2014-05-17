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
    """ Print user message. In arduino code this was sent to serial port, but 
    on RPi might go to console. Consider method rename"""
    print msg

def print_block(block):
    """ Print parsed message 
    :param block: array of 6 bytes 
    """
    (signature, x, y, width, height) = block
    serial_print("sig: %d x: %d y: %d width: %d height: %d" % (signature, x, y, width, height))


class Pixy:
    def __init__(self, link, addr=PIXY_DEFAULT_ADDR):
        self.link = link       # communication module
        self.blocks = []       # array of message byte arrays
        self.skipStart = False # boolean indicating whether sync is needed
        self.link.init(addr)

    def getBlocks(self, maxBlocks=1000):
        """ Read maxBlocks messages from the SPI interface.  
        :returns: number of message blocks uint16_t 
        """
        if not self.skipStart:
            if not self._getStart():
                return 0
        else:
            self.skipStart = False

        # wireline message structure consists of checksum followed by data bytes. Frame boundaries
        # indicated by use of PIXY_START_WORD in place of checksum.  Null checksum terminates block.
        while len(self.blocks) < min(maxBlocks, PIXY_MAXIMUM_ARRAYSIZE):
            checksum = self.link.getWord()
            if checksum == PIXY_START_WORD: # start of next frame
                self.skipStart = True
                return len(self.blocks)
            elif checksum == 0:
                return len(self.blocks)

            # accumulate data words into array
            block = []
            for ii in range(BLOCK_LEN):
                block.append(self.link.getWord())

            trialsum = sum(block)

            if (checksum == trialsum):
                self.blocks.append(block)
            else:
                serial_print("cs error")

            # TODO checkme -- seems odd that there is a potentially discarded word here at the end
            w = self.link.getWord()

            if w != PIXY_START_WORD:
                return len(self.blocks)
                

    def _short_to_bytes(v):
        """Split a short into a byte array.
        :param v: data value of type uint16_t
        :returns: [msb, lsb]"""
        return [ (v >> 8) & 0xff, v & 0xff ]

    def setServos(self, s0, s1):
        """ Write a servo command to the link stream
        :param s0: first word of serial data, uint16_t
        :param s1: second word of serial data, uint16_6
        :returns: int8_t number of bytes written
        """
        # Array of 6 bytes, command header plus two short words
        outBuf = [ 0x00, 0xff ] + self._short_to_bytes(s0) + self._short_to_bytes(s1)
        return self.link.send(outBuf)

    def _getStart(self):
        """Attempt to sync with message frame
        :returns: True is synchronized else false if two zero words received
        """
        lastw = 0xffff
        while (True):
            w = self.link.getWord()
            if w == 0 and lastw == 0:
                self._delay_microsec(10)
                return False
            elif w == lastw == PIXY_START_WORD: # two aligned start words means sync'd
                return True
            elif w == PIXY_START_WORDX: # reversed start word means we need to shift stream
                serial_print("reorder")
                self.link.getByte() # resync

            lastw = w

    def _delay_microsec(self, duration_usec):
        """Sleep for specified number of microseconds"""
        # TODO sleep duration
        pass


