from typing import Self
from PySide6.QtCore import QObject, QReadWriteLock, Signal, Slot, QDateTime, QTimer

class Experiment(QObject):
	type: int = 0 # 0 - Si, 1 - InGaAs, 2 - Sample
	status: int = 0 # 0 - idle, 1 - started, 2 - paused, 3 - ended
	dateTime: str = ""
	currentWl: float = 300
	steps: int = 0
	
	sampleName: str = ""
	startWl: float = 300.0
	stopWl: float = 2000.0
	stepWl: float = 5.0
	delay: float = 0.0
	channel: int = 1
	voltageFlag: bool = False
	voltage: float = 0.0
	nplc: int = 1
	averageFlag: bool = False
	average: int = 1

	data = []

	started     = Signal()
	paused      = Signal()
	resumed     = Signal()
	stoped      = Signal()
	dataChanged = Signal()

	# test!!!
	dataGenerated = Signal(float, float)

	def __init__(self, etype: int, parent=None):
		super(Experiment, self).__init__(parent)
		self.type = etype
		self.lock = QReadWriteLock()
		self.reset()
		# test!!!
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.dataGenerate)
		self.dataGenerated.connect(self.dataAdd)

	def rlock(self):
		self.lock.lockForRead()

	def wlock(self):
		self.lock.lockForWrite()

	def unlock(self):
		self.lock.unlock()

	def fill(self, e: Self):
		self.sampleName  = e.sampleName
		self.startWl     = e.startWl
		self.stopWl      = e.stopWl
		self.stepWl      = e.stepWl
		self.delay       = e.delay
		self.channel     = e.channel
		self.voltageFlag = e.voltageFlag
		self.voltage     = e.voltage
		self.nplc        = e.nplc
		self.averageFlag = e.averageFlag
		self.average     = e.average
		self.currentWl   = e.startWl

	def reset(self):
		if self.type == 0:
			self.sampleName  = "Si"
			self.startWl     = 300
			self.stopWl      = 1100
			self.stepWl      = 5
			self.delay       = 0
			self.channel     = 2
			self.voltageFlag = False
			self.voltage     = 0
			self.nplc        = 1
			self.averageFlag = False
			self.average     = 1
			self.currentWl   = self.startWl
		elif self.type == 1:
			self.sampleName  = "InGaAs"
			self.startWl     = 900
			self.stopWl      = 1700
			self.stepWl      = 10
			self.delay       = 0
			self.channel     = 2
			self.voltageFlag = False
			self.voltage     = 0
			self.nplc        = 1
			self.averageFlag = False
			self.average     = 1
			self.currentWl   = self.startWl
		elif self.type == 2:
			self.sampleName  = ""
			self.startWl     = 300
			self.stopWl      = 2000
			self.stepWl      = 5
			self.delay       = 0
			self.channel     = 1
			self.voltageFlag = False
			self.voltage     = 0
			self.nplc        = 1
			self.averageFlag = False
			self.average     = 1
			self.currentWl   = self.startWl

	@Slot()
	def start(self):
		self.status = 1
		self.dateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		# test!!!
		self.timer.start(1000)
		# end test!!!
		self.started.emit()

	@Slot()
	def pause(self):
		self.status = 2
		# test!!!
		self.timer.stop()
		# test!!!
		self.paused.emit()

	@Slot()
	def resume(self):
		self.status = 1
		# test!!!
		self.timer.start(1000)
		# test!!!
		self.resumed.emit()

	@Slot()
	def stop(self):
		self.status = 3
		# test!!!
		self.timer.stop()
		# test!!!
		self.stoped.emit()

	@Slot(float, float)
	def dataAdd(self, wl: float, current: float):
		self.wlock()
		self.data.append([wl, current])
		self.unlock()
		self.currentWl = wl
		self.dataChanged.emit()

	# test!!!
	@Slot()
	def dataGenerate(self):
		print(f"dataGenerate")
		if self.status > 2:
			return
		if self.steps == 0:
			self.currentWl = self.startWl
		if self.startWl > self.stopWl:
			d = -1
		else:
			d = 1
		wl = self.currentWl + d * self.stepWl
		if (d == 1 and wl > self.stopWl) or (d == -1 and wl < self.stopWl):
			self.stop()
			return
		else:
			self.currentWl = wl
			self.steps = self.steps + 1
		I = 1e-9 * (wl-self.startWl)/(self.stopWl-self.startWl)
		self.dataGenerated.emit(wl, I)
