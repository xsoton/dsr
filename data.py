from typing import Self, List
from dataclasses import dataclass
import time
import json
from PySide6.QtCore import (
	Qt, QObject, QReadWriteLock, Signal, Slot,
	QDateTime, QTimer, QDir, QFile, QIODevice
)
from device_dsr import DSR
from device_k6482 import K6482

# e = {
# 	"type": 0,
# 	"status": 0,
# 	"dateTime": "",
# 	"fileName": "",
# 	"steps": 0,
# 	"currentWl": 0,
# 	"sampleName": "",
# 	"startWl": 200,
# 	"stopWl": 2000,
# 	"stepWl": 5,
# 	"delay": 0,
# 	"channel": 1,
# 	"voltageFlag": 0,
# 	"voltage": 0,
# 	"nplc": 1,
# 	"averageFlag": 0,
# 	"average": 1,
# 	"x": [],
# 	"y": []
# }

class Controller(QObject):
	started     = Signal()
	paused      = Signal()
	resumed     = Signal()
	stoped      = Signal()
	dataChanged = Signal()

	def __init__(self, dsr: DSR, k6482: K6482, parent=None):
		super(Controller, self).__init__(parent)
		self.dsr = dsr
		self.k6482 = k6482

		self.lock = QReadWriteLock()

		self.sig_next_point = Signal()
		self.sig_next_point.connect(self.next_point, Qt.QueuedConnection)

	def rlock(self):
		self.lock.lockForRead()

	def wlock(self):
		self.lock.lockForWrite()

	def unlock(self):
		self.lock.unlock()

	def newExperiment(self, type: int):
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

	@Slot(Dict)
	def onStart(self, e: Dict):
		self.e = e
		self.e["status"] = 1
		self.e["dateTime"] = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		self.e["fileName"] = f"{self.e["dateTime"]}_{self.e["sampleName"]}.json"

		# set parameters
		self.k6482.set_channel(e["channel"])
		self.k6482.set_output(e["voltageFlag"])
		self.k6482.set_voltage(e["voltage"])
		self.k6482.set_nplc(e["nplc"])
		self.k6482.set_averageFlag(e["averageFlag"])
		self.k6482.set_average(e["average"])

		# signaling
		self.sig_next_point.emit()
		self.started.emit()

	@Slot()
	def onPause(self):
		self.e["status"] = 2
		self.paused.emit()

	@Slot()
	def onResume(self):
		self.e["status"] = 1
		self.sig_next_point.emit()
		self.resumed.emit()

	@Slot()
	def onStop(self):
		e = self.e
		e["status"] = 3
		with open(e["fileName"], "w") as f:
			json.dump(e, f, indent="\t")
		self.stoped.emit()

	@Slot()
	def next_point(self):
		e = self.e
		if e["status"] == 1:
			d = -1 if e["startWl"] > e["stopWl"] else 1
			wl = e["startWl"] + d * e["stepWl"] * e["steps"]
			if (d == 1 and wl > e["stopWl"]) or (d == -1 and wl < e["stopWl"]):
				self.onStop()
			else:
				wl = self.dsr.setWl(wl)
				er = self.dsr.get_error()
				if len(er) > 0:
					print(f"next_point DSR error: {er}")
					self.dsr.clear_error()
				e["currentWl"] = wl

				time.sleep(e["delay"])
				
				current = self.k6482.get_current()
				er = self.k6482.get_error()
				if len(er) > 0:
					print(f"next_point K6482 error: {er}")
					self.k6482.clear_error()
				
				e["steps"] = e["steps"] + 1
				self.wlock()
				e["x"].append(wl)
				e["y"].append(current)
				self.unlock()
				self.dataChanged.emit()
				self.sig_next_point.emit()
