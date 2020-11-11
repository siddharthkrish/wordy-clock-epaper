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
font_small = ImageFont.truetype('fonts/NovaMono.ttf', 22) # 30 characters
font_medium = ImageFont.truetype('fonts/NovaMono.ttf', 26) # 20 characters
font_big = ImageFont.truetype('fonts/NovaMono.ttf', 42) # XX characters
habbo = ImageFont.truetype('fonts/Habbo.ttf', 24)
class RenderText:
    current_line_start = 0
    line_spacing = 5
    line_start = 5

    def resetLineStart(self):
        self.current_line_start = 0
    
    def drawText(self, draw, text, font):
        _w, y = draw.textsize(text, font = font)
        y += self.current_line_start
        self.current_line_start = y
        draw.text((self.line_start, y), text, font=font)

def getTextPosition(draw, font, text):
    w, h = draw.textsize(text, font = font)
    h += int(h*0.21)
    logging.info("w: %s, h: %s, x: %s, y: %s",w,h,(WIDTH-w)/2, (HEIGHT-h)/2)
    return (WIDTH-w)/2, (HEIGHT-h)/2

def getFont(text):
    if len(text) > 22:
        logging.info('font-small')
        return font_small
    elif len(text) > 10 & len(text) <= 22:
        logging.info('font-medium')
        return font_medium
    else:
        return font_big

renderer = RenderText()

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
        
        renderer.resetLineStart()
        renderer.drawText(draw, line_1, habbo)
        renderer.drawText(draw, line_2, getFont(line_2))
        renderer.drawText(draw, line_3, font_small)

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
