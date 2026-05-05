# RPI-Implementations---EECS-113

Smart home controller on a Raspberry Pi, built for EECS 113 at UCI. Reads temperature and humidity, runs a simulated HVAC system, and handles motion-activated lighting. Everything shows up on a 16x2 LCD.

## What it does

The HVAC logic reads from a DHT11 and pulls daily humidity from the CIMIS API, then computes a weather index: temp in Fahrenheit + 0.05 * humidity. If the index is more than 3 above the target, the blue LED (AC) turns on. More than 3 below, the red LED (heat) turns on. Up/down buttons adjust the target between 65 and 95 F. If the index ever goes above 90, all three LEDs flash until the temperature drops, then AC kicks on.

Motion lighting is straightforward: PIR sensor on pin 11, LED stays on for 10 seconds, resets the timer on each new detection.

The LCD (PCF8574 I2C backpack) shows temperature vs. target, door state, HVAC state, and light state on two lines. Temporary messages like "AC is on" pop up for a few seconds then the status screen comes back.

There's also a door button. Opening it turns off the HVAC.

## Hardware

- Raspberry Pi (BOARD pin numbering)
- DHT11 temperature sensor, pin 15
- LEDs: red/heat pin 18, blue/AC pin 31, green/alarm pin 12
- PIR motion sensor pin 11, LED pin 12
- Buttons: temp up pin 22, temp down pin 16, door pin 32
- 16x2 LCD with PCF8574 I2C backpack (0x27 or 0x3F)

## Dependencies

```
RPi.GPIO
requests
```

Adafruit_CharLCD, PCF8574, and Freenove_DHT are bundled in the repo.

## Run

```bash
python3 main.py
```

Logs write to app.log.

## Notes

CIMIS API calls are cached per day with `@lru_cache` so it doesn't hit the endpoint on every loop. The API occasionally returns None, so the code retries until it gets something back.

DHT11.py is a standalone test script from the Freenove kit. Run it first to make sure the sensor is wired correctly.
