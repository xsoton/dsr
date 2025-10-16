from typing import Self
from PySide6.QtCore import QObject, Signal, Slot
import pyvisa

class K6482(QObject):
	debug = False

	opened: bool

	channel: int
	voltageFlag: bool
	voltage: float
	nplc: int
	averageFlag: bool
	average: int

	newCurrent     = Signal(float, float)
	newChannel     = Signal(int)
	newVoltageFlag = Signal(bool)
	newVoltage     = Signal(float)
	newNplc        = Signal(int)
	newAverageFlag = Signal(bool)
	newAverage     = Signal(int)

	def __init__(self, filename: str, parent=None):
		super(K6482, self).__init__(parent)
		self.filename = filename
		self.opened = False
		self.error = []

		self.channel     = 1
		self.voltageFlag = False
		self.voltage     = 0.0
		self.nplc        = 1
		self.averageFlag = False
		self.average     = 1

		self._voltageFlag = False
		self._voltage     = False
		self._nplc        = False
		self._averageFlag = False
		self._average     = False

		self.c1 = 0.0
		self.c2 = 0.0

		self.rm = pyvisa.ResourceManager('@py')

	def open(self):
		self.k = self.rm.open_resource(self.filename)
		self.k.timeout = 25000
		self.opened = True

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
			if self.debug: print(f"K6482 write: {cmd.encode()}")
			self.k.write(cmd)

	def read(self):
		if not self.opened:
			self.error.append("read: not opened")
			return ""
		else:
			r = self.k.read()
			if self.debug: print(f"K6482 read: {r.encode()}")
			return r

	def set_channel(self, channel: int):
		if not self.opened:
			self.error.append("set_channel: not opened")
		elif channel != 1 and channel != 2:
			self.error.append(f"set_channel: '{channel}' out of range [1:2]")
		else:
			self.channel = channel

	def get_channel(self):
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
			self._voltage = True
			self.write(f"source{self.channel}:voltage {self.voltage:.3f}")

	def get_voltage(self):
		if not self.opened:
			self.error.append("get_voltage: not opened")
			return -1
		elif self._voltage:
			return self.voltage
		else:
			self.write(f"source{self.channel}:voltage?")
			buf = self.read()
			self.voltage = float(buf)
			return self.voltage

	def set_output(self, output: bool):
		if not self.opened:
			self.error.append("set_output: not opened")
		else:
			self.voltageFlag = output
			self._voltageFlag = True
			self.write(f"output{self.channel} {"on" if output else "off"}")

	def get_output(self):
		if not self.opened:
			self.error.append("get_output: not opened")
			return False
		elif self._voltageFlag:
			return self.voltageFlag
		else:
			self.write(f"output{self.channel}?")
			buf = self.read()
			self.voltageFlag = bool(int(buf))
			return self.voltageFlag

	def set_nplc(self, nplc: int):
		if not self.opened:
			self.error.append("set_nplc: not opened")
		elif nplc < 0.01 or nplc > 10.0:
			self.error.append(f"set_nplc: '{nplc}' out of range [0.01:10.0]")
		else:
			self.nplc = nplc
			self._nplc = True
			self.write(f"sense{self.channel}:current:nplcycles {self.nplc}")

	def get_nplc(self):
		if not self.opened:
			self.error.append("get_nplc: not opened")
			return -1.0
		elif self._nplc:
			return self.nplc
		else:
			self.write(f"sense{self.channel}:current:nplcycles?")
			buf = self.read()
			self.nplc = int(buf)
			return self.nplc

	def set_average(self, average: int):
		if not self.opened:
			self.error.append("set_average: not opened")
		elif average < 1 or average > 100:
			self.error.append(f"set_average: '{average}' out of range [1:100]")
		else:
			self.average = average
			self._average = True
			self.write(f"sense{self.channel}:average:count {self.average}")

	def get_average(self):
		if not self.opened:
			self.error.append("get_average: not opened")
			return -1
		elif self._average:
			return self.average
		else:
			self.write(f"sense{self.channel}:average:count?")
			buf = self.read()
			self.average = int(buf)
			return self.average


	def set_averageFlag(self, averageFlag: bool):
		if not self.opened:
			self.error.append("set_averageFlag: not opened")
		else:
			self.averageFlag = averageFlag
			self._averageFlag = True
			self.write(f"sense{self.channel}:average {"on" if averageFlag else "off"}")

	def get_averageFlag(self):
		if not self.opened:
			self.error.append("get_averageFlag: not opened")
			return False
		elif self._averageFlag:
			return self.averageFlag
		else:
			self.write(f"sense{self.channel}:average?")
			buf = self.read()
			self.averageFlag = bool(int(buf))
			return self.averageFlag

	def get_current(self):
		if not self.opened:
			self.error.append("get_current: not opened")
			return 0.0
		else:
			self.write("read?")
			buf = self.read()
			ii = buf.split(",")
			self.c1 = float(ii[0])
			self.c2 = float(ii[1])
			return self.c1 if self.channel == 1 else self.c2

	@Slot()
	def getCurrent(self):
		if self.debug: print("K6482 -> getCurrent")
		self.get_current()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newCurrent.emit(self.c1, self.c2)
		return self.c1 if self.channel == 1 else self.c2

	@Slot()
	def getChannel(self):
		if self.debug: print(f"K6482 -> getChannel")
		self.get_channel()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newChannel.emit(self.channel)
		return self.channel

	@Slot(int)
	def setChannel(self, channel: int):
		if self.debug: print(f"K6482 -> setChannel {channel}")
		self.set_channel(channel)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newChannel.emit(self.channel)

	@Slot()
	def getVoltageFlag(self):
		if self.debug: print(f"K6482 -> getVoltageFlag")
		self.get_output()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newVoltageFlag.emit(self.voltageFlag)
		return self.voltageFlag

	@Slot(bool)
	def setVoltageFlag(self, voltageFlag: bool):
		if self.debug: print(f"K6482 -> setVoltageFlag {voltageFlag}")
		self.set_output(voltageFlag)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newVoltageFlag.emit(self.voltageFlag)

	@Slot()
	def getVoltage(self):
		if self.debug: print(f"K6482 -> getVoltage")
		self.get_voltage()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newVoltage.emit(self.voltage)
		return self.voltage

	@Slot(float)
	def setVoltage(self, voltage: float):
		if self.debug: print(f"K6482 -> setVoltage {voltage}")
		self.set_voltage(voltage)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newVoltage.emit(self.voltage)

	@Slot()
	def getNplc(self):
		if self.debug: print(f"K6482 -> getNplc")
		self.get_nplc()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newNplc.emit(self.nplc)
		return self.nplc

	@Slot(int)
	def setNplc(self, nplc: int):
		if self.debug: print(f"K6482 -> setNplc {nplc}")
		self.set_nplc(nplc)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newNplc.emit(self.nplc)

	@Slot()
	def getAverageFlag(self):
		if self.debug: print(f"K6482 -> getAverageFlag")
		self.get_averageFlag()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newAverageFlag.emit(self.averageFlag)
		return self.averageFlag

	@Slot(bool)
	def setAverageFlag(self, averageFlag: bool):
		if self.debug: print(f"K6482 -> setAverageFlag {averageFlag}")
		self.set_averageFlag(averageFlag)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newAverageFlag.emit(self.averageFlag)

	@Slot()
	def getAverage(self):
		if self.debug: print(f"K6482 -> getAverage")
		self.get_average()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newAverage.emit(self.average)
		return self.average

	@Slot(int)
	def setAverage(self, average: int):
		if self.debug: print(f"K6482 -> setAverage {average}")
		self.set_average(average)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newAverage.emit(self.average)

	def get_error(self): return self.error
	def clear_error(self): self.error.clear()
