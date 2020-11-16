#!/bin/bash

ps -ef | grep display | awk '{ print $2 }' | xargs kill
python3 cleanup.py
