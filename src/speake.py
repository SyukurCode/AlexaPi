#!/usr/bin/env python3
import os
import speech_recognition as sr
import tuya_control
import dispenser
import say
import logging
import re
import volume
import yaml
import alexapi.config
logger = logging.getLogger(__name__)

config_exists = alexapi.config.filename is not None

if config_exists:
	with open(alexapi.config.filename, 'r') as stream:
		config = yaml.load(stream)


def getNumber(text):
        p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
        result = 0
        if re.search(p, text) is not None:
                for catch in re.finditer(p, text):
                        result = catch[0]
        return result

class reading:
	_listener = None
	_audio = None
	_audio_file = None
	_tuya = None
	_dispenser = None
	_engine = None
	_command = None
	_speaker = None
	def __init__(self,audio_file):
		self._audio_file = audio_file
		self._tuya = tuya_control.control()
		self._dispenser = dispenser.control()
		self._engine = say.talk('ms')
		self._speaker = volume.Volume()
		self._listener = sr.Recognizer()
		self._audio = sr.AudioFile(self._audio_file)

		with self._audio as source:
			voice = self._listener.record(source)

		try:
			#self._command = self._listener.recognize_google(voice, language="ms-MY")
			self._command = self._listener.recognize_google(voice)
			self._command = self._command.lower()
			logging.info('Your command: ' + self._command)
		except:
			logger.error("Please run 'sudo apt install flac'")
			logger.error("sound not valid")

		if not self._command is None:
			if 'dispense' in self._command or 'stop' in self._command or 'water' in self._command:
				self._dispenser.process_command(self._command)
			elif 'time' in self._command and 'prayer' not in self._command:
				self._engine.tellTime()
			elif 'date' in self._command:
				self._engine.tellDate()
			elif 'prayer' in self._command:
				self._engine.tellWaktuSolat()
			elif 'weather' in self._command:
				self._engine.weather()
			elif 'joke' in self._command:
				self._engine.telljoke()
			elif 'who' in self._command or 'what' in self._command and not 'status' in self._command:
				self._engine.wiki(self._command)
			elif 'thank you' in self._command:
				self._engine.say("You are, welcome")
			elif 'assalamualaikum' in self._command:
				self._engine.say("Waalaikumusalam.")
			elif 'volume' in self._command or 'speaker' in self._command:
				vol = int(getNumber(self._command))

				if 'up' in self._command or 'increase' in self._command:
					self._speaker.up()
					self._engine.say("tahap speaker ditetapkan pada " + self._speaker.status())
				elif 'down' in self._command or 'decrease' in self._command:
					self._speaker.down()
					self._engine.say("tahap speaker ditetapkan pada " + self._speaker.status())
				elif 'full' in self._command:
					self._speaker.set_volume(100)
					self._engine.say('tahap speaker ditetapkan pada ' + self._speaker.status())
				elif 'unmute' in self._command:
					self._speaker.Mute(False)
					self._engine.say("tahap speaker ditetapkan pada " + self._speaker.status())
				elif 'quiet' in self._command or 'mute' in self._command:
					self._engine.say('Tetapan senyap diaktifkan')
					self._speaker.Mute(True)

				else:
					if vol > 30:
						self._speaker.set_volume(vol)
						self._engine.say("tahap speaker ditetapkan " + str(vol))
				logger.debug("set new volume = %s", self._speaker.status())
			elif 'intro' in self._command or 'yourself' in self._command:
				myname = config['triggers']['pocketsphinx']['phrase']
				self._engine.say("Hai, nama saya ialah {}.".format(myname))
				self._engine.say("saya adalah pembantu peribadi di rumah ini")
				self._engine.say("saya boleh lakukan beberapa perkara ringkas seperti nyalakan lampu,")
				self._tuya.process_command("turn on island light",response=False)
				self._engine.say("dan padamkan lampu")
				self._tuya.process_command("turn off island light",response=False)
				self._engine.say("saya juga boleh membantu anda tuangkan air dengan tepat,")
				self._engine.say("memberitahu maklumat tentang cuaca, membuat carian di wikipedia, berjenaka dan memberitahu anda waktu atau tarikh semasa")
			elif 'on' in self._command or 'off' in self._command or 'status' in self._command:
				if 'status' in self._command:
					if 'kitchen' in self._command:
						isON = self._tuya.status(self._command)
						if 'light' in self._command:
							isON = self._tuya.status("kitchen light")
							self._engine.say("keadaan kitchen light ")

							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")
						else:
							isON = self._tuya.status("kitchen light")
							self._engine.say("keadaan kitchen light ")
							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")

							isON = self._tuya.status("island light")
							self._engine.say("dan keadaan island light ")
							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")


					elif 'island' in self._command:
						isON = self._tuya.status("island light")
						self._engine.say("Keadaan Island light ")

						if isON:
							self._engine.say("ON")
						else:
							self._engine.say("OFF")

					elif 'entrance' in self._command:
						isON = self._tuya.status(self._command)
						self._engine.say("Keadaan island light  ")

						if isON:
							self._engine.say("ON")
						else:
							self._engine.say("OFF")

					elif 'dining' in self._command:
						isON = self._tuya.status(self._command)
						if 'fan' in self._command:
							self._engine.say("Keadaan Dining fan ")
							isON = self._tuya.status("dining fan")

							if isON:
                                                        	self._engine.say("ON")
							else:
								self._engine.say("OFF")
						elif 'light' in self._command:
							isON = self._tuya.status("dining light")
							self._engine.say("Keadaan Dining light ")

							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")
						else:
							self._engine.say("Keadaan Dining fan ")
							isON = self._tuya.status("dining fan")

							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")

							isON = self._tuya.status("dining light")
							self._engine.say("dan keadaan Dining light ")

							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")

					elif 'living' in self._command:
						isON =  self._tuya.status(self._command)
						if 'fan' in self._command:
							self._engine.say("keadaan Living fan ")
							isON = self._tuya.status("living fan")

							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")
						elif 'light' in self._command:
							self._engine.say("keadaan Living light ")
							isON = self._tuya.status("living light")
							if isON:
                                                        	self._engine.say("ON")
							else:
								self._engine.say("OFF")
						else:
							self._engine.say("keadaan Living fan ")
							isON = self._tuya.status("living fan")

							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")

							self._engine.say("dan keadaan Living light ")
							isON = self._tuya.status("living light")
							if isON:
								self._engine.say("ON")
							else:
								self._engine.say("OFF")

					elif 'all' in self._command:
						kitchen_light = self._tuya.status("kitchen light")
						entrance_light = self._tuya.status("entrance")
						island_light = self._tuya.status("island")
						dining_light = self._tuya.status("dining light")
						dining_fan = self._tuya.status("dining fan")
						living_fan = self._tuya.status("living fan")
						living_light = self._tuya.status("living light")

						if kitchen_light and entrance_light:
							self._engine.say("semua suis Kitchen dalam keadaan ON")
						elif kitchen_light:
							self._engine.say("suis Kitchen light dalam keadaan on")
							self._engine.say("suis island light dalam keadaan off")
						elif island_light:
							self._engine.say("suis Island light dalam keadaan on")
							self._engine.say("suis Kitchen light dalam keadaan off")
						else:
							self._engine.say("semua suis Kitchen dalam keadaan off")

						if entrance_light:
							self._engine.say("suis entrance light dalam keadaan on")
						else:
							self._engine.say("suis entrance light dalam keadaan off")

						if dining_light and dining_fan:
							self._engine.say("semua suis dining dalam keadaan on")
						elif dining_light:
							self._engine.say("suis dining light dalam keadaan on")
							self._engine.say("suis dining fan dalam keadaan off")
						elif dining_fan:
							self._engine.say("suis dining fan dalam keadaan on")
							self._engine.say("suis dining light dalam keadaan off")

						else:
							self._engine.say("semua suis Dining dalam keadaan off")

						if living_light and living_fan:
							self._engine.say("semua suis living dalam keadaan on")
						elif living_light:
							self._engine.say("suis living light dalam keadaan on")
							self._engine.say("suis living fan keadaan off")
						elif living_fan:
							self._engine.say("suis living fan dalam keadaan on")
							self._engine.say("suis living light dalam keadaan off")
						else:
							self._engine.say("semua suis Living dalam keadaan off")

				else:
					word = self._tuya.process_command(self._command)
					self._engine.say(word)
		if os.path.exists(self._audio_file):
			os.remove(self._audio_file)
		else:
			logging.warn("audio file does not exist")




