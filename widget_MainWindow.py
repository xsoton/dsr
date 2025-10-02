from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication

import sys
import pyqtgraph as pg

from ui_mainWindow import Ui_MainWindow
from widget_PlotWidget import PlotWidget
from widget_ExpControl import ExpControl
from widget_ResControl import ResControl
from data import Data

class MainWindow(QMainWindow, Ui_MainWindow):
	sig_exit = Signal()

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("DSR600")
		self.move(20, 20)
		self.centralwidget.resize(200, 200)

		self.data = [Data(), Data(), Data()]

		n = ["Si", "InGaAs", "Sample", "Result"]
		exps = []

		for i in range(3):
			p = PlotWidget()
			e = ExpControl(i, self.data[i])
			exps.append(e)

			self.sig_exit.connect(e.onExit)
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

		exps[0].sig_checked.connect(e.onChecked)
		exps[1].sig_checked.connect(e.onChecked)
		exps[2].sig_checked.connect(e.onChecked)
		exps[2].sig_ended.connect(e.onEnded)

		# test
		exps[2].sig_newCurve.connect(p.newCurve)

	@Slot()
	def disableTabBar(self):
		self.tabs.tabBar().setDisabled(True)

	@Slot()
	def enableTabBar(self):
		self.tabs.tabBar().setDisabled(False)

	def closeEvent(self, event):
		self.sig_exit.emit()
		event.accept()

if __name__ == '__main__':
	pg.setConfigOptions(antialias=True)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
