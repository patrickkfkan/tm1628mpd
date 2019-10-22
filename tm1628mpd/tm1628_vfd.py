import os, fcntl
import struct
import logging
from os import open as os_open
from os import O_RDWR
from ioctl_opt import IOW
import ctypes

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TM1628Vfd:

	def __init__(self, deviceNode="/dev/vfd"):
		self._device_node = deviceNode
		if not os.path.exists(deviceNode):
			logger.warning("Device node %s does not exist. Subsequent ops WILL fail!", deviceNode)
		size = ctypes.c_int(0)
		self._TM1628_IOC_MAGIC = ord('S')
		self._TM1628_IOC_POWER = IOW(self._TM1628_IOC_MAGIC,  0, size)
		self._TM1628_IOC_SBRIGHT = IOW(self._TM1628_IOC_MAGIC,  1, size)
		self._TM1628_IOC_MAXNR = 4

	def enableDisplay(self, value):
		self.__writeTM1628(self._TM1628_IOC_POWER, int(value))

	def setBrightness(self, value):
		self.__writeTM1628(self._TM1628_IOC_SBRIGHT, value)

	def openDeviceNodeForReadWrite(self):
		try:
			return os_open(self._device_node, O_RDWR)
		except Exception as e:
			logger.error("Could not open device node %s!", self._device_node, exc_info=True)
			return None

	def __writeTM1628(self, cmd, value, isBuf = False):
		if isBuf:
			value = ''.join([struct.pack('I', cmd), value])
		else:
			value = struct.pack('i', value)

		try:
			with open(self._device_node, "wb") as vfd:
				fcntl.ioctl(vfd, cmd, value)
			return True
		except Exception as e:
			logger.error("Could not open device node %s!", self._device_node, exc_info=True)
			return False

