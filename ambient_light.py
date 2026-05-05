import RPi.GPIO as GPIO
import time
import threading
import logging
from lcd_manager import write_message, write_temporary_message, set_main_menu_message

GPIO.setmode(GPIO.BOARD)

ledPin    = 12
sensorPin = 11

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(sensorPin, GPIO.IN)

timer = None
light_status = False

def turn_on_light():
    global timer, light_status
    if light_status:  # already on, nothing to do
        return
    if timer is not None:
        timer.cancel()
    logging.info('Turning on light')
    set_main_menu_message('ON', 'light')
    write_temporary_message("Light is on", duration=3)
    print("Motion detected!")
    GPIO.output(ledPin, GPIO.HIGH)
    light_status = True
    timer = threading.Timer(10, turn_off_light)
    timer.start()

def turn_off_light():
    global timer, light_status
    if not light_status:  # already off, nothing to do
        return
    GPIO.output(ledPin, GPIO.LOW)
    print("No motion detected")
    set_main_menu_message('OFF', 'light')
    write_temporary_message("Light is off", duration=3)
    logging.info('Turning off light')
    light_status = False
    timer = None

def setup():
    time.sleep(2)
    logging.info('PIR is ready')
    GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(ledPin, GPIO.LOW)

def loop():
    if GPIO.input(sensorPin):
        turn_on_light()
    else:
        turn_off_light()
    time.sleep(1)

def cleanup():
    GPIO.cleanup()
