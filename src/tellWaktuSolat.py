import say
import waktuSolat
#import readEvent
from datetime import datetime
from hijri_converter import Hijri
hijri = Hijri.today()
now = datetime.now()
hour = now.hour
minute = now.minute
talk = say.talk(language='ms')
arab = say.talk(language='ar')
word_to_say = waktuSolat.checkTime()
if word_to_say is not None:
        #talk.say(word_to_say)
        #talk.play("/opt/AlexaPi/src/resources/azan.mp3")
	if hijri.month == 9 and "imsak" in word_to_say:
		arab.say("نـَوَيْتُ صَوْمَ غـَدٍ عَـنْ ا َدَاءِ فـَرْضِ شـَهْرِ رَمـَضَانَ هـَذِهِ السَّـنـَةِ لِلـّهِ تـَعَالىَ")
	if "subuh" in word_to_say or "zohor" in word_to_say or "asar" in word_to_say or "isyak" in word_to_say or "maghrib" in word_to_say:
		if hijri.month == 9 and "maghrib" in word_to_say:
			arab.say("اَللّهُمَّ لَكَ صُمْتُ وَبِكَ آمَنْتُ وَعَلَى رِزْقِكَ أَفْطَرْتُ بِرَحْمَتِكَ يَا اَرْحَمَ الرَّحِمِيْنَ")
		else:
			if "maghrib" in word_to_say:
				talk.play("/home/pi/Music/Adzan/azan_macca.mp3")
			elif "subuh" in word_to_say:
				talk.play("/home/pi/Music/Adzan/azan_subuh_madina.mp3")
			else:
				talk.tellHadith()

