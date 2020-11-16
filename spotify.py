#!/usr/bin/python3
# -*- coding:utf-8 -*-

# task list
# [] access token expired
# [] timeloop wait till song pending time
# [] paused song
import os
import time
import logging
import spotipy
import spotipy.util as util

from timeloop import Timeloop
from datetime import timedelta

# load .env file. system environment variables take presidence
from dotenv import load_dotenv
load_dotenv()

callback = {
  'track_change': None
}

class SpotifyUser:
  scope = 'user-read-currently-playing'
  track_id = ''

  def __init__(self):
    username = os.environ['SPOTIPY_USERNAME']
    self.token = util.prompt_for_user_token(username, self.scope)
    self.spotify = spotipy.Spotify(auth=self.token)

  def currentTrack(self):
    track_info = {
      "playing": False,
      "name": "",
      "artist": "",
      "album": ""
    }

    if self.token:
      results = self.spotify.current_user_playing_track()
      
      if results:  
        track = results['item']

        if track:
          track_info['playing'] = results["is_playing"]
          track_info['name'] = track['name']
          track_info['artist'] = track['artists'][0]['name']
          track_info['album'] = track['album']['name']
          track_info['id'] = track['id']
    else:
      logging.warn("Can't get token for", username)
    return track_info

tl = Timeloop()
sp = SpotifyUser()

# check for a song every 5 minutes
@tl.job(interval=timedelta(seconds=5))
def spotifyListner():
  track_info = sp.currentTrack()
  if sp.track_id != track_info['id']:
    sp.track_id = track_info['id']
    logging.debug("track changed")
    if callback['track_change']:
      callback['track_change'](track_info)

def displayTrackInfo(track_info):
  if track_info['playing']:
    logging.debug("now playing...\n{} by {}".format(track_info['name'], track_info['artist']))
  else:
    logging.debug("it's very quiet here...")

# sample use
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  callback['track_change'] = displayTrackInfo
  # start listening to some music events
  tl.start(block=True)


