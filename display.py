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
from spotify import callback, tl, SpotifyUser

epd = epd4in2.EPD()
WIDTH, HEIGHT = epd.width, epd.height
TIME_X, TIME_Y = 30, 70
displayFontSmall = ImageFont.truetype('fonts/NovaMono.ttf', 22) # 30 characters
displayFontMedium = ImageFont.truetype('fonts/NovaMono.ttf', 26) # 20 characters
displayFontBig = ImageFont.truetype('fonts/NovaMono.ttf', 32) # XX characters

def getTextPosition(draw, dFont text):
    w, h = draw.textsize(text, font = dFont)
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

        track_info_text = "now playing...\n{}\n{}".format(track_info['name'], track_info['artist'])
        dFont = displayFontBig
        if len(track_info['name']) > 22
            dFont = displayFontSmall
        elif len(track_info['name']) < 22 & len(track_info['name']) > 10
            dFont = displayFontMedium

        x, y = getTextPosition(draw, track_info_text, dFont)
        draw.multiline_text((x, y), track_info_text, font = dFont)
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
