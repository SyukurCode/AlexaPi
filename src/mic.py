import pyaudio
import wave
import speake
import time
import os
import logging

FORMAT = pyaudio.paInt16
#CHANNELS = 2
CHANNELS = 1
#RATE = 44100
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
#WAVE_OUTPUT_FILENAME = "/home/pi/file.wav"

logger = logging.getLogger(__name__)

class record:
	_pa = None
	_file_path = None

	def __init__(self,file_path):
		self._pa = pyaudio.PyAudio()
		self._file_path = file_path

	def listen(self):
		logging.info("Listening...")
		stream = self._pa.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

		frames = []

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)

	        # stop Recording
		stream.stop_stream()
		stream.close()
		self._pa.terminate()

		waveFile = wave.open(self._file_path + 'file.wav', 'wb')
		waveFile.setnchannels(CHANNELS)
		waveFile.setsampwidth(self._pa.get_sample_size(FORMAT))
		waveFile.setframerate(RATE)
		waveFile.writeframes(b''.join(frames))
		waveFile.close()

		if os.path.exists(self._file_path + 'file.wav'):
			translate = speake.reading(self._file_path + 'file.wav')


