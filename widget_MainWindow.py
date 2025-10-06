from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication

import sys
import pyqtgraph as pg

from ui_mainWindow import Ui_MainWindow
from widget_PlotWidget import PlotWidget
from widget_ExpControl import ExpControl
from widget_ResControl import ResControl
from data import Data
from device_dsr import DSR
from device_k6482 import K6482

class MainWindow(QMainWindow, Ui_MainWindow):
	sig_exit = Signal()

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("DSR600")
		self.move(20, 20)
		self.centralwidget.resize(200, 200)

		self.data = [Data(), Data(), Data()]

		self.dsr = DSR("/dev/ttyUSB0")
		self.dsr.open()

		self.k6482 = K6482("GPIB0::25::INSTR")
		self.k6482.open()

		self.eThread = QThread()
		self.eThread.finished.connect(self.eThread.deleteLater)
		self.eThread.start()

		self.eThread.finished.connect(self.dsr.close)
		self.eThread.finished.connect(self.dsr.deleteLater)
		self.eThread.finished.connect(self.k6482.deleteLater)

		self.dsr.moveToThread(self.eThread)
		self.k6482.moveToThread(self.eThread)

		n = ["Si", "InGaAs", "Sample", "Result"]
		self.exps = []

		for i in range(3):
			p = PlotWidget()
			e = ExpControl(i, self.data[i], self.dsr, self.k6482, self.eThread)
			self.exps.append(e)

			# self.sig_exit.connect(e.onExit)
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
		e = ResControl(self.data)

		p.setYLabel("Responsivity, A/W")

		self.sig_exit.connect(e.onExit)
		e.sig_updateData.connect(p.updateData)
		e.sig_show      .connect(p.show)
		e.sig_hide      .connect(p.hide)
		e.sig_showAll   .connect(p.showAll)
		e.sig_hideAll   .connect(p.hideAll)
		e.sig_updateDataIndex.connect(p.updateDataIndex)

		l = QHBoxLayout()
		l.addWidget(p)
		l.addWidget(e)

		w = QWidget()
		w.setLayout(l)
		self.tabs.addTab(w, n[3])

		self.tabs.currentChanged.connect(self.onTabChanged)

		self.exps[0].sig_checked.connect(e.onChecked)
		self.exps[1].sig_checked.connect(e.onChecked)
		self.exps[2].sig_checked.connect(e.onChecked)
		self.exps[2].sig_ended.connect(e.onEnded)

		# test
		self.exps[2].sig_newCurve.connect(p.newCurve)
		
		self.exps[0].timer_start()

	@Slot()
	def disableTabBar(self):
		self.tabs.tabBar().setDisabled(True)

	@Slot()
	def enableTabBar(self):
		self.tabs.tabBar().setDisabled(False)

	@Slot(int)
	def onTabChanged(self, index: int):
		for e in self.exps:
			e.timer_stop()
		if index < 3:
			self.exps[index].timer_start()

	def closeEvent(self, event):
		# self.dsr.close()
		# self.k6482.close()
		self.eThread.quit()
		self.eThread.wait()
		self.sig_exit.emit()
		event.accept()

if __name__ == '__main__':
	pg.setConfigOptions(antialias=True)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
