from typing import Self, List
from PySide6.QtCore import QObject, Signal, Slot
import serial

class DSR(QObject):
	opened: bool
	inited: bool
	gl = [100.0, 300.0, 1100.0]
	fl = [100.0, 450.0, 600.0, 800.0, 1400.0, 2000.0]
	g = 0
	f = 0

	error = List[str]

	shutterDone = Signal(bool)
	setWlDone   = Signal(float)

	def __init__(self, filename: str, parent=None):
		super(DSR, self).__init__(parent)
		self.filename = filename
		self.opened = False
		self.inited = False
		self.error = []
		self.g = 0
		self.f = 0

	def open(self):
		self.s = serial.Serial(self.filename, timeout=100)
		self.s.reset_input_buffer()
		self.s.reset_output_buffer()
		self.opened = True
		self.cmd_hello()
	
	def close(self):
		if not self.opened:
			self.error.append("close: not opened")
		else:
			self.s.close()

	def write(self, cmd):
		if not self.opened:
			self.error.append("write: not opened")
		else:
			buf = f"{cmd}\r".encode()
			self.s.write(buf)
			self.s.flush()
			print(f"DSR write: {buf}")

	def read(self):
		if not self.opened:
			self.error.append("read: not opened")
			return ""
		else:
			buf = self.s.read_until(expected = b'\r', size = 100)
			print(f"DSR read: {buf}")
			return buf[:-1].decode()

	# === CMD ===

	def cmd_hello(self):
		if not self.opened:
			self.error.append("cmd_hello: not opened")
		else:
			cmd = "HELLO"
			for i in range(2):
				self.write(cmd)
				r = self.read()
				if r == "OK":
					self.inited = True
					break
				else:
					self.inited = False
					self.error.append(f"cmd_hello: '{r}' returned")

	def cmd_get_systeminfo(self):
		ret = ""
		if not self.opened or not self.inited:
			self.error.append("cmd_get_systeminfo: not opened or not inited")
		else:
			cmd = "SYSTEMINFO?"
			cmd_len = len(cmd)-1
			self.write(cmd)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = r
				r = self.read()
				if r != "OK":
					self.error.append(f"cmd_get_systeminfo: '{r}' returned")
		return ret


	def cmd_get_info(self, addr: int):
		ret = -1
		if not self.opened or not self.inited:
			self.error.append("cmd_get_info: not opened or not inited")
		elif addr < 0 or addr > 1022:
			self.error.append(f"cmd_get_info: '{addr}' out of range [0:1022]")
		else:
			cmd = "SAVEINFO?"
			cmd_len = len(cmd)-1
			cmdf = f"{cmd} {addr}"
			cut_len = len(cmdf)
			self.write(cmdf)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = int(r[cut_len:])
				r = self.read()
				if r != "OK":
					self.error.append(f"cmd_get_info: '{r}' returned")
		return ret

	def cmd_set_info(self, addr, value):
		if not self.opened or not self.inited:
			self.error.append("cmd_set_info: not opened or not inited")
		elif addr < 0 or addr > 1022:
			self.error.append(f"cmd_set_info: '{addr}' out of range [0:1022]")
		elif value < 0 or value > 255:
			self.error.append(f"cmd_set_info: '{value}' out of range [0:255]")
		else:
			cmd = "SAVEINFO"
			cmdf = f"{cmd} {addr},{value}"
			self.write(cmdf)
			r = self.read()
			if r != "OK":
				self.error.append(f"cmd_set_info: '{r}' returned")

	def cmd_get_port(self):
		ret = -1
		if not self.opened or not self.inited:
			self.error.append("cmd_get_port: not opened or not inited")
		else:
			cmd = "PORT_INPUT?"
			cmd_len = len(cmd)-1
			cut_len = cmd_len+1
			self.write(cmd)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = int(r[cut_len:])
				r = self.read()
				if r != "OK":
					self.error.append(f"cmd_get_port: '{r}' returned")
		return ret

	def cmd_set_port(self, value):
		if not self.opened or not self.inited:
			self.error.append("cmd_set_port: not opened or not inited")
		elif value < 0 or value > 15:
			self.error.append(f"cmd_set_port: '{value}' out of range [0:15]")
		else:
			cmd = "PORT_OUTPUT"
			cmdf = f"{cmd} {value}"
			self.write(cmdf)
			r = self.read()
			if r != "OK":
				self.error.append(f"cmd_set_port: '{r}' returned")

	def cmd_get_grating(self):
		ret = -1
		if not self.opened or not self.inited:
			self.error.append("cmd_get_grating: not opened or not inited")
		elif self.g > 0:
			ret = self.g
		else:
			cmd = "GRATING?"
			cmd_len = len(cmd)-1
			cut_len = cmd_len+1
			self.write(cmd)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = int(r[cut_len:])
				r = self.read()
				if r != "OK":
					self.error.append(f"cmd_get_grating: '{r}' returned")
				else:
					self.g = ret
		return ret

	def cmd_set_grating(self, value):
		if not self.opened or not self.inited:
			self.error.append("cmd_set_grating: not opened or not inited")
		elif value < 1 or value > 3:
			self.error.append(f"cmd_set_grating: '{value}' out of range [1:3]")
		elif self.g != value:
			cmd = "GRATING"
			cmdf = f"{cmd} {value}"
			self.write(cmdf)
			r = self.read()
			if r == "0":
				r = self.read()
				if r != "OK":
					self.error.append(f"cmd_set_grating: '{r}' returned")
				else:
					self.g = value

	def get_position(self):
		ret = -1.0
		if not self.opened or not self.inited:
			self.error.append("get_position: not opened or not inited")
		else:
			cmd = "POSITION?"
			cmd_len = len(cmd)-1
			cut_len = cmd_len+1
			self.write(cmd)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = float(r[cut_len:])
				r = self.read()
				if r != "OK":
					self.error.append(f"get_position: '{r}' returned")
		return ret

	def cmd_moveto(self, value):
		ret = -1.0
		if not self.opened or not self.inited:
			self.error.append("cmd_moveto: not opened or not inited")
		elif value < 200.0 or value > 2000.0:
			self.error.append(f"cmd_moveto: '{value}' out of range [200.0:2000.0]")
		else:
			cmd = "MOVETO"
			cmdf = f"{cmd} {value}"
			self.write(cmdf)
			r = self.read()
			if (r[0] != "O") and (r[0] != "E"):
				ret = float(r)
				r = self.read()
				if r != "OK":
					self.error.append(f"cmd_moveto: '{r}' returned")
		return ret

	def cmd_move(self, value):
		ret = -1.0
		if not self.opened or not self.inited:
			self.error.append("cmd_move: not opened or not inited")
		elif value < 0.0 or value > 2000.0:
			self.error.append(f"cmd_moveto: '{value}' out of range [0.0:2000.0]")
		else:
			cmd = "MOVE"
			cmdf = f"{cmd} {value}"
			self.write(cmdf)
			r = self.read()
			ret = float(r)
			r = self.read()
			if r != "OK":
				self.error.append(f"cmd_move: '{r}' returned")
		return ret

	def cmd_get_filter(self):
		ret = -1
		if not self.opened or not self.inited:
			self.error.append("cmd_get_filter: not opened or not inited")
		elif self.f > 0:
			ret = self.f
		else:
			cmd = "FILTER?"
			cmd_len = len(cmd)-1
			cut_len = cmd_len+1
			self.write(cmd)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = int(r[cut_len:])
				r = self.read()
				if r != "OK":
					self.error.append(f"cmd_get_filter: '{r}' returned")
				else:
					self.f = ret
		return ret

	def cmd_set_filter(self, value):
		if not self.opened or not self.inited:
			self.error.append("cmd_set_filter: not opened or not inited")
		elif value < 1 or value > 6:
			self.error.append(f"cmd_set_filter: '{value}' out of range [1:6]")
		elif self.f != value:
			cmd = "FILTER"
			cmdf = f"{cmd} {value}"
			self.write(cmdf)
			r = self.read()
			if r != "OK":
				self.error.append(f"cmd_set_filter: '{r}' returned")
			else:
				self.f = value

	def cmd_get_exitport(self):
		ret = -1
		if not self.opened or not self.inited:
			self.error.append("cmd_get_exitport: not opened or not inited")
		else:
			cmd = "EXITPORT?"
			cmd_len = len(cmd)-1
			cut_len = cmd_len+1
			self.write(cmd)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = int(r[cut_len:])
				r = self.read()
				if r != "OK":
					self.error.append(f"cmd_get_exitport: '{r}' returned")
		return ret

	def cmd_set_exitport(self, value):
		if not self.opened or not self.inited:
			self.error.append("cmd_set_exitport: not opened or not inited")
		elif value < 1 or value > 1:
			self.error.append(f"cmd_set_exitport: '{value}' out of range [0:1]")
		else:
			cmd = "EXITPORT"
			cmdf = f"{cmd} {value}"
			self.write(cmdf)
			r = self.read()
			if r != "OK":
				self.error.append(f"cmd_set_exitport: '{r}' returned")

	# === EXPORT ===

	@Slot(bool)
	def setShutter(self, s: bool):
		i = self.cmd_get_port()
		i = (i & 16) >> 4
		if i == 0 and s:
			self.cmd_set_port(1)
		elif i == 1 and not s:
			self.cmd_set_port(0)
		self.shutterDone.emit(s)
	
	def set_grating(self, g):
		i = self.cmd_get_grating()
		if i != g:
			self.cmd_set_grating(g)

	def set_filter(self, f):
		i = self.cmd_get_filter()
		if i != f:
			self.cmd_set_filter(f)

	def set_exitport(self, ep):
		i = self.cmd_get_exitport()
		if i != ep:
			self.cmd_set_exitport(ep)

	@Slot(float)
	def setWl(self, wl: float):
		g = 1
		for i in range(len(self.gl)):
			if wl >= self.gl[i]:
				g = i+1
			else:
				break
		
		f = 1
		for i in range(len(self.fl)):
			if wl >= self.fl[i]:
				f = i+1
			else:
				break

		print(f"setWl {wl} g = {g} f = {f}")

		self.set_grating(g)
		self.set_filter(f)
		wl = self.cmd_moveto(wl)
		self.setWlDone.emit(wl)
		return wl

	def get_error(self):
		return self.error

	def clear_error(self):
		self.error.clear()


if __name__ == '__main__':

	dsr = DSR("/dev/ttyUSB0")
	dsr.open()

	print(dsr.get_position())

	dsr.close()
