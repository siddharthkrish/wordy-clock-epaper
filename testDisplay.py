#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import datetime
import logging
import time
import traceback

from PIL import Image,ImageDraw,ImageFont

# Local dependencies
from timeUtils import timeInWords
from spotify import callback, tl, SpotifyUser
from textUtils import fitTextToLine

WIDTH, HEIGHT = 400, 300
track_font = ImageFont.truetype('fonts/NovaMono.ttf', 42)
artist_playing = ImageFont.truetype('fonts/PTMono-Regular.ttf', 20)
class RenderText:
    current_line_start = 50
    line_spacing = 5
    line_start = 5

    def resetLineStart(self):
        self.current_line_start = 50
    
    def drawText(self, draw, text, font):
      # at size 42, nova mono can display 16 characters on a 400 width screen
      # split song name across 2 lines if characters > 16
      lines = fitTextToLine(text, 17)

      counter = 0
      displayText = ''
      for line in lines:
        if counter > 0:
          displayText += '\n'
        displayText += line
        counter += 1

      logging.info("display '%s' at %d,%d", displayText, self.line_start, self.current_line_start)
      draw.multiline_text((self.line_start, self.current_line_start), displayText, font=font)
      _w, y = draw.multiline_textsize(displayText, font = font)
      # update next line start to current text height + line spacing
      self.current_line_start += (y + self.line_spacing)
    
def getFont(text):
    return track_font

renderer = RenderText()

def trackChanged(track_info):
    logging.info('track changed')
    try:
        # Create a blank image
        image = Image.new('1', (WIDTH, HEIGHT), 128)
        draw = ImageDraw.Draw(image)
        track_name = track_info['name']

        renderer.resetLineStart()
        renderer.drawText(draw, track_name, getFont(track_name))
        renderer.drawText(draw, track_info['artist'], artist_playing)

        image.save(track_info['name'] + '.png')

    except IOError as e:
        logging.info(e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    callback['track_change'] = trackChanged

    try:
        logging.info("init and Clear")

        # start listening to some music events
        tl.start(block=True)
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        exit()
