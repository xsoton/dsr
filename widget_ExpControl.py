from PySide6.QtCore import Qt, QThread, Signal, Slot, QRegularExpression, QLocale, QItemSelection, QItemSelectionModel
from PySide6.QtGui import QStandardItemModel, QStandardItem, QRegularExpressionValidator, QDoubleValidator, QIntValidator
from PySide6.QtWidgets import QWidget

from typing import Self, List

from ui_expControl import Ui_expControl
from data import Experiment, Data
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

	def __init__(self, etype: int, data: Data, dsr: DSR, k6482: K6482, thread: QThread, parent=None):
		super(ExpControl, self).__init__(parent)
		self.setupUi(self)

		# starting experiment type
		self.etype = etype
		self.data = data
		self.wl = 550
		self.shutter = False

		self.dsr = dsr
		self.k6482 = k6482
		self.data.exp = Experiment(self.etype, self.dsr, self.k6482)

		self.eThread = thread
		# self.eThread = QThread()
		# self.eThread.finished.connect(self.eThread.deleteLater)
		# self.eThread.start()

		e = self.data.exp
		self.eThread.finished.connect(e.deleteLater)
		r = e.moveToThread(self.eThread)
		print(f"moveToThread is {r}")

		# initialize filters
		re = QRegularExpression(r"[a-zA-Zа-яА-Я0-9\_][a-zA-Zа-яА-Я0-9\_\-\.]*")
		self.sample_edit.setValidator(QRegularExpressionValidator(re, self))

		v = QDoubleValidator(300.00, 2000.00, 2, self)
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

		self.wl_edit.setText(f"{self.wl}")
		self.shutter_check.setChecked(self.shutter)

		m = QStandardItemModel()
		m.itemChanged.connect(self.onItemChanged)
		self.exp_list_view.setModel(m)
		self.exp_list_view.selectionModel().selectionChanged.connect(self.onSelectionChanged)
		self.data.expSelected = -1

		self.updateExpView()
		self.updateActiveView()

		self.link_signals()

		self.sig_shutter.emit(False)

	def updateExpView(self):
		e = self.data.exp

		self.sample_edit.setText(e.sampleName)
		if e.sampleName == "":
			self.sample_edit.setStyleSheet("background-color: yellow")
		else:
			self.sample_edit.setStyleSheet("")
		self.start_edit.setText(f"{e.startWl}")
		self.stop_edit.setText(f"{e.stopWl}")
		self.step_edit.setText(f"{e.stepWl}")
		self.channel1_radio.setChecked(True if e.channel == 1 else False)
		self.channel2_radio.setChecked(True if e.channel == 2 else False)
		self.voltage_check.setChecked(e.voltageFlag)
		self.voltage_edit.setText(f"{e.voltage}")
		self.nplc_edit.setText(f"{e.nplc}")
		self.average_check.setChecked(e.averageFlag)
		self.average_edit.setText(f"{e.average}")
		self.progress_bar.setValue(int(100*(e.currentWl-e.startWl)/(e.stopWl-e.startWl)))

	def updateActiveView(self):
		e = self.data.exp
		# 0 - idle, 1 - started, 2 - paused, 3 - ended
		if e.status == 0:
			self.start_button.setText("Start")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Reset")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(False)
			self.frame_amp.setDisabled(False)
			self.frame_mono.setDisabled(False)
			self.exp_list_view.setDisabled(False)
		elif e.status == 1:
			self.start_button.setText("Pause")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.exp_list_view.setDisabled(True)
		elif e.status == 2:
			self.start_button.setText("Resume")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(False)
			self.exp_list_view.setDisabled(True)
		elif e.status == 3:
			self.start_button.setText("Start")
			self.start_button.setDisabled(True)
			self.stop_button.setText("New")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.exp_list_view.setDisabled(False)

	def addExpToListView(self):
		e = self.data.expList[-1]
		i = len(self.data.expList)-1
		p = self.exp_list_view.model().invisibleRootItem()

		it = QStandardItem(f"{i} : {e.sampleName}")
		it.setCheckable(True)
		it.setSelectable(True)
		it.setEditable(False)
		p.appendRow(it)
		self.exp_list_view.selectionModel().select(it.index(), QItemSelectionModel.SelectionFlag.ClearAndSelect)

	def link_signals(self):
		self.sample_edit.returnPressed.connect(self.sample_edit_new_slot)
		self.sample_edit.inputRejected.connect(self.sample_edit_rejected_slot)
		self.start_edit.returnPressed.connect(self.start_edit_new_slot)
		self.stop_edit.returnPressed.connect(self.stop_edit_slot)
		self.step_edit.returnPressed.connect(self.step_edit_slot)
		self.delay_edit.returnPressed.connect(self.delay_edit_slot)
		self.channel1_radio.clicked.connect(self.channel1_radio_slot)
		self.channel2_radio.clicked.connect(self.channel2_radio_slot)
		self.voltage_check.clicked.connect(self.voltage_check_slot)
		self.voltage_edit.returnPressed.connect(self.voltage_edit_slot)
		self.nplc_edit.returnPressed.connect(self.nplc_edit_slot)
		self.average_check.clicked.connect(self.average_check_slot)
		self.average_edit.returnPressed.connect(self.average_edit_slot)

		self.wl_edit.returnPressed.connect(self.wl_edit_slot)
		self.shutter_check.clicked.connect(self.shutter_check_slot)

		self.start_button.released.connect(self.start_button_slot)
		self.stop_button .released.connect(self.stop_button_slot)

		self.sample_edit .textEdited.connect(self.sample_edit_edited_slot)
		self.start_edit  .textEdited.connect(self.start_edit_edited_slot)
		self.stop_edit   .textEdited.connect(self.stop_edit_edited_slot)
		self.step_edit   .textEdited.connect(self.step_edit_edited_slot)
		self.delay_edit  .textEdited.connect(self.delay_edit_edited_slot)
		self.voltage_edit.textEdited.connect(self.voltage_edit_edited_slot)
		self.nplc_edit   .textEdited.connect(self.nplc_edit_edited_slot)
		self.average_edit.textEdited.connect(self.average_edit_edited_slot)

		self.wl_edit.textEdited.connect(self.wl_edit_edited_slot)

		e = self.data.exp
		self.sig_reset .connect(self.onReset)
		self.sig_start .connect(e.onStart)
		self.sig_pause .connect(e.onPause)
		self.sig_resume.connect(e.onResume)
		self.sig_stop  .connect(e.onStop)
		e.started      .connect(self.onStarted)
		e.paused       .connect(self.onPaused)
		e.resumed      .connect(self.onResumed)
		e.stoped       .connect(self.onStoped)
		e.dataChanged  .connect(self.onDataChanged)

		self.sig_wl         .connect(self.dsr.setWl)
		self.sig_shutter    .connect(self.dsr.setShutter)
		self.dsr.setWlDone  .connect(self.onSetWlDone)
		self.dsr.shutterDone.connect(self.onShutterDone)

	def sample_edit_new_slot(self):
		self.data.exp.sampleName = self.sample_edit.text()
		self.sample_edit.setStyleSheet("")
	def sample_edit_edited_slot(self, text):
		if len(text) == 0 or self.data.exp.sampleName != text:
			self.sample_edit.setStyleSheet("background: yellow; color: black")
	def sample_edit_rejected_slot(self):
		self.sample_edit.setStyleSheet("background: red; color: white")

	def start_edit_new_slot(self):
		self.data.exp.startWl = float(self.start_edit.text())
		self.start_edit.setStyleSheet("")
	def start_edit_edited_slot(self, text):
		if len(text) == 0 or self.data.exp.startWl != float(text):
			self.start_edit.setStyleSheet("background: yellow")

	def stop_edit_slot(self):
		self.data.exp.stopWl = float(self.stop_edit.text())
		self.stop_edit.setStyleSheet("")
	def stop_edit_edited_slot(self, text):
		if len(text) == 0 or self.data.exp.stopWl != float(text):
			self.stop_edit.setStyleSheet("background: yellow")

	def step_edit_slot(self):
		self.data.exp.stepWl = float(self.step_edit.text())
		self.step_edit.setStyleSheet("")
	def step_edit_edited_slot(self, text):
		if len(text) == 0 or self.data.exp.stepWl != float(text):
			self.step_edit.setStyleSheet("background: yellow")

	def delay_edit_slot(self):
		self.data.exp.delay = float(self.delay_edit.text())
		self.delay_edit.setStyleSheet("")
	def delay_edit_edited_slot(self, text):
		if len(text) == 0 or self.data.exp.delay != float(text):
			self.delay_edit.setStyleSheet("background: yellow")

	def channel1_radio_slot(self):
		self.data.exp.channel = 1 if self.channel1_radio.isChecked() else 2

	def channel2_radio_slot(self):
		self.data.exp.channel = 2 if self.channel2_radio.isChecked() else 1

	def voltage_check_slot(self):
		self.data.exp.voltageFlag = self.voltage_check.isChecked()

	def voltage_edit_slot(self):
		self.data.exp.voltage = float(self.voltage_edit.text())
		self.voltage_edit.setStyleSheet("")
	def voltage_edit_edited_slot(self, text):
		if len(text) == 0 or self.data.exp.voltage != float(text):
			self.voltage_edit.setStyleSheet("background: yellow")

	def nplc_edit_slot(self):
		self.data.exp.nplc = int(self.nplc_edit.text())
		self.nplc_edit.setStyleSheet("")
	def nplc_edit_edited_slot(self, text):
		if len(text) == 0 or self.data.exp.nplc != int(text):
			self.nplc_edit.setStyleSheet("background: yellow")

	def average_check_slot(self):
		self.data.exp.averageFlag = self.average_check.isChecked()

	def average_edit_slot(self):
		self.data.exp.average = int(self.average_edit.text())
		self.average_edit.setStyleSheet("")
	def average_edit_edited_slot(self, text):
		if len(text) == 0 or self.data.exp.average != int(text):
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

	def shutter_check_slot(self):
		print("shutter_check_slot")
		self.shutter = self.shutter_check.isChecked()
		self.start_button .setDisabled(True)
		self.stop_button  .setDisabled(True)
		self.frame_meas   .setDisabled(True)
		self.frame_amp    .setDisabled(True)
		self.frame_mono   .setDisabled(True)
		self.exp_list_view.setDisabled(True)
		self.sig_shutter.emit(self.shutter)
	@Slot(bool)
	def onShutterDone(self, shutter: bool):
		print("onShutterDone")
		self.shutter = shutter
		self.shutter_check.setCheckState(Qt.Checked if self.shutter else Qt.Unchecked)
		self.updateActiveView()

	def start_button_slot(self):
		e = self.data.exp
		if len(e.sampleName) == 0: return
		if   e.status == 0: e.status = 1; self.sig_start.emit()
		elif e.status == 1: e.status = 2; self.sig_pause.emit()
		elif e.status == 2: e.status = 1; self.sig_resume.emit()

	def stop_button_slot(self):
		e = self.data.exp
		if   e.status == 0:               self.sig_reset.emit()
		elif e.status == 1: e.status = 3; self.sig_stop.emit()
		elif e.status == 2: e.status = 3; self.sig_stop.emit()

	@Slot(QStandardItem)
	def onItemChanged(self, item: QStandardItem):
		i = item.row()
		c = (item.checkState() == Qt.Checked)
		s = self.data.expSelected
		l = self.data.expCheckedList

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
		l = self.data.expCheckedList

		for idx in s1.indexes():
			i = idx.row()
			self.data.expSelected = i
			if i not in l:
				self.sig_show.emit(i)

		for idx in s2.indexes():
			i = idx.row()
			if i not in l:
				self.sig_hide.emit(i)

		self.data.exp.fill(self.data.expList[self.data.expSelected])

		self.updateExpView()
		self.updateActiveView()

	@Slot(int)
	def onReset(self):
		self.data.exp.reset()
		self.updateExpView()

	@Slot(int)
	def onStarted(self):
		self.updateActiveView()
		i = self.data.expSelected
		l = self.data.expCheckedList
		if i >= 0 and i not in l:
			self.sig_hide.emit(self.data.expSelected)
		self.sig_newCurve.emit()

	@Slot(int)
	def onPaused(self):
		self.updateActiveView()

	@Slot(int)
	def onResumed(self):
		self.updateActiveView()

	@Slot(int)
	def onStoped(self):
		e = self.data.exp
		self.sig_start  .disconnect(e.onStart)
		self.sig_pause  .disconnect(e.onPause)
		self.sig_resume .disconnect(e.onResume)
		self.sig_stop   .disconnect(e.onStop)
		e.started       .disconnect(self.onStarted)
		e.paused        .disconnect(self.onPaused)
		e.resumed       .disconnect(self.onResumed)
		e.stoped        .disconnect(self.onStoped)
		e.dataChanged   .disconnect(self.onDataChanged)
		self.data.expList.append(e)
		self.data.expSelected = len(self.data.expList)-1

		e = Experiment(self.etype, self.dsr, self.k6482)
		e.fill(self.data.exp)
		self.eThread.finished.connect(e.deleteLater)
		r = e.moveToThread(self.eThread)
		print(f"moveToThread is {r}")
		self.sig_start  .connect(e.onStart)
		self.sig_pause  .connect(e.onPause)
		self.sig_resume .connect(e.onResume)
		self.sig_stop   .connect(e.onStop)
		e.started       .connect(self.onStarted)
		e.paused        .connect(self.onPaused)
		e.resumed       .connect(self.onResumed)
		e.stoped        .connect(self.onStoped)
		e.dataChanged   .connect(self.onDataChanged)
		self.data.exp = e
		self.updateActiveView()
		self.addExpToListView()
		self.sig_ended.emit()

	@Slot()
	def onDataChanged(self):
		e = self.data.exp
		e.rlock()
		self.progress_bar.setValue(int(100*(e.currentWl-e.startWl)/(e.stopWl-e.startWl)))
		x = e.data[0].copy()
		y = e.data[1].copy()
		e.unlock()
		self.sig_updateData.emit(x, y)

	# @Slot()
	# def onExit(self):
	# 	self.eThread.quit()
	# 	self.eThread.wait()
