from typing import Self, List
from dataclasses import dataclass
import time
import json
from enum import Enum
from PySide6.QtCore import Qt, QObject, QReadWriteLock, Signal, Slot, QDateTime, QTimer
from device_dsr import DSR
from device_k6482 import K6482

class RespController(QObject):
	debug = False

	started     = Signal()
	paused      = Signal()
	resumed     = Signal()
	stoped      = Signal()
	dataChanged = Signal()

	sig_next_point = Signal()

	e: dict

	def __init__(self, dsr: DSR, k6482: K6482, parent=None):
		super(RespController, self).__init__(parent)

		self.dsr = dsr
		self.k6482 = k6482

		self.lock = QReadWriteLock()
		self.e = {}
		self.startedFlag = False

		self.sig_next_point.connect(self.next_point, Qt.QueuedConnection)

	def rlock(self):
		self.lock.lockForRead()

	def wlock(self):
		self.lock.lockForWrite()

	def unlock(self):
		self.lock.unlock()

	def newExperiment(self, type: int):
		if self.debug: print(f"RespController -> newExperiment {type}")
		e = {}
		if type == 0:
			e["sampleName"]  = "Si"
			e["startWl"]     = 300
			e["stopWl"]      = 1100
			e["stepWl"]      = 5
			e["channel"]     = 2
		elif type == 1:
			e["sampleName"]  = "InGaAs"
			e["startWl"]     = 900
			e["stopWl"]      = 1700
			e["stepWl"]      = 10
			e["channel"]     = 2
		elif type == 2:
			e["sampleName"]  = ""
			e["startWl"]     = 300
			e["stopWl"]      = 2000
			e["stepWl"]      = 5
			e["channel"]     = 1
		e["delay"]       = 0
		e["voltageFlag"] = False
		e["voltage"]     = 0
		e["nplc"]        = 1
		e["averageFlag"] = False
		e["average"]     = 1
		e["type"]      = type
		e["status"]    = 0
		e["dateTime"]  = ""
		e["fileName"]  = ""
		e["steps"]     = 0
		e["currentWl"] = e["startWl"]
		e["x"] = []
		e["y"] = []
		return e

	@Slot()
	def onStart(self):
		if self.debug: print(f"RespController -> onStart")
		e = self.e
		e["status"] = 1
		e["dateTime"] = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		e["fileName"] = f"{e["dateTime"]}_{e["sampleName"]}.json"

		self.startedFlag = True

		# signaling
		self.sig_next_point.emit()
		self.started.emit()

	@Slot()
	def onPause(self):
		if self.debug: print(f"RespController -> onPause")
		if self.startedFlag:
			self.e["status"] = 2
			self.paused.emit()

	@Slot()
	def onResume(self):
		if self.debug: print(f"RespController -> onResume")
		if self.startedFlag:
			self.e["status"] = 1
			self.sig_next_point.emit()
			self.resumed.emit()

	@Slot()
	def onStop(self):
		if self.debug: print(f"RespController -> onStop")
		if self.startedFlag:
			e = self.e
			e["status"] = 3
			with open(e["fileName"], "w") as f:
				json.dump(e, f, indent="\t")
			self.stoped.emit()

	@Slot()
	def next_point(self):
		if self.debug: print(f"RespController -> next_point")
		e = self.e
		if e["status"] == 1:
			d = -1 if e["startWl"] > e["stopWl"] else 1
			wl = e["startWl"] + d * e["stepWl"] * e["steps"]
			if (d == 1 and wl > e["stopWl"]) or (d == -1 and wl < e["stopWl"]):
				self.onStop()
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
				self.sig_next_point.emit()

class TimeState(Enum):
	NEXT = 1
	STEP = 2

class TimeController(QObject):
	debug = True

	started     = Signal()
	paused      = Signal()
	resumed     = Signal()
	stoped      = Signal()
	dataChanged = Signal()

	sig_next_point = Signal()

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

		self.sig_next_point.connect(self.next_point, Qt.QueuedConnection)

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
		e["duration"]    = 0.0
		e["t"]  = []
		e["I"]  = []
		e["V"]  = []
		e["wl"] = []
		e["sh"] = []
		return e

	@Slot()
	def onStart(self):
		if self.debug: print(f"TimeController -> onStart")
		e = self.e
		e["status"] = 1
		e["dateTime"] = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		e["fileName"] = f"{e["dateTime"]}_{e["sampleName"]}.json"

		self.startedFlag = True
		self.state = TimeState.NEXT
		self.start_time = 0
		self.time_stage = 0
		e["stage"] = 0
		for es in e["script"]:
			e["duration"] = e["duration"] + es["t"]

		# signaling
		self.sig_next_point.emit()
		self.started.emit()

	@Slot()
	def onPause(self):
		if self.debug: print(f"TimeController -> onPause")
		if self.startedFlag:
			self.e["status"] = 2
			self.paused.emit()

	@Slot()
	def onResume(self):
		if self.debug: print(f"TimeController -> onResume")
		if self.startedFlag:
			self.e["status"] = 1
			self.sig_next_point.emit()
			self.resumed.emit()

	@Slot()
	def onStop(self):
		if self.debug: print(f"TimeController -> onStop")
		if self.startedFlag:
			self.startedFlag = False
			e = self.e
			e["status"] = 3
			self.state = TimeState.NEXT
			with open(e["fileName"], "w") as f:
				json.dump(e, f, indent="\t")
			self.stoped.emit()

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
					self.sig_next_point.emit()
				else:
					self.onStop()
			elif self.state == TimeState.STEP:
				if self.start_time == 0:
					self.start_time = QDateTime.currentMSecsSinceEpoch()
					e["time"] = 0
				else:
					e["time"] = QDateTime.currentMSecsSinceEpoch() - self.start_time

				if e["time"] - self.time_stage > e["script"][e["stage"]]["t"]:
					e["stage"] = e["stage"] + 1
					self.time_stage = self.time_stage + e["script"][e["stage"]]["t"]
					self.state = TimeState.NEXT
					self.sig_next_point.emit()
				else:
					self.wlock()
					e["t"] .append(e["time"])
					e["V"] .append(self.k6482.getVoltage())
					e["wl"].append(self.dsr.getWl())
					e["sh"].append(self.dsr.getShutter())
					s["I"] .append(self.k6482.getCurrent())
					self.unlock()
					self.dataChanged.emit()
					self.sig_next_point.emit()
