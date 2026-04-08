import RPi.GPIO as GPIO
import time
import threading
import logging
from lcd_manager import write_message, write_temporary_message, set_main_menu_message

# Set pin mode
GPIO.setmode(GPIO.BOARD)

# Set up pins
ledPin = 12       # define ledPin
sensorPin = 11    # define sensorPin

GPIO.setup(ledPin, GPIO.OUT)    # set ledPin to OUTPUT mode
GPIO.setup(sensorPin, GPIO.IN)  # set sensorPin to INPUT mode

timer = None
light_status = False

def turn_on_light():
    global timer, light_status
    if light_status:  # Light is already on, no need to update
        return
    if timer is not None:
        timer.cancel()
    logging.info('Turning on light')
    set_main_menu_message('ON', 'light')
    write_temporary_message("Light is on", duration=3)
    print("Motion detected!")
    GPIO.output(ledPin, GPIO.HIGH)
    light_status = True  # Update the status
    timer = threading.Timer(10, turn_off_light)
    timer.start()

def turn_off_light():
    global timer, light_status
    if not light_status:  # Light is already off, no need to update
        return
    GPIO.output(ledPin, GPIO.LOW)
    print("No motion detected")
    set_main_menu_message('OFF', 'light')
    write_temporary_message("Light is off", duration=3)
    logging.info('Turning off light')
    light_status = False  # Update the status
    timer = None

# Initialization
def setup():
    time.sleep(2)
    logging.info('PIR is ready')
    GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(ledPin, GPIO.LOW)

# Loop
def loop():
    if GPIO.input(sensorPin):
        turn_on_light()
    else:
        turn_off_light()
    time.sleep(1)

# Cleanup
def cleanup():
    GPIO.cleanup()
