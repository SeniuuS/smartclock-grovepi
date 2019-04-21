from grovepi import *
import grovepi
from grove_rgb_lcd import *
from math import isnan
import datetime
import random

ultrasonic_ranger = 2
dht_sensor_port = 7
dht_sensor_type = 0

last_range = -1
last_change = datetime.datetime.now()

last_temp = -1
last_hum = -1

while True:
        try:
                # Get range of ultrasonic wave in cm
                current_range = grovepi.ultrasonicRead(ultrasonic_ranger)

                now = datetime.datetime.now()

                # Get temp in °C and humidity in %
                [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)

                r = random.randint(0,255)
                g = random.randint(0,255)
                b = random.randint(0,255)

                if last_range != current_range:
                        last_range = current_range
                        last_change = datetime.datetime.now()
                elif (now - last_change) > datetime.timedelta(seconds=10):
                        r = 0
                        g = 0
                        b = 0

                # Check if temp sensor is working
                if isnan(temp) is True or isnan(hum) is True:
                        print("Temperature sensor not getting any values")
                        temp = last_temp
                        hum = last_hum
                else:
                        last_temp = temp
                        last_hum = hum

                setRGB(r, g, b)
                setText(now.strftime("%d/%m/%y") + " T:" + str(temp) + "C" + "\n" + now.strftime("%H:%M:%S") + " H:" + str(hum) + "%")

        except (IOError, TypeError) as e:
                print(str(e))
                setRGB(0,0,0)
                setText("")

        except KeyboardInterrupt as e:
                print(str(e))
                setRGB(0,0,0)
                setText("")
                break

        time.sleep(0.5)
