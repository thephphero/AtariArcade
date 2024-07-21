<<<<<<< HEAD
# AtariArcade
=======
# Atari Arcade
## Intro
## Hardware Configuration

## System Configuration

1. Configure the boot.txt file to include the gpio pins used for shutting down. You will need to Change sda and scl pin assigment, because pin 3 and 5 will be used to shutdown the pie. Also add a line to disable rainbow at the beginning of the startup process
   Add the following lines to the end of the /boot/config.txt:
```   
dtoverlay=i2c-gpio,i2c_gpio_sda=9,i2c_gpio_scl=17,bus=3
#Disable rainbow at startup
disable_splash=1
```

2. Next, you will want to change the boot splash screen in order to give the arcade a more Atari look and feel. Do this by

3. Now add the paths to the python scripts to the end of your /etc/rc.local file, so that they run at startup:

```
    python3 /home/pi/RetroPie/scripts/arcade_control.py &
    python3 /home/pi/RetroPie/scripts/mqtt/publisher.py &
    python3 /home/pi/RetroPie/scripts/mqtt/subscriber.py &
```
>>>>>>> origin/master
