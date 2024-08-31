
from enum import Enum

class waktu(Enum):
	imsak = 0
	subuh = 1
	syuruk = 2
	zohor = 3
	asar = 4
	magrib = 5
	isyak = 6

class RequestType:
	STARTED = 'STARTED'
	INTERRUPTED = 'INTERRUPTED'
	FINISHED = 'FINISHED'
	ERROR = 'ERROR'

	def __init__(self):
		pass



class PlayerActivity:
	PLAYING = 'PLAYING'
	PAUSED = 'PAUSED'
	IDLE = 'IDLE'

	def __init__(self):
		pass
