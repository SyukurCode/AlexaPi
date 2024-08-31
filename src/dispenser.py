from subprocess import call
import paho.mqtt.client as mqtt
import time
import re
import say
import logging

logger = logging.getLogger(__name__)

resources_path = '/opt/AlexaPi/src/resources/'

mqttBroker ="192.168.0.88"


def getNumber(text):
	p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
	result = 0
	if re.search(p, text) is not None:
		for catch in re.finditer(p, text):
			result = catch[0]
	return result
class control:
	_command = None
	_value = None
	_message = None
	_array = None
	_text = None
	_client = None
	_engine = None
	_response = 1

	def __init__(self):
		self._engine = say.talk('ms')
	def timeout(self):
		time.sleep(3)
		if self._response == 0:
			self._engine.say("Tiada jawapan daripada dispenser")
			logger.info("Response: Tiada jawapan daripada dispenser")
	def process_command(self,text):
		self._text = text
		self._client = mqtt.Client("Sender")
		self._client.username_pw_set("syukur", "syukur123***")
		try:
			self._client.connect(mqttBroker,1883)

			self._client.loop_start()
			self._client.subscribe("alexa")
			self._client.on_message = self.on_message
			self._client.publish("waterdispenser", "/check/0")
			self._response = 0
			self.timeout()
			logger.info("request send to dispenser")
		except:
			logger.error("Fail to connect to broker server")
			self._engine.say("Pelayan broker gagal dihubungi")

	def on_message(self,client, userdata, message):
		self._response = 1
		self._message = str(message.payload.decode("utf-8"))
		self._array = self._message.split('/')
		self._command = self._array[1]
		self._value = self._array[2]
		self.show_result()
		time.sleep(1)
		self._client.loop_stop()

	def show_result(self):
		#print('command: ' + self._command)
		#print('value: ' + self._value)
		if self._command == 'status':
			if self._value == 'ready':
				if 'stop' not in self._text:
					self.dispensing(self._text)
			elif self._value == 'noglass':
				logger.info('Response :no glass')
				self._engine.say("Sila letakan gelas")
			elif self._value == 'nowater':
				logger.info('Response :no water')
				self._engine.say("Kekurangan air")
			elif self._value == 'inuse':
				if 'stop' in self._text:
					logger.info('Response :stop dispense')
					self._client.publish("waterdispenser", "/stop/0")
					self._engine.say('Okay')
				else:
					logger.info('Response :dispenser is busy')
					self._engine.say("Sila tunggu sebentar!, dispenser sedang digunakan")
	def dispensing(self,command):
		volume = getNumber(command)
		logger.info("command receive :" + command)
		if int(volume) == 0:
			volume = '250'
		elif int(volume) < 99:
			self._engine.say("Kapasiti air mesti lebih dari 100 ml")
			logger.info("Response : water capacity must above 100ml")
			exit()
		elif int(volume) > 2501:
			self._engine.say("Kapasiti ini tidak dibernarkan")
			logger.info("Response : Alowed below than 2500ml")
			exit()
		if 'one glass' in command:
			volume = '250'
		if 'one jug' in command:
			volume = '1500'

		if 'normal' in command:
			if int(volume) > 99:
				logger.info('Response :Dispense normal ' + volume)
				self._client.publish("waterdispenser", "/normal/" + volume)
				self._engine.say("Menuangkan air...")
			else:
				self._engine.say("Kapasiti air mestilah lebih dari 100 ml")
				logger.info("Response : water capacity must above 100ml")

		elif 'warm' in command:
			if int(volume) > 99:
				logger.info('Response :Dispense warm ' + volume)
				self._client.publish("waterdispenser", "/warm/" + volume)
				self._engine.say("Menuangkan air suam...")
			else:
				self._engine.say("Maaf kapasiti air mesti melebihi 100 ml")
				logger.info("Response : water capacity must above 100ml")

		elif 'hot' in command:
			if int(volume) > 99:
				logger.info('Response :Dispense hot ' + volume)
				self._engine.say("Hati-hati!,")
				self._client.publish("waterdispenser", "/hot/" + volume)
				self._engine.say("Menuangkan air panas")
			else:
				self._engine.say("alamak! kapasiti air perlu melebih 100 ml")
				logger.info("Response : water capacity must above 100ml")
		else :
			if int(volume) > 99:
				logger.info('Dispense normal: ' + volume)
				self._client.publish("waterdispenser", "/normal/" + volume)
				self._engine.say("Menuangkan air")
			else:
				self._engine.say("kapasiti air mesti lebih dari 100 ml")
				logger.info("Response : water capacity must above 100ml")

time.sleep(2)

