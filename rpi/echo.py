from pixy import Pixy
import pixy_link

def setup():
    # TODO initialize serial interface should be linked with pixy.serial_print code completion
    pass

def loop():
    pixy = Pixy(pixy_link.LinkSPI())
    while(True):
        blocks = pixy.getBlocks()
        for ii, block in enumerate(blocks):
            pixy.serial_print("%d,%d,%d,%d,%d,%d" % ([ii] + block))

setup()
loop()
