import json
from datetime import datetime
from os.path import exists


now = datetime.now()
nowstr = now.strftime("%Y-%m-%d")
filename = '/opt/AlexaPi/src/event.json'
filename_exists = exists(filename)
def checkTime():
	word = ''
	filename_exists = exists(filename)
	if filename_exists:
		with open(filename, 'r') as stream:
			alldata = json.load(stream)
		for data in alldata['event']:
			if data['date'] == nowstr:
				logs("Read: {}".format(data['name']))
				word += data['name'] + ','
		return word
	else:
		logs("File event.log not found")

def logs(text):
        log_file = "/opt/AlexaPi/src/event.log"
        log_date = now.strftime("%m-%d-%Y %H:%M:%S %p")
        log = open(log_file, "a")  # append mode
        log.write("{}:{}\n".format(log_date,text))
        log.close()


lala = checkTime()
print(lala)
