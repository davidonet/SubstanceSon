#!/usr/bin/python2.7


from Adafruit_I2C import Adafruit_I2C
# import numpy as np
import math
import time
import liblo

class PWM : 
    i2c = None
    
    # Registers/etc.
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALLLED_ON_L = 0xFA
    __ALLLED_ON_H = 0xFB
    __ALLLED_OFF_L = 0xFC
    __ALLLED_OFF_H = 0xFD
    
    def __init__(self, address=0x40, debug=False):
        self.i2c = Adafruit_I2C(address)
        self.address = address
        self.debug = debug
        if (self.debug):
            print "Reseting PCA9685"
        self.i2c.write8(self.__MODE1, 0x00)
        oldmode = self.i2c.readU8(self.__MODE1);
        
    def setPWMFreq(self, freq):
        oldmode = self.i2c.readU8(self.__MODE1);
        newmode = (oldmode & 0x7F) | 0x10  # sleep
        self.i2c.write8(self.__MODE1, newmode)  # go to sleep
        self.i2c.write8(self.__PRESCALE, int(math.floor(freq)))
        self.i2c.write8(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.i2c.write8(self.__MODE1, oldmode | 0x80)
        
    def setPWM(self, channel, duty):
        self.i2c.write8(self.__LED0_ON_L + 4 * channel, duty & 0xFF)
        self.i2c.write8(self.__LED0_ON_H + 4 * channel, (duty >> 8) & 0xFF)
        self.i2c.write8(self.__LED0_OFF_L + 4 * channel, (duty >> 16) & 0xFF)
        self.i2c.write8(self.__LED0_OFF_H + 4 * channel, (duty >> 24) & 0xFF)
    
pwm = PWM(0x41, debug=True)
pwm.setPWMFreq(3)
print "Reseting PWMs"
for c in range(0, 16):
    pwm.setPWM(c, 4095)

server = liblo.Server(1234)

def pwm_cb(path, args):
    channel, value = args
    duty = 1 + ((100 - value) * 4094) / 100
    pwm.setPWM(channel, duty)
    print "pwm on %d set to %d %% -> %d" % (channel, value, duty)

def pulse_cb(path, args):
    channel, duration = args
    pwm.setPWM(channel, 256)
    time.sleep(duration / 1000)
    pwm.setPWM(channel, 4095)
    print "%d ms pulse on %d" % (duration, channel)

def note_cb(path, args):
    velocity, on = args
    part = path.split("/")
    if(part[1] == "midi"):
        if(part[2] == "note"):
            channel = int(part[4]) - 36
            power = int(velocity * 100)
            if(on):
                duty = 1 + ((100 - power) * 4094) / 100
                pwm.setPWM(channel, duty)
                print "pwm on %d channel with  %d %%" % (channel, power)
            else:
                pwm.setPWM(channel, 0)
                print "stop on %d channel" % (channel)
               
def control_cb(path, args): 
    part = path.split("/")
    if(part[1] == "midi"):
        if("cc" in part[2]):
            channel = int(part[2][2:]) - 16
            power = int(args[0] * 100)
            duty = 1 + ((100 - power) * 4094) / 100
            pwm.setPWM(channel, duty)
            print "pwm on %d channel with  %d %%" % (channel, power)
            
            

for c in range(0, 16):
    pwm.setPWM(c, 1)
    time.sleep(.1)
    pwm.setPWM(c, 4095)
    print "Testing %d channel" % (c)
    
print "Reseting PWMs"
for c in range(0, 16):
    pwm.setPWM(c, 4095)
        

server.add_method("/pwm", 'ii', pwm_cb)
server.add_method("/pulse", 'ii', pulse_cb)
server.add_method(None, 'fi', note_cb)
server.add_method(None, 'f', control_cb)


print "\n ***** Starting OSC server *****"
while True:
    server.recv(100)
