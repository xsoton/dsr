from PySide6.QtCore import QObject, QReadWriteLock, Signal, Slot

class Experiment():
	status: int = 0 # 0 - idle, 1 - started, 2 - paused, 3 - ended
	
	sampleName: str = ""
	dateTime: str = ""
	startWl: float = 300.0
	stopWl: float = 2000.0
	stepWl: float = 5.0
	wl: float = 300
	delay: float = 0.0
	channel: int = 1
	voltageFlag: bool = False
	voltage: float = 0.0
	nplc: int = 1
	averageFlag: bool = False
	average: int = 1

	def __init__(self):
		self.lock = QReadWriteLock()

	def rlock(self):
		self.lock.lockForRead()

	def wlock(self):
		self.lock.lockForWrite()

	def unlock(self):
		self.lock.unlock()

class Data():
	data = []

	def __init__(self):
		self.lock = QReadWriteLock()

	def rlock(self):
		self.lock.lockForRead()

	def wlock(self):
		self.lock.lockForWrite()

	def unlock(self):
		self.lock.unlock()

	def addPoint(self, x, y):
		self.data.append([x, y])


class Session(QObject):
	ids = [-1, -1, -1]
	exp = [[], [], []]
	dat = [[], [], []]

	expChanged = Signal()
	datChanged = Signal()

	def __init__(self, parent=None):
		super(Session, self).__init__(parent)
		self.lock = QReadWriteLock()
		self.new_exp(0)
		self.new_exp(1)
		self.new_exp(2)

	def rlock(self):
		self.lock.lockForRead()

	def wlock(self):
		self.lock.lockForWrite()

	def unlock(self):
		self.lock.unlock()

	def new_exp(self, etype: int):
		print("new_exp")
		if etype < 0 or etype > 2:
			return -1
		self.wlock()
		new_id = len(self.exp[etype])
		e = Experiment()
		d = Data()
		if etype == 0:
			e.sampleName = "Si"
			e.startWl = 300
			e.stopWl = 1100
			e.stepWl = 5
			e.channel = 2
		elif etype == 1:
			e.sampleName = "InGaAs"
			e.startWl = 900
			e.stopWl = 1700
			e.stepWl = 10
			e.channel = 2
		elif etype == 2:
			e.sampleName = ""
			e.startWl = 300
			e.stopWl = 2000
			e.stepWl = 5
			e.channel = 1
		e.wl = e.startWl
		self.dat[etype].append(d)
		self.exp[etype].append(e)
		self.ids[etype] = new_id
		self.unlock()
		return new_id

	def get_id(self, etype: int):
		if (etype < 0) or (etype > 2):
			return -1
		self.rlock()
		i = self.ids[etype]
		self.unlock()
		return i

	def set_id(self, etype: int, id: int):
		if (etype < 0) or (etype > 2) or (id < 0) or (id >= len(self.exp[etype])):
			return
		self.wlock()
		ids[etype] = id
		self.unlock()

	def get_exp(self, etype: int):
		if (etype < 0) or (etype > 2):
			return None
		if (self.ids[etype] < 0) or (self.ids[etype] >= len(self.exp[etype])):
			return None
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		return e

	def get_dat(self, etype: int):
		if (etype < 0) or (etype > 2):
			return None
		if (self.ids[etype] < 0) or (self.ids[etype] >= len(self.dat[etype])):
			return None
		self.rlock()
		e = self.dat[etype][self.ids[etype]]
		self.unlock()
		return d

	@Slot(int)
	def new_slot(self, etype: int):
		print("new_slot")
		self.new_exp(etype)
		self.expChanged.emit()

	@Slot(int)
	def start_slot(self, etype: int):
		print("start_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.status = 1
		e.unlock()
		self.expChanged.emit()

	@Slot(int)
	def pause_slot(self, etype: int):
		print("pause_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.status = 2
		e.unlock()
		self.expChanged.emit()

	@Slot(int)
	def resume_slot(self, etype: int):
		print("resume_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.status = 1
		e.unlock()
		self.expChanged.emit()

	@Slot(int)
	def stop_slot(self, etype: int):
		print("stop_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.status = 3
		e.unlock()
		self.expChanged.emit()

	@Slot(int, str)
	def newSampleName_slot(self, etype: int, sampleName: str):
		print("newSampleName_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.sampleName = sampleName
		e.unlock()
		self.expChanged.emit()

	@Slot(int, float)
	def newStartWl_slot(self, etype: int, startWl: float):
		print("newStartWl_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.startWl = startWl
		e.unlock()
		self.expChanged.emit()

	@Slot(int, float)
	def newStopWl_slot(self, etype: int, stopWl: float):
		print("newStopWl_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.stopWl = stopWl
		e.unlock()
		self.expChanged.emit()

	@Slot(int, float)
	def newStepWl_slot(self, etype: int, stepWl: float):
		print("newStepWl_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.stepWl = stepWl
		e.unlock()
		self.expChanged.emit()

	@Slot(int, float)
	def newDelay_slot(self, etype: int, delay: float):
		print("newDelay_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.delay = delay
		e.unlock()
		self.expChanged.emit()

	@Slot(int, int)
	def newChannel_slot(self, etype: int, channel: int):
		print("newChannel_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.channel = channel
		e.unlock()
		self.expChanged.emit()

	@Slot(int, bool)
	def newVoltageFlag_slot(self, etype: int, voltageFlag: bool):
		print("newVoltageFlag_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.voltageFlag = voltageFlag
		e.unlock()
		self.expChanged.emit()

	@Slot(int, float)
	def newVoltage_slot(self, etype: int, voltage: float):
		print("newVoltage_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.voltage = voltage
		e.unlock()
		self.expChanged.emit()

	@Slot(int, int)
	def newNplc_slot(self, etype: int, nplc: int):
		print("newNplc_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.nplc = nplc
		e.unlock()
		self.expChanged.emit()

	@Slot(int, bool)
	def newAverageFlag_slot(self, etype: int, averageFlag: bool):
		print("newAverageFlag_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.averageFlag = averageFlag
		e.unlock()
		self.expChanged.emit()

	@Slot(int, int)
	def newAverage_slot(self, etype: int, average: int):
		print("newAverage_slot")
		self.rlock()
		e = self.exp[etype][self.ids[etype]]
		self.unlock()
		e.wlock()
		e.average = average
		e.unlock()
		self.expChanged.emit()

	@Slot(float)
	def setWl_slot(self, wl: float):
		print("setWl_slot")

	@Slot(bool)
	def setShutter_slot(self, shutter: bool):
		print("setShutter_slot")
