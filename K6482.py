from typing import Self
from PySide6.QtCore import QObject, Signal, Slot
import pyvisa

class K6482(QObject):
	debug = False

	opened: bool

	channel    : int
	output     : list[bool]
	voltage    : list[float]
	nplc       : list[float]
	averageFlag: list[bool]
	average    : list[int]

	newCurrent     = Signal(float, float)
	newChannel     = Signal(int)
	newOutput      = Signal(bool)
	newVoltage     = Signal(float)
	newNplc        = Signal(float)
	newAverageFlag = Signal(bool)
	newAverage     = Signal(int)

	def __init__(self, filename: str, parent=None):
		super(K6482, self).__init__(parent)
		self.filename = filename
		self.opened = False
		self.error = []

		self.channel = 1

	def open(self):
		if self.debug: print(f"K6482 -> open")
		try:
			self.rm = pyvisa.ResourceManager()
			self.k = self.rm.open_resource(self.filename)
			self.k.timeout = 25000
			self.opened = True
		except Exception as e:
			self.error.append(f"open: {str(e)}")
			self.opened = False
		if self.opened:
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
		if self.debug: print(f"K6482 -> close")
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
			self.write(f"source{self.channel}:voltage {voltage:.3f}")

	def get_voltage(self):
		if not self.opened:
			self.error.append("get_voltage: not opened")
			return -1
		else:
			self.write(f"source{self.channel}:voltage?")
			return float(self.read())

	def set_output(self, output: bool):
		if not self.opened:
			self.error.append("set_output: not opened")
		else:
			self.write(f"output{self.channel} {"on" if output else "off"}")

	def get_output(self):
		if not self.opened:
			self.error.append("get_output: not opened")
			return False
		else:
			self.write(f"output{self.channel}?")
			return bool(int(self.read()))

	def set_nplc(self, nplc: float):
		if not self.opened:
			self.error.append("set_nplc: not opened")
		elif nplc < 0.01 or nplc > 10.0:
			self.error.append(f"set_nplc: '{nplc}' out of range [0.01:10.0]")
		else:
			self.write(f"sense{self.channel}:current:nplcycles {nplc}")

	def get_nplc(self):
		if not self.opened:
			self.error.append("get_nplc: not opened")
			return -1.0
		else:
			self.write(f"sense{self.channel}:current:nplcycles?")
			return float(self.read())

	def set_average(self, average: int):
		if not self.opened:
			self.error.append("set_average: not opened")
		elif average < 1 or average > 100:
			self.error.append(f"set_average: '{average}' out of range [1:100]")
		else:
			self.write(f"sense{self.channel}:average:count {average}")

	def get_average(self):
		if not self.opened:
			self.error.append("get_average: not opened")
			return -1
		else:
			self.write(f"sense{self.channel}:average:count?")
			return int(self.read())


	def set_averageFlag(self, averageFlag: bool):
		if not self.opened:
			self.error.append("set_averageFlag: not opened")
		else:
			self.write(f"sense{self.channel}:average {"on" if averageFlag else "off"}")

	def get_averageFlag(self):
		if not self.opened:
			self.error.append("get_averageFlag: not opened")
			return False
		else:
			self.write(f"sense{self.channel}:average?")
			return bool(int(self.read()))

	def get_current(self):
		if not self.opened:
			self.error.append("get_current: not opened")
			return 0.0
		else:
			self.write("read?")
			ii = self.read().split(",")
			return float(ii[0]), float(ii[1])

	@Slot()
	def getCurrent(self):
		if self.debug: print("K6482 -> getCurrent")
		c1, c2 = self.get_current()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newCurrent.emit(c1, c2)

	@Slot()
	def getChannel(self):
		if self.debug: print(f"K6482 -> getChannel")
		self.get_channel()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newChannel.emit(self.channel)

	@Slot(int)
	def setChannel(self, channel: int):
		if self.debug: print(f"K6482 -> setChannel {channel}")
		self.set_channel(channel)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newChannel.emit(self.channel)

	@Slot()
	def getOutput(self):
		if self.debug: print(f"K6482 -> getOutput")
		output = self.get_output()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newOutput.emit(output)

	@Slot(bool)
	def setOutput(self, output: bool):
		if self.debug: print(f"K6482 -> setOutput {output}")
		self.set_output(output)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newOutput.emit(output)

	@Slot()
	def getVoltage(self):
		if self.debug: print(f"K6482 -> getVoltage")
		voltage = self.get_voltage()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newVoltage.emit(voltage)

	@Slot(float)
	def setVoltage(self, voltage: float):
		if self.debug: print(f"K6482 -> setVoltage {voltage}")
		self.set_voltage(voltage)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newVoltage.emit(voltage)

	@Slot()
	def getNplc(self):
		if self.debug: print(f"K6482 -> getNplc")
		nplc = self.get_nplc()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newNplc.emit(nplc)

	@Slot(float)
	def setNplc(self, nplc: float):
		if self.debug: print(f"K6482 -> setNplc {nplc}")
		self.set_nplc(nplc)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newNplc.emit(nplc)

	@Slot()
	def getAverageFlag(self):
		if self.debug: print(f"K6482 -> getAverageFlag")
		averageFlag = self.get_averageFlag()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newAverageFlag.emit(averageFlag)

	@Slot(bool)
	def setAverageFlag(self, averageFlag: bool):
		if self.debug: print(f"K6482 -> setAverageFlag {averageFlag}")
		self.set_averageFlag(averageFlag)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newAverageFlag.emit(averageFlag)

	@Slot()
	def getAverage(self):
		if self.debug: print(f"K6482 -> getAverage")
		average = self.get_average()
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newAverage.emit(average)

	@Slot(int)
	def setAverage(self, average: int):
		if self.debug: print(f"K6482 -> setAverage {average}")
		self.set_average(average)
		if len(self.error) > 0: print(f"K6482 errors {self.error}"); self.clear_error()
		self.newAverage.emit(average)

	def   get_error(self): return self.error
	def clear_error(self): self.error.clear()
