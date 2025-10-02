from PySide6.QtCore import Qt, QThread, Signal, Slot, QRegularExpression, QLocale, QItemSelection, QItemSelectionModel
from PySide6.QtGui import (
	QGuiApplication, QColor, QStandardItemModel, QStandardItem,
	QRegularExpressionValidator, QDoubleValidator, QIntValidator)
from PySide6.QtWidgets import *
import pyqtgraph as pg
import sys
from design import Ui_MainWindow
from exp_control import Ui_exp_control
from res_control import Ui_res_control
from experiment import Experiment
from dsr import DSR

class ExpControl(QWidget, Ui_exp_control):
	exp: Experiment
	expList = []
	expSelected: int
	expCheckedList = []

	wl = 550
	shutter = False

	eThread: QThread

	sig_reset  = Signal()
	sig_start  = Signal()
	sig_pause  = Signal()
	sig_resume = Signal()
	sig_stop   = Signal()

	sig_show       = Signal(int)
	sig_hide       = Signal(int)
	sig_showAll    = Signal()
	sig_hideAll    = Signal()
	sig_new_curve  = Signal()
	sig_updateData = Signal(list, list)

	sig_disable_view = Signal(bool)

	sig_wl      = Signal(float)
	sig_shutter = Signal(bool)

	def __init__(self, etype: int, parent=None):
		super(ExpControl, self).__init__(parent)
		self.setupUi(self)

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

		self.etype = etype

		self.wl = 550
		self.shutter = False

		self.wl_edit.setText(f"{self.wl}")
		self.shutter_check.setChecked(self.shutter)

		# add standard experiments
		self.exp = Experiment(self.etype)
		self.updateExpView()
		self.updateActiveView()

		m = QStandardItemModel()
		m.itemChanged.connect(self.itemChanged_slot)
		self.exp_list_view.setModel(m)
		self.exp_list_view.selectionModel().selectionChanged.connect(self.selectionChanged_slot)
		self.expSelected = -1

		self.link_signals()

		self.eThread = QThread()
		self.eThread.finished.connect(self.eThread.deleteLater)
		self.eThread.start()

	def updateExpView(self):
		e = self.exp

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
		e = self.exp
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
			self.sig_disable_view.emit(False)
		elif e.status == 1:
			self.start_button.setText("Pause")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.exp_list_view.setDisabled(True)
			self.sig_disable_view.emit(True)
		elif e.status == 2:
			self.start_button.setText("Resume")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(False)
			self.exp_list_view.setDisabled(True)
			self.sig_disable_view.emit(True)
		elif e.status == 3:
			self.start_button.setText("Start")
			self.start_button.setDisabled(True)
			self.stop_button.setText("New")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.exp_list_view.setDisabled(False)
			self.sig_disable_view.emit(False)

	def addExpToListView(self):
		i = len(self.expList)-1
		e = self.expList[-1]

		item = QStandardItem(f"{i} : {e.sampleName}")
		item.setCheckable(True)
		item.setSelectable(True)
		item.setEditable(False)
		self.exp_list_view.model().invisibleRootItem().appendRow(item)
		self.exp_list_view.selectionModel().select(item.index(), QItemSelectionModel.SelectionFlag.ClearAndSelect)

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

		e = self.exp
		self.sig_reset .connect(self.reset_slot)
		self.sig_start .connect(e.start)
		self.sig_pause .connect(e.pause)
		self.sig_resume.connect(e.resume)
		self.sig_stop  .connect(e.stop)
		e.started      .connect(self.started_slot)
		e.paused       .connect(self.paused_slot)
		e.resumed      .connect(self.resumed_slot)
		e.stoped       .connect(self.stoped_slot)
		e.dataChanged  .connect(self.dataChanged_slot)

		# СИГНАЛЫ ДРАЙВЕРУ!!!
		# self.sig_wl.connect(self.setWl_slot)
		# self.sig_shutter.connect(self.setShutter_slot)

		# БИНД СЛОТА!!!! setWl_done_slot

	def sample_edit_new_slot(self):
		self.exp.sampleName = self.sample_edit.text()
		self.sample_edit.setStyleSheet("")
	def sample_edit_edited_slot(self, text):
		if self.exp.sampleName != text:
			self.sample_edit.setStyleSheet("background: yellow; color: black")
	def sample_edit_rejected_slot(self):
		self.sample_edit.setStyleSheet("background: red; color: white")

	def start_edit_new_slot(self):
		self.exp.startWl = float(self.start_edit.text())
		self.start_edit.setStyleSheet("")
	def start_edit_edited_slot(self, text):
		if self.exp.startWl != float(text):
			self.start_edit.setStyleSheet("background: yellow")

	def stop_edit_slot(self):
		self.exp.stopWl = float(self.stop_edit.text())
		self.stop_edit.setStyleSheet("")
	def stop_edit_edited_slot(self, text):
		if self.exp.stopWl != float(text):
			self.stop_edit.setStyleSheet("background: yellow")

	def step_edit_slot(self):
		self.exp.stepWl = float(self.step_edit.text())
		self.step_edit.setStyleSheet("")
	def step_edit_edited_slot(self, text):
		if self.exp.stepWl != float(text):
			self.step_edit.setStyleSheet("background: yellow")

	def delay_edit_slot(self):
		self.exp.delay = float(self.delay_edit.text())
		self.delay_edit.setStyleSheet("")
	def delay_edit_edited_slot(self, text):
		if self.exp.delay != float(text):
			self.delay_edit.setStyleSheet("background: yellow")

	def channel1_radio_slot(self):
		self.exp.channel = 1 if self.channel1_radio.isChecked() else 2

	def channel2_radio_slot(self):
		self.exp.channel = 2 if self.channel2_radio.isChecked() else 1

	def voltage_check_slot(self):
		self.exp.voltageFlag = self.voltage_check.isChecked()

	def voltage_edit_slot(self):
		self.exp.voltage = float(self.voltage_edit.text())
		self.voltage_edit.setStyleSheet("")
	def voltage_edit_edited_slot(self, text):
		if self.exp.voltage != float(text):
			self.voltage_edit.setStyleSheet("background: yellow")

	def nplc_edit_slot(self):
		self.exp.nplc = int(self.nplc_edit.text())
		self.nplc_edit.setStyleSheet("")
	def nplc_edit_edited_slot(self, text):
		if self.exp.nplc != int(text):
			self.nplc_edit.setStyleSheet("background: yellow")

	def average_check_slot(self):
		self.exp.averageFlag = self.average_check.isChecked()

	def average_edit_slot(self):
		self.exp.average = int(self.average_edit.text())
		self.average_edit.setStyleSheet("")
	def average_edit_edited_slot(self, text):
		if self.exp.average != int(text):
			self.average_edit.setStyleSheet("background: yellow")

	def wl_edit_slot(self):
		self.wl = float(self.wl_edit.text())
		self.wl_edit.setStyleSheet("")
		self.sig_wl.emit(self.wl)
	def wl_edit_edited_slot(self, text):
		if self.wl != float(text):
			self.wl_edit.setStyleSheet("background: yellow")
	@Slot(float)
	def setWl_done_slot(self, wl: float):
		self.wl_edit.setStyleSheet("background: green")

	def shutter_check_slot(self):
		self.shutter = self.shutter_check.isChecked()
		self.sig_shutter.emit(self.shutter)

	def start_button_slot(self):
		e = self.exp
		if len(e.sampleName) == 0: return
		if e.status == 0:
			e.status = 1
			self.eThread.finished.connect(e.deleteLater)
			e.moveToThread(self.eThread)
			self.sig_start.emit()
		elif e.status == 1:
			e.status = 2
			self.sig_pause.emit()
		elif e.status == 2:
			e.status = 1
			self.sig_resume.emit()

	def stop_button_slot(self):
		e = self.exp
		if   e.status == 0:               self.sig_reset.emit()
		elif e.status == 1: e.status = 3; self.sig_stop.emit()
		elif e.status == 2: e.status = 3; self.sig_stop.emit()

	@Slot(QStandardItem)
	def itemChanged_slot(self, item: QStandardItem):
		print("itemChanged_slot")
		i = item.row()
		c = (item.checkState() == Qt.Checked)
		l = self.expCheckedList
		s = self.expSelected
		if c and (i not in l):
			l.append(i)
			self.sig_show.emit(i)
		elif i in l:
			l.remove(i)
			if i != s:
				self.sig_hide.emit(i)

	@Slot(QItemSelection, QItemSelection)
	def selectionChanged_slot(self, s1: QItemSelection, s2: QItemSelection):
		print("selectionChanged_slot")
		i = self.exp_list_view.selectionModel().selection().indexes()[0].row()
		self.expSelected = i
		e = self.exp
		e1 = self.expList[i]
		if e.status == 0:
			e.fill(e1)
		elif e.status == 3:
			self.exp = e1
		self.updateExpView()
		self.updateActiveView()

		l = self.expCheckedList
		self.sig_hideAll.emit()
		self.sig_show.emit(i)
		for i in l:
			self.sig_show.emit(i)

	@Slot(int)
	def reset_slot(self):
		self.exp.reset()
		self.updateExpView()

	@Slot(int)
	def started_slot(self):
		self.updateActiveView()
		l = self.expCheckedList
		s = self.expSelected
		self.sig_new_curve.emit()
		if s != -1 and s not in l:
			self.sig_hide.emit(self.expSelected)

	@Slot(int)
	def paused_slot(self):
		self.updateActiveView()

	@Slot(int)
	def resumed_slot(self):
		self.updateActiveView()

	@Slot(int)
	def stoped_slot(self):
		e = self.exp
		self.sig_start .disconnect(e.start)
		self.sig_pause .disconnect(e.pause)
		self.sig_resume.disconnect(e.resume)
		self.sig_stop  .disconnect(e.stop)
		e.started      .disconnect(self.started_slot)
		e.paused       .disconnect(self.paused_slot)
		e.resumed      .disconnect(self.resumed_slot)
		e.stoped       .disconnect(self.stoped_slot)
		e.dataChanged  .disconnect(self.dataChanged_slot)
		self.expList.append(e)
		self.expSelected = len(self.expList)-1
		self.addExpToListView()

		e = Experiment(self.etype)
		e.fill(self.exp)
		self.sig_start .connect(e.start)
		self.sig_pause .connect(e.pause)
		self.sig_resume.connect(e.resume)
		self.sig_stop  .connect(e.stop)
		e.started      .connect(self.started_slot)
		e.paused       .connect(self.paused_slot)
		e.resumed      .connect(self.resumed_slot)
		e.stoped       .connect(self.stoped_slot)
		e.dataChanged  .connect(self.dataChanged_slot)
		self.exp = e
		self.updateActiveView()

	@Slot()
	def dataChanged_slot(self):
		e = self.exp
		e.rlock()
		self.progress_bar.setValue(int(100*(e.currentWl-e.startWl)/(e.stopWl-e.startWl)))
		x = e.data[0].copy()
		y = e.data[1].copy()
		e.unlock()
		self.sig_updateData.emit(x, y)

	@Slot()
	def onExit(self):
		self.eThread.quit()
		self.eThread.wait()

class ResControl(QWidget, Ui_res_control):
	sig_show       = Signal(int)
	sig_hide       = Signal(int)
	sig_showAll    = Signal()
	sig_hideAll    = Signal()
	sig_new_curve  = Signal()
	sig_updateData = Signal(list, list)

	def __init__(self, parent=None):
		super(ResControl, self).__init__(parent)
		self.setupUi(self)


class PlotWidget(pg.PlotWidget):
	color_list = [
		QColor("black"),
		QColor("red"),
		QColor("green"),
		QColor("blue"),
		QColor(204, 204, 0),
		QColor(255, 0, 127),
		QColor(0, 204, 204),
		QColor(255, 128, 0)]

	def __init__(self):
		super(PlotWidget, self).__init__()
		self.setBackground("w")
		self.setMinimumSize(700, 500)
		styles = {"color": "black", "font-size": "16px", "font": "Calibri"}
		#self.setTitle("vac", color="b", size="20pt")
		self.setLabel("left", "Current, A", **styles)
		self.setLabel("bottom", "Wavelength, nm", **styles)
		self.addLegend()
		self.showGrid(x=True, y=True)
		# self.setXRange(300, 2000)
		# self.setYRange(0, 1)
		self.getPlotItem().enableAutoRange(axis=pg.ViewBox.XAxis)
		self.getPlotItem().enableAutoRange(axis=pg.ViewBox.YAxis)
		self.zero_axis_pen = pg.mkPen(color="black", width=1)
		self.v_line = pg.InfiniteLine(pos=0, angle=0, pen=self.zero_axis_pen)
		self.h_line = pg.InfiniteLine(pos=0, angle=90, pen=self.zero_axis_pen)
		self.addItem(self.v_line)
		self.addItem(self.h_line)

		self.items = []
		self.color_index = 0

	@Slot()
	def new_curve(self):
		print("new_curve")
		color=self.color_list[self.color_index]
		self.color_index = self.color_index + 1
		if self.color_index >= len(self.color_list):
			self.color_list = 0
		pen = pg.mkPen(color=color, width=1)
		item = pg.PlotCurveItem(pen=pen)
		item.setPen(pen)
		self.items.append(item)
		self.addItem(item)

	@Slot(list, list)
	def updateData(self, x, y):
		print("updateData")
		self.items[-1].setData(x, y)

	@Slot(int)
	def show(self, i):
		print(f"show {i}")
		self.items[i].show()

	@Slot()
	def showAll(self):
		print("showAll")
		for item in self.items:
			item.show()

	@Slot(int)
	def hide(self, i):
		print(f"hide {i}")
		self.items[i].hide()

	@Slot()
	def hideAll(self):
		print("hideAll")
		for item in self.items:
			item.hide()


class MainWindow(QMainWindow, Ui_MainWindow):

	ready = []

	sig_exit = Signal()

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("DSR600")
		self.move(20, 20)
		self.centralwidget.resize(200, 200)

		wl = []
		for i in range(3):
			p = PlotWidget()
			c = ExpControl(i)
			c.sig_show        .connect(p.show)
			c.sig_hide        .connect(p.hide)
			c.sig_showAll     .connect(p.showAll)
			c.sig_hideAll     .connect(p.hideAll)
			c.sig_new_curve   .connect(p.new_curve)
			c.sig_updateData  .connect(p.updateData)
			c.sig_disable_view.connect(self.disable_view)
			self.sig_exit.connect(c.onExit)
			l = QHBoxLayout()
			l.addWidget(p)
			l.addWidget(c)
			w = QWidget()
			w.setLayout(l)
			wl.append(w)

		self.tabs.addTab(wl[0], "Si")
		self.tabs.addTab(wl[1], "InGaAs")
		self.tabs.addTab(wl[2], "Sample")

		p = PlotWidget()
		c = ResControl()
		c.sig_show      .connect(p.show)
		c.sig_hide      .connect(p.hide)
		c.sig_showAll   .connect(p.showAll)
		c.sig_hideAll   .connect(p.hideAll)
		c.sig_new_curve .connect(p.new_curve)
		c.sig_updateData.connect(p.updateData)
		l = QHBoxLayout()
		l.addWidget(p)
		l.addWidget(c)
		w = QWidget()
		w.setLayout(l)

		self.tabs.addTab(w, "Result")
		# self.tabs.setTabEnabled(3, False)

	@Slot(bool)
	def disable_view(self, disable: bool):
		self.tabs.tabBar().setDisabled(disable)

	def closeEvent(self, event):
		self.sig_exit.emit()
		event.accept()

if __name__ == '__main__':
	pg.setConfigOptions(antialias=True)

	app = QApplication(sys.argv)
	window = MainWindow()
	# window = ExpControl()
	# window = ResControl()
	window.show()
	app.exec()
