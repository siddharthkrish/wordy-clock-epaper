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
line_spacing = 10
current_line_start = 0
line_start = 10
displayFontSmall = ImageFont.truetype('fonts/NovaMono.ttf', 22) # 30 characters
displayFontMedium = ImageFont.truetype('fonts/NovaMono.ttf', 26) # 20 characters
displayFontBig = ImageFont.truetype('fonts/NovaMono.ttf', 32) # XX characters

def getTextPosition(draw, font, text):
    w, h = draw.textsize(text, font = font)
    h += int(h*0.21)
    logging.info("w: %s, h: %s, x: %s, y: %s",w,h,(WIDTH-w)/2, (HEIGHT-h)/2)
    return (WIDTH-w)/2, (HEIGHT-h)/2

def getNextLinePosition(draw, font, text):
    w, h = draw.textsize(text, font = font)
    h += int((h*0.21)+line_spacing)
    current_line_start = h + current_line_start
    return line_start, current_line_start

def trackChanged(track_info):
    logging.info('track changed')
    try:
        epd.init()
        # Create a blank image
        Himage = Image.new('1', (WIDTH, HEIGHT), 128)
        draw = ImageDraw.Draw(Himage)

        line_1 = 'now playing...'
        line_2 = track_info['name']
        line_3 = track_info['artist']
        dFont = displayFontBig
        if len(track_info['name']) > 22:
            dFont = displayFontSmall
        elif len(track_info['name']) > 10 & len(track_info['name']) <= 22:
            dFont = displayFontMedium

        # x, y = getTextPosition(draw, dFont, track_info_text)
        # draw.multiline_text((x, y), track_info_text, font = dFont)
        x, y = getNextLinePosition(draw, displayFontSmall, "")
        draw.text((x,y), line_1, font=displayFontSmall)
        x, y = getNextLinePosition(draw, displayFontSmall, line_1)
        draw.text((x,y), line_2, font=dFont)
        x, y = getNextLinePosition(draw, dFont, line_2)
        draw.text((x,y), line_3, font=displayFontSmall)
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
