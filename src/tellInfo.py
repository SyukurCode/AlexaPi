import say
import os
import random
#import waktuSolat
#import readEvent
from datetime import datetime
from hijri_converter import Hijri
hijri = Hijri.today()
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year
talk = say.talk(language='ms')
#arab = say.talk(language='ar')
#word_to_say = waktuSolat.checkTime()
#talk.say(readEvent.checkTime())
#talk.tellHadith()
#talk.play("/opt/AlexaPi/src/resources/no_internet_services.mp3")
#if hour > 4 or hour == 0:
if hour > 6 and hour < 23:
	if minute == 0:
		#tell_event = readEvent.checkTime()
		talk.play("/opt/AlexaPi/src/resources/beep.wav")
		talk.tellTime()

		if hijri.month == 10:
			directory = "/home/pi/Music/Raya/"
			files = os.listdir(directory)
			mp3_files = [file for file in files if file.endswith('.mp3')]
			if not mp3_files:
				talk.say("No mp3 file")

			random_mp3 = random.choice(mp3_files)
			talk.play(directory + random_mp3)

		if day == 22 and month == 7:
			directory = "/home/pi/Music/Birthday/"
			files = os.listdir(directory)
			mp3_files = [file for file in files if file.endswith('.mp3')]
			if not mp3_files:
				talk.say("No mp3 file")
			random_mp3 = random.choice(mp3_files)
			talk.play(directory + random_mp3)

		#if tell_event is not None:
		#	talk.say(tell_event)
		if hour == 7 or hour == 8:
			talk.weather()
		if hour == 12:
			talk.tellWaktuSolat()

#if word_to_say is not None:
	#talk.say(word_to_say)
	#talk.play("/opt/AlexaPi/src/resources/azan.mp3")
#	if hijri.month == 9 and "imsak" in word_to_say:
#		arab.say("نـَوَيْتُ صَوْمَ غـَدٍ عَـنْ ا َدَاءِ فـَرْضِ شـَهْرِ رَمـَضَانَ هـَذِهِ السَّـنـَةِ لِلـّهِ تـَعَالىَ")
#	if "subuh" in word_to_say or "zohor" in word_to_say or "asar" in word_to_say or "maghrib" in word_to_say or "isyak" in word_to_say:
#		if hijri.month == 9 and "maghrib" in word_to_say:
#			arab.say("اَللّهُمَّ لَكَ صُمْتُ وَبِكَ آمَنْتُ وَعَلَى رِزْقِكَ أَفْطَرْتُ بِرَحْمَتِكَ يَا اَرْحَمَ الرَّحِمِيْنَ")
#		else:
#			talk.tellHadith()
