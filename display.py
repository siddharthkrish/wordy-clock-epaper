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
track_font = ImageFont.truetype('fonts/NovaMono.ttf', 24)
artist_playing = ImageFont.truetype('fonts/PTMono-Regular.ttf', 20)
class RenderText:
    current_line_start = 55
    line_spacing = 5
    line_start = 5

    def resetLineStart(self):
        self.current_line_start = 55
    
    def drawText(self, draw, text, font):
        draw.text((self.line_start, self.current_line_start), text, font=font)
        _w, y = draw.textsize(text, font = font)
        # update next line start to current text height + line spacing
        self.current_line_start += (y + self.line_spacing)

def getTextPosition(draw, font, text):
    w, h = draw.textsize(text, font = font)
    h += int(h*0.21)
    logging.info("w: %s, h: %s, x: %s, y: %s",w,h,(WIDTH-w)/2, (HEIGHT-h)/2)
    return (WIDTH-w)/2, (HEIGHT-h)/2

def getFont(text):
    return track_font

renderer = RenderText()

def trackChanged(track_info):
    logging.info('track changed')
    try:
        epd.init()
        # Create a blank image
        Himage = Image.new('1', (WIDTH, HEIGHT), 128)
        draw = ImageDraw.Draw(Himage)

        renderer.resetLineStart()
        renderer.drawText(draw, track_info['name'], getFont(name['artist']))
        renderer.drawText(draw, track_info['artist'], font_small)

        image_buffer = epd.getbuffer(Himage)
        epd.display(image_buffer)
        epd.sleep()
    except IOError as e:
        logging.info(e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
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
