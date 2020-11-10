#!/bin/bash

ps -ef | grep clock | awk '{ print $2 }' | xargs kill
python3 cleanup.py
