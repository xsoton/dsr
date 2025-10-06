from typing import Self
from PySide6.QtCore import QObject, Signal, Slot
import pyvisa

class K6482(QObject):
	opened: bool

	channel: int
	voltageFlag: bool
	voltage: float
	nplc: int
	averageFlag: bool
	average: int

	newCurrent = Signal(float, float)

	def __init__(self, filename: str, parent=None):
		super(K6482, self).__init__(parent)
		self.filename = filename
		self.opened = False
		self.error = []
		self.rm = pyvisa.ResourceManager('@py')

	def open(self):
		self.k = self.rm.open_resource(self.filename)
		self.k.timeout = 25000
		self.opened = True

		self.channel = 1
		self.voltageFlag = False
		self.voltage = 0.0
		self.nplc = 1
		self.averageFlag = False
		self.average = 1

		self.write("*rst")
		self.write("output1 off")
		self.write("output2 off")
		self.write("system:azero on")
		self.write("sense1:current:range:auto on")
		self.write("sense1:current:nplcycles 1")
		self.write("sense1:average off")
		self.write("sense1:average:count 1")
		self.write("sense1:average:tcontrol repeat")
		self.write("source1:gconnect 0")
		self.write("source1:voltage:mode fixed")
		self.write("source1:voltage 0")
		self.write("sense2:current:range:auto on")
		self.write("sense2:current:nplcycles 1")
		self.write("sense2:average off")
		self.write("sense2:average:count 1")
		self.write("sense2:average:tcontrol repeat")
		self.write("source2:gconnect 0")
		self.write("source2:voltage:mode fixed")
		self.write("source2:voltage 0")

	def close(self):
		if not self.opened:
			self.error.append("write: not opened")
		else:
			self.write("*rst")

	def write(self, cmd):
		if not self.opened:
			self.error.append("write: not opened")
		else:
			print(f"K6482 write: {cmd.encode()}")
			self.k.write(cmd)

	def read(self):
		if not self.opened:
			self.error.append("read: not opened")
			return ""
		else:
			r = self.k.read()
			print(f"K6482 read: {r.encode()}")
			return r

	def set_channel(self, channel: int):
		if not self.opened:
			self.error.append("set_channel: not opened")
		elif channel != 1 and channel != 2:
			self.error.append(f"cmd_get_info: '{channel}' out of range [1:2]")
		else:
			self.channel = channel

	def get_channel(self, channel: int):
		if not self.opened:
			self.error.append("get_channel: not opened")
			return -1
		else:
			return self.channel

	def set_voltage(self, voltage: float):
		if not self.opened:
			self.error.append("set_voltage: not opened")
		elif voltage < -10.0 or voltage > 10:
			self.error.append(f"set_voltage: '{voltage}' out of range [-10.0:10.0]")
		else:
			self.voltage = voltage
			self.write(f"source{self.channel}:voltage {self.voltage:.3f}")

	def get_voltage(self, voltage: int):
		if not self.opened:
			self.error.append("get_voltage: not opened")
			return -1
		else:
			return self.voltage

	def set_output(self, output: bool):
		if not self.opened:
			self.error.append("set_output: not opened")
		else:
			self.voltageFlag = output
			self.write(f"output{self.channel} {"on" if output else "off"}")

	def get_output(self, voltage: int):
		if not self.opened:
			self.error.append("get_output: not opened")
			return False
		else:
			return self.voltageFlag

	def set_nplc(self, nplc: float):
		if not self.opened:
			self.error.append("set_nplc: not opened")
		elif nplc < 0.01 or nplc > 10.0:
			self.error.append(f"set_nplc: '{nplc}' out of range [0.01:10.0]")
		else:
			self.nplc = nplc
			self.write(f"sense{self.channel}:current:nplcycles {self.nplc:.2f}")

	def get_nplc(self, nplc: int):
		if not self.opened:
			self.error.append("get_nplc: not opened")
			return -1.0
		else:
			return self.nplc

	def set_average(self, average: int):
		if not self.opened:
			self.error.append("set_average: not opened")
		elif average < 1 or average > 100:
			self.error.append(f"set_average: '{average}' out of range [1:100]")
		else:
			self.average = average
			self.write(f"sense{self.channel}:average:count {self.average}")

	def get_average(self, average: int):
		if not self.opened:
			self.error.append("get_average: not opened")
			return -1
		else:
			return self.average

	def set_averageFlag(self, averageFlag: bool):
		if not self.opened:
			self.error.append("set_averageFlag: not opened")
		else:
			self.averageFlag = averageFlag
			self.write(f"sense{self.channel}:average {"on" if averageFlag else "off"}")

	def get_averageFlag(self, voltage: int):
		if not self.opened:
			self.error.append("get_averageFlag: not opened")
			return False
		else:
			return self.averageFlag

	@Slot()
	def get_current(self):
		self.write("read?")
		buf = self.read()
		ii = buf.split(",")
		c1 = float(ii[0])
		c2 = float(ii[1])
		self.newCurrent.emit(c1, c2)
		return c1 if self.channel == 1 else c2
		# return float(ii[self.channel-1])

	def get_error(self):
		return self.error

	def clear_error(self):
		self.error.clear()