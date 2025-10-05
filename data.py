from typing import Self, List
from dataclasses import dataclass
import time
from PySide6.QtCore import (Qt, QObject, QReadWriteLock, Signal, Slot,
	QDateTime, QTimer, QDir, QFile, QIODevice)
from device_dsr import DSR
from device_k6482 import K6482

class Experiment(QObject):
	type: int = 0 # 0 - Si, 1 - InGaAs, 2 - Sample
	status: int = 0 # 0 - idle, 1 - started, 2 - paused, 3 - ended
	dateTime: str = ""
	filename: str = ""
	steps: int = 0
	currentWl: float = 300.0

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

	started     = Signal()
	paused      = Signal()
	resumed     = Signal()
	stoped      = Signal()
	dataChanged = Signal()
	setWlDone   = Signal(float)

	sig_next_point  = Signal()

	def __init__(self, etype: int, dsr: DSR, k6482: K6482, parent=None):
		super(Experiment, self).__init__(parent)
		self.type = etype
		self.status = 0
		self.dateTime = ""
		self.data = [[], []]
		self.dsr = dsr
		self.k6482 = k6482

		self.lock = QReadWriteLock()
		self.reset()

		self.sig_next_point.connect(self.next_point, Qt.QueuedConnection)

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
		self.steps       = 0

	def reset(self):
		if self.type == 0:
			self.sampleName  = "Si"
			self.startWl     = 300
			self.stopWl      = 1100
			self.stepWl      = 5
			self.channel     = 2
		elif self.type == 1:
			self.sampleName  = "InGaAs"
			self.startWl     = 900
			self.stopWl      = 1700
			self.stepWl      = 10
			self.channel     = 2
		elif self.type == 2:
			self.sampleName  = ""
			self.startWl     = 300
			self.stopWl      = 2000
			self.stepWl      = 5
			self.channel     = 1
		self.delay       = 0
		self.voltageFlag = False
		self.voltage     = 0
		self.nplc        = 1
		self.averageFlag = False
		self.average     = 1
		self.currentWl   = self.startWl
		self.steps       = 0

	@Slot()
	def onSetWl(self, wl: float):
		wl = self.dsr.set_wl(wl)
		e = self.dsr.get_error()
		if len(e) > 0:
			print("next_point DSR error: {e}")
			self.dsr.clear_error()
		self.setWlDone.emit(wl)

	@Slot()
	def onShutter(self, s: bool):
		if s:
			self.dsr.shutter_open()
		else:
			self.dsr.shutter_close()
		e = self.dsr.get_error()
		if len(e) > 0:
			print("next_point DSR error: {e}")
			self.dsr.clear_error()

	@Slot()
	def onStart(self):
		self.status = 1

		self.dateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		self.fileName = f"{self.dateTime}_{self.sampleName}.dat"
		self.file = QFile(self.fileName)
		self.file.open(QIODevice.ReadWrite)
		self.file.write(f"# DSR600: Spectrum Responsivity Experiment\n".encode())
		self.file.write(f"# dateTime: {self.dateTime}\n".encode())
		self.file.write(f"# sampleName: {self.sampleName}\n".encode())
		self.file.write(f"# startWl: {self.startWl}\n".encode())
		self.file.write(f"# stopWl: {self.stopWl}\n".encode())
		self.file.write(f"# stepWl: {self.stepWl}\n".encode())
		self.file.write(f"# delay: {self.sampleName}\n".encode())
		self.file.write(f"# channel: {self.channel}\n".encode())
		self.file.write(f"# voltageFlag: {self.voltageFlag}\n".encode())
		self.file.write(f"# voltage: {self.voltage}\n".encode())
		self.file.write(f"# nplc: {self.nplc}\n".encode())
		self.file.write(f"# averageFlag: {self.averageFlag}\n".encode())
		self.file.write(f"# average: {self.average}\n".encode())
		self.file.write(f"# Columns:\n".encode())
		self.file.write(f"#   1 - Wavelength, nm\n".encode())
		self.file.write(f"#   2 - Current, A\n".encode())
		self.file.flush()

		# set parameters
		self.k6482.set_channel(self.channel)
		self.k6482.set_output(self.voltageFlag)
		self.k6482.set_voltage(self.voltage)
		self.k6482.set_nplc(self.nplc)
		self.k6482.set_averageFlag(self.averageFlag)
		self.k6482.set_average(self.average)

		self.sig_next_point.emit()

		self.started.emit()

	@Slot()
	def onPause(self):
		self.status = 2
		self.paused.emit()

	@Slot()
	def onResume(self):
		self.status = 1
		self.sig_next_point.emit()
		self.resumed.emit()

	@Slot()
	def onStop(self):
		self.status = 3
		self.file.close()
		self.stoped.emit()

	@Slot()
	def next_point(self):
		if self.status == 1:
			d = -1 if self.startWl > self.stopWl else 1
			wl = self.startWl + d * self.stepWl * self.steps
			if (d == 1 and wl > self.stopWl) or (d == -1 and wl < self.stopWl):
				self.onStop()
			else:
				wl = self.dsr.set_wl(wl)
				e = self.dsr.get_error()
				if len(e) > 0:
					print("next_point DSR error: {e}")
					self.dsr.clear_error()
				self.currentWl = wl

				time.sleep(self.delay)
				
				current = self.k6482.get_current()
				e = self.k6482.get_error()
				if len(e) > 0:
					print("next_point K6482 error: {e}")
					self.k6482.clear_error()
				
				self.steps = self.steps + 1
				self.wlock()
				self.data[0].append(wl)
				self.data[1].append(current)
				self.unlock()
				self.file.write(f"{wl:.2f}\t{current:+.9e}\n".encode())
				self.file.flush()
				self.dataChanged.emit()
				self.sig_next_point.emit()

@dataclass(init=False)
class Data():
	exp: Experiment
	expList: List[Experiment]
	expSelected: int
	expCheckedList = List[int]

	def __init__(self):
		self.exp = None
		self.expList = []
		self.expSelected = -1
		self.expCheckedList = []
