from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication
from PySide6.QtGui import QIcon

import sys
import pyqtgraph as pg

from ui_mainWindow import Ui_MainWindow
from widget_PlotWidget  import PlotWidget
from widget_ExpControl  import ExpControl
from widget_ResControl  import ResControl
from widget_TimeControl import TimeControl
from controller import RespController, TimeController
from device_dsr import DSR
from device_k6482 import K6482

class MainWindow(QMainWindow, Ui_MainWindow):
	debug = False

	sig_exit = Signal()
	index: int

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("DSR600")
		self.move(20, 20)
		self.centralwidget.resize(200, 200)
		self.setWindowIcon(QIcon("img/icon-64.png"))

		pg.setConfigOptions(antialias=True)

		self.dsr = DSR("/dev/ttyUSB0")
		self.dsr.open()

		self.k6482 = K6482("GPIB0::25::INSTR")
		self.k6482.open()

		self.respController = RespController(self.dsr, self.k6482)
		self.timeController = TimeController(self.dsr, self.k6482)

		self.eThread = QThread()
		self.eThread.finished.connect(self.eThread.deleteLater)
		self.eThread.start()

		self.eThread.finished.connect(self.dsr.close)
		self.eThread.finished.connect(self.dsr.deleteLater)
		self.eThread.finished.connect(self.k6482.deleteLater)
		self.eThread.finished.connect(self.respController.onStop)
		self.eThread.finished.connect(self.respController.deleteLater)
		self.eThread.finished.connect(self.timeController.onStop)
		self.eThread.finished.connect(self.timeController.deleteLater)

		self.dsr       .moveToThread(self.eThread)
		self.k6482     .moveToThread(self.eThread)
		self.respController.moveToThread(self.eThread)
		self.timeController.moveToThread(self.eThread)

		n = ["Si", "InGaAs", "Sample", "Result", "Time"]
		self.exps = []
		self.time = None

		for i in range(3):
			p = PlotWidget()
			e = ExpControl(i, self.respController, self.dsr, self.k6482)
			self.exps.append(e)

			# self.sig_exit   .connect(e.onExit)
			e.sig_newCurve  .connect(p.newCurve)
			e.sig_updateData.connect(p.updateData)
			e.sig_show      .connect(p.show)
			e.sig_hide      .connect(p.hide)
			e.sig_showAll   .connect(p.showAll)
			e.sig_hideAll   .connect(p.hideAll)
			e.sig_start     .connect(self.disableTabBar)
			e.sig_ended     .connect(self.enableTabBar)

			l = QHBoxLayout()
			l.addWidget(p)
			l.addWidget(e)

			w = QWidget()
			w.setLayout(l)
			self.tabs.addTab(w, n[i])

		p = PlotWidget()
		r = ResControl(self.exps)
		self.exps.append(r)
		p.setYLabel("Responsivity, A/W")
		# self.sig_exit.connect(e.onExit)
		r.sig_updateData.connect(p.updateData)
		r.sig_show      .connect(p.show)
		r.sig_hide      .connect(p.hide)
		r.sig_showAll   .connect(p.showAll)
		r.sig_hideAll   .connect(p.hideAll)
		r.sig_updateDataIndex.connect(p.updateDataIndex)
		l = QHBoxLayout()
		l.addWidget(p)
		l.addWidget(r)
		w = QWidget()
		w.setLayout(l)
		self.tabs.addTab(w, n[3])

		self.exps[0].sig_checked .connect(r.onChecked)
		self.exps[1].sig_checked .connect(r.onChecked)
		self.exps[2].sig_checked .connect(r.onChecked)
		self.exps[2].sig_ended   .connect(r.onEnded)
		self.exps[2].sig_newCurve.connect(p.newCurve)

		p = PlotWidget()
		e = TimeControl(self.timeController, self.dsr, self.k6482)
		self.exps.append(e)
		self.time = e
		p.setXLabel("Time, s")
		p.setYLabel("Current, A")
		# self.sig_exit   .connect(e.onExit)
		e.sig_newCurve  .connect(p.newCurve)
		e.sig_updateData.connect(p.updateData)
		e.sig_show      .connect(p.show)
		e.sig_hide      .connect(p.hide)
		e.sig_showAll   .connect(p.showAll)
		e.sig_hideAll   .connect(p.hideAll)
		e.sig_start     .connect(self.disableTabBar)
		e.sig_ended     .connect(self.enableTabBar)
		l = QHBoxLayout()
		l.addWidget(p)
		l.addWidget(e)
		w = QWidget()
		w.setLayout(l)
		self.tabs.addTab(w, n[4])

		self.tabs.currentChanged.connect(self.onTabChanged)
		self.onTabChanged(0)

	@Slot()
	def disableTabBar(self):
		if self.debug: print("MainWindow -> disableTabBar")
		self.tabs.tabBar().setDisabled(True)

	@Slot()
	def enableTabBar(self):
		if self.debug: print("MainWindow -> enableTabBar")
		self.tabs.tabBar().setDisabled(False)

	@Slot(int)
	def onTabChanged(self, index: int):
		if self.debug: print(f"MainWindow -> onTabChanged {index}")
		self.index = index
		for i in range(len(self.exps)):
			if i == index:
				self.exps[i].activate()
			else:
				self.exps[i].deactivate()

	def closeEvent(self, event):
		if self.debug: print(f"MainWindow -> closeEvent index = {self.index}")
		if self.index < 3:
			self.exps[self.index].onExit()
			self.respController.onStop()
		if self.index == 4:
			self.time.onExit()
			self.timeController.onStop()
		self.eThread.quit()
		self.eThread.wait()
		event.accept()

if __name__ == '__main__':
	pg.setConfigOptions(antialias=True)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
