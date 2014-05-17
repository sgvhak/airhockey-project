# Dummy SPI module -- maybe convert this into a test shim feeding transfer data

SPI_CLOCK_DIV16 = 4000000/16
def setClockDivider(clock):
    pass
def begin():
    pass
def transfer(b):
    return 0x5a
