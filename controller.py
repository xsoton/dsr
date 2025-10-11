from typing import Self, List
from dataclasses import dataclass
import time
import json
from enum import Enum
from PySide6.QtCore import Qt, QObject, QReadWriteLock, Signal, Slot, QDateTime, QTimer
from device_dsr import DSR
from device_k6482 import K6482

class RespState(Enum):
	NEXT = 1
	STEP = 2

class RespController(QObject):
	debug = False

	startDone   = Signal()
	pauseDone   = Signal()
	resumeDone  = Signal()
	stopDone    = Signal()
	dataChanged = Signal()

	next_point = Signal()

	e: dict

	def __init__(self, dsr: DSR, k6482: K6482, parent=None):
		super(RespController, self).__init__(parent)

		self.dsr = dsr
		self.k6482 = k6482

		self.lock = QReadWriteLock()
		self.e = {}
		self.startedFlag = False

		self.next_point.connect(self.next_point, Qt.QueuedConnection)

	def rlock(self) : self.lock.lockForRead()
	def wlock(self) : self.lock.lockForWrite()
	def unlock(self): self.lock.unlock()

	@Slot()
	def start(self):
		if self.debug: print(f"RespController -> start")
		e = self.e
		e["status"] = 1
		e["dateTime"] = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		e["fileName"] = f"{e["dateTime"]}_{e["sampleName"]}.json"

		self.startedFlag = True

		# signaling
		self.next_point.emit()
		self.startDone.emit()

	@Slot()
	def pause(self):
		if self.debug: print(f"RespController -> pause")
		if self.startedFlag:
			self.e["status"] = 2
			self.pauseDone.emit()

	@Slot()
	def resume(self):
		if self.debug: print(f"RespController -> resume")
		if self.startedFlag:
			self.e["status"] = 1
			self.next_point.emit()
			self.resumeDone.emit()

	@Slot()
	def stop(self):
		if self.debug: print(f"RespController -> stop")
		if self.startedFlag:
			e = self.e
			e["status"] = 3
			with open(e["fileName"], "w") as f:
				json.dump(e, f, indent="\t")
			self.stopDone.emit()

	@Slot()
	def next_point(self):
		if self.debug: print(f"RespController -> next_point")
		e = self.e
		if e["status"] == 1:
			d = -1 if e["startWl"] > e["stopWl"] else 1
			wl = e["startWl"] + d * e["stepWl"] * e["steps"]
			if (d == 1 and wl > e["stopWl"]) or (d == -1 and wl < e["stopWl"]):
				self.stop()
			else:
				wl = self.dsr.setWl(wl)
				time.sleep(e["delay"])
				current = self.k6482.getCurrent()

				e["currentWl"] = wl
				e["steps"] = e["steps"] + 1
				self.wlock()
				e["x"].append(wl)
				e["y"].append(current)
				self.unlock()
				self.dataChanged.emit()
				self.next_point.emit()

class TimeState(Enum):
	NEXT = 1
	STEP = 2

class TimeController(QObject):
	debug = False

	startDone   = Signal()
	pauseDone   = Signal()
	resumeDone  = Signal()
	stopDone    = Signal()
	dataChanged = Signal()

	next_point = Signal()

	e: dict

	state: TimeState
	start_time: int
	time_stage: int
	time: int


	def __init__(self, dsr: DSR, k6482: K6482, parent=None):
		super(TimeController, self).__init__(parent)

		self.dsr = dsr
		self.k6482 = k6482

		self.lock = QReadWriteLock()
		self.e = {}
		self.startedFlag = False
		self.state = TimeState.NEXT
		self.start_time = 0
		self.time_stage = 0

		self.next_point.connect(self.next_point, Qt.QueuedConnection)

	def rlock(self):
		self.lock.lockForRead()

	def wlock(self):
		self.lock.lockForWrite()

	def unlock(self):
		self.lock.unlock()

	def newExperiment(self):
		if self.debug: print(f"TimeController -> newExperiment")
		e = {}
		e["sampleName"]  = ""
		e["script"]      = [] # of {"t": 20, "V": 0.3, "wl": 550, "sh": True}
		e["channel"]     = 1
		e["voltageFlag"] = False
		e["voltage"]     = 0
		e["nplc"]        = 1
		e["averageFlag"] = False
		e["average"]     = 1
		e["type"]        = 3
		e["status"]      = 0
		e["dateTime"]    = ""
		e["fileName"]    = ""
		e["stage"]       = 0
		e["time"]        = 0.0
		e["duration"]    = 1.0
		e["t"]  = []
		e["I"]  = []
		return e

	@Slot()
	def start(self):
		if self.debug: print(f"TimeController -> start")
		e = self.e
		e["status"] = 1
		e["dateTime"] = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		e["fileName"] = f"{e["dateTime"]}_{e["sampleName"]}.json"

		self.startedFlag = True
		self.state = TimeState.NEXT
		self.start_time = 0
		self.time_stage = 0
		e["stage"] = 0
		e["duration"] = 0.0
		for es in e["script"]:
			e["duration"] = e["duration"] + es["t"]

		# signaling
		self.next_point.emit()
		self.startDone.emit()

	@Slot()
	def pause(self):
		if self.debug: print(f"TimeController -> pause")
		if self.startedFlag:
			self.e["status"] = 2
			self.pauseDone.emit()

	@Slot()
	def resume(self):
		if self.debug: print(f"TimeController -> resume")
		if self.startedFlag:
			self.e["status"] = 1
			self.next_point.emit()
			self.resumeDone.emit()

	@Slot()
	def stop(self):
		if self.debug: print(f"TimeController -> stop")
		if self.startedFlag:
			self.startedFlag = False
			e = self.e
			e["status"] = 3
			self.state = TimeState.NEXT
			with open(e["fileName"], "w") as f:
				json.dump(e, f, indent="\t")
			self.stopDone.emit()

	@Slot()
	def next_point(self):
		if self.debug: print(f"TimeController -> next_point {self.state}")
		e = self.e
		if e["status"] == 1:
			if self.state == TimeState.NEXT:
				if e["stage"] < len(e["script"]):
					self.dsr.setWl(e["script"][e["stage"]]["wl"])
					self.dsr.setShutter(e["script"][e["stage"]]["sh"])
					if e["script"][e["stage"]]["V"] != 0.0:
						self.k6482.setVoltageFlag(True)
						self.k6482.setVoltage(e["script"][e["stage"]]["V"])
					self.state = TimeState.STEP
					self.next_point.emit()
				else:
					self.stop()
			elif self.state == TimeState.STEP:
				if self.debug: print(f"{self.start_time=}")
				if self.start_time == 0:
					self.start_time = QDateTime.currentMSecsSinceEpoch()
					e["time"] = 0
				else:
					e["time"] = (QDateTime.currentMSecsSinceEpoch() - self.start_time) * 1e-3

				if self.debug: print(f"{e["time"]=}")
				if e["time"] - self.time_stage > e["script"][e["stage"]]["t"]:
					self.time_stage = self.time_stage + e["script"][e["stage"]]["t"]
					e["stage"] = e["stage"] + 1
					self.state = TimeState.NEXT
					self.next_point.emit()
				else:
					self.wlock()
					e["t"] .append(e["time"])
					e["I"] .append(self.k6482.getCurrent())
					self.unlock()
					self.dataChanged.emit()
					self.next_point.emit()
