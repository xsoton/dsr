from PySide6.QtCore import (Qt, QTimer, Signal, Slot,
	QRegularExpression, QLocale, QItemSelection, QItemSelectionModel)
from PySide6.QtGui import (QStandardItemModel, QStandardItem,
	QValidator, QRegularExpressionValidator, QDoubleValidator, QIntValidator)
from PySide6.QtWidgets import QWidget, QFileDialog

from typing import List
from math import *
import os
import json

from ui_timeControl import Ui_timeControl
from controller import TimeController
from device_dsr import DSR
from device_k6482 import K6482

class TimeControl(QWidget, Ui_timeControl):
	debug = False

	reset  = Signal()
	start  = Signal()
	pause  = Signal()
	resume = Signal()
	stop   = Signal()

	busy   = Signal()
	idle   = Signal()

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

	exp: dict
	expList: List[dict]
	expSelected: int
	expCheckedList = List[int]

	def __init__(self, controller: TimeController, dsr: DSR, k6482: K6482, parent=None):
		super(TimeControl, self).__init__(parent)
		self.setupUi(self)

		self.activated = False

		# starting experiment type
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

		v = QDoubleValidator(0.00, 1440*600, 3, self)
		v.setLocale(QLocale(QLocale.C))
		self.time_v = v

		v = QDoubleValidator(-10.00, 10.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.voltage_edit.setValidator(v)
		self.voltage_v = v

		v = QDoubleValidator(200.00, 2000.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.wl_v = v

		v = QIntValidator(0, 1, self)
		v.setLocale(QLocale(QLocale.C))
		self.sh_v = v

		v = QDoubleValidator(0.01, 10.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.nplc_edit.setValidator(v)

		v = QIntValidator(1, 100, self)
		v.setLocale(QLocale(QLocale.C))
		self.average_edit.setValidator(v)

		self.wl = self.dsr.get_wl()
		self.newWl(self.wl)

		self.shutter = self.dsr.get_shutter()
		self.newShutter(self.shutter)

		m = QStandardItemModel()
		m.itemChanged.connect(self.onItemChanged)
		self.exp_list_view.setModel(m)
		self.exp_list_view.selectionModel().selectionChanged.connect(self.onSelectionChanged)

		self.updateExpView()
		self.updateActiveView()

		self.link_signals()

	def timer_start(self):
		if self.debug: print(f"TimeControl -> timer_start")
		if self.activated and not self.timerActivated and self.exp["status"] != 1:
			self.timerActivated = True
			self.getCurrent.emit()

	def timer_stop(self):
		if self.debug: print(f"TimeControl -> timer_stop")
		if self.activated:
			self.timerActivated = False

	def newExperiment(self):
		if self.debug: print(f"TimeControl -> newExperiment")
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
		self.exp = e

	def updateExpView(self):
		if self.debug: print(f"TimeControl -> updateExpView")
		e = self.exp

		self.sample_edit.setText(e["sampleName"])
		if e["sampleName"] == "":
			self.sample_edit.setStyleSheet("background-color: yellow")
		else:
			self.sample_edit.setStyleSheet("")
		s = ""
		for sc in e["script"]:
			s = s + f"{sc["t"]} {sc["V"]} {sc["wl"]} {int(sc["sh"])}\n"
			print(f"{s=}")
		self.exp_edit.setPlainText(s)
		self.channel1_radio.setChecked(True if e["channel"] == 1 else False)
		self.channel2_radio.setChecked(True if e["channel"] == 2 else False)
		self.voltage_check.setChecked(e["voltageFlag"])
		self.voltage_edit.setText(f"{e["voltage"]}")
		self.nplc_edit.setText(f"{e["nplc"]}")
		self.average_check.setChecked(e["averageFlag"])
		self.average_edit.setText(f"{e["average"]}")
		self.progress_bar.setValue(int(100*e["time"]/e["duration"]))

	def disableActiveView(self):
		if self.debug: print(f"TimeControl -> disableActiveView")
		self.frame_meas   .setDisabled(True)
		self.frame_amp    .setDisabled(True)
		self.timer_stop()
		self.busy.emit()

	def updateActiveView(self):
		if self.debug: print(f"TimeControl -> updateActiveView")
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
			# self.frame_mono.setDisabled(True)
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
		self.idle.emit()

	def addExpToListView(self):
		if self.debug: print(f"TimeControl -> addExpToListView")
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
		if self.debug: print(f"TimeControl -> link_signals")
		self.sample_edit   .returnPressed.connect(self.sample_new)
		self.sample_edit   .inputRejected.connect(self.sample_rejected)
		self.sample_edit   .textEdited   .connect(self.sample_edited)
		self.exp_edit      .textChanged  .connect(self.exp_edited)
		self.exp_button    .released     .connect(self.exp_released)
		self.channel1_radio.clicked      .connect(self.channel1_clicked)
		self.channel2_radio.clicked      .connect(self.channel2_clicked)
		self.voltage_check .clicked      .connect(self.voltage_clicked)
		self.voltage_edit  .returnPressed.connect(self.voltage_new)
		self.voltage_edit  .textChanged  .connect(self.voltage_edited)
		self.nplc_edit     .returnPressed.connect(self.nplc_new)
		self.nplc_edit     .textChanged  .connect(self.nplc_edited)
		self.average_check .clicked      .connect(self.average_clicked)
		self.average_edit  .returnPressed.connect(self.average_new)
		self.average_edit  .textChanged  .connect(self.average_edited)
		self.wl_edit       .returnPressed.connect(self.wl_new)
		self.wl_edit       .textEdited   .connect(self.wl_edited)
		self.shutter_check .clicked      .connect(self.shutter_clicked)
		self.start_button  .released     .connect(self.start_released)
		self.stop_button   .released     .connect(self.stop_released)
		self.load_button   .released     .connect(self.load_pressed)

		self.reset .connect(self.onReset)

	def link_controller(self):
		if self.debug: print(f"TimeControl -> link_controller")
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
		if self.debug: print(f"TimeControl -> unlink_controller")
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
		if self.debug: print(f"TimeControl -> activate")
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

			self.setChannel    .emit(e["channel"])
			self.setVoltageFlag.emit(e["voltageFlag"])
			self.setVoltage    .emit(e["voltage"])
			self.setNplc       .emit(e["nplc"])
			self.setAverageFlag.emit(e["averageFlag"])
			self.setAverage    .emit(e["average"])

			self.activated = True
			self.timer_start()

	def deactivate(self):
		if self.debug: print(f"TimeControl -> deactivate")
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
		if self.debug: print(f"TimeControl -> sample_new")
		self.exp["sampleName"] = self.sample_edit.text()
		self.sample_edit.setStyleSheet("")
	def sample_edited(self, text):
		if self.debug: print(f"TimeControl -> sample_edited")
		if len(text) == 0 or self.exp["sampleName"] != text:
			self.sample_edit.setStyleSheet("background: yellow; color: black")
	def sample_rejected(self):
		if self.debug: print(f"TimeControl -> sample_rejected")
		self.sample_edit.setStyleSheet("background: red; color: white")

	def exp_released(self):
		if self.debug: print(f"TimeControl -> exp_released")
		r1, r2 = self.parse_exp(self.exp_edit.toPlainText())
		if r2:
			self.exp["script"] = []
			for e in r1:
				self.exp["script"].append(e)
			self.exp_edit.setStyleSheet("")
		else:
			self.exp_edit.setStyleSheet("background: red; color: white")
	def exp_edited(self):
		if self.debug: print(f"TimeControl -> exp_edited")
		c = True
		r1, r2 = self.parse_exp(self.exp_edit.toPlainText())
		print(self.exp["script"])
		print(r1)
		if r2:
			if len(self.exp["script"]) == len(r1) and len(r1) > 0:
				print(f"1 {c=}")
				for i in range(len(r1)):
					if r1[i]["t"] != self.exp["script"][i]["t"]:
						c = False
					if r1[i]["V"] != self.exp["script"][i]["V"]:
						c = False
					if r1[i]["wl"] != self.exp["script"][i]["wl"]:
						c = False
					if r1[i]["sh"] != self.exp["script"][i]["sh"]:
						c = False
					print(f"2 {c=}")
			else:
				c = False
				print(f"3 {c=}")
		else:
			c = False
			print(f"4 {c=}")

		if not c:
			self.exp_edit.setStyleSheet("background: yellow")
	def parse_exp(self, text: str):
		a = text.strip().split('\n')
		r1 = []
		r2 = True
		for e in a:
			l = e.strip().split(' ')
			if len(l) == 4:
				tv, _, _ = self.time_v   .validate(l[0], 0)
				vv, _, _ = self.voltage_v.validate(l[1], 0)
				wv, _, _ = self.wl_v     .validate(l[2], 0)
				sv, _, _ = self.sh_v     .validate(l[3], 0)

				tv = tv == QValidator.State.Acceptable
				vv = vv == QValidator.State.Acceptable
				wv = wv == QValidator.State.Acceptable
				sv = sv == QValidator.State.Acceptable

				if tv and vv and wv and sv:
					t  = float(l[0])
					V  = float(l[1])
					wl = float(l[2])
					sh = bool(int(l[3]))
					r1.append({"t": t, "V": V, "wl": wl, "sh": sh})
				else:
					r2 = False
			else:
				r2 = False

		return (r1, r2)

	def channel1_clicked(self):
		if self.debug: print(f"TimeControl -> channel1_clicked")
		self.exp["channel"] = 1 if self.channel1_radio.isChecked() else 2
		self.disableActiveView()
		self.setChannel.emit(self.exp["channel"])
	def channel2_clicked(self):
		if self.debug: print(f"TimeControl -> channel2_clicked")
		self.exp["channel"] = 2 if self.channel2_radio.isChecked() else 1
		self.disableActiveView()
		self.setChannel.emit(self.exp["channel"])
	@Slot(int)
	def newChannel(self, channel: int):
		if self.debug: print(f"TimeControl -> newChannel")
		self.channel1_radio.setChecked(True if channel == 1 else False)
		if self.activated: self.exp["channel"] = 1 if channel == 1 else 2
		self.updateActiveView()

	def voltage_clicked(self):
		if self.debug: print(f"TimeControl -> voltage_clicked")
		self.exp["voltageFlag"] = self.voltage_check.isChecked()
		self.disableActiveView()
		self.setVoltageFlag.emit(self.exp["voltageFlag"])
	@Slot(bool)
	def newVoltageFlag(self, voltageFlag: bool):
		if self.debug: print(f"TimeControl -> newVoltageFlag")
		self.voltage_check.setChecked(voltageFlag)
		if self.activated: self.exp["voltageFlag"] = voltageFlag
		self.updateActiveView()

	def voltage_new(self):
		if self.debug: print(f"TimeControl -> voltage_new")
		self.exp["voltage"] = float(self.voltage_edit.text())
		self.voltage_edit.setStyleSheet("")
		self.disableActiveView()
		self.setVoltage.emit(self.exp["voltage"])
	def voltage_edited(self, text):
		if self.debug: print(f"TimeControl -> voltage_edited")
		if len(text) == 0 or self.k6482.voltage != float(text):
			self.voltage_edit.setStyleSheet("background: yellow")
		else:
			self.voltage_edit.setStyleSheet("background: green; color: white")
	@Slot(float)
	def newVoltage(self, voltage: float):
		if self.debug: print(f"TimeControl -> newVoltage")
		self.voltage_edit.setStyleSheet("background: green; color: white")
		self.voltage_edit.setText(f"{voltage}")
		if self.activated: self.exp["voltage"] = voltage
		self.updateActiveView()

	def nplc_new(self):
		if self.debug: print(f"TimeControl -> nplc_new")
		self.exp["nplc"] = int(self.nplc_edit.text())
		self.nplc_edit.setStyleSheet("")
		self.disableActiveView()
		self.setNplc.emit(self.exp["nplc"])
	def nplc_edited(self, text):
		if self.debug: print(f"TimeControl -> nplc_edited")
		if len(text) == 0 or self.k6482.nplc != int(text):
			self.nplc_edit.setStyleSheet("background: yellow")
		else:
			self.nplc_edit.setStyleSheet("background: green; color: white")
	@Slot(int)
	def newNplc(self, nplc: int):
		if self.debug: print(f"TimeControl -> newNplc")
		self.nplc_edit.setStyleSheet("background: green; color: white")
		self.nplc_edit.setText(f"{nplc}")
		if self.activated: self.exp["nplc"] = nplc
		self.updateActiveView()

	def average_clicked(self):
		if self.debug: print(f"TimeControl -> average_clicked")
		self.exp["averageFlag"] = self.average_check.isChecked()
		self.disableActiveView()
		self.setAverageFlag.emit(self.exp["averageFlag"])
	@Slot(bool)
	def newAverageFlag(self, averageFlag: bool):
		if self.debug: print(f"TimeControl -> newAverageFlag")
		self.average_check.setChecked(averageFlag)
		if self.activated: self.exp["averageFlag"] = averageFlag
		self.updateActiveView()

	def average_new(self):
		if self.debug: print(f"TimeControl -> average_new")
		self.exp["average"] = int(self.average_edit.text())
		self.average_edit.setStyleSheet("")
		self.disableActiveView()
		self.setAverage.emit(self.exp["average"])
	def average_edited(self, text):
		if self.debug: print(f"TimeControl -> average_edited")
		if len(text) == 0 or self.k6482.average != int(text):
			self.average_edit.setStyleSheet("background: yellow")
		else:
			self.average_edit.setStyleSheet("background: green; color: white")
	@Slot(int)
	def newAverage(self, average: int):
		if self.debug: print(f"TimeControl -> newAverage")
		self.average_edit.setStyleSheet("background: green; color: white")
		self.average_edit.setText(f"{average}")
		if self.activated: self.exp["average"] = average
		self.updateActiveView()

	def wl_new(self):
		if self.debug: print(f"TimeControl -> average_clicked")
		self.wl = float(self.wl_edit.text())
		self.wl_edit.setStyleSheet("")
		self.disableActiveView()
		self.setWl.emit(self.wl)
	def wl_edited(self, text):
		if len(text) == 0 or self.wl != float(text):
			self.wl_edit.setStyleSheet("background: yellow")
	@Slot(float)
	def newWl(self, wl: float):
		if self.debug: print(f"TimeControl -> newWl {wl}")
		self.wl = wl
		self.wl_edit.setText(f"{self.wl:.3f}")
		self.wl_edit.setStyleSheet("background: green; color: white")
		self.updateActiveView()

	def shutter_clicked(self):
		if self.debug: print(f"TimeControl -> average_clicked")
		self.shutter = self.shutter_check.isChecked()
		self.disableActiveView()
		self.setShutter.emit(self.shutter)
	@Slot(bool)
	def newShutter(self, shutter: bool):
		if self.debug: print(f"TimeControl -> newShutter {shutter}")
		self.shutter = shutter
		self.shutter_check.setCheckState(Qt.Checked if self.shutter else Qt.Unchecked)
		self.updateActiveView()

	def start_released(self):
		if self.debug: print(f"TimeControl -> start_released")
		e = self.exp
		c = self.controller
		if len(e["sampleName"]) == 0: return
		if e["status"] == 0:
			self.timer_stop()
			self.busy.emit()
			c.e = e
			self.start.emit()
		elif e["status"] == 1:
			self.pause.emit()
		elif e["status"] == 2:
			self.timer_stop();
			self.resume.emit()

	def stop_released(self):
		if self.debug: print(f"TimeControl -> stop_released")
		e = self.exp
		if   e["status"] == 0: self.reset.emit()
		elif e["status"] == 1: self.stop.emit()
		elif e["status"] == 2: self.stop.emit()

	def load_pressed(self):
		if self.debug: print(f"TimeControl -> load_pressed")
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
		if self.debug: print(f"TimeControl -> load")
		with open(fn, "r") as f:
			en = json.load(f)
			a = True
			if en["type"] != 3:
				a = False
			if a:
				for e in self.expList:
					if en["dateTime"] == e["dateTime"]:
						a = False
			if a:
				self.expList.append(en)
				self.newCurve.emit()
				self.updateData.emit(en["t"], en["I"])
				self.addExpToListView()
				self.idle.emit()

	@Slot(QStandardItem)
	def onItemChanged(self, item: QStandardItem):
		if self.debug: print(f"TimeControl -> onItemChanged")
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

	@Slot(QItemSelection, QItemSelection)
	def onSelectionChanged(self, s1: QItemSelection, s2: QItemSelection):
		if self.debug: print(f"TimeControl -> onSelectionChanged")
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
		e["script"]      = e1["script"]
		e["channel"]     = e1["channel"]
		e["voltageFlag"] = e1["voltageFlag"]
		e["voltage"]     = e1["voltage"]
		e["nplc"]        = e1["nplc"]
		e["averageFlag"] = e1["averageFlag"]
		e["average"]     = e1["average"]
		e["time"]        = e1["time"]
		e["duration"]    = e1["duration"]

		self.updateExpView()
		self.updateActiveView()

	@Slot(int)
	def onReset(self):
		if self.debug: print(f"TimeControl -> onReset")
		del self.exp
		self.newExperiment()
		self.updateExpView()

	@Slot(int)
	def startDone(self):
		if self.debug: print(f"TimeControl -> startDone")
		self.updateActiveView()
		i = self.expSelected
		l = self.expCheckedList
		if i >= 0 and i not in l:
			self.hide.emit(self.expSelected)
		self.newCurve.emit()

	@Slot(int)
	def pauseDone(self):
		if self.debug: print(f"TimeControl -> pauseDone")
		self.timer_start()
		self.updateActiveView()

	@Slot(int)
	def resumeDone(self):
		if self.debug: print(f"TimeControl -> resumeDone")
		self.updateActiveView()

	@Slot(int)
	def stopDone(self):
		if self.debug: print(f"TimeControl -> stopDone")
		self.timer_start()
		self.unlink_controller()
		self.expList.append(self.exp)
		self.expSelected = len(self.expList)-1

		self.newExperiment()
		e = self.exp
		e["sampleName"]  = self.exp["sampleName"]
		e["script"]      = self.exp["script"]
		e["channel"]     = self.exp["channel"]
		e["voltageFlag"] = self.exp["voltageFlag"]
		e["voltage"]     = self.exp["voltage"]
		e["nplc"]        = self.exp["nplc"]
		e["averageFlag"] = self.exp["averageFlag"]
		e["average"]     = self.exp["average"]
		e["time"]        = self.exp["time"]
		e["duration"]    = self.exp["duration"]
		self.link_controller()
		self.updateActiveView()
		self.addExpToListView()
		self.idle.emit()

	@Slot()
	def dataChanged(self):
		if self.debug: print(f"TimeControl -> dataChanged")
		e = self.exp
		c = self.controller
		# print(e)
		c.rlock()
		self.progress_bar.setValue(int(100*e["time"]/e["duration"]))
		x = e["t"]
		y = e["I"]
		c.unlock()
		self.updateData.emit(x, y)

	@Slot(float, float)
	def newCurrent(self, c1: float, c2: float):
		# if self.debug: print(f"TimeControl -> newCurrent {c1}, {c2}")
		self.current1_label.setText(f"{c1:+.5e}")
		self.current2_label.setText(f"{c2:+.5e}")
		if self.timerActivated:
			self.getCurrent.emit()

	@Slot()
	def onExit(self):
		if self.debug: print(f"TimeControl -> onExit")
		self.deactivate()
