from typing import Self
from PySide6.QtCore import QObject, Signal, Slot
import pyvisa

class K2400(QObject):
	debug = True

	opened: bool

	mode: int # 1 = voltage source, 2 - current source
	output: bool
	voltage: float
	current: float
	nplc: int

	newMode        = Signal(int)
	newOutput      = Signal(bool)
	newVoltage     = Signal(float)
	newCurrent     = Signal(float)
	newNplc        = Signal(int)

	def __init__(self, filename: str, parent=None):
		super(K2400, self).__init__(parent)
		self.filename = filename
		self.opened = False
		self.error = []

		self.mode     = 1
		self.output   = False
		self.voltage  = 0.0
		self.current  = 0.0
		self.nplc     = 1

		self.rm = pyvisa.ResourceManager('@py')

	def open(self):
		self.k = self.rm.open_resource(self.filename)
		self.k.timeout = 25000
		self.opened = True

		self.write("*rst")
		self.write("output off")
		self.write("system:azero on")
		self.write("source:function current")
		self.write("source:current:mode fixed")
		self.write("source:current:range:auto on")
		self.write("source:current 0")
		self.write("sense:function \"voltage\"")
		self.write("sense:voltage:range:auto on")
		self.write("sense:voltage:nplcycles 1")
		self.write("format:elements voltage,current")
		self.write("system:error:all?")
		self.read()

	def close(self):
		if not self.opened:
			self.error.append("write: not opened")
		else:
			self.write("*rst")

	def write(self, cmd):
		if not self.opened:
			self.error.append("write: not opened")
		else:
			if self.debug: print(f"K2400 write: {cmd.encode()}")
			self.k.write(cmd)

	def read(self):
		if not self.opened:
			self.error.append("read: not opened")
			return ""
		else:
			r = self.k.read()
			if self.debug: print(f"K2400 read: {r.encode()}")
			return r

	def set_mode(self, mode: int):
		if not self.opened:
			self.error.append("set_mode: not opened")
		elif mode != 1 and mode != 2:
			self.error.append(f"set_mode: '{mode}' out of range [1:2]")
		else:
			self.mode = mode
			self.write(f"source:function {"voltage" if self.mode == 1 else "current"}")

	def get_mode(self):
		if not self.opened:
			self.error.append("get_mode: not opened")
			return -1
		else:
			self.write(f"source:function?")
			buf = self.read().strip()
			if buf[:4] == "VOLT": self.mode = 1
			else:                 self.mode = 2
			return self.mode

	def set_voltage(self, voltage: float):
		if not self.opened:
			self.error.append("set_voltage: not opened")
		elif voltage < -10.0 or voltage > 10:
			self.error.append(f"set_voltage: '{voltage}' out of range [-10.0:10.0]")
		else:
			self.voltage = voltage
			self.write(f"source:voltage {self.voltage:.3f}")

	def get_voltage(self):
		if not self.opened:
			self.error.append("get_voltage: not opened")
			return -1
		elif not self.output:
			self.error.append("get_voltage: output is not on")
			return -1
		else:
			self.write(f"read?")
			buf = self.read()
			self.voltage = float(buf.strip().split(",")[0])
			return self.voltage


	def set_output(self, output: bool):
		if not self.opened:
			self.error.append("set_output: not opened")
		else:
			self.output = output
			self.write(f"output {"on" if output else "off"}")

	def get_output(self):
		if not self.opened:
			self.error.append("get_output: not opened")
			return False
		elif self._output:
			return self.output
		else:
			self.write(f"output?")
			buf = self.read()
			self.output = bool(int(buf))
			return self.output

	def set_nplc(self, nplc: int):
		if not self.opened:
			self.error.append("set_nplc: not opened")
		elif nplc < 0.01 or nplc > 10.0:
			self.error.append(f"set_nplc: '{nplc}' out of range [0.01:10.0]")
		else:
			self.nplc = nplc
			self.write(f"sense:{"current" if self.mode == 1 else "voltage"}:nplcycles {self.nplc}")

	def get_nplc(self):
		if not self.opened:
			self.error.append("get_nplc: not opened")
			return -1.0
		else:
			self.write(f"sense:{"current" if self.mode == 1 else "voltage"}:nplcycles?")
			buf = self.read()
			self.nplc = int(buf)
			return self.nplc


	def set_current(self, current: float):
		if not self.opened:
			self.error.append("set_current: not opened")
		elif current < -1.05 or current > 1.05:
			self.error.append(f"set_current: '{current}' out of range [-1.05:1.05]")
		else:
			self.current = current
			self.write(f"source:current {self.current:.3f}")

	def get_current(self):
		if not self.opened:
			self.error.append("get_current: not opened")
			return -1
		elif not self.output:
			self.error.append("get_current: output is not on")
			return -1
		else:
			self.write(f"read?")
			buf = self.read()
			self.current = float(buf.strip().split(",")[1])
			return self.current

	@Slot()
	def getMode(self):
		if self.debug: print(f"K2400 -> getMode")
		self.get_mode()
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newMode.emit(self.mode)
		return self.mode

	@Slot(int)
	def setMode(self, mode: int):
		if self.debug: print(f"K2400 -> setMode {mode}")
		self.set_mode(mode)
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newMode.emit(self.mode)

	@Slot()
	def getOutput(self):
		if self.debug: print(f"K2400 -> getOutput")
		self.get_output()
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newOutput.emit(self.output)
		return self.output

	@Slot(bool)
	def setOutput(self, output: bool):
		if self.debug: print(f"K2400 -> setOutput {output}")
		self.set_output(output)
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newOutput.emit(self.output)

	@Slot()
	def getVoltage(self):
		if self.debug: print(f"K2400 -> getVoltage")
		self.get_voltage()
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newVoltage.emit(self.voltage)
		return self.voltage

	@Slot(float)
	def setVoltage(self, voltage: float):
		if self.debug: print(f"K2400 -> setVoltage {voltage}")
		self.set_voltage(voltage)
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newVoltage.emit(self.voltage)

	@Slot()
	def getCurrent(self):
		if self.debug: print("K2400 -> getCurrent")
		self.get_current()
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newCurrent.emit(self.current)
		return self.current

	@Slot(float)
	def setCurrent(self, current: float):
		if self.debug: print(f"K2400 -> setCurrent {current}")
		self.set_current(current)
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newCurrent.emit(self.current)
		return self.current

	@Slot()
	def getNplc(self):
		if self.debug: print(f"K2400 -> getNplc")
		self.get_nplc()
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newNplc.emit(self.nplc)
		return self.nplc

	@Slot(int)
	def setNplc(self, nplc: int):
		if self.debug: print(f"K2400 -> setNplc {nplc}")
		self.set_nplc(nplc)
		if len(self.error) > 0: print(f"K2400 errors {self.error}"); self.clear_error()
		self.newNplc.emit(self.nplc)

	def get_error(self): return self.error
	def clear_error(self): self.error.clear()

if __name__ == '__main__':
	k = K2400("GPIB0::24::INSTR")

	k.open()
	k.set_output(True)
	k.setCurrent(1e-3)
	r = k.get_current(); print(r)
	r = k.get_current(); print(r)
	r = k.get_current(); print(r)
	r = k.get_current(); print(r)
	r = k.get_current(); print(r)
	k.setCurrent(0)
	k.set_output(False)
