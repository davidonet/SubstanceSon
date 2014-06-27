# Hardware

* Raspberry Pi [http://www.raspberrypi.org/]
* I2C 16 Channel PWM Servo & SPI 23017 x1 - 16 GPIO Board [http://www.pridopia.co.uk/pi-9685-23017-lp.html]
* Occidentalis v0.2 [https://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro/occidentalis-v0-dot-2]
* 16 mosfet board to drive vibrator
* Power supply

# OSC messages

## continuous duty cycle control message
Send to a specific vibrator a pwm percent

    osc:/pwm <vibrator #> <pwm %>

Send 0% to stop

## pulse message
generate a millisecond pulse on specific vibrator

    osc:/pulse <vibrator #> <duration in ms>

## note from midi translator 
Vibrator #0 is C3 note, velocity is converted in pwm percent

    osc:/midi/note/<channel> <pitch> <velocity> <trigger>

## control change from midi translator
vibrator power can adjust with control change. In order to keep standard midi label vibrator #0 is cc 16

    osc:/midi/cc<number>/<channel> <value>
    
Midi translation is based on osculator specifications : [http://dl.osculator.net/doc/OSCulator+2.11+Manual.pdf]    
