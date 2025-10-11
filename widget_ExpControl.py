from PySide6.QtCore import (Qt, QTimer, Signal, Slot,
	QRegularExpression, QLocale, QItemSelection, QItemSelectionModel)
from PySide6.QtGui import (QStandardItemModel, QStandardItem,
	QRegularExpressionValidator, QDoubleValidator, QIntValidator)
from PySide6.QtWidgets import QWidget, QFileDialog

from typing import List
from math import *
import os
import json

from ui_expControl import Ui_expControl
from controller import RespController
from device_dsr import DSR
from device_k6482 import K6482

class ExpControl(QWidget, Ui_expControl):
	debug = True

	reset  = Signal()
	start  = Signal()
	pause  = Signal()
	resume = Signal()
	stop   = Signal()
	ended  = Signal()

	getWl      = Signal()
	setWl      = Signal(float)
	getShutter = Signal()
	setShutter = Signal(bool)

	getCurrent     = Signal()
	getChannel     = Signal()
	setChannel     = Signal(int)
	getVoltageFlag = Signal()
	setVoltageFlag = Signal(bool)
	getVoltage     = Signal()
	setVoltage     = Signal(float)
	getNplc        = Signal()
	setNplc        = Signal(int)
	getAverageFlag = Signal()
	setAverageFlag = Signal(bool)
	getAverage     = Signal()
	setAverage     = Signal(int)

	newCurve   = Signal()
	updateData = Signal(list, list)
	show       = Signal(int)
	hide       = Signal(int)
	showAll    = Signal()
	hideAll    = Signal()

	updateResList = Signal()

	exp: dict
	expList: List[dict]
	expSelected: int
	expCheckedList = List[int]

	def __init__(self, etype: int, controller: RespController, dsr: DSR, k6482: K6482, parent=None):
		super(ExpControl, self).__init__(parent)
		self.setupUi(self)

		self.activated = False

		# starting experiment type
		self.etype = etype
		self.controller = controller
		self.dsr = dsr
		self.k6482 = k6482
		self.file_dialog = QFileDialog()

		self.wl = 0.0
		self.shutter = False

		self.newExperiment()
		self.expList = []
		self.expSelected = -1
		self.expCheckedList = []

		self.timerActivated = False

		# initialize filters
		re = QRegularExpression(r"[a-zA-Zа-яА-Я0-9\_][a-zA-Zа-яА-Я0-9\_\-\.]*")
		v = QRegularExpressionValidator(re, self)
		self.sample_edit.setValidator(v)

		v = QDoubleValidator(200.00, 2000.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.start_edit.setValidator(v)
		self.stop_edit.setValidator(v)
		self.wl_edit.setValidator(v)

		v = QDoubleValidator(0.00, 1800.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.step_edit.setValidator(v)

		v = QDoubleValidator(0.00, 100.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.delay_edit.setValidator(v)

		v = QDoubleValidator(-10.00, 10.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.voltage_edit.setValidator(v)

		v = QDoubleValidator(0.01, 10.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.nplc_edit.setValidator(v)

		v = QIntValidator(1, 100, self)
		v.setLocale(QLocale(QLocale.C))
		self.average_edit.setValidator(v)

		m = QStandardItemModel()
		m.itemChanged.connect(self.onItemChanged)
		self.exp_list_view.setModel(m)
		self.exp_list_view.selectionModel().selectionChanged.connect(self.onSelectionChanged)

		self.updateExpView()
		self.updateActiveView()

		self.link_signals()

	def timer_start(self):
		if self.debug: print(f"ExpControl {self.etype} -> timer_start")
		if self.activated and not self.timerActivated and self.exp["status"] != 1:
			self.timerActivated = True
			self.getCurrent.emit()

	def timer_stop(self):
		if self.debug: print(f"ExpControl {self.etype} -> timer_stop")
		if self.activated:
			self.timerActivated = False

	def newExperiment(self):
		if self.debug: print(f"ExpControl -> newExperiment {self.etype}")
		e = {}
		if self.etype == 0:
			e["sampleName"]  = "Si"
			e["startWl"]     = 300
			e["stopWl"]      = 1100
			e["stepWl"]      = 5
			e["channel"]     = 2
		elif self.etype == 1:
			e["sampleName"]  = "InGaAs"
			e["startWl"]     = 900
			e["stopWl"]      = 1700
			e["stepWl"]      = 10
			e["channel"]     = 2
		elif self.etype == 2:
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
		e["type"]        = self.etype
		e["status"]      = 0
		e["dateTime"]    = ""
		e["fileName"]    = ""
		e["steps"]       = 0
		e["currentWl"]   = e["startWl"]
		e["x"]           = []
		e["y"]           = []
		self.exp = e

	def updateExpView(self):
		if self.debug: print(f"ExpControl {self.etype} -> updateExpView")
		e = self.exp

		self.sample_edit.setText(e["sampleName"])
		if e["sampleName"] == "":
			self.sample_edit.setStyleSheet("background-color: yellow")
		else:
			self.sample_edit.setStyleSheet("")
		self.start_edit    .setText(f"{e["startWl"]}")
		self.stop_edit     .setText(f"{e["stopWl"]}")
		self.step_edit     .setText(f"{e["stepWl"]}")
		self.delay_edit    .setText(f"{e["delay"]}")
		self.channel1_radio.setChecked(True if e["channel"] == 1 else False)
		self.channel2_radio.setChecked(True if e["channel"] == 2 else False)
		self.voltage_check .setChecked(e["voltageFlag"])
		self.voltage_edit  .setText(f"{e["voltage"]}")
		self.nplc_edit     .setText(f"{e["nplc"]}")
		self.average_check .setChecked(e["averageFlag"])
		self.average_edit  .setText(f"{e["average"]}")
		self.progress_bar  .setValue(int(100*(e["currentWl"]-e["startWl"])/(e["stopWl"]-e["startWl"])))

	def disableActiveView(self):
		self.frame_meas   .setDisabled(True)
		self.frame_amp    .setDisabled(True)
		self.frame_mono   .setDisabled(True)
		self.frame_control.setDisabled(True)
		self.timer_stop()

	def updateActiveView(self):
		if self.debug: print(f"ExpControl {self.etype} -> updateActiveView")
		e = self.exp
		# 0 - idle, 1 - started, 2 - paused, 3 - ended
		if e["status"] == 0:
			self.start_button.setText("Start")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Reset")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(False)
			self.frame_amp.setDisabled(False)
			self.frame_mono.setDisabled(False)
			self.load_button.setDisabled(False)
		elif e["status"] == 1:
			self.start_button.setText("Pause")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.load_button.setDisabled(True)
		elif e["status"] == 2:
			self.start_button.setText("Resume")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(False)
			self.load_button.setDisabled(False)
		elif e["status"] == 3:
			self.start_button.setText("Start")
			self.start_button.setDisabled(True)
			self.stop_button.setText("New")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.load_button.setDisabled(False)
		self.frame_control.setDisabled(False)
		self.timer_start()

	def addExpToListView(self):
		if self.debug: print(f"ExpControl {self.etype} -> addExpToListView")
		e = self.expList[-1]
		i = len(self.expList)-1
		p = self.exp_list_view.model().invisibleRootItem()

		it = QStandardItem(f"{i} : {e["sampleName"]}")
		it.setCheckable(True)
		it.setSelectable(True)
		it.setEditable(False)
		p.appendRow(it)
		self.exp_list_view.selectionModel().select(it.index(), QItemSelectionModel.SelectionFlag.ClearAndSelect)

	def link_signals(self):
		if self.debug: print(f"ExpControl {self.etype} -> link_signals")
		self.sample_edit   .returnPressed.connect(self.sample_new)
		self.sample_edit   .textEdited   .connect(self.sample_edited)
		self.sample_edit   .inputRejected.connect(self.sample_rejected)
		self.start_edit    .returnPressed.connect(self.start_new)
		self.start_edit    .textEdited   .connect(self.start_edited)
		self.stop_edit     .returnPressed.connect(self.stop_new)
		self.stop_edit     .textEdited   .connect(self.stop_edited)
		self.step_edit     .returnPressed.connect(self.step_new)
		self.step_edit     .textEdited   .connect(self.step_edited)
		self.delay_edit    .returnPressed.connect(self.delay_new)
		self.delay_edit    .textEdited   .connect(self.delay_edited)
		self.channel1_radio.clicked      .connect(self.channel1_clicked)
		self.channel2_radio.clicked      .connect(self.channel2_clicked)
		self.voltage_check .clicked      .connect(self.voltage_clicked)
		self.voltage_edit  .returnPressed.connect(self.voltage_new)
		self.voltage_edit  .textEdited   .connect(self.voltage_edited)
		self.nplc_edit     .returnPressed.connect(self.nplc_new)
		self.nplc_edit     .textEdited   .connect(self.nplc_edited)
		self.average_check .clicked      .connect(self.average_clicked)
		self.average_edit  .returnPressed.connect(self.average_new)
		self.average_edit  .textEdited   .connect(self.average_edited)
		self.wl_edit       .returnPressed.connect(self.wl_new)
		self.wl_edit       .textEdited   .connect(self.wl_edited)
		self.shutter_check .clicked      .connect(self.shutter_clicked)
		self.start_button  .released     .connect(self.start_released)
		self.stop_button   .released     .connect(self.stop_released)
		self.load_button   .released     .connect(self.load_released)

		self.reset.connect(self.onReset)

	def link_controller(self):
		c = self.controller
		self.start   .connect(c.start)
		self.pause   .connect(c.pause)
		self.resume  .connect(c.resume)
		self.stop    .connect(c.stop)
		c.startDone  .connect(self.startDone)
		c.pauseDone  .connect(self.pauseDone)
		c.resumeDone .connect(self.resumeDone)
		c.stopDone   .connect(self.stopDone)
		c.dataChanged.connect(self.dataChanged)

	def unlink_controller(self):
		c = self.controller
		self.start   .disconnect(c.start)
		self.pause   .disconnect(c.pause)
		self.resume  .disconnect(c.resume)
		self.stop    .disconnect(c.stop)
		c.startDone  .disconnect(self.startDone)
		c.pauseDone  .disconnect(self.pauseDone)
		c.resumeDone .disconnect(self.resumeDone)
		c.stopDone   .disconnect(self.stopDone)
		c.dataChanged.disconnect(self.dataChanged)

	def activate(self):
		if self.debug: print(f"ExpControl {self.etype} -> activate")
		if not self.activated:
			self.link_controller()

			self.disableActiveView()
			e = self.exp
			self.channel1_radio.setChecked(e["channel"] == 1)
			self.channel2_radio.setChecked(e["channel"] == 2)
			self.voltage_check .setChecked(e["voltageFlag"])
			self.voltage_edit  .setText(f"{e["voltage"]}")
			self.nplc_edit     .setText(f"{e["nplc"]}")
			self.average_check .setChecked(e["averageFlag"])
			self.average_edit  .setText(f"{e["average"]}")

			self.getWl               .connect(self.dsr.getWl)
			self.setWl               .connect(self.dsr.setWl)
			self.getShutter          .connect(self.dsr.getShutter)
			self.setShutter          .connect(self.dsr.setShutter)
			self.dsr.newWl           .connect(self.newWl)
			self.dsr.newShutter      .connect(self.newShutter)
			self.getCurrent          .connect(self.k6482.getCurrent)
			self.getChannel          .connect(self.k6482.getChannel)
			self.setChannel          .connect(self.k6482.setChannel)
			self.getVoltageFlag      .connect(self.k6482.getVoltageFlag)
			self.setVoltageFlag      .connect(self.k6482.setVoltageFlag)
			self.getVoltage          .connect(self.k6482.getVoltage)
			self.setVoltage          .connect(self.k6482.setVoltage)
			self.getNplc             .connect(self.k6482.getNplc)
			self.setNplc             .connect(self.k6482.setNplc)
			self.getAverageFlag      .connect(self.k6482.getAverageFlag)
			self.setAverageFlag      .connect(self.k6482.setAverageFlag)
			self.getAverage          .connect(self.k6482.getAverage)
			self.setAverage          .connect(self.k6482.setAverage)
			self.k6482.newCurrent    .connect(self.newCurrent)
			self.k6482.newChannel    .connect(self.newChannel)
			self.k6482.newVoltageFlag.connect(self.newVoltageFlag)
			self.k6482.newVoltage    .connect(self.newVoltage)
			self.k6482.newNplc       .connect(self.newNplc)
			self.k6482.newAverageFlag.connect(self.newAverageFlag)
			self.k6482.newAverage    .connect(self.newAverage)

			self.getWl         .emit()
			self.getShuttert   .emit()
			self.setChannel    .emit(e["channel"])
			self.setVoltageFlag.emit(e["voltageFlag"])
			self.setVoltage    .emit(e["voltage"])
			self.setNplc       .emit(e["nplc"])
			self.setAverageFlag.emit(e["averageFlag"])
			self.setAverage    .emit(e["average"])

			self.activated = True
			self.timer_start()

	def deactivate(self):
		if self.debug: print(f"ExpControl {self.etype} -> deactivate")
		if self.activated:
			self.unlink_controller()
			self.timer_stop()
			self.activated = False

			self.getWl               .disconnect(self.dsr.getWl)
			self.setWl               .disconnect(self.dsr.setWl)
			self.getShutter          .disconnect(self.dsr.getShutter)
			self.setShutter          .disconnect(self.dsr.setShutter)
			self.dsr.newWl           .disconnect(self.newWl)
			self.dsr.newShutter      .disconnect(self.newShutter)
			self.getCurrent          .disconnect(self.k6482.getCurrent)
			self.getChannel          .disconnect(self.k6482.getChannel)
			self.setChannel          .disconnect(self.k6482.setChannel)
			self.getVoltageFlag      .disconnect(self.k6482.getVoltageFlag)
			self.setVoltageFlag      .disconnect(self.k6482.setVoltageFlag)
			self.getVoltage          .disconnect(self.k6482.getVoltage)
			self.setVoltage          .disconnect(self.k6482.setVoltage)
			self.getNplc             .disconnect(self.k6482.getNplc)
			self.setNplc             .disconnect(self.k6482.setNplc)
			self.getAverageFlag      .disconnect(self.k6482.getAverageFlag)
			self.setAverageFlag      .disconnect(self.k6482.setAverageFlag)
			self.getAverage          .disconnect(self.k6482.getAverage)
			self.setAverage          .disconnect(self.k6482.setAverage)
			self.k6482.newCurrent    .disconnect(self.newCurrent)
			self.k6482.newChannel    .disconnect(self.newChannel)
			self.k6482.newVoltageFlag.disconnect(self.newVoltageFlag)
			self.k6482.newVoltage    .disconnect(self.newVoltage)
			self.k6482.newNplc       .disconnect(self.newNplc)
			self.k6482.newAverageFlag.disconnect(self.newAverageFlag)
			self.k6482.newAverage    .disconnect(self.newAverage)

	def sample_new(self):
		self.exp["sampleName"] = self.sample_edit.text()
		self.sample_edit.setStyleSheet("")
	def sample_edited(self, text):
		if len(text) == 0 or self.exp["sampleName"] != text:
			self.sample_edit.setStyleSheet("background: yellow; color: black")
	def sample_rejected(self):
		self.sample_edit.setStyleSheet("background: red; color: white")

	def start_new(self):
		self.exp["startWl"] = float(self.start_edit.text())
		self.start_edit.setStyleSheet("")
	def start_edited(self, text):
		if len(text) == 0 or self.exp["startWl"] != float(text):
			self.start_edit.setStyleSheet("background: yellow")

	def stop_new(self):
		self.exp["stopWl"] = float(self.stop_edit.text())
		self.stop_edit.setStyleSheet("")
	def stop_edited(self, text):
		if len(text) == 0 or self.exp["stopWl"] != float(text):
			self.stop_edit.setStyleSheet("background: yellow")

	def step_new(self):
		self.exp["stepWl"] = float(self.step_edit.text())
		self.step_edit.setStyleSheet("")
	def step_edited(self, text):
		if len(text) == 0 or self.exp["stepWl"] != float(text):
			self.step_edit.setStyleSheet("background: yellow")

	def delay_new(self):
		self.exp["delay"] = float(self.delay_edit.text())
		self.delay_edit.setStyleSheet("")
	def delay_edited(self, text):
		if len(text) == 0 or self.exp["delay"] != float(text):
			self.delay_edit.setStyleSheet("background: yellow")

	def channel1_clicked(self):
		self.exp["channel"] = 1 if self.channel1_radio.isChecked() else 2
		self.disableActiveView()
		self.setChannel.emit(self.exp["channel"])
	def channel2_clicked(self):
		self.exp["channel"] = 2 if self.channel2_radio.isChecked() else 1
		self.disableActiveView()
		self.setChannel.emit(self.exp["channel"])
	@Slot(int)
	def newChannel(self, channel: int):
		if self.debug: print(f"ExpControl {self.etype} -> newChannel")
		self.channel1_radio.setChecked(True if channel == 1 else False)
		if self.activated: self.exp["channel"] = 1 if channel == 1 else 2
		self.updateActiveView()

	def voltage_clicked(self):
		self.exp["voltageFlag"] = self.voltage_check.isChecked()
		self.disableActiveView()
		self.setVoltageFlag.emit(self.exp["voltageFlag"])
	@Slot(bool)
	def newVoltageFlag(self, voltageFlag: bool):
		if self.debug: print(f"ExpControl {self.etype} -> newVoltageFlag")
		self.voltage_check.setChecked(voltageFlag)
		if self.activated: self.exp["voltageFlag"] = voltageFlag
		self.updateActiveView()

	def voltage_new(self):
		self.exp["voltage"] = float(self.voltage_edit.text())
		self.voltage_edit.setStyleSheet("")
		self.disableActiveView()
		self.setVoltage.emit(self.exp["voltage"])
	def voltage_edited(self, text):
		if len(text) == 0 or self.exp["voltage"] != float(text):
			self.voltage_edit.setStyleSheet("background: yellow")
	@Slot(float)
	def newVoltage(self, voltage: float):
		if self.debug: print(f"ExpControl {self.etype} -> newVoltage")
		self.voltage_edit.setStyleSheet("background: green; color: white")
		self.voltage_edit.setText(f"{voltage}")
		if self.activated: self.exp["voltage"] = voltage
		self.updateActiveView()

	def nplc_new(self):
		self.exp["nplc"] = int(self.nplc_edit.text())
		self.nplc_edit.setStyleSheet("")
		self.disableActiveView()
		self.setNplc.emit(self.exp["nplc"])
	def nplc_edited(self, text):
		if len(text) == 0 or self.exp["nplc"] != int(text):
			self.nplc_edit.setStyleSheet("background: yellow")
	@Slot(int)
	def newNplc(self, nplc: int):
		if self.debug: print(f"ExpControl {self.etype} -> newNplc")
		self.nplc_edit.setStyleSheet("background: green; color: white")
		self.nplc_edit.setText(f"{nplc}")
		if self.activated: self.exp["nplc"] = nplc
		self.updateActiveView()

	def average_clicked(self):
		self.exp["averageFlag"] = self.average_check.isChecked()
		self.disableActiveView()
		self.setAverageFlag.emit(self.exp["averageFlag"])
	@Slot(bool)
	def newAverageFlag(self, averageFlag: bool):
		if self.debug: print(f"ExpControl {self.etype} -> newAverageFlag")
		self.average_check.setChecked(averageFlag)
		if self.activated: self.exp["averageFlag"] = averageFlag
		self.updateActiveView()

	def average_new(self):
		self.exp["average"] = int(self.average_edit.text())
		self.average_edit.setStyleSheet("")
		self.disableActiveView()
		self.setAverage.emit(self.exp["average"])
	def average_edited(self, text):
		if len(text) == 0 or self.exp["average"] != int(text):
			self.average_edit.setStyleSheet("background: yellow")
	@Slot(int)
	def newAverage(self, average: int):
		if self.debug: print(f"ExpControl {self.etype} -> newAverage")
		self.average_edit.setStyleSheet("background: green; color: white")
		self.average_edit.setText(f"{average}")
		if self.activated: self.exp["average"] = average
		self.updateActiveView()

	def wl_new(self):
		self.wl = float(self.wl_edit.text())
		self.wl_edit.setStyleSheet("")
		self.disableActiveView()
		self.getWl.emit(self.wl)
	def wl_edited(self, text):
		if len(text) == 0 or self.wl != float(text):
			self.wl_edit.setStyleSheet("background: yellow")
	@Slot(float)
	def newWl(self, wl: float):
		if self.debug: print(f"ExpControl {self.etype} -> newWl {wl}")
		self.wl = wl
		self.wl_edit.setText(f"{self.wl:.3f}")
		self.wl_edit.setStyleSheet("background: green; color: white")
		self.updateActiveView()

	def shutter_clicked(self):
		self.shutter = self.shutter_check.isChecked()
		self.disableActiveView()
		self.setShutter.emit(self.shutter)
	@Slot(bool)
	def newShutter(self, shutter: bool):
		if self.debug: print(f"ExpControl {self.etype} -> newShutter {shutter}")
		self.shutter = shutter
		self.shutter_check.setCheckState(Qt.Checked if self.shutter else Qt.Unchecked)
		self.updateActiveView()

	def start_released(self):
		e = self.exp
		c = self.controller
		if len(e["sampleName"]) == 0: return
		if e["status"] == 0:
			self.timer_stop()
			c.e = e
			self.start.emit()
		elif e["status"] == 1:
			self.pause.emit()
		elif e["status"] == 2:
			self.timer_stop();
			self.resume.emit()

	def stop_released(self):
		e = self.exp
		if   e["status"] == 0: self.reset.emit()
		elif e["status"] == 1: self.stop.emit()
		elif e["status"] == 2: self.stop.emit()

	def load_released(self):
		if self.debug: print(f"ExpControl {self.etype} -> load_released")
		file_filters = 'JSON File (*.json);; All (*.*)'
		response = self.file_dialog.getOpenFileNames(
			parent = self,
			caption = 'Select a file',
			dir = os.getcwd(),
			filter = file_filters,
			selectedFilter = 'JSON File (*.json)'
		)
		
		for fn in response[0]:
			self.load(fn)

	def load(self, fn: str):
		if self.debug: print(f"ExpControl {self.etype} -> load")
		with open(fn, "r") as f:
			en = json.load(f)
			a = True
			if en["type"] != self.etype:
				a = False
			if a:
				for e in self.expList:
					if en["dateTime"] == e["dateTime"]:
						a = False
			if a:
				self.expList.append(en)
				self.newCurve.emit()
				self.updateData.emit(en["x"], en["y"])
				self.addExpToListView()
				self.ended.emit()

	@Slot(QStandardItem)
	def onItemChanged(self, item: QStandardItem):
		if self.debug: print(f"ExpControl {self.etype} -> onItemChanged")
		i = item.row()
		c = (item.checkState() == Qt.Checked)
		s = self.expSelected
		l = self.expCheckedList

		if i not in l:
			if c:
				l.append(i)
				# if i != s:
				self.show.emit(i)
		else:
			if not c:
				l.remove(i)
				# if i != s:
				self.hide.emit(i)

		self.updateResList.emit()

	@Slot(QItemSelection, QItemSelection)
	def onSelectionChanged(self, s1: QItemSelection, s2: QItemSelection):
		if self.debug: print(f"ExpControl {self.etype} -> onSelectionChanged")
		l = self.expCheckedList

		for idx in s1.indexes():
			i = idx.row()
			self.expSelected = i
			if i not in l:
				self.show.emit(i)

		for idx in s2.indexes():
			i = idx.row()
			if i not in l:
				self.hide.emit(i)

		e = self.exp
		e1 = self.expList[self.expSelected]
		e["sampleName"]  = e1["sampleName"]
		e["startWl"]     = e1["startWl"]
		e["stopWl"]      = e1["stopWl"]
		e["stepWl"]      = e1["stepWl"]
		e["channel"]     = e1["channel"]
		e["delay"]       = e1["delay"]
		e["voltageFlag"] = e1["voltageFlag"]
		e["voltage"]     = e1["voltage"]
		e["nplc"]        = e1["nplc"]
		e["averageFlag"] = e1["averageFlag"]
		e["average"]     = e1["average"]
		e["currentWl"]   = e1["currentWl"]

		self.updateExpView()
		self.updateActiveView()

	@Slot(int)
	def onReset(self):
		if self.debug: print(f"ExpControl {self.etype} -> onReset")
		del self.exp
		self.newExperiment()
		self.updateExpView()

	@Slot(int)
	def startDone(self):
		if self.debug: print(f"ExpControl {self.etype} -> startDone")
		self.updateActiveView()
		i = self.expSelected
		l = self.expCheckedList
		if i >= 0 and i not in l:
			self.hide.emit(self.expSelected)
		self.newCurve.emit()

	@Slot(int)
	def pauseDone(self):
		if self.debug: print(f"ExpControl {self.etype} -> pauseDone")
		self.timer_start()
		self.updateActiveView()

	@Slot(int)
	def resumeDone(self):
		if self.debug: print(f"ExpControl {self.etype} -> resumeDone")
		self.updateActiveView()

	@Slot(int)
	def stopDone(self):
		if self.debug: print(f"ExpControl {self.etype} -> stopDone")
		self.timer_start()
		self.unlink_controller()
		self.expList.append(self.exp)
		self.expSelected = len(self.expList)-1

		self.newExperiment()
		e = self.exp
		e["sampleName"]  = self.exp["sampleName"]
		e["startWl"]     = self.exp["startWl"]
		e["stopWl"]      = self.exp["stopWl"]
		e["stepWl"]      = self.exp["stepWl"]
		e["channel"]     = self.exp["channel"]
		e["delay"]       = self.exp["delay"]
		e["voltageFlag"] = self.exp["voltageFlag"]
		e["voltage"]     = self.exp["voltage"]
		e["nplc"]        = self.exp["nplc"]
		e["averageFlag"] = self.exp["averageFlag"]
		e["average"]     = self.exp["average"]
		self.link_controller()
		self.updateActiveView()
		self.addExpToListView()
		self.ended.emit()

	@Slot()
	def dataChanged(self):
		if self.debug: print(f"ExpControl {self.etype} -> dataChanged")
		e = self.exp
		c = self.controller
		# print(e)
		c.rlock()
		self.progress_bar.setValue(int(100*(e["currentWl"]-e["startWl"])/(e["stopWl"]-e["startWl"])))
		x = e["x"]
		y = e["y"]
		c.unlock()
		self.updateData.emit(x, y)

	@Slot(float, float)
	def newCurrent(self, c1: float, c2: float):
		if self.debug: print(f"ExpControl {self.etype} -> newCurrent {c1}, {c2}")
		self.current1_label.setText(f"{c1:+.5e}")
		self.current2_label.setText(f"{c2:+.5e}")
		if self.timerActivated:
			self.getCurrent.emit()

	@Slot()
	def onExit(self):
		if self.debug: print(f"ExpControl {self.etype} -> onExit")
		self.deactivate()
