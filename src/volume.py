##import os
#import signal
import subprocess
import sys
import logging
logger = logging.getLogger(__name__)

DEBUG = False

VOLUME_MIN = 30
VOLUME_MAX = 100
VOLUME_INCREMENT = 5

class VolumeError(Exception):
	pass

class Volume:
	MIN = VOLUME_MIN
	MAX = VOLUME_MAX
	INCREMENT = VOLUME_INCREMENT

	def __init__(self):
    		# Set an initial value for last_volume in case we're muted when we start.
		self.last_volume = self.MIN
		self._sync()

	def up(self):
		return self.change(self.INCREMENT)

	def down(self):
		return self.change(-self.INCREMENT)

	def change(self, delta):
		v = self.volume + delta
		v = self._constrain(v)
		return self.set_volume(v)

	def set_volume(self, v):
		self.volume = self._constrain(v)
		output = self.amixer("sset PCM {}%".format(v))
		self._sync(output)
		return self.volume

	def Mute(self,ismute):
		"""
		Toggles muting between on and off.
		"""

		#if self.is_muted:
		if ismute :
			output = self.amixer("sset 'PCM' mute")
			logger.info('speaker muted')
		elif not ismute:
			# We're about to mute ourselves, so we should remember the last volume
			# value we had because we'll want to restore it later.
			self.last_volume = self.volume
			output = self.amixer("sset 'PCM' unmute")
			logger.info('speaker unmute')
		self._sync(output)
		#if not self.is_muted:
			# If we just unmuted ourselves, we should restore whatever volume we
			# had previously.
		#	self.set_volume(self.last_volume)
		#return self.is_muted

	def status(self):
		if self.is_muted:
			return "{}% (muted)".format(self.volume)
		return "{}%".format(self.volume)
  	# Read the output of `amixer` to get the system volume and mute state.
  	#
  	# This is designed not to do much work because it'll get called with every
  	# click of the knob in either direction, which is why we're doing simple
  	# string scanning and not regular expressions.
	def _sync(self, output=None):
		if output is None:
			output = self.amixer("get 'PCM'")
		lines = output.readlines()
		if DEBUG:
			strings = [line.decode('utf8') for line in lines]
			debug("OUTPUT:")
			debug("".join(strings))
		last = lines[-1].decode('utf-8')
	# The last line of output will have two values in square brackets. The
	# first will be the volume (e.g., "[95%]") and the second will be the
	# mute state ("[off]" or "[on]").
		i1 = last.rindex('[') + 1
		i2 = last.rindex(']')

		self.is_muted = last[i1:i2] == 'off'

		i1 = last.index('[') + 1
		i2 = last.index('%')
    	# In between these two will be the percentage value.
		pct = last[i1:i2]

		self.volume = int(pct)

  	# Ensures the volume value is between our minimum and maximum.
	def _constrain(self, v):
		if v < self.MIN:
			return self.MIN
		if v > self.MAX:
			return self.MAX
		return v

	def amixer(self, cmd):
		p = subprocess.Popen("amixer {}".format(cmd), shell=True, stdout=subprocess.PIPE)
		code = p.wait()
		if code != 0:
			#raise VolumeError("Unknown error")
			sys.exit(0)

		return p.stdout


#vol = Volume()
#vol.Mute(False)
