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
