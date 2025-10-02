from typing import Self
from PySide6.QtCore import QObject, Signal, Slot
import serial

class DSR(QObject):
	opened: bool
	inited: bool
	gl = [100.0, 300.0, 1100.0]
	fl = [100.0, 450.0, 600.0, 800.0, 1400.0, 2000.0]

	def __init__(self, filename: str, parent=None):
		super(DSR, self).__init__(parent)
		self.filename = filename
		self.opened = False
		self.inited = False
		self.error = []

	def open(self):
		self.s = serial.Serial(self.filename, timeout=100)
		self.opened = True
		self.cmd_hello()
	
	def close(self):
		if self.opened:
			self.s.close()
		else:
			self.error.append("close: not opened")

	def write(self, cmd):
		if not self.opened:
			self.error.append("write: not opened")
		else:
			buf = f"{cmd}\r".encode()
			self.s.write(buf)
			self.s.flush()

	def read(self):
		ret = ""
		if not self.opened:
			self.error.append("read: not opened")
		else:
			r = self.s.read_until(expected = b'\r', size = 100)
			ret = r[:-1].decode()
		return ret

	# === CMD ===

	def cmd_hello(self):
		if not self.opened:
			self.error.append("cmd_hello: not opened")
		else:
			cmd = "HELLO"
			for i in range(2):
				self.write(cmd)
				r = self.read()
				self.error.append(f"cmd_hello: '{r}' returned")
				if r == "OK":
					self.inited = True
					break
				else:
					self.inited = False

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
			self.error.append(f"cmd_set_port: '{r}' returned")

	def cmd_get_grating(self):
		ret = -1
		if not self.opened or not self.inited:
			self.error.append("cmd_get_grating: not opened or not inited")
		else:
			cmd = "GRATING?"
			cmd_len = len(cmd)-1
			cut_len = cmd_len+1
			self.write(cmd)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = int(r[cut_len:])
				r = self.read()
			self.error.append(f"cmd_get_grating: '{r}' returned")
		return ret

	def cmd_set_grating(self, value):
		if not self.opened or not self.inited:
			self.error.append("cmd_set_grating: not opened or not inited")
		elif value < 1 or value > 3:
			self.error.append(f"cmd_set_grating: '{value}' out of range [1:3]")
		else:
			cmd = "GRATING"
			cmdf = f"{cmd} {value}"
			self.write(cmdf)
			r = self.read()
			if r == "0":
				r = self.read()
			self.error.append(f"cmd_set_grating: '{r}' returned")

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
			self.error.append(f"cmd_move: '{r}' returned")
		return ret

	def cmd_get_filter(self):
		ret = -1
		if not self.opened or not self.inited:
			self.error.append("cmd_get_filter: not opened or not inited")
		else:
			cmd = "FILTER?"
			cmd_len = len(cmd)-1
			cut_len = cmd_len+1
			self.write(cmd)
			r = self.read()
			if r[:cmd_len] == cmd[:cmd_len]:
				ret = int(r[cut_len:])
				r = self.read()
			self.error.append(f"cmd_get_filter: '{r}' returned")
		return ret

	def cmd_set_filter(self, value):
		if not self.opened or not self.inited:
			self.error.append("cmd_set_filter: not opened or not inited")
		elif value < 1 or value > 6:
			self.error.append(f"cmd_set_filter: '{value}' out of range [1:6]")
		else:
			cmd = "FILTER"
			cmdf = f"{cmd} {value}"
			self.write(cmdf)
			r = self.read()
			self.error.append(f"cmd_set_filter: '{r}' returned")

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
			self.error.append(f"cmd_set_exitport: '{r}' returned")

	# === EXPORT ===

	def shutter_open(self):
		i = self.cmd_get_port()
		i = (i & 16) >> 4
		if i == 0:
			self.cmd_set_port(1)

	def shutter_close(self):
		i = self.cmd_get_port()
		i = (i & 16) >> 4
		if i == 1:
			self.cmd_set_port(0)

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

	def set_wl(self, l):
		g = 1
		for i in range(len(self.gl)):
			if l >= self.gl[i]:
				g = i+1
			else:
				break
		
		f = 1
		for i in range(len(self.fl)):
			if l >= self.fl[i]:
				f = i+1
			else:
				break

		self.set_grating(g)
		self.set_filter(f)
		return self.cmd_moveto(l)
