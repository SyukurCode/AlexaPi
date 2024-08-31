#! /usr/bin/env python3
import importlib
import os
import tempfile
import sys
import threading
import hashlib
import yaml
import requests

import alexapi.config
import alexapi.tunein as tunein
from alexapi.constants import RequestType, PlayerActivity

import warnings
warnings.filterwarnings("ignore", category=yaml.YAMLLoadWarning)

config_exists = alexapi.config.filename is not None

if config_exists:
        with open(alexapi.config.filename, 'r') as stream:
                config = yaml.load(stream)

if not config_exists:
        logger.critical('Can not find configuration file. Exiting...')
        sys.exit(1)

class Player:
	config = None
	platform = None
	pHandler = None
	tunein_parser = None
	navigation_token = None
	playlist_last_item = None
	progressReportRequired = []

	def __init__(self): # pylint: disable=redefined-outer-name
		pHandler.setup()
		platform.setup()

		self.config = config
		self.platform = platform
		self.pHandler = pHandler # pylint: disable=invalid-name
		self.tunein_parser = tunein.TuneIn(5000)

	def play_playlist(self, payload):
		self.navigation_token = payload['navigationToken']
		self.playlist_last_item = payload['audioItem']['streams'][-1]['streamId']

		for stream in payload['audioItem']['streams']: # pylint: disable=redefined-outer-name
			streamId = stream['streamId']
			if stream['progressReportRequired']:
				self.progressReportRequired.append(streamId)

			url = stream['streamUrl']
			if stream['streamUrl'].startswith("cid:"):
				url = "file://" + tmp_path + hashlib.md5(stream['streamUrl'].replace("cid:", "", 1).encode()).hexdigest() + ".mp3"

			if (url.find('radiotime.com') != -1):
				url = self.tunein_playlist(url)

			self.pHandler.queued_play(url, stream['offsetInMilliseconds'], audio_type='media', stream_id=streamId)

	def play_speech(self, mrl):
		self.stop()
		self.pHandler.blocking_play(mrl)


	def stop(self):
		self.pHandler.stop()

	def is_playing(self):
		return self.pHandler.is_playing()

	def get_volume(self):
		return self.pHandler.volume

	def set_volume(self, volume):
		self.pHandler.set_volume(volume)

	def playback_callback(self, requestType, playerActivity, streamId):
                if (requestType == RequestType.STARTED) and (playerActivity == PlayerActivity.PLAYING):
                        self.platform.indicate_playback()
                elif (requestType in [RequestType.INTERRUPTED, RequestType.FINISHED, RequestType.ERROR]) and (playerActivity == PlayerActivity.IDLE):
                        self.platform.indicate_playback(False)

                if streamId:
                        if streamId in self.progressReportRequired:
                                self.progressReportRequired.remove(streamId)
                                gThread = threading.Thread(target=alexa_playback_progress_report_request, args=(requestType, playerActivity, streamId))
                                gThread.start()

                        if (requestType == RequestType.FINISHED) and (playerActivity == PlayerActivity.IDLE) and (self.playlist_last_item == streamId):
                                gThread = threading.Thread(target=alexa_getnextitem, args=(self.navigation_token,))
                                self.navigation_token = None
                                gThread.start()

	def tunein_playlist(self, url):

		req = requests.get(url)
		lines = req.content.decode().split('\n')

		nurl = self.tunein_parser.parse_stream_url(lines[0])
		if nurl:
			return nurl[0]

		return ""

im = importlib.import_module('alexapi.device_platforms.' + config['platform']['device'] + 'platform', package=None)
cl = getattr(im, config['platform']['device'].capitalize() + 'Platform')
platform = cl(config)


# Playback handler
def playback_callback(requestType, playerActivity, streamId):
        return player.playback_callback(requestType, playerActivity, streamId)

im = importlib.import_module('alexapi.playback_handlers.' + config['sound']['playback_handler'] + "handler", package=None)
cl = getattr(im, config['sound']['playback_handler'].capitalize() + 'Handler')
pHandler = cl(config, playback_callback)
player = Player()


path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
resources_path = os.path.join(path, 'resources', '')
tmp_path = os.path.join(tempfile.mkdtemp(prefix='AlexaPi-runtime-'), '')

MAX_VOLUME = 100
MIN_VOLUME = 30

#class sound:
#	def __init__(self):
#		pHandler.setup()
#		platform.setup()
#	def play(self,url):
#		player.play_speech(url)

