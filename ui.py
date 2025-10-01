from PySide6.QtCore import Qt, QThread, Signal, Slot, QRegularExpression, QLocale, QItemSelection, QItemSelectionModel
from PySide6.QtGui import (
	QGuiApplication, QColor, QStandardItemModel, QStandardItem,
	QRegularExpressionValidator, QDoubleValidator, QIntValidator)
from PySide6.QtWidgets import *
import pyqtgraph as pg
import sys
from design import Ui_MainWindow
from experiment import Experiment
from dsr import DSR

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

	def new_curve(self):
		color=self.color_list[self.color_index]
		self.color_index = self.color_index + 1
		if self.color_index >= len(self.color_list):
			self.color_list = 0
		pen = pg.mkPen(color=color, width=1)
		item = pg.PlotCurveItem(pen=pen)
		item.setPen(pen)
		self.items.append(item)
		self.addItem(item)

	def updateData(self, x, y):
		self.items[-1].setData(x, y)

	def show(self, i):
		self.items[i].show()

	def showAll(self):
		for item in self.items:
			item.show()

	def hide(self, i):
		self.items[i].hide()

	def hideAll(self):
		for item in self.items:
			item.hide()


class MainWindow(QMainWindow, Ui_MainWindow):
	etype: int = 0

	exp = []
	expList = [[], [], []]
	dataShowList = [[], [], []]

	wl      = 550
	shutter = False

	expListModels = []
	expSelectionList = []
	expCheckedList = [[], [], []]

	plotWidgets = []

	eThread: QThread

	sig_new    = Signal()
	sig_reset  = Signal()
	sig_start  = Signal()
	sig_pause  = Signal()
	sig_resume = Signal()
	sig_stop   = Signal()

	sig_wl      = Signal(float)
	sig_shutter = Signal(bool)

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("DSR600")
		self.move(20, 20)
		self.centralwidget.resize(200, 200)

		self.plotWidgets.append(PlotWidget())
		self.plotWidgets.append(PlotWidget())
		self.plotWidgets.append(PlotWidget())
		# self.plotWidgets.append(PlotWidget())
		self.tabs.addTab(self.plotWidgets[0], "Si")
		self.tabs.addTab(self.plotWidgets[1], "InGaAs")
		self.tabs.addTab(self.plotWidgets[2], "Sample")
		# self.tabs.addTab(self.plotWidgets[3], "Result")
		# self.tabs.setTabEnabled(3, False)

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

		# starting experiment type
		self.etype = 0

		self.wl_edit.setText(f"{self.wl}")
		self.shutter_check.setChecked(self.shutter)

		# add standard experiments
		self.exp.append(Experiment(0))
		self.exp.append(Experiment(1))
		self.exp.append(Experiment(2))
		self.updateExpView()
		self.updateActiveView()

		self.expListModels.append(QStandardItemModel())
		self.expListModels.append(QStandardItemModel())
		self.expListModels.append(QStandardItemModel())
		self.expListModels[0].itemChanged.connect(self.itemChanged_slot)
		self.expListModels[1].itemChanged.connect(self.itemChanged_slot)
		self.expListModels[2].itemChanged.connect(self.itemChanged_slot)
		self.exp_list_view.setModel(self.expListModels[0])
		self.exp_list_view.selectionModel().selectionChanged.connect(self.selectionChanged_slot)
		self.expSelectionList.append(-1)
		self.expSelectionList.append(-1)
		self.expSelectionList.append(-1)
		self.updateExpListView()

		self.link_signals()

		self.eThread = QThread()
		self.eThread.finished.connect(self.eThread.deleteLater)
		self.eThread.start()

	def updateExpView(self):
		e = self.exp[self.etype]

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
		e = self.exp[self.etype]
		# 0 - idle, 1 - started, 2 - paused, 3 - ended
		if e.status == 0:
			self.start_button.setText("Start")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Reset")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(False)
			self.frame_amp.setDisabled(False)
			self.frame_mono.setDisabled(False)
			self.tabs.tabBar().setDisabled(False)
			self.exp_list_view.setDisabled(False)
		elif e.status == 1:
			self.start_button.setText("Pause")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.tabs.tabBar().setDisabled(True)
			self.exp_list_view.setDisabled(True)
		elif e.status == 2:
			self.start_button.setText("Resume")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(False)
			self.tabs.tabBar().setDisabled(True)
			self.exp_list_view.setDisabled(True)
		elif e.status == 3:
			self.start_button.setText("Start")
			self.start_button.setDisabled(True)
			self.stop_button.setText("New")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.tabs.tabBar().setDisabled(False)
			self.exp_list_view.setDisabled(False)

	def updateExpListView(self):
		l = self.expList[self.etype]
		s = self.expSelectionList[self.etype]
		index = None
		make_selection = False

		self.exp_list_view.selectionModel().selectionChanged.disconnect(self.selectionChanged_slot)

		model = self.expListModels[self.etype]
		model.itemChanged.disconnect(self.itemChanged_slot)
		model.clear()
		parentItem = model.invisibleRootItem()

		for i in range(len(l)):
			e = l[i]

			e.rlock()
			status = e.status
			sampleName = e.sampleName
			e.unlock()

			item = QStandardItem(f"{i} : {sampleName}")
			item.setCheckable(True)
			item.setSelectable(True)
			item.setEditable(False)
			parentItem.appendRow(item)
			if i == s:
				make_selection = True
				index = item.index()
			if i in self.expCheckedList[self.etype]:
				item.setCheckState(Qt.Checked)

		model.itemChanged.connect(self.itemChanged_slot)

		self.exp_list_view.setModel(model)
		if make_selection:
			self.exp_list_view.selectionModel().select(index, QItemSelectionModel.SelectionFlag.ClearAndSelect)
		self.exp_list_view.selectionModel().selectionChanged.connect(self.selectionChanged_slot)

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

		self.tabs.currentChanged.connect(self.tabs_changed_slot)

		self.sig_reset .connect(self.reset_slot)

		e = self.exp[self.etype]
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
		# self.sig_wl.connect(self.session.setWl_slot)
		# self.sig_shutter.connect(self.session.setShutter_slot)

		# БИНД СЛОТА!!!! setWl_done_slot

	def sample_edit_new_slot(self):
		self.exp[self.etype].sampleName = self.sample_edit.text()
		self.sample_edit.setStyleSheet("")
	def sample_edit_edited_slot(self, text):
		if self.exp[self.etype].sampleName != text:
			self.sample_edit.setStyleSheet("background: yellow; color: black")
	def sample_edit_rejected_slot(self):
		self.sample_edit.setStyleSheet("background: red; color: white")

	def start_edit_new_slot(self):
		self.exp[self.etype].startWl = float(self.start_edit.text())
		self.start_edit.setStyleSheet("")
	def start_edit_edited_slot(self, text):
		if self.exp[self.etype].startWl != float(text):
			self.start_edit.setStyleSheet("background: yellow")

	def stop_edit_slot(self):
		self.exp[self.etype].stopWl = float(self.stop_edit.text())
		self.stop_edit.setStyleSheet("")
	def stop_edit_edited_slot(self, text):
		if self.exp[self.etype].stopWl != float(text):
			self.stop_edit.setStyleSheet("background: yellow")

	def step_edit_slot(self):
		self.exp[self.etype].stepWl = float(self.step_edit.text())
		self.step_edit.setStyleSheet("")
	def step_edit_edited_slot(self, text):
		if self.exp[self.etype].stepWl != float(text):
			self.step_edit.setStyleSheet("background: yellow")

	def delay_edit_slot(self):
		self.exp[self.etype].delay = float(self.delay_edit.text())
		self.delay_edit.setStyleSheet("")
	def delay_edit_edited_slot(self, text):
		if self.exp[self.etype].delay != float(text):
			self.delay_edit.setStyleSheet("background: yellow")

	def channel1_radio_slot(self):
		self.exp[self.etype].channel = 1 if self.channel1_radio.isChecked() else 2

	def channel2_radio_slot(self):
		self.exp[self.etype].channel = 2 if self.channel2_radio.isChecked() else 1

	def voltage_check_slot(self):
		self.exp[self.etype].voltageFlag = self.voltage_check.isChecked()

	def voltage_edit_slot(self):
		self.exp[self.etype].voltage = float(self.voltage_edit.text())
		self.voltage_edit.setStyleSheet("")
	def voltage_edit_edited_slot(self, text):
		if self.exp[self.etype].voltage != float(text):
			self.voltage_edit.setStyleSheet("background: yellow")

	def nplc_edit_slot(self):
		self.exp[self.etype].nplc = int(self.nplc_edit.text())
		self.nplc_edit.setStyleSheet("")
	def nplc_edit_edited_slot(self, text):
		if self.exp[self.etype].nplc != int(text):
			self.nplc_edit.setStyleSheet("background: yellow")

	def average_check_slot(self):
		self.exp[self.etype].averageFlag = self.average_check.isChecked()

	def average_edit_slot(self):
		self.exp[self.etype].average = int(self.average_edit.text())
		self.average_edit.setStyleSheet("")
	def average_edit_edited_slot(self, text):
		if self.exp[self.etype].average != int(text):
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

	def tabs_changed_slot(self, index: int):
		e = self.exp[self.etype]
		self.sig_start .disconnect(e.start)
		self.sig_pause .disconnect(e.pause)
		self.sig_resume.disconnect(e.resume)
		self.sig_stop  .disconnect(e.stop)
		e.started      .disconnect(self.started_slot)
		e.paused       .disconnect(self.paused_slot)
		e.resumed      .disconnect(self.resumed_slot)
		e.stoped       .disconnect(self.stoped_slot)
		e.dataChanged  .disconnect(self.dataChanged_slot)

		self.etype = index

		e = self.exp[self.etype]
		self.sig_start .connect(e.start)
		self.sig_pause .connect(e.pause)
		self.sig_resume.connect(e.resume)
		self.sig_stop  .connect(e.stop)
		e.started      .connect(self.started_slot)
		e.paused       .connect(self.paused_slot)
		e.resumed      .connect(self.resumed_slot)
		e.stoped       .connect(self.stoped_slot)
		e.dataChanged  .connect(self.dataChanged_slot)

		self.updateExpView()
		self.updateActiveView()
		self.updateExpListView()

	def start_button_slot(self):
		e = self.exp[self.etype]
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
		e = self.exp[self.etype]
		if   e.status == 0:               self.sig_reset.emit()
		elif e.status == 1: e.status = 3; self.sig_stop.emit()
		elif e.status == 2: e.status = 3; self.sig_stop.emit()

	@Slot(QStandardItem)
	def itemChanged_slot(self, item: QStandardItem):
		i = item.row()
		c = (item.checkState() == Qt.Checked)
		l = self.expCheckedList[self.etype]
		s = self.expSelectionList[self.etype]
		p = self.plotWidgets[self.etype]
		if c and (i not in l):
			l.append(i)
			p.show(i)
		elif i in l:
			l.remove(i)
			if i != s:
				p.hide(i)

	@Slot(QItemSelection, QItemSelection)
	def selectionChanged_slot(self, s1: QItemSelection, s2: QItemSelection):
		i = self.exp_list_view.selectionModel().selection().indexes()[0].row()
		self.expSelectionList[self.etype] = i
		e = self.exp[self.etype]
		e1 = self.expList[self.etype][i]
		if e.status == 0:
			e.fill(e1)
		elif e.status == 3:
			self.exp[self.etype] = e1
		self.updateExpView()
		self.updateActiveView()

		l = self.expCheckedList[self.etype]
		p = self.plotWidgets[self.etype]
		p.hideAll()
		p.show(i)
		for i in l:
			p.show(i)

	@Slot(int)
	def reset_slot(self):
		self.exp[self.etype].reset()
		self.updateExpView()

	@Slot(int)
	def started_slot(self):
		self.updateActiveView()
		l = self.expCheckedList[self.etype]
		p = self.plotWidgets[self.etype]
		p.hideAll()
		for i in l:
			p.show(i)
		self.plotWidgets[self.etype].new_curve()

	@Slot(int)
	def paused_slot(self):
		self.updateActiveView()

	@Slot(int)
	def resumed_slot(self):
		self.updateActiveView()

	@Slot(int)
	def stoped_slot(self):
		e = self.exp[self.etype]
		self.sig_start .disconnect(e.start)
		self.sig_pause .disconnect(e.pause)
		self.sig_resume.disconnect(e.resume)
		self.sig_stop  .disconnect(e.stop)
		e.started      .disconnect(self.started_slot)
		e.paused       .disconnect(self.paused_slot)
		e.resumed      .disconnect(self.resumed_slot)
		e.stoped       .disconnect(self.stoped_slot)
		e.dataChanged  .disconnect(self.dataChanged_slot)
		self.expList[self.etype].append(e)
		self.expSelectionList[self.etype] = len(self.expList[self.etype])-1

		e = Experiment(self.etype)
		e.fill(self.exp[self.etype])
		self.sig_start .connect(e.start)
		self.sig_pause .connect(e.pause)
		self.sig_resume.connect(e.resume)
		self.sig_stop  .connect(e.stop)
		e.started      .connect(self.started_slot)
		e.paused       .connect(self.paused_slot)
		e.resumed      .connect(self.resumed_slot)
		e.stoped       .connect(self.stoped_slot)
		e.dataChanged  .connect(self.dataChanged_slot)
		self.exp[self.etype] = e
		self.updateActiveView()
		self.updateExpListView()

	@Slot()
	def dataChanged_slot(self):
		e = self.exp[self.etype]
		e.rlock()
		self.progress_bar.setValue(int(100*(e.currentWl-e.startWl)/(e.stopWl-e.startWl)))
		x = e.data[0].copy()
		y = e.data[1].copy()
		e.unlock()
		self.plotWidgets[self.etype].updateData(x, y)

	def closeEvent(self, event):
		self.eThread.quit()
		self.eThread.wait()
		event.accept()

if __name__ == '__main__':
	pg.setConfigOptions(antialias=True)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
