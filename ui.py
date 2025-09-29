from PySide6.QtCore import (
	Qt, QCoreApplication, QThread, Signal, Slot, QFile, QRegularExpression,
	QLocale)
from PySide6.QtGui import (
	QGuiApplication, QPalette, QColor, QPixmap, QIcon, QTransform,
	QRegularExpressionValidator, QDoubleValidator, QIntValidator,
	QStandardItemModel, QStandardItem)
from PySide6.QtWidgets import *

# import numpy as np
# import pyqtgraph as pg
import sys

from design import Ui_MainWindow
from experiment import Experiment, Data, Session
# from filenames import *

# class PlotWidget(pg.PlotWidget):
# 	def __init__(self):
# 		super(PlotWidget, self).__init__()
# 		self.setBackground("w")
# 		self.setMinimumSize(700, 500)
# 		styles = {"color": "black", "font-size": "16px", "font": "Calibri"}
# 		#self.setTitle("vac", color="b", size="20pt")
# 		self.setLabel("left", "Current, A / Bias, V", **styles)
# 		self.setLabel("bottom", "Time, S", **styles)
# 		self.addLegend()
# 		self.showGrid(x=True, y=True)
# 		self.plotItem.enableAutoRange(axis=pg.ViewBox.YAxis)
# 		self.zero_axis_pen = pg.mkPen(color='k', width=1)
# 		self.v_line = pg.InfiniteLine(pos=0, angle=0, pen=self.zero_axis_pen)
# 		self.h_line = pg.InfiniteLine(pos=0, angle=90, pen=self.zero_axis_pen)
# 		self.addItem(self.v_line)
# 		self.addItem(self.h_line)

# 		self.viewbox_2 = pg.ViewBox()
# 		self.plotItem.showAxis('right')
# 		self.plotItem.scene().addItem(self.viewbox_2)
# 		self.plotItem.getAxis('right').linkToView(self.viewbox_2)
# 		self.viewbox_2.setXLink(self.plotItem)
# 		self.plotItem.getAxis('right').setLabel('Temperature, C', **styles)
# 		self.updateViews()
# 		self.plotItem.vb.sigResized.connect(self.updateViews)

# 	## Handle view resizing 
# 	def updateViews(self):
# 		## view has resized; update auxiliary views to match
# 		self.viewbox_2.setGeometry(self.plotItem.vb.sceneBoundingRect())
		
# 		## need to re-update linked axes since this was called
# 		## incorrectly while views had different shapes.
# 		## (probably this should be handled in ViewBox.resizeEvent)
# 		self.viewbox_2.linkedViewChanged(self.plotItem.vb, self.viewbox_2.XAxis)

# 	def scatter(self, x, y, color, symbol, size, label=" "):
# 		pen = pg.mkPen(color)
# 		brush = pg.mkBrush(color)
# 		return self.plot(x, y, pen=None, symbol=symbol, symbolSize=size, symbolPen=pen, symbolBrush=brush, name=label)

# 	def scatter_vb2(self, x, y, color, symbol, size, label=" "):
# 		pen = pg.mkPen(color)
# 		brush = pg.mkBrush(color)
# 		line = pg.PlotDataItem(x, y, pen=None, symbol=symbol, symbolSize=size, symbolPen=pen, symbolBrush=brush, name=label)
# 		self.viewbox_2.addItem(line)
# 		self.plot([], [], pen=None, symbol=symbol, symbolSize=size, symbolPen=pen, symbolBrush=brush, name=label)
# 		return line

# 	def plotting(self, x, y, color, style=Qt.SolidLine, label=" "):
# 		return self.plot(x, y, pen=pg.mkPen(color=color, width=2, style=style), name=label)


class MainWindow(QMainWindow, Ui_MainWindow):
	# plot_widget: PlotWidget
	etype: int = 0

	expStd = []
	exp    = []

	wl      = 550
	shutter = False

	start  = Signal(int, Experiment)
	pause  = Signal(int)
	resume = Signal(int)
	stop   = Signal(int)

	setWl          = Signal(float)
	setShutter     = Signal(bool)

	def __init__(self, session: Session, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.centralwidget.resize(200, 200)

		# self.plot_widget = PlotWidget()
		# self.main_splitter.insertWidget(0, self.plot_widget)

		self.setWindowTitle("DSR600")
		self.move(20, 20)

		palette = QGuiApplication.palette()
		palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(120, 120, 120))
		palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button,     QColor(240, 240, 240))
		palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text,       QColor(120, 120, 120))
		palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(120, 120, 120))
		palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base,       QColor(240, 240, 240))
		self.setPalette(palette)

		# <filters>
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
		# </filters>

		self.etype = 0

		# fill STD experiments' parameters
		e = Experiment()
		e.sampleName = "Si"
		e.startWl = 300
		e.stopWl = 1100
		e.stepWl = 5
		e.wl = 300
		e.channel = 2
		self.expStd.append(e)
		
		e = Experiment()
		e.sampleName = "InGaAs"
		e.startWl = 900
		e.stopWl = 1700
		e.stepWl = 10
		e.wl = 900
		e.channel = 2
		self.expStd.append(e)
		
		e = Experiment()
		e.sampleName = ""
		e.startWl = 300
		e.stopWl = 2000
		e.stepWl = 5
		e.wl = 300
		e.channel = 1
		self.expStd.append(e)
		
		# copy current experiments' parameters from STD
		self.exp.append(Experiment())
		self.exp.append(Experiment())
		self.exp.append(Experiment())
		self.updateFromStd(0)
		self.updateFromStd(1)
		self.updateFromStd(2)

		self.session = session

		self.updateExpView()

		self.model = QStandardItemModel()
		self.curves_list.setModel(self.model)
		self.updateCurvesList()

		self.link_signals()

	def updateFromStd(self, etype: int):
		self.updateFromExp(etype, self.expStd[etype])

	def updateFromExp(self, etype: int, exp: Experiment):
		self.exp[etype].status      = exp.status
		self.exp[etype].sampleName  = exp.sampleName
		self.exp[etype].startWl     = exp.startWl
		self.exp[etype].stopWl      = exp.stopWl
		self.exp[etype].stepWl      = exp.stepWl
		self.exp[etype].wl          = exp.wl
		self.exp[etype].delay       = exp.delay
		self.exp[etype].channel     = exp.channel
		self.exp[etype].voltageFlag = exp.voltageFlag
		self.exp[etype].voltage     = exp.voltage
		self.exp[etype].nplc        = exp.nplc
		self.exp[etype].averageFlag = exp.averageFlag
		self.exp[etype].average     = exp.average

	def updateExpView(self):
		print("updateExpView")
		
		e = self.exp[self.etype]

		self.sample_edit.setText(e.sampleName)
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
		self.progress_bar.setValue(int(100*(e.wl-e.startWl)/(e.stopWl-e.startWl)))
		
		self.wl_edit.setText(f"{self.wl}")
		self.shutter_check.setChecked(self.shutter)

		# 0 - idle, 1 - started, 2 - paused, 3 - ended
		if e.status == 0:
			self.start_button.setText("Start")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(True)
			self.frame_meas.setDisabled(False)
			self.frame_amp.setDisabled(False)
			self.frame_mono.setDisabled(False)
			self.tabs.tabBar().setDisabled(False)
		elif e.status == 1:
			self.start_button.setText("Pause")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.tabs.tabBar().setDisabled(True)
		elif e.status == 2:
			self.start_button.setText("Resume")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(False)
			self.tabs.tabBar().setDisabled(True)
		elif e.status == 3:
			self.start_button.setText("Start")
			self.start_button.setDisabled(True)
			self.stop_button.setText("New")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.tabs.tabBar().setDisabled(False)


	# 3 models for every list!!!
	def updateCurvesList(self):
		st = ["new", "running", "paused", "ended"]

		self.session.rlock()
		ids = self.session.ids
		exp = self.session.exp
		self.session.unlock()

		self.model.clear()
		parentItem = self.model.invisibleRootItem()

		it = None

		t = self.etype
		id = ids[t]
		for i in range(len(exp[t])):
			e = exp[t][i]
			e.rlock()
			status = e.status
			sampleName = e.sampleName
			e.unlock()

			item = QStandardItem(f"{i} : {sampleName} - {st[status]}")
			item.setCheckable(True)
			item.setSelectable(True)
			parentItem.appendRow(item)

		self.curves_list.setModel(self.model)

	def link_signals(self):
		print("link_signals")
		self.sample_edit.returnPressed.connect(self.sample_edit_new_slot)
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
		self.start_button.released.connect(self.start_button_slot)
		self.stop_button.released.connect(self.stop_button_slot)

		self.wl_edit.returnPressed.connect(self.wl_edit_slot)
		self.shutter_check.clicked.connect(self.shutter_check_slot)
		
		self.tabs.currentChanged.connect(self.tabs_changed_slot)

		self.start.connect(self.session.start_slot)
		self.pause.connect(self.session.pause_slot)
		self.resume.connect(self.session.resume_slot)
		self.stop.connect(self.session.stop_slot)
		
		# СИГНАЛЫ ДРАЙВЕРУ!!!
		# self.setWl.connect(self.session.setWl_slot)
		# self.setShutter.connect(self.session.setShutter_slot)

	def sample_edit_new_slot(self):
		sampleName = self.sample_edit.text()
		self.exp[self.etype].sampleName = sampleName
		print(f"sample_edit_new_slot \"{sampleName}\"")
	
	def start_edit_new_slot(self):
		startWl = float(self.start_edit.text())
		self.exp[self.etype].startWl = startWl
		print(f"start_edit_new_slot \"{startWl}\"")

	def stop_edit_slot(self):
		stopWl = float(self.stop_edit.text())
		self.exp[self.etype].stopWl = stopWl
		print(f"stop_edit_slot \"{stopWl}\"")

	def step_edit_slot(self):
		stepWl = float(self.step_edit.text())
		self.exp[self.etype].stepWl = stepWl
		print(f"step_edit_slot \"{stepWl}\"")

	def delay_edit_slot(self):
		delay = float(self.delay_edit.text())
		self.exp[self.etype].delay = delay
		print(f"delay_edit_slot \"{delay}\"")

	def channel1_radio_slot(self):
		channel = 1 if self.channel1_radio.isChecked() else 2
		self.exp[self.etype].channel = channel
		print(f"channel1_radio_slot \"{channel}\"")

	def channel2_radio_slot(self):
		channel = 2 if self.channel2_radio.isChecked() else 1
		self.exp[self.etype].channel = channel
		print(f"channel2_radio_slot \"{channel}\"")

	def voltage_check_slot(self):
		voltageFlag = self.voltage_check.isChecked()
		self.exp[self.etype].voltageFlag = voltageFlag
		print(f"voltage_check_slot \"{voltageFlag}\"")

	def voltage_edit_slot(self):
		voltage = float(self.voltage_edit.text())
		self.exp[self.etype].voltage = voltage
		print(f"voltage_edit_slot \"{voltage}\"")

	def nplc_edit_slot(self):
		nplc = int(self.nplc_edit.text())
		self.exp[self.etype].nplc = nplc
		print(f"nplc_edit_slot \"{nplc}\"")

	def average_check_slot(self):
		averageFlag = self.average_check.isChecked()
		self.exp[self.etype].averageFlag = averageFlag
		print(f"average_check_slot \"{averageFlag}\"")

	def average_edit_slot(self):
		average = int(self.average_edit.text())
		self.exp[self.etype].average = average
		print(f"average_edit_slot \"{average}\"")

	def wl_edit_slot(self):
		wl = float(self.wl_edit.text())
		self.wl = wl
		print(f"wl_edit_slot \"{wl}\"")
		self.setWl.emit(wl)

	def shutter_check_slot(self):
		shutter = self.shutter_check.isChecked()
		self.shutter = shutter
		print(f"shutter_check_slot \"{shutter}\"")
		self.setShutter.emit(shutter)

	def tabs_changed_slot(self, index: int):
		print(f"tabs_changed_slot \"{index}\"")
		self.etype = index
		self.updateExpView()
		self.updateCurvesList()

	def start_button_slot(self):
		print(f"start_button_slot \"{self.start_button.text()}\"")
		e = self.exp[self.etype]
		if len(e.sampleName) == 0: return
		if   e.status == 0: e.status = 1; self.start.emit(self.etype, e)
		elif e.status == 1: e.status = 2; self.pause.emit(self.etype)
		elif e.status == 2: e.status = 1; self.resume.emit(self.etype)
		self.updateExpView()
		self.updateCurvesList()

	def stop_button_slot(self):
		print(f"stop_button_slot \"{self.stop_button.text()}\"")
		e = self.exp[self.etype]
		if   e.status == 1: e.status = 3; self.stop.emit(self.etype)
		elif e.status == 2: e.status = 3; self.stop.emit(self.etype)
		elif e.status == 3: self.updateFromStd(self.etype)
		self.updateExpView()
		self.updateCurvesList()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	session = Session()
	window = MainWindow(session)
	window.show()
	app.exec()
