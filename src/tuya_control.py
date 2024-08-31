import logging
import os
import requests
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
import json

ACCESS_ID = "d45hutht38y7euun95mk"
ACCESS_KEY = "9d1f3135dae744bfbf084f4d92db1f54"
API_ENDPOINT = "https://openapi.tuyaus.com"

logger = logging.getLogger(__name__)

resources_path = '/opt/AlexaPi/src/resources/'

# Enable debug log
TUYA_LOGGER.setLevel(logging.INFO)

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Set up device_id
DINING = "77568873e09806daa3ec"
DINING_FAN = 'switch_1'
DINING_FAN_ON = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=fabf04dd-bc83-4333-9353-a79420d320b7&token=e3bfb3f1-d23f-4f20-8254-b4b0f50638d2&response=json'
DINING_FAN_OFF = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=f16e5386-f879-4818-a7ca-42bb711979f7&token=0fce54d8-63e9-43fd-ace6-c2100382e3cb&response=json'
DINING_LIGHT = 'switch_2'
DINING_LIGHT_ON = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=994335c1-0470-4b1b-817b-82edb5fd6f47&token=7c6c8c4a-d6fd-4498-a45d-bdfdea248b2d&response=json'
DINING_LIGHT_OFF = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=1bbd09d8-820d-477b-a82a-784cf51db7e1&token=01a50353-38f1-4aa7-86a5-601c0f86c964&response=json'
LIVING = "156224867c87ce90c8b5"
LIVING_FAN = 'switch_1'
LIVING_FAN_ON = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=3236ec6f-6a3f-45de-9e6c-7e1c812d9af1&token=1e33a455-b598-4def-99eb-fd59ae5bba2b&response=json'
LIVING_FAN_OFF = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=301ae51a-63e9-4b21-8f1e-158a05b0a1ff&token=fab60692-8418-4d64-8668-089beb966d07&response=json'
LIVING_LIGHT = 'switch_2'
LIVING_LIGHT_ON = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=aee6becf-fd0e-44d8-9a6a-92cfd75c72d2&token=eca0400c-8935-4170-bfe3-5f5c443cd6a3&response=json'
LIVING_LIGHT_OFF = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=3ebe634f-4f88-4a34-89dc-603866075c93&token=255b431b-ee98-40a6-8071-633c41f9586d&response=json'
KITCHEN = "03078768e09806daa960"
ISLAND_LIGHT = 'switch_1'
ISLAND_LIGHT_ON = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=50072504-1bcc-4431-9be5-5173f8a7a04a&token=b1f499ae-ce48-4c55-92bd-41014fa95925&response=json'
ISLAND_LIGHT_OFF = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=4820e33c-de1a-44ab-bdaa-47829bbe59c1&token=d88081c5-24a8-4e39-b594-ffa6b17faa60&response=json'
KITCHEN_LIGHT = 'switch_2'
KITCHEN_LIGHT_ON = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=2201877c-a033-488d-8929-7a19a7242d6a&token=f06693ea-ebb7-4d5d-8b98-2750764fb46f&response=json'
KITCHEN_LIGHT_OFF = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=5ac27400-b3d7-462d-9e68-052fe945ce0d&token=ae897c63-2001-4489-986f-5cc51ccb5af1&response=json'
ENTRANCE_LIGHT = 'switch_3'
ENTRANCE_LIGHT_ON = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=903e1f9f-9abe-480a-96ff-1902f776c748&token=54c67969-6fde-4ee4-bf85-afb4f4c5a024&response=json'
ENTRANCE_LIGHT_OFF = 'https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=3ac2d6f1-dbf6-46c3-99aa-4f8ec2312f6b&token=bb2a4ece-1944-4cdd-844b-75bc86cb91e1&response=json'

class control:
	_command = None
	def __init__(self):
		self._command = None
	def process_command(self,command,response=True):
		self._command = command
		return self.directive(command,response)
	def api_call(self,device):
		response = requests.get(device)
		data = response.json()
		print(data)
		result = data['URLRoutineTrigger']['triggerActivationStatus']
		if result == 'success':
			return True
		return False
	def directive(self,command,_response=True):
		speech_word = ''
		speech_device = ''
		speech_switch = ''
		speech_state = ''
		state = False
		direct = ''
		switch = ''
		if 'on' in command:
			state = True
			speech_state = 'dihidupkan'
		if 'off' in command:
			state = False
			speech_state = 'dimatikan'
		if 'all' in command:
			direct = 'all'
			speech_device = 'semua'
		if 'living' in command:
			direct = LIVING
			speech_device = 'living'
		if 'dining' in command:
			direct = DINING
			speech_device = 'dining'
		if 'kitchen' in command or 'entrance' in command or 'island' in command:
			direct = KITCHEN
			if 'entrance' in command:
				speech_device = 'entrance'
			else:
				speech_device = 'kitchen'
		if 'kitchen' in command and 'light' in command:
			if state:
				switch = KITCHEN_LIGHT_ON
			else:
				switch = KITCHEN_LIGHT_OFF
			speech_switch = 'light'
		if 'island' in command and 'light' in command:
			if state:
				switch = ISLAND_LIGHT_ON
			else:
				switch = ISLAND_LIGHT_OFF
			speech_device = 'island'
			speech_switch = 'light'
		if 'dining' in command and 'light' in command:
			if state:
				switch = DINING_LIGHT_ON
			else:
				switch = DINING_LIGHT_OFF
			speech_switch = 'light'
		if 'dining' in command and 'fan' in command:
			if state:
				switch = DINING_FAN_ON
			else:
				switch = DINING_FAN_OFF
			speech_switch = 'fan'
		if 'living' in command and 'light' in command:
			if state:
				switch = LIVING_LIGHT_ON
			else:
				switch = LIVING_LIGHT_OFF
			speech_switch = 'light'
		if 'living' in command and 'fan' in command:
			if state:
				switch = LIVING_FAN_ON
			else:
				switch = LIVING_FAN_OFF
			speech_switch = 'fan'
		if 'entrance' in command and 'light' in command:
			if state:
				switch = ENTRANCE_LIGHT_ON
			else:
				switch = ENTRANCE_LIGHT_OFF
			speech_switch = 'light'

		# This for single switch
		if not direct == '' and not switch == '':
			isSuccess = self.api_call(switch)
			if isSuccess:
				if _response :
					speech_word = '{} {} {}'.format(speech_device,speech_switch,speech_state)
					return speech_word
		# This for combo switch
		if direct == LIVING and switch == '' :
			isSuccess_fan = False
			isSuccess_light = False
			if state:
				isSuccess_fan = self.api_call(LIVING_FAN_ON)
				isSuccess_light = self.api_call(LIVING_LIGHT_ON)
			else:
				isSuccess_fan = self.api_call(LIVING_FAN_OFF)
				isSuccess_light = self.api_call(LIVING_LIGHT_OFF)

			if _response and isSuccess_fan and isSuccess_light:
				speech_word = 'kesemua suis {} {}'.format(speech_device,speech_state)
				return speech_word
		if direct == DINING and switch == '' :
			isSuccess_fan = False
			isSuccess_light = False
			if state:
				isSuccess_fan = self.api_call(DINING_FAN_ON)
				isSuccess_light = self.api_call(DINING_LIGHT_ON)
			else:
				isSuccess_fan = self.api_call(DINING_FAN_OFF)
				isSuccess_light = self.api_call(DINING_LIGHT_OFF)

			if _response and isSuccess_fan and isSuccess_light:
				speech_word = 'kesemua suis {} {}'.format(speech_device,speech_state)
				return speech_word
		if direct == KITCHEN and switch == '':
			isSuccess_island = False
			isSuccess_light = False
			if state:
				isSuccess_island = self.api_call(ISLAND_LIGHT_ON)
				isSuccess_light = self.api_call(KITCHEN_LIGHT_ON)
			else:
				isSuccess_island = self.api_call(ISLAND_LIGHT_OFF)
				isSuccess_light = self.api_call(KITCHEN_LIGHT_OFF)

			if _response and isSuccess_island and isSuccess_light:
				speech_word = 'kesemua suis {} {}'.format(speech_device,speech_state)
				return speech_word
		if direct == 'all':
			if state:
				isLivingFan = self.api_call(LIVING_FAN_ON)
				isLivingLight = self.api_call(LIVING_LIGHGT_ON)
				isDiningFan = self.api_call(DINING_FAN_ON)
				isDiningLight = self.api_call(DINING_LIGHT_ON)
				isKitchenLight = self.api_call(KITCHEN_LIGHT_ON)
				isIslandLight = self.api_call(ISLAND_LIGHT_ON)
				isEntranceLight = self.api_call(ENTRANCE_LIGHT_ON)
			else:
				isLivingFan = self.api_call(LIVING_FAN_OFF)
				isLivingLight = self.api_call(LIVING_LIGHT_OFF)
				isDiningFan = self.api_call(DINING_FAN_OFF)
				isDiningLight = self.api_call(DINING_LIGHT_OFF)
				isKitchenLight = self.api_call(KITCHEN_LIGHT_OFF)
				isIslandLight = self.api_call(ISLAND_LIGHT_OFF)
				isEntranceLight = self.api_call(ENTRANCE_LIGHT_OFF)

			if _response and isLivingFan and isLivingLight and isDiningFan and isDiningLight and isKitchenLight and isIslandLight and isEntranceLight:
				speech_word = 'kesemua suis {} {}'.format(speech_device,speech_state)
				return speech_word
