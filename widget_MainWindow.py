from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication

import sys
import pyqtgraph as pg

from ui_mainWindow import Ui_MainWindow
from widget_PlotWidget import PlotWidget
from widget_ExpControl import ExpControl
from widget_ResControl import ResControl
from controller import Controller
from device_dsr import DSR
from device_k6482 import K6482

class MainWindow(QMainWindow, Ui_MainWindow):
	sig_exit = Signal()
	index: int

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("DSR600")
		self.move(20, 20)
		self.centralwidget.resize(200, 200)

		self.dsr = DSR("/dev/ttyUSB0")
		self.dsr.open()

		self.k6482 = K6482("GPIB0::25::INSTR")
		self.k6482.open()

		self.controller = Controller(self.dsr, self.k6482)

		self.eThread = QThread()
		self.eThread.finished.connect(self.eThread.deleteLater)
		self.eThread.start()

		self.eThread.finished.connect(self.dsr.close)
		self.eThread.finished.connect(self.dsr.deleteLater)
		self.eThread.finished.connect(self.k6482.deleteLater)
		self.eThread.finished.connect(self.controller.onStop)
		self.eThread.finished.connect(self.controller.deleteLater)

		self.dsr       .moveToThread(self.eThread)
		self.k6482     .moveToThread(self.eThread)
		self.controller.moveToThread(self.eThread)

		n = ["Si", "InGaAs", "Sample", "Result"]
		self.exps = []

		for i in range(3):
			p = PlotWidget()
			e = ExpControl(i, self.controller, self.dsr, self.k6482)
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

		self.tabs.currentChanged.connect(self.onTabChanged)

		self.exps[0].sig_checked .connect(r.onChecked)
		self.exps[1].sig_checked .connect(r.onChecked)
		self.exps[2].sig_checked .connect(r.onChecked)
		self.exps[2].sig_ended   .connect(r.onEnded)
		self.exps[2].sig_newCurve.connect(p.newCurve)
		
		self.onTabChanged(0)

	@Slot()
	def disableTabBar(self):
		self.tabs.tabBar().setDisabled(True)

	@Slot()
	def enableTabBar(self):
		self.tabs.tabBar().setDisabled(False)

	@Slot(int)
	def onTabChanged(self, index: int):
		self.index = index
		for i in range(3):
			if i == index:
				self.exps[i].activate()
			else:
				self.exps[i].deactivate()

	def closeEvent(self, event):
		if self.index < 3:
			self.exps[self.index].onExit()
			self.controller.onStop()
		self.eThread.quit()
		self.eThread.wait()
		event.accept()

if __name__ == '__main__':
	pg.setConfigOptions(antialias=True)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
