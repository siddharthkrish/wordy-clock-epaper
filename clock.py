#!/usr/bin/python
# -*- coding:utf-8 -*-
import spotipy
import sys
import os
import datetime
import logging
import time
import traceback

from signal import signal, SIGINT
from waveshare_epd import epd4in2
from PIL import Image,ImageDraw,ImageFont

# Local dependencies
from timeUtils import timeInWords

epd = epd4in2.EPD()
WIDTH, HEIGHT = epd.width, epd.height
TIME_X, TIME_Y = 30, 70
#font35 = ImageFont.truetype('Habbo.ttf', 60)
displayFont = ImageFont.truetype('NovaMono.ttf', 50)

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        while True:
            epd.init()

            # Create a blank image
            Himage = Image.new('1', (WIDTH, HEIGHT), 128)
            draw = ImageDraw.Draw(Himage)

            time_now = datetime.datetime.now()
            time_string = timeInWords(time_now.hour, time_now.minute)
            date_string = time_now.strftime('%Y-%m-%d')

            logging.info("time: " + time_string)
            draw.multiline_text((TIME_X, TIME_Y), time_string, font = displayFont)
            image_buffer = epd.getbuffer(Himage)
            epd.display(image_buffer)
            epd.sleep()

            time.sleep(120)
    
        logging.info("Goto Sleep...")
        epd.sleep()
        epd.Dev_exit()
    
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd.Clear()
        epd.sleep()
        epd4in2.epdconfig.module_exit()
        exit()
