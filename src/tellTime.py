import say
from datetime import datetime

now = datetime.now()
hour = now.hour
talk = say.talk(language='ms')

if hour > 4:
	talk.tellTime()
elif hour == 7:
	talk.tellTime()
	talk.weather()
elif hour == 0:
	talk.tellTime()
	talk.telljoke()

#talk.tellHadith()
