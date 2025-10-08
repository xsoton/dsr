from PySide6.QtCore import Qt, QFile, QIODevice, QTimer, QThread, Signal, Slot, QRegularExpression, QLocale, QItemSelection, QItemSelectionModel
from PySide6.QtGui import QStandardItemModel, QStandardItem, QRegularExpressionValidator, QDoubleValidator, QIntValidator
from PySide6.QtWidgets import QWidget, QFileDialog

from typing import Self, List
from math import *
import os
import json

from ui_expControl import Ui_expControl
from controller import Controller
from device_dsr import DSR
from device_k6482 import K6482

class ExpControl(QWidget, Ui_expControl):

	sig_reset  = Signal()
	sig_start  = Signal()
	sig_pause  = Signal()
	sig_resume = Signal()
	sig_stop   = Signal()
	sig_ended  = Signal()

	sig_wl      = Signal(float)
	sig_shutter = Signal(bool)

	sig_newCurve   = Signal()
	sig_updateData = Signal(list, list)
	sig_show       = Signal(int)
	sig_hide       = Signal(int)
	sig_showAll    = Signal()
	sig_hideAll    = Signal()

	sig_checked = Signal()

	timer: QTimer

	exp: dict
	expList: List[dict]
	expSelected: int
	expCheckedList = List[int]

	def __init__(self, etype: int, controller: Controller, dsr: DSR, k6482: K6482, parent=None):
		super(ExpControl, self).__init__(parent)
		self.setupUi(self)

		# starting experiment type
		self.etype = etype
		self.controller = controller
		self.dsr = dsr
		self.k6482 = k6482
		self.file_dialog = QFileDialog()

		self.exp = self.controller.newExperiment(self.etype)
		self.expList = []
		self.expSelected = -1
		self.expCheckedList = []

		self.timeout = 500
		self.timer = QTimer()
		self.timer.timeout.connect(self.k6482.get_current)
		self.k6482.newCurrent.connect(self.onNewCurrent)

		# initialize filters
		re = QRegularExpression(r"[a-zA-Zа-яА-Я0-9\_][a-zA-Zа-яА-Я0-9\_\-\.]*")
		v = QRegularExpressionValidator(re, self)
		self.sample_edit.setValidator(v)

		v = QDoubleValidator(200.00, 2000.00, 2, self)
		v.setLocale(QLocale(QLocale.C))
		self.start_edit.setValidator(v)
		self.stop_edit.setValidator(v)
		self.wl_edit.setValidator(v)

		v = QDoubleValidator(0.00, 1700.00, 2, self)
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

		self.wl = self.dsr.get_wl()
		self.wl_edit.setText(f"{self.wl}")

		self.shutter = self.dsr.get_shutter()
		self.shutter_check.setChecked(self.shutter)

		m = QStandardItemModel()
		m.itemChanged.connect(self.onItemChanged)
		self.exp_list_view.setModel(m)
		self.exp_list_view.selectionModel().selectionChanged.connect(self.onSelectionChanged)

		self.updateExpView()
		self.updateActiveView()

		self.link_signals()

		self.activated = False

	def timer_start(self):
		if self.activated:
			self.timer.start(self.timeout)
	def timer_stop(self):
		if self.activated:
			self.timer.stop()

	def updateExpView(self):
		e = self.exp

		self.sample_edit.setText(e["sampleName"])
		if e["sampleName"] == "":
			self.sample_edit.setStyleSheet("background-color: yellow")
		else:
			self.sample_edit.setStyleSheet("")
		self.start_edit.setText(f"{e["startWl"]}")
		self.stop_edit.setText(f"{e["stopWl"]}")
		self.step_edit.setText(f"{e["stepWl"]}")
		self.channel1_radio.setChecked(True if e["channel"] == 1 else False)
		self.channel2_radio.setChecked(True if e["channel"] == 2 else False)
		self.voltage_check.setChecked(e["voltageFlag"])
		self.voltage_edit.setText(f"{e["voltage"]}")
		self.nplc_edit.setText(f"{e["nplc"]}")
		self.average_check.setChecked(e["averageFlag"])
		self.average_edit.setText(f"{e["average"]}")
		self.progress_bar.setValue(int(100*(e["currentWl"]-e["startWl"])/(e["stopWl"]-e["startWl"])))

	def updateActiveView(self):
		# print("updateActiveView")
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
			self.exp_list_view.setDisabled(False)
		elif e["status"] == 1:
			self.start_button.setText("Pause")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.load_button.setDisabled(True)
			self.exp_list_view.setDisabled(True)
		elif e["status"] == 2:
			self.start_button.setText("Resume")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(False)
			self.load_button.setDisabled(False)
			self.exp_list_view.setDisabled(True)
		elif e["status"] == 3:
			self.start_button.setText("Start")
			self.start_button.setDisabled(True)
			self.stop_button.setText("New")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.load_button.setDisabled(False)
			self.exp_list_view.setDisabled(False)

	def addExpToListView(self):
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
		self.sample_edit   .returnPressed.connect(self.sample_edit_new_slot)
		self.sample_edit   .inputRejected.connect(self.sample_edit_rejected_slot)
		self.sample_edit   .textEdited   .connect(self.sample_edit_edited_slot)
		self.start_edit    .returnPressed.connect(self.start_edit_new_slot)
		self.start_edit    .textEdited   .connect(self.start_edit_edited_slot)
		self.stop_edit     .returnPressed.connect(self.stop_edit_slot)
		self.stop_edit     .textEdited   .connect(self.stop_edit_edited_slot)
		self.step_edit     .returnPressed.connect(self.step_edit_slot)
		self.step_edit     .textEdited   .connect(self.step_edit_edited_slot)
		self.delay_edit    .returnPressed.connect(self.delay_edit_slot)
		self.delay_edit    .textEdited   .connect(self.delay_edit_edited_slot)
		self.channel1_radio.clicked      .connect(self.channel1_radio_slot)
		self.channel2_radio.clicked      .connect(self.channel2_radio_slot)
		self.voltage_check .clicked      .connect(self.voltage_check_slot)
		self.voltage_edit  .returnPressed.connect(self.voltage_edit_slot)
		self.voltage_edit  .textEdited   .connect(self.voltage_edit_edited_slot)
		self.nplc_edit     .returnPressed.connect(self.nplc_edit_slot)
		self.nplc_edit     .textEdited   .connect(self.nplc_edit_edited_slot)
		self.average_check .clicked      .connect(self.average_check_slot)
		self.average_edit  .returnPressed.connect(self.average_edit_slot)
		self.average_edit  .textEdited   .connect(self.average_edit_edited_slot)
		self.wl_edit       .returnPressed.connect(self.wl_edit_slot)
		self.wl_edit       .textEdited   .connect(self.wl_edit_edited_slot)
		self.shutter_check .clicked      .connect(self.shutter_check_slot)
		self.start_button  .released     .connect(self.start_button_slot)
		self.stop_button   .released     .connect(self.stop_button_slot)
		self.load_button   .released     .connect(self.onLoadPressed)

		self.sig_wl         .connect(self.dsr.setWl)
		self.sig_shutter    .connect(self.dsr.setShutter)
		self.dsr.setWlDone  .connect(self.onSetWlDone)
		self.dsr.shutterDone.connect(self.onShutterDone)

	def activate(self):
		c = self.controller
		if not self.activated:
			self.sig_reset .connect(self.onReset)
			self.sig_start .connect(c.onStart)
			self.sig_pause .connect(c.onPause)
			self.sig_resume.connect(c.onResume)
			self.sig_stop  .connect(c.onStop)
			c.started      .connect(self.onStarted)
			c.paused       .connect(self.onPaused)
			c.resumed      .connect(self.onResumed)
			c.stoped       .connect(self.onStoped)
			c.dataChanged  .connect(self.onDataChanged)
			self.activated = True
			self.timer_start()

	def deactivate(self):
		c = self.controller
		if self.activated:
			self.sig_reset .disconnect(self.onReset)
			self.sig_start .disconnect(c.onStart)
			self.sig_pause .disconnect(c.onPause)
			self.sig_resume.disconnect(c.onResume)
			self.sig_stop  .disconnect(c.onStop)
			c.started      .disconnect(self.onStarted)
			c.paused       .disconnect(self.onPaused)
			c.resumed      .disconnect(self.onResumed)
			c.stoped       .disconnect(self.onStoped)
			c.dataChanged  .disconnect(self.onDataChanged)
			self.activated = False
			self.timer_stop()

	def sample_edit_new_slot(self):
		self.exp["sampleName"] = self.sample_edit.text()
		self.sample_edit.setStyleSheet("")
	def sample_edit_edited_slot(self, text):
		if len(text) == 0 or self.exp["sampleName"] != text:
			self.sample_edit.setStyleSheet("background: yellow; color: black")
	def sample_edit_rejected_slot(self):
		self.sample_edit.setStyleSheet("background: red; color: white")

	def start_edit_new_slot(self):
		self.exp["startWl"] = float(self.start_edit.text())
		self.start_edit.setStyleSheet("")
	def start_edit_edited_slot(self, text):
		if len(text) == 0 or self.exp["startWl"] != float(text):
			self.start_edit.setStyleSheet("background: yellow")

	def stop_edit_slot(self):
		self.exp["stopWl"] = float(self.stop_edit.text())
		self.stop_edit.setStyleSheet("")
	def stop_edit_edited_slot(self, text):
		if len(text) == 0 or self.exp["stopWl"] != float(text):
			self.stop_edit.setStyleSheet("background: yellow")

	def step_edit_slot(self):
		self.exp["stepWl"] = float(self.step_edit.text())
		self.step_edit.setStyleSheet("")
	def step_edit_edited_slot(self, text):
		if len(text) == 0 or self.exp["stepWl"] != float(text):
			self.step_edit.setStyleSheet("background: yellow")

	def delay_edit_slot(self):
		self.exp["delay"] = float(self.delay_edit.text())
		self.delay_edit.setStyleSheet("")
	def delay_edit_edited_slot(self, text):
		if len(text) == 0 or self.exp["delay"] != float(text):
			self.delay_edit.setStyleSheet("background: yellow")

	def channel1_radio_slot(self):
		self.exp["channel"] = 1 if self.channel1_radio.isChecked() else 2

	def channel2_radio_slot(self):
		self.exp["channel"] = 2 if self.channel2_radio.isChecked() else 1

	def voltage_check_slot(self):
		self.exp["voltageFlag"] = self.voltage_check.isChecked()

	def voltage_edit_slot(self):
		self.exp["voltage"] = float(self.voltage_edit.text())
		self.voltage_edit.setStyleSheet("")
	def voltage_edit_edited_slot(self, text):
		if len(text) == 0 or self.exp["voltage"] != float(text):
			self.voltage_edit.setStyleSheet("background: yellow")

	def nplc_edit_slot(self):
		self.exp["nplc"] = int(self.nplc_edit.text())
		self.nplc_edit.setStyleSheet("")
	def nplc_edit_edited_slot(self, text):
		if len(text) == 0 or self.exp["nplc"] != int(text):
			self.nplc_edit.setStyleSheet("background: yellow")

	def average_check_slot(self):
		self.exp["averageFlag"] = self.average_check.isChecked()

	def average_edit_slot(self):
		self.exp["average"] = int(self.average_edit.text())
		self.average_edit.setStyleSheet("")
	def average_edit_edited_slot(self, text):
		if len(text) == 0 or self.exp["average"] != int(text):
			self.average_edit.setStyleSheet("background: yellow")

	def wl_edit_slot(self):
		self.wl = float(self.wl_edit.text())
		self.wl_edit.setStyleSheet("")
		self.start_button .setDisabled(True)
		self.stop_button  .setDisabled(True)
		self.frame_meas   .setDisabled(True)
		self.frame_amp    .setDisabled(True)
		self.frame_mono   .setDisabled(True)
		self.exp_list_view.setDisabled(True)
		self.timer_stop()
		self.sig_wl.emit(self.wl)
	def wl_edit_edited_slot(self, text):
		if len(text) == 0 or self.wl != float(text):
			self.wl_edit.setStyleSheet("background: yellow")
	@Slot(float)
	def onSetWlDone(self, wl: float):
		self.wl = wl
		self.wl_edit.setText(f"{self.wl:.3f}")
		self.wl_edit.setStyleSheet("background: green; color: white")
		self.updateActiveView()
		self.timer_start()

	def shutter_check_slot(self):
		# print("shutter_check_slot")
		self.shutter = self.shutter_check.isChecked()
		self.start_button .setDisabled(True)
		self.stop_button  .setDisabled(True)
		self.frame_meas   .setDisabled(True)
		self.frame_amp    .setDisabled(True)
		self.frame_mono   .setDisabled(True)
		self.exp_list_view.setDisabled(True)
		self.timer_stop()
		self.sig_shutter.emit(self.shutter)
	@Slot(bool)
	def onShutterDone(self, shutter: bool):
		# print("onShutterDone")
		self.shutter = shutter
		self.shutter_check.setCheckState(Qt.Checked if self.shutter else Qt.Unchecked)
		self.updateActiveView()
		self.timer_start()

	def start_button_slot(self):
		e = self.exp
		c = self.controller
		if len(e["sampleName"]) == 0: return
		if e["status"] == 0:
			self.timer_stop();
			c.e = e;
			self.sig_start.emit()
		elif e["status"] == 1:
			self.sig_pause.emit()
		elif e["status"] == 2:
			self.timer_stop();
			self.sig_resume.emit()

	def stop_button_slot(self):
		e = self.exp
		if   e["status"] == 0: self.sig_reset.emit()
		elif e["status"] == 1: self.sig_stop.emit()
		elif e["status"] == 2: self.sig_stop.emit()

	def onLoadPressed(self):
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
		# print(fn)
		with open(fn, "r") as f:
			en = json.load(f)
			a = True
			for e in self.expList:
				if en["dateTime"] == e["dateTime"]:
					a = False
			if a:
				self.expList.append(en)
				self.sig_newCurve.emit()
				self.sig_updateData.emit(en["x"], en["y"])
				self.addExpToListView()
				self.sig_ended.emit()

	@Slot(QStandardItem)
	def onItemChanged(self, item: QStandardItem):
		i = item.row()
		c = (item.checkState() == Qt.Checked)
		s = self.expSelected
		l = self.expCheckedList

		if i not in l:
			if c:
				l.append(i)
				if i != s:
					self.sig_show.emit(i)
		else:
			if not c:
				l.remove(i)
				if i != s:
					self.sig_hide.emit(i)

		self.sig_checked.emit()

	@Slot(QItemSelection, QItemSelection)
	def onSelectionChanged(self, s1: QItemSelection, s2: QItemSelection):
		l = self.expCheckedList

		for idx in s1.indexes():
			i = idx.row()
			self.expSelected = i
			if i not in l:
				self.sig_show.emit(i)

		for idx in s2.indexes():
			i = idx.row()
			if i not in l:
				self.sig_hide.emit(i)

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

		self.updateExpView()
		self.updateActiveView()

	@Slot(int)
	def onReset(self):
		del self.exp
		self.exp = self.controller.newExperiment(self.etype)
		self.updateExpView()

	@Slot(int)
	def onStarted(self):
		self.updateActiveView()
		i = self.expSelected
		l = self.expCheckedList
		if i >= 0 and i not in l:
			self.sig_hide.emit(self.expSelected)
		self.sig_newCurve.emit()

	@Slot(int)
	def onPaused(self):
		self.timer_start()
		self.updateActiveView()

	@Slot(int)
	def onResumed(self):
		self.updateActiveView()

	@Slot(int)
	def onStoped(self):
		self.timer_start()
		self.deactivate()
		self.expList.append(self.exp)
		self.expSelected = len(self.expList)-1

		e = self.controller.newExperiment(self.etype)
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
		self.exp = e
		self.activate()
		self.updateActiveView()
		self.addExpToListView()
		self.sig_ended.emit()

	@Slot()
	def onDataChanged(self):
		e = self.exp
		c = self.controller
		# print(e)
		c.rlock()
		self.progress_bar.setValue(int(100*(e["currentWl"]-e["startWl"])/(e["stopWl"]-e["startWl"])))
		x = e["x"]
		y = e["y"]
		c.unlock()
		self.sig_updateData.emit(x, y)

	@Slot(float, float)
	def onNewCurrent(self, c1: float, c2: float):
		self.current1_label.setText(f"{c1:+.5e}")
		self.current2_label.setText(f"{c2:+.5e}")

	@Slot()
	def onExit(self):
		self.deactivate()
