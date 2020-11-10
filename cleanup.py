#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import traceback

from waveshare_epd import epd4in2


epd = epd4in2.EPD()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

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
