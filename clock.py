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
#font35 = ImageFont.truetype('fonts/Habbo.ttf', 60)
displayFont = ImageFont.truetype('fonts/NovaMono.ttf', 50)

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

def getTextPosition(draw, text):
    w, h = draw.textsize(text, font = displayFont)
    h += int(h*0.21)
    logging.info("w: %s, h: %s, x: %s, y: %s",w,h,(WIDTH-w)/2, (HEIGHT-h)/2)
    return (WIDTH-w)/2, (HEIGHT-h)/2

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
            x, y = getTextPosition(draw, time_string)
            draw.multiline_text((x, y), time_string, font = displayFont)
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
