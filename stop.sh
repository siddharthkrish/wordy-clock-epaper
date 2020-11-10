#!/bin/bash

ps -ef | grep clock | awk '{ print $2 }' | xargs kill
