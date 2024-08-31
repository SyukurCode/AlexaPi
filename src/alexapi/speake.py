#!/usr/bin/env python3
import logging
import speech_recognition as sr

logger = logging.getLogger(__name__)

class reading:
	_listener = None
	_audio = None
	_audio_file = None
	def __init__(self,audio_file):
		self._audio_file = audio_file
		self._listener = sr.Recognizer()
		self._audio = sr.AudioFile(self._audio_file)
		with self._audio as source:
			voice = self._listener.record(source)

		command = self._listener.recognize_google(voice)
		command = command.lower()
		logger.debug(command)

