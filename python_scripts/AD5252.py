
import sys
import smbus
import time


def ad5252(t):	

# Provide some adjustment in temp

    tAdjusted = float(t) - 0.75


# Convert adjusted temp to potentiometer posn.

    Ohms = 0.0005*(tAdjusted)**4 - 0.0578*(tAdjusted)**3 + 3.4155*(tAdjusted)**2 - 130.73*(tAdjusted) + 2857
    PotPosn = round((Ohms/5000)*128)
    PotPosn_array = [PotPosn]


# Get I2C bus
    bus = smbus.SMBus(1)

# AD5252 address, 0x2C(44)
# Send instruction for POT channel-0, 0x01(01)
#               0x80(128)       Input resistance value
# bus.write_i2c_block_data(0x2C, 0x01, [0xFA])

# AD5252 address, 0x2C(44)
# Send instruction for POT channel-1, 0x03(03)
#               0x80(128)       Input resistance value
    bus.write_i2c_block_data(0x2C, 0x03, PotPosn_array)

    time.sleep(0.5)

# AD5252 address, 0x2C(44)
# Read data back from 0x01(01), 1 byte
#     data = bus.read_byte_data(0x2C, 0x01)

# Convert the data
#     res_0 = (data / 256.0 ) * 10.0

# AD5252 address, 0x2C(44)
# Read data back from 0x03(03), 1 byte
#    data = bus.read_byte_data(0x2C, 0x03)

# Convert the data
#    res_1 = (data / 256.0 ) * 10.0

# Output data to screen
#    print("Resistance Channel-0 : %.2f K" % res_0)
#    print("Resistance Channel-1 : %.2f K" % res_1)
#    print("Ohms : %.2f Ohms" % Ohms)
#    print("Posn : % 2d" % PotPosn)





if __name__ == "__main__":
    ad5252(sys.argv[1])  
