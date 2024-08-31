#from subprocess import call
from datetime import datetime
from geopy.geocoders import Nominatim
import time
import pyjokes
import wikipedia
import requests, json
import logging
import tempfile
import os
import waktuSolat
import alexapi.config
import sys
import yaml
import sound_player
from os.path import exists
from hijri_converter import Hijri, Gregorian
from googletrans import Translator
from gtts import gTTS
translator = Translator()

headless_mode = True
logger = logging.getLogger(__name__)

config_exists = alexapi.config.filename is not None
if config_exists:
        with open(alexapi.config.filename, 'r') as stream:
                config = yaml.safe_load(stream)
else:
        logger.error("config file not found")
        sys.exit(0)

path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))
resources_path = os.path.join(path, 'resources', '')
tmp_path = os.path.join(tempfile.mkdtemp(prefix='AlexaPi-runtime-'), '')

class talk:
	_speech = tmp_path
	_player = None
	_language = None
	_language_set = None
	_time_of_day = 'morning'
	def __init__(self,language='en'):
		self._player = sound_player.Player()
		self._language_set = language
	def say(self,text):
		self._language = self.detectLanguage(text)
		#logger.debug("Language detect is :{}".format(self._language))
		try:
			speech = gTTS(text, lang=self._language_set, slow=False)
			speech.save(self._speech + "speech.mp3")
			logs("Saying:" + text)
			self._player.play_speech(self._speech + "speech.mp3")
		except:
			logger.error("Fail to catch sound")
	def play(self,url):
		if os.path.exists(url):
			logs("Playing:" + url)
			self._player.play_speech(url)
		else:
			self.say("audio file not found")
	def tellGreeting(self):
		now = datetime.now()
		hour = now.hour

		if hour > 22:
			if self._language_set == 'en':
				greeting = "Good night"
			elif self._language_set == 'ms':
				greeting = "Selamat malam"
				self._time_of_day = "malam"
			return greeting + "!"
		elif hour > 14:
			if self._language_set == 'en':
				greeting = "Good evening"
			elif self._language_set == 'ms':
				greeting = "Selamat petang"
				self._time_of_day = "petang"
			return greeting + "!"
		elif hour > 11:
			if self._language_set == 'en':
				greeting = "Good afternoon"
			elif self._language_set == 'ms':
				greeting = "Selamat tengahari"
				self._time_of_day = "tengahari"
			return greeting + "!"
		elif hour < 12:
			if self._language_set == 'en':
				greeting = "Good morning"
			elif self._language_set == 'ms':
				greeting = "Selamat pagi"
				self._time_of_day = "pagi"
			return greeting + "!"

		return greeting + "!"

	def weather(self,q=''):
		if q == '':
			q = self.getGeolocation()
		URL = 'https://weatherapi-com.p.rapidapi.com/current.json'
		response = requests.get(URL, headers = {'X-RapidAPI-Key': '54fb9b7572msh379005da4331487p1e99d0jsn5583a3aa2af4','X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'},params = {'q': 'Kajang, Selangor, Malaysia'})
		if response.status_code == 200:
			data = response.json()
			weather = data['current']['condition']['text']
			temperature = data['current']['temp_c']
			humidity = data['current']['humidity']
			tempFeels = data['current']['feelslike_c']
			windSpeed = data['current']['wind_kph']
			UV = data['current']['uv']
			weather = self.translating(weather,'ms')
			self.say("Cuaca kini di " + config['prayer']['city'] + ", " + config['prayer']['state'] + ", " + weather + ", manakala bacaan suhu adalah " + str(temperature) + " Darjah selsius")
			self.say("Namun suhu terasa seperti " + str(tempFeels) + " Darjah selsius")
			self.say("Kadar kelembapan sekitar " + str(humidity) + " peratus")
			self.say("kelajuan angin bertiup " + str(windSpeed) + " km per jam")
			self.say("Pendedahan sinar UV pada skala " + str(UV))
		else:
			# showing the error message
			logger.debug("Error in the HTTP request")

	def telljoke(self):
		jenaka = self.translating(pyjokes.get_joke(),'ms')
		if self._language_set == 'ms':
			self.say(jenaka)
		else:
			self.say(pyjokes.get_joke())

	def wiki(self,whatis='who is Amazon alexa'):
		try:
			whatis = whatis.replace("what ","")
			whatis = whatis.replace("is ","")
			info = wikipedia.summary(whatis,3)
			maklumat = self.translating(info,'ms')
			self.say(maklumat)
		except:
			self.say("carian tidak ditemui")

	def tellTime(self):
		self.say(self.tellGreeting())
		time = datetime.now().strftime('%I:%M')
		if self._language_set == 'en':
			self.say('Now, ' + time)
		elif self._language_set == 'ms':
			self.say('Sekarang pukul ' + time)
		#logs("Telling time now {}".format(time))
	def tellDate(self):
		today = datetime.now().strftime('%B %-d %Y')
		if self._language_set == 'en':
			self.say('Today is, ' + today)
		elif self._language_set == 'ms':
			self.say('Hari ini ' + today)
		#logs("Telling date today {}".format(today))
	def tellWaktuSolat(self):
		prayer = waktuSolat.tellWaktu()
		prayers = prayer.split("\n")
		for pray in prayers:
			self.say(pray)
	def tellHadith(self):
		hijri = Hijri.today()
		if hijri.month == 9:
			endpoint = "http://192.168.0.88:5002/api/hadith/random2?word=Ramadhan"
		else:
			endpoint = "http://192.168.0.88:5002/api/hadith/random"
		response = requests.get(endpoint)
		if response.status_code == 200:
			data = response.json()
			kitab = data['data']['kitab']
			collection = data['data']['collection_no']
			text = data['data']['text']
			text = text.replace(';',',')
			kitab = kitab.replace("nasai","nasa'i")
			self.say(text)
			self.say("Hadis riwayat {}".format(kitab))
			logs("Bacaan hadith:-Kitab:{}-collection_no:{}".format(kitab,collection))
		else:
			if data['status'] == 204:
				error= data['error']['message']
				if error:
					self.say(error)
				self.say("capaian pengkalan data tidak berjaya")

	def translating(self,text,lang='ms'):
		translations = translator.translate(text, dest=lang)
		return translations.text

	def detectLanguage(self,text):
		lans = translator.detect(text).lang
		for lan in lans:
			#GET SINGLE LANGUAGE
			if len(lan) == 2:
				return lan
			else:
				return lans
	def getGeolocation(self):
		state = config['prayer']['state']
		city =  config['prayer']['city']
		country = config['prayer']['country']
		loc = Nominatim(user_agent="GetLoc")
		getLocation = loc.geocode("{} {}".format(city,state))
		return "{},{}".format(getLocation.latitude,getLocation.longitude)
def logs(text):
        now = datetime.now()
        log_file = "/opt/AlexaPi/src/say.log"
        log_date = now.strftime("%m-%d-%Y %H:%M:%S %p")
        log = open(log_file, "a")  # append mode
        log.write("{}:{}\n".format(log_date,text))
        log.close()
