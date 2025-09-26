import serial
import time

class DSR():
	
	is_opened = 0
	is_inited = 0
	error = ""
	gl = [100.0, 300.0, 1100.0]
	fl = [100.0, 450.0, 600.0, 800.0, 1400.0, 2000.0]

	def __init__(self, filename):
		self.filename = filename

	def open(self):
		self.s = serial.Serial(self.filename, timeout=100)
		self.is_opened = 1
		self.hello()
	
	def close(self):
		if self.is_opened == 0:
			return
		self.s.close()

	def write(self, cmd):
		if self.is_opened == 0:
			return
		buf = f"{cmd}\r".encode()
		print(f"#SEND: {buf}")
		self.s.write(buf)
		self.s.flush()

	def read(self):
		if self.is_opened == 0:
			return ""
		r = self.s.read_until(expected = b'\r', size = 100)
		print(f"#RECV: {r}")
		return r[:-1].decode()

	def hello(self):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return
		
		cmd = "HELLO"
		
		for i in range(2):
			self.write(cmd)
			r = self.read()
			self.error = r
			if r == "OK":
				self.is_inited = 1
				break
			else:
				self.is_inited = 0
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return

	def systeminfo(self):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return ""
		
		cmd = "SYSTEMINFO?"
		cmd_len = len(cmd)-1
		ret = ""
		
		self.write(cmd)
		r = self.read()
		if r[:cmd_len] == cmd[:cmd_len]:
			ret = r
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def get_info(self, addr):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return -1
		if addr < 0 or addr > 1022:
			self.error = "OUT OF RANGE"
			return -1
		
		cmd = "SAVEINFO?"
		cmd_len = len(cmd)-1
		cmdf = f"{cmd} {addr}"
		cut_len = len(cmdf)

		ret = -1
		
		self.write(cmdf)
		r = self.read()
		if r[:cmd_len] == cmd[:cmd_len]:
			ret = int(r[cut_len:])
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def set_info(self, addr, value):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return
		if addr < 0 or addr > 1022:
			self.error = "OUT OF RANGE"
			return
		if value < 0 or value > 255:
			self.error = "OUT OF RANGE"
			return
		
		cmd = "SAVEINFO"
		cmdf = f"{cmd} {addr},{value}"
		
		self.write(cmdf)
		r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return

	def get_port(self):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return -1
		
		cmd = "PORT_INPUT?"
		cmd_len = len(cmd)-1
		cut_len = cmd_len+1

		ret = -1
		
		self.write(cmd)
		r = self.read()
		if r[:cmd_len] == cmd[:cmd_len]:
			ret = int(r[cut_len:])
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def set_port(self, value):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return
		if value < 0 or value > 15:
			self.error = "OUT OF RANGE"
			return
		
		cmd = "PORT_OUTPUT"
		cmdf = f"{cmd} {value}"
		
		self.write(cmdf)
		r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return

	def get_grating(self):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return -1
		
		cmd = "GRATING?"
		cmd_len = len(cmd)-1
		cut_len = cmd_len+1

		ret = -1
		
		self.write(cmd)
		r = self.read()
		if r[:cmd_len] == cmd[:cmd_len]:
			ret = int(r[cut_len:])
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def set_grating(self, value):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return
		if value < 1 or value > 3:
			self.error = "OUT OF RANGE"
			return
		
		cmd = "GRATING"
		cmdf = f"{cmd} {value}"
		
		self.write(cmdf)
		r = self.read()
		if r == "0":
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return

	def get_position(self):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return -1
		
		cmd = "POSITION?"
		cmd_len = len(cmd)-1
		cut_len = cmd_len+1

		ret = -1.0
		
		self.write(cmd)
		r = self.read()
		if r[:cmd_len] == cmd[:cmd_len]:
			ret = float(r[cut_len:])
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def moveto(self, value):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return -1.0
		if value < 200.0 or value > 2000.0:
			self.error = "OUT OF RANGE"
			return -1.0
		
		cmd = "MOVETO"
		cmdf = f"{cmd} {value}"

		ret = -1.0
		
		self.write(cmdf)
		r = self.read()
		if (r[0] != "O") and (r[0] != "E"):
			ret = float(r)
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def move(self, value):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return -1.0
		if value > 2000.0:
			self.error = "OUT OF RANGE"
			return -1.0
		
		cmd = "MOVE"
		cmdf = f"{cmd} {value}"

		ret = -1.0
		
		self.write(cmdf)
		r = self.read()
		ret = float(r)
		r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def get_filter(self):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return -1
		
		cmd = "FILTER?"
		cmd_len = len(cmd)-1
		cut_len = cmd_len+1

		ret = -1
		
		self.write(cmd)
		r = self.read()
		if r[:cmd_len] == cmd[:cmd_len]:
			ret = int(r[cut_len:])
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def set_filter(self, value):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return
		if value < 1 or value > 6:
			self.error = "OUT OF RANGE"
			return
		
		cmd = "FILTER"
		cmdf = f"{cmd} {value}"
		
		self.write(cmdf)
		r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return

	def get_exitport(self):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return -1
		
		cmd = "EXITPORT?"
		cmd_len = len(cmd)-1
		cut_len = cmd_len+1

		ret = -1
		
		self.write(cmd)
		r = self.read()
		if r[:cmd_len] == cmd[:cmd_len]:
			ret = int(r[cut_len:])
			r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return ret

	def set_exitport(self, value):
		if self.is_opened == 0:
			self.error = "NOT OPENED"
			return
		if value < 0 or value > 1:
			self.error = "OUT OF RANGE"
			return
		
		cmd = "EXITPORT"
		cmdf = f"{cmd} {value}"
		
		self.write(cmdf)
		r = self.read()
		self.error = r
		
		if self.error != "OK":
			print(f"# Error: command '{cmd}' returned {self.error}")

		return

	# ====================================================

	def shutter_open(self):
		i = self.get_port()
		i = (i & 16) >> 4
		if i == 0:
			self.set_port(1)

	def shutter_close(self):
		i = self.get_port()
		i = (i & 16) >> 4
		if i == 1:
			self.set_port(0)

	def grating(self, g):
		i = self.get_grating()
		if i != g:
			self.set_grating(g)

	def filter(self, f):
		i = self.get_filter()
		if i != f:
			self.set_filter(f)

	def exitport(self, ep):
		i = self.get_exitport()
		if i != ep:
			self.set_exitport(ep)

	def wl(self, l):
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

		self.grating(g)
		self.filter(f)
		r = self.moveto(l)
		return r



	


dsr = DSR('/dev/ttyUSB0')

dsr.open()

l = dsr.wl(500)
print(l)

dsr.close()
