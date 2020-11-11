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
import spotify

epd = epd4in2.EPD()
WIDTH, HEIGHT = epd.width, epd.height
TIME_X, TIME_Y = 30, 70
displayFont = ImageFont.truetype('fonts/NovaMono.ttf', 50)

def getTextPosition(draw, text):
    w, h = draw.textsize(text, font = displayFont)
    h += int(h*0.21)
    logging.info("w: %s, h: %s, x: %s, y: %s",w,h,(WIDTH-w)/2, (HEIGHT-h)/2)
    return (WIDTH-w)/2, (HEIGHT-h)/2

def trackChanged(track_info):
    logging.info('track changed')
    try:
        epd.init()
        # Create a blank image
        Himage = Image.new('1', (WIDTH, HEIGHT), 128)
        draw = ImageDraw.Draw(Himage)

        track_info_text = "now playing...\n{} by {}".format(track_info['name'], track_info['artist'])
        x, y = getTextPosition(draw, track_info_text)
        draw.multiline_text((x, y), time_string, font = displayFont)
        image_buffer = epd.getbuffer(Himage)
        epd.display(image_buffer)
        epd.sleep()
    except IOError as e:
        logging.info(e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    callback['track_change'] = trackChanged

    try:
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        # start listening to some music events
        tl.start(block=True)    
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd.Clear()
        epd.sleep()
        epd4in2.epdconfig.module_exit()
        exit()
