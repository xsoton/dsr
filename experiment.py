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

	start  = Signal(Experiment)
	pause  = Signal()
	resume = Signal()
	stop   = Signal()

	newExpStarted = Signal(int)
	newExpPaused  = Signal(int)
	newExpResumed = Signal(int)
	newExpStoped  = Signal(int)

	def __init__(self, parent=None):
		super(Session, self).__init__(parent)
		self.lock = QReadWriteLock()

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
		e.wl = e.startWl
		self.ids[etype] = new_id
		self.exp[etype].append(e)
		self.dat[etype].append(d)
		self.unlock()
		return new_id

	def updateFromExp(self, etype: int, e: Experiment):
		self.exp[etype][self.ids[etype]].status      = e.status
		self.exp[etype][self.ids[etype]].sampleName  = e.sampleName
		self.exp[etype][self.ids[etype]].startWl     = e.startWl
		self.exp[etype][self.ids[etype]].stopWl      = e.stopWl
		self.exp[etype][self.ids[etype]].stepWl      = e.stepWl
		self.exp[etype][self.ids[etype]].wl          = e.wl
		self.exp[etype][self.ids[etype]].delay       = e.delay
		self.exp[etype][self.ids[etype]].channel     = e.channel
		self.exp[etype][self.ids[etype]].voltageFlag = e.voltageFlag
		self.exp[etype][self.ids[etype]].voltage     = e.voltage
		self.exp[etype][self.ids[etype]].nplc        = e.nplc
		self.exp[etype][self.ids[etype]].averageFlag = e.averageFlag
		self.exp[etype][self.ids[etype]].average     = e.average

	@Slot(int, Experiment)
	def start_slot(self, etype: int, e: Experiment):
		print("start_slot")
		self.new_exp(etype)
		self.updateFromExp(etype, e)
		e = self.exp[etype][self.ids[etype]]
		e.status = 1
		e.dateTime = "???" # GENERATE date
		self.start.emit(e)
		self.newExpStarted.emit(e)

	@Slot(int)
	def pause_slot(self, etype: int):
		print("pause_slot")
		e = self.exp[etype][self.ids[etype]]
		e.status = 2
		self.pause.emit()
		self.newExpPaused.emit(e)

	@Slot(int)
	def resume_slot(self, etype: int):
		print("resume_slot")
		e = self.exp[etype][self.ids[etype]]
		e.status = 1
		self.resume.emit()
		self.newExpResumed.emit(e)

	@Slot(int)
	def stop_slot(self, etype: int):
		print("stop_slot")
		e = self.exp[etype][self.ids[etype]]
		e.status = 3
		self.stop.emit()
		self.newExpStoped.emit(e)
