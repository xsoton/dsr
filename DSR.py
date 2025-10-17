from typing import List
import time
from PySide6.QtCore import QObject, Signal, Slot
import serial

class DSR(QObject):
	debug = False
	
	opened: bool
	inited: bool
	gl = [100.0, 300.0, 1100.0]
	fl = [100.0, 450.0, 600.0, 800.0, 1400.0, 2000.0]
	g = 0
	f = 0
	sh = False

	error = List[str]

	newWl      = Signal(float)
	newShutter = Signal(bool)

	def __init__(self, filename: str, parent=None):
		super(DSR, self).__init__(parent)
		self.filename = filename
		self.opened = False
		self.inited = False
		self.error = []
		self.g = 0
		self.f = 0
		self.sh = False
		self.sha = False
		self.wl = -1

	def open(self):
		if self.debug: print(f"DSR -> open")
		try:
			self.s = serial.Serial(self.filename, timeout=0.1)
			self.opened = True
		except serial.SerialException as e:
			self.error.append(f"open: {str(e)}")
			self.opened = False
		if self.opened:
			self.s.reset_input_buffer()
			self.s.reset_output_buffer()
			time.sleep(1)
			self.cmd_hello()
	
	def close(self):
		if self.debug: print(f"DSR -> close")
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
			# print(f"DSR write: {buf}")

	def read(self):
		if not self.opened:
			self.error.append("read: not opened")
			return ""
		else:
			# buf = self.s.read_until(expected = b'\r', size = 100)
			while True:
				buf1 = self.s.read(100)
				if len(buf1) > 0:
					buf2 = self.s.read(100)
					break
			buf = buf1 + buf2
			# print(f"DSR read: {buf}")
			return buf.decode().strip().split('\r')

	# === CMD ===

	def cmd_hello(self):
		if not self.opened:
			self.error.append("cmd_hello: not opened")
		else:
			cmd = "HELLO"
			for i in range(2):
				self.write(cmd)
				r = self.read()
				if r[-1] == "OK":
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
			if r[0][:cmd_len] == cmd[:cmd_len]:
				ret = r[0]
				if r[-1] != "OK":
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
			if r[0][:cmd_len] == cmd[:cmd_len]:
				ret = int(r[0][cut_len:])
				if r[-1] != "OK":
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
			if r[-1] != "OK":
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
			if r[0][:cmd_len] == cmd[:cmd_len]:
				ret = int(r[0][cut_len:])
				if r[-1] != "OK":
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
			if r[-1] != "OK":
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
			if r[0][:cmd_len] == cmd[:cmd_len]:
				ret = int(r[0][cut_len:])
				if r[-1] != "OK":
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
			if r[-1] != "OK":
				self.error.append(f"cmd_set_grating: '{r}' returned")
			else:
				self.g = value

	def cmd_get_position(self):
		ret = -1.0
		if not self.opened or not self.inited:
			self.error.append("cmd_get_position: not opened or not inited")
		else:
			cmd = "POSITION?"
			cmd_len = len(cmd)-1
			cut_len = cmd_len+1
			self.write(cmd)
			r = self.read()
			if r[0][:cmd_len] == cmd[:cmd_len]:
				ret = float(r[0][cut_len:])
				if r[-1] != "OK":
					self.error.append(f"cmd_get_position: '{r}' returned")
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
			if (r[0][0] != "O") and (r[0][0] != "E"):
				ret = float(r[0])
				if r[-1] != "OK":
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
			ret = float(r[0])
			if r[-1] != "OK":
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
			if r[0][0] != "F":
				r = r[1:]
			if r[0][:cmd_len] == cmd[:cmd_len]:
				ret = int(r[0][cut_len:])
				if r[-1] != "OK":
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
			if r[-0] != "OK":
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
			if r[0][:cmd_len] == cmd[:cmd_len]:
				ret = int(r[0][cut_len:])
				if r[-1] != "OK":
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
			if r[-1] != "OK":
				self.error.append(f"cmd_set_exitport: '{r}' returned")

	# === EXPORT ===

	def get_shutter(self):
		if self.debug: print(f"DSR -> get_shutter")
		if not self.sha:
			i = self.cmd_get_port()
			i = (i & 16) >> 4
			self.sh = (i == 1)
			self.sha = True
		return self.sh

	def set_shutter(self, sh: bool):
		if self.debug: print(f"DSR -> set_shutter")
		i = self.cmd_get_port()
		i = (i & 16) >> 4
		self.sh = (i == 1)
		if not self.sh and sh:
			self.cmd_set_port(1)
		elif self.sh and not sh:
			self.cmd_set_port(0)
		self.sh = sh
		self.sha = True
		# print(self.error)
		self.clear_error()

	@Slot()
	def getShutter(self):
		if self.debug: print(f"DSR -> getShutter")
		self.get_shutter()
		self.newShutter.emit(self.sh)
		return self.sh

	@Slot(bool)
	def setShutter(self, sh: bool):
		if self.debug: print(f"DSR -> setShutter")
		self.set_shutter(sh)
		self.newShutter.emit(self.sh)

	def set_exitport(self, ep):
		i = self.cmd_get_exitport()
		if i != ep:
			self.cmd_set_exitport(ep)

	def get_wl(self):
		if self.wl < 0:
			self.wl = self.cmd_get_position()
		return self.wl

	@Slot()
	def getWl(self):
		if self.debug: print(f"DSR -> getWl")
		self.get_wl()
		self.newWl.emit(self.wl)
		return self.wl

	@Slot(float)
	def setWl(self, wl: float):
		if self.debug: print(f"DSR -> setWl {wl}")

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

		self.get_shutter()
		sh = self.sh
		self.cmd_get_grating()
		self.cmd_get_filter()

		csh = (self.g != g) or (self.f != f)

		if csh:
			self.set_shutter(False)
		if self.g != g:
			self.cmd_set_grating(g)
		if self.f != f:
			self.cmd_set_filter(f)
		self.wl = self.cmd_moveto(wl)
		if csh:
			self.set_shutter(sh)
		# print(self.error)
		self.clear_error()
		self.newWl.emit(self.wl)
		return self.wl

	def   get_error(self): return self.error
	def clear_error(self): self.error.clear()


if __name__ == '__main__':

	dsr = DSR("/dev/ttyUSB0")
	dsr.open()

	print(dsr.setWl(550))

	dsr.close()
