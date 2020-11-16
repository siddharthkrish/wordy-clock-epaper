#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import logging
import traceback

from waveshare_epd import epd4in2

# Local dependencies
from spotify import callback, tl, SpotifyUser
from renderText import RenderText

epd = epd4in2.EPD()

renderer = RenderText()

def trackChanged(track_info):
    logging.info('track changed')
    try:
        epd.init()
        image = renderer.render(track_info)

        epd.display(image)
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
