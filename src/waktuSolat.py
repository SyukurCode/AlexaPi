import requests, json
from datetime import datetime
from alexapi.constants import waktu
import alexapi.config
import sys
import yaml
from os.path import exists
from hijri_converter import Hijri
prayers = [waktu.imsak,waktu.subuh,waktu.syuruk,waktu.zohor,waktu.asar,waktu.magrib,waktu.isyak]

hijri = Hijri.today()
now = datetime.now()
nowstr = now.strftime("%m-%d-%Y")
date = { "date": nowstr }

config_exists = alexapi.config.filename is not None
if config_exists:
	with open(alexapi.config.filename, 'r') as stream:
		config = yaml.safe_load(stream)
else:
	logs("config file not found")
	sys.exit(0)

filename = '/opt/AlexaPi/src/waktu_solat.json'
filename_exists = exists(filename)

def getPrayerTime():
	negeri = config['prayer']['state']
	zon = config['prayer']['zone']
	URL = "https://waktu-solat-api.herokuapp.com/api/v1/prayer_times.json?negeri={}&zon={}".format(negeri,zon)
	response = requests.get(URL)
	if response.status_code == 200:
		data = response.json()
		content = data['data']
		content.update(date)
		with open(filename, 'w', encoding ='utf8') as stream:
			json.dump(content,stream,ensure_ascii = True)
	else:
		logs("fail to fectch data from api")
		sys.exit(0)

def checkTime():
	filename_exists = exists(filename)
	if filename_exists:
		with open(filename, 'r') as stream:
			prayer_config = json.load(stream)
		date_data = prayer_config['date']
		prayer_date = datetime.strptime(date_data, '%m-%d-%Y')
		#check data is today
		diff_date = now - prayer_date
		if diff_date.days == 0:
			negeri = prayer_config['negeri']
			zon = prayer_config['zon'][0]['nama']
			#print("Negeri:",negeri)
			#print("Zon:",zon)
			for prayer in prayers:
				name = prayer_config['zon'][0]['waktu_solat'][prayer.value]['name']
				time = prayer_config['zon'][0]['waktu_solat'][prayer.value]['time']
				prayer_time = datetime.strptime(time, '%H:%M')
				if now.hour == prayer_time.hour and now.minute == prayer_time.minute:
					logs("Tell waktu {}".format(name))
					if hijri.month == 9 and name == 'maghrib':
						return "Sekarang telah masuk waktu {} dan waktu berbuka puasa bagi seluruh zon {} ".format(name,zon) + \
							"dan kawasan - kawasan yang sewaktu dengannya"
					return "Sekarang telah masuk waktu {} bagi seluruh zon {}, {}.".format(name,zon,negeri)
			return None

		else:
			logs("update new data")
			getPrayerTime()
	else:
		logs("Create new data file")
		getPrayerTime()
def tellWaktu():
	text = ""
	negeri = config['prayer']['state']
	zon = config['prayer']['zone']
	URL = "https://waktu-solat-api.herokuapp.com/api/v1/prayer_times.json?negeri={}&zon={}".format(negeri,zon)
	response = requests.get(URL)
	if response.status_code == 200:
		data = response.json()
		prayers = data['data']['zon'][0]['waktu_solat']
		text = "Berikut adalah waktu solat bagi seluruh zon {}, {} dan kawasan - kawasan yang sewaktu denganya.\n".format(zon,negeri)
		for prayer in prayers:
			prayer_time = datetime.strptime(prayer["time"], '%H:%M')
			text = text + "{} {} ".format(prayer["name"],prayer_time.strftime("%I:%M %p").replace("AM","Pagi.\n").replace("PM","Petang.\n"))
		return text

def time(waktu,zon,negeri):
	URL = "https://waktu-solat-api.herokuapp.com/api/v1/prayer_times.json?negeri={}&zon={}".format(negeri,zon)
	response = requests.get(URL)
	if response.status_code == 200:
		data = response.json()
		name = data['data']['zon'][0]['waktu_solat'][waktu.value]['name']
		time = data['data']['zon'][0]['waktu_solat'][waktu.value]['time']
		prayer_time = datetime.strptime(time, '%H:%M')
		return prayer_time


def logs(text):
	log_file = "/opt/AlexaPi/src/waktu_solat.log"
	log_date = now.strftime("%m-%d-%Y %H:%M:%S %p")
	log = open(log_file, "a")  # append mode
	log.write("{}:{}\n".format(log_date,text))
	log.close()
