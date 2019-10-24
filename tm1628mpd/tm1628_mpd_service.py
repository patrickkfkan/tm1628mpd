import threading
from os import open as os_open
from os import write as os_write
from os import O_RDWR
from datetime import datetime
from mpd import MPDClient
from .tm1628_vfd import TM1628Vfd
import struct
import time
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TM1628MpdService():

	def __init__(self, host, port):
		self._vfd = TM1628Vfd()
		self._vfd_dev = self._vfd.openDeviceNodeForReadWrite()
		if self._vfd_dev is None:
			logger.error("Could not open VFD device node! Exiting...")
			quit()
		self._host = host
		self._port = port
		self._mpdclient = MPDClient()
		self._mpdclient.timeout = None
		self._mpdclient.idletimeout = None
		self._rlock = threading.RLock()
		self.__configureVfd()

	def start(self):
		oldPlayTimeHr = -1
		oldPlayTimeMin = -1
		oldPlayTimeSec = -1
		oldTime = -1
		logger.info("Service started...")
		while True:
			clock = True
			clientConnected = self.__checkAndConnectToMpd()
			if clientConnected:
                try:
				    clientStatus = self._mpdclient.status()
                except Exception as e:
    				logger.error("Failed to obtain MPD status!", exc_info=True)
                    clientStatus = None

				if clientStatus is not None and "state" in clientStatus and clientStatus["state"] == "play" and "elapsed" in clientStatus:	# Show play time
					currentPlayTime = float(clientStatus["elapsed"])
					currentPlayTimeHr = min(int(currentPlayTime / 3600), 99)
					if currentPlayTimeHr == 99:
						currentPlayTimeMin = min(int((currentPlayTime - 356400) / 60), 99)
						currentPlayTimeSec = 0
					else:
						currentPlayTimeMin = int((currentPlayTime % 3600) / 60)
						currentPlayTimeSec = int(currentPlayTime % 60)
					clock = False
					if currentPlayTimeHr == 0 and (oldPlayTimeMin != currentPlayTimeMin or oldPlayTimeSec != currentPlayTimeSec):
						oldPlayTimeHr = -1
						oldPlayTimeMin = currentPlayTimeMin
						oldPlayTimeSec = currentPlayTimeSec
						bytePlayTime = struct.pack(b"bbbb", currentPlayTimeMin, currentPlayTimeSec, 0, 1)
						os_write(self._vfd_dev, bytePlayTime)
					elif currentPlayTimeHr > 0 and (oldPlayTimeHr != currentPlayTimeHr or oldPlayTimeMin != currentPlayTimeMin):
						oldPlayTimeHr = currentPlayTimeHr
						oldPlayTimeMin = currentPlayTimeMin
						oldPlayTimeSec = -1
						bytePlayTime = struct.pack(b"bbbb", currentPlayTimeHr, currentPlayTimeMin, 0, 1)
						os_write(self._vfd_dev, bytePlayTime)

			if clock:
				currentTime = datetime.now().time().hour + datetime.now().time().minute
				if (oldTime != currentTime):
					oldTime = currentTime
					byteTime = struct.pack(b"bbbb", datetime.now().time().hour, datetime.now().time().minute, datetime.now().time().second, 1)
					os_write(self._vfd_dev, byteTime)
	
	def __configureVfd(self):
		if (self._rlock.acquire()):
			self._vfd.enableDisplay(True)
			self._vfd.setBrightness(7)
			self._rlock.release()

	def __checkAndConnectToMpd(self):
		global mpd
		try:
			self._mpdclient.ping()
		except:
			try:
				self._mpdclient.connect(self._host, self._port)
				self._mpdclient.ping()
				logger.info("Connected to MPD at %s:%s", self._host, self._port)
			except Exception as e:
				logger.warning("Failed to connect to MPD at %s:%s. Retrying in 10 seconds...", self._host, self._port, exc_info=True)
				time.sleep(10)
				return False

		return True

	def __cleanUp(self):
		self._mpdclient.disconnect()
		self._vfd_dev.close()

