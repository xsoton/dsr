from typing import Self
from PySide6.QtCore import QObject, QReadWriteLock, Signal, Slot, QDateTime

class Experiment(QObject):
	type: int = 0 # 0 - Si, 1 - InGaAs, 2 - Sample
	status: int = 0 # 0 - idle, 1 - started, 2 - paused, 3 - ended
	dateTime: str = ""
	currentWl: float = 300
	
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

	def __init__(self, etype: int, parent=None):
		super(Experiment, self).__init__(parent)
		self.type = etype
		self.lock = QReadWriteLock()
		self.reset()

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

	@Slot()
	def start(self):
		self.status = 1
		self.dateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		# START EXPERIMENT
		self.started.emit()

	@Slot()
	def pause(self):
		self.status = 2
		# PAUSE EXPERIMENT
		self.paused.emit()

	@Slot()
	def resume(self):
		self.status = 1
		# RESUME EXPERIMENT
		self.resumed.emit()

	@Slot()
	def stop(self):
		self.status = 3
		# STOP EXPERIMENT
		self.stoped.emit()

	@Slot(float, float)
	def dataAdd(self, wl: float, current: float):
		self.wlock()
		self.data.append([wl, current])
		self.unlock()
		self.dataChanged.emit()
