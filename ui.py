from PySide6.QtCore import (
	Qt, QCoreApplication, Signal, Slot, QFile, QRegularExpression,
	QLocale)
from PySide6.QtGui import (
	QGuiApplication, QPalette, QColor, QPixmap, QIcon, QTransform,
	QRegularExpressionValidator, QDoubleValidator, QIntValidator)
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
	eid:   int = 0

	new    = Signal(int)
	start  = Signal(int)
	pause  = Signal(int)
	resume = Signal(int)
	stop   = Signal(int)

	newSampleName  = Signal(int, str)
	newStartWl     = Signal(int, float)
	newStopWl      = Signal(int, float)
	newStepWl      = Signal(int, float)
	newDelay       = Signal(int, float)
	newChannel     = Signal(int, int)
	newVoltageFlag = Signal(int, bool)
	newVoltage     = Signal(int, float)
	newNplc        = Signal(int, int)
	newAverageFlag = Signal(int, bool)
	newAverage     = Signal(int, int)

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

		self.session = session
		self.etype = 0
		self.eid = 0

		self.set_parameters()

		self.link_signals()

	@Slot()
	def set_parameters(self):
		print("set_parameters")
		self.eid = self.session.get_id(self.etype)
		e = self.session.get_exp(self.etype)
		e.rlock()
		status      = e.status
		sampleName  = e.sampleName
		startWl     = e.startWl
		stopWl      = e.stopWl
		stepWl      = e.stepWl
		channel     = e.channel
		voltageFlag = e.voltageFlag
		voltage     = e.voltage
		nplc        = e.nplc
		averageFlag = e.averageFlag
		average     = e.average
		wl          = e.wl
		e.unlock()
		self.sample_edit.setText(sampleName)
		self.start_edit.setText(f"{startWl}")
		self.stop_edit.setText(f"{stopWl}")
		self.step_edit.setText(f"{stepWl}")
		self.channel1_radio.setChecked(True if channel == 1 else False)
		self.channel2_radio.setChecked(True if channel == 2 else False)
		self.voltage_check.setChecked(voltageFlag)
		self.voltage_edit.setText(f"{voltage}")
		self.nplc_edit.setText(f"{nplc}")
		self.average_check.setChecked(averageFlag)
		self.average_edit.setText(f"{average}")
		self.progress_bar.setValue(int(100*(wl-startWl)/(stopWl-startWl)))

		# 0 - idle, 1 - started, 2 - paused, 3 - ended
		if status == 0:
			self.start_button.setText("Start")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(True)
			self.frame_meas.setDisabled(False)
			self.frame_amp.setDisabled(False)
			self.frame_mono.setDisabled(False)
			self.tabs.tabBar().setDisabled(False)
		elif status == 1:
			self.start_button.setText("Pause")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.tabs.tabBar().setDisabled(True)
		elif status == 2:
			self.start_button.setText("Resume")
			self.start_button.setDisabled(False)
			self.stop_button.setText("Stop")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(False)
			self.tabs.tabBar().setDisabled(True)
		elif status == 3:
			self.start_button.setText("Start")
			self.start_button.setDisabled(True)
			self.stop_button.setText("New")
			self.stop_button.setDisabled(False)
			self.frame_meas.setDisabled(True)
			self.frame_amp.setDisabled(True)
			self.frame_mono.setDisabled(True)
			self.tabs.tabBar().setDisabled(False)

	def link_signals(self):
		print("link_signals")
		self.sample_edit.returnPressed.connect(self.sample_edit_new_slot)
		self.start_edit.returnPressed.connect(self.start_edit_new_slot)
		self.stop_edit.returnPressed.connect(self.stop_edit_slot)
		self.step_edit.returnPressed.connect(self.step_edit_slot)
		self.delay_edit.returnPressed.connect(self.delay_edit_slot)
		self.wl_edit.returnPressed.connect(self.wl_edit_slot)
		self.shutter_check.clicked.connect(self.shutter_check_slot)
		self.channel1_radio.clicked.connect(self.channel1_radio_slot)
		self.channel2_radio.clicked.connect(self.channel2_radio_slot)
		self.voltage_check.clicked.connect(self.voltage_check_slot)
		self.voltage_edit.returnPressed.connect(self.voltage_edit_slot)
		self.nplc_edit.returnPressed.connect(self.nplc_edit_slot)
		self.average_check.clicked.connect(self.average_check_slot)
		self.average_edit.returnPressed.connect(self.average_edit_slot)
		self.start_button.released.connect(self.start_button_slot)
		self.stop_button.released.connect(self.stop_button_slot)
		self.tabs.currentChanged.connect(self.tabs_changed_slot)

		self.session.expChanged.connect(self.set_parameters)

		self.new.connect(self.session.new_slot)
		self.start.connect(self.session.start_slot)
		self.pause.connect(self.session.pause_slot)
		self.resume.connect(self.session.resume_slot)
		self.stop.connect(self.session.stop_slot)
		self.newSampleName.connect(self.session.newSampleName_slot)
		self.newStartWl.connect(self.session.newStartWl_slot)
		self.newStopWl.connect(self.session.newStopWl_slot)
		self.newStepWl.connect(self.session.newStepWl_slot)
		self.newDelay.connect(self.session.newDelay_slot)
		self.newChannel.connect(self.session.newChannel_slot)
		self.newVoltageFlag.connect(self.session.newVoltageFlag_slot)
		self.newVoltage.connect(self.session.newVoltage_slot)
		self.newNplc.connect(self.session.newNplc_slot)
		self.newAverageFlag.connect(self.session.newAverageFlag_slot)
		self.newAverage.connect(self.session.newAverage_slot)
		self.setWl.connect(self.session.setWl_slot)
		self.setShutter.connect(self.session.setShutter_slot)

		
	def sample_edit_new_slot(self):
		sampleName = self.sample_edit.text()
		print(f"sample_edit_new_slot \"{sampleName}\"")
		self.newSampleName.emit(self.etype, sampleName)
	
	def start_edit_new_slot(self):
		startWl = float(self.start_edit.text())
		print(f"start_edit_new_slot \"{startWl}\"")
		self.newStartWl.emit(self.etype, startWl)

	def stop_edit_slot(self):
		stopWl = float(self.stop_edit.text())
		print(f"stop_edit_slot \"{stopWl}\"")
		self.newStopWl.emit(self.etype, stopWl)

	def step_edit_slot(self):
		stepWl = float(self.step_edit.text())
		print(f"step_edit_slot \"{stepWl}\"")
		self.newStepWl.emit(self.etype, stepWl)

	def delay_edit_slot(self):
		delay = float(self.delay_edit.text())
		print(f"delay_edit_slot \"{delay}\"")
		self.newDelay.emit(self.etype, delay)

	def channel1_radio_slot(self):
		channel = 1 if self.channel1_radio.isChecked() else 2
		print(f"channel1_radio_slot \"{channel}\"")
		self.newChannel.emit(self.etype, channel)

	def channel2_radio_slot(self):
		channel = 2 if self.channel2_radio.isChecked() else 1
		print(f"channel2_radio_slot \"{channel}\"")
		self.newChannel.emit(self.etype, channel)

	def voltage_check_slot(self):
		voltageFlag = self.voltage_check.isChecked()
		print(f"voltage_check_slot \"{voltageFlag}\"")
		self.newVoltageFlag.emit(self.etype, voltageFlag)

	def voltage_edit_slot(self):
		voltage = float(self.voltage_edit.text())
		print(f"voltage_edit_slot \"{voltage}\"")
		self.newVoltage.emit(self.etype, voltage)

	def nplc_edit_slot(self):
		nplc = int(self.nplc_edit.text())
		print(f"nplc_edit_slot \"{nplc}\"")
		self.newNplc.emit(self.etype, nplc)

	def average_check_slot(self):
		averageFlag = self.average_check.isChecked()
		print(f"average_check_slot \"{averageFlag}\"")
		self.newAverageFlag.emit(self.etype, averageFlag)

	def average_edit_slot(self):
		average = int(self.average_edit.text())
		print(f"average_edit_slot \"{average}\"")
		self.newAverage.emit(self.etype, average)

	def wl_edit_slot(self):
		wl = float(self.wl_edit.text())
		print(f"wl_edit_slot \"{wl}\"")
		self.setWl.emit(wl)

	def shutter_check_slot(self):
		shutterFlag = self.shutter_check.isChecked()
		print(f"shutter_check_slot \"{shutterFlag}\"")
		self.setShutter.emit(shutterFlag)

	def start_button_slot(self):
		print(f"start_button_slot \"{self.start_button.text()}\"")
		self.session.rlock()
		e = self.session.get_exp(self.etype)
		self.session.unlock()
		e.wlock()
		s = e.status
		e.unlock()
		if   s == 0: self.start.emit(self.etype)
		elif s == 1: self.pause.emit(self.etype)
		elif s == 2: self.resume.emit(self.etype)

	def stop_button_slot(self):
		print(f"stop_button_slot \"{self.stop_button.text()}\"")
		self.session.rlock()
		e = self.session.get_exp(self.etype)
		self.session.unlock()
		e.wlock()
		s = e.status
		e.unlock()
		if   s == 1: self.stop.emit(self.etype)
		elif s == 2: self.stop.emit(self.etype)
		elif s == 3: self.new.emit(self.etype)

	def tabs_changed_slot(self, index: int):
		print(f"tabs_changed_slot \"{index}\"")
		self.etype = index
		self.set_parameters()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	session = Session()
	window = MainWindow(session)
	window.show()
	app.exec()
