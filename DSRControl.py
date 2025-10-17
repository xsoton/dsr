from PySide6.QtCore import Qt, QThread, Signal, Slot, QLocale, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QWidget

import sys

from ui_DSRControl import Ui_DSRControl
from DSR import DSR

class DSRControl(QWidget, Ui_DSRControl):
	debug = False

	getWl      = Signal()
	setWl      = Signal(float)
	getShutter = Signal()
	setShutter = Signal(bool)

	newWl      = Signal(float)
	newShutter = Signal(bool)

	def __init__(self, parent=None):
		super(DSRControl, self).__init__(parent)
		self.setupUi(self)

		self.activated = True

		self.wl = 0.0
		self.shutter = False

		self.dsr = DSR("/dev/ttyUSB0")
		self.dsr.open()

		self.eThread = QThread()
		self.eThread.finished.connect(self.eThread.deleteLater)
		self.eThread.finished.connect(self.dsr.close)
		self.eThread.finished.connect(self.dsr.deleteLater)
		self.eThread.start()
		self.dsr.moveToThread(self.eThread)

		re = QRegularExpression(r"((2000)|(1\d{3})|([2-9]\d{2}))(\.\d{,3})?")
		v = QRegularExpressionValidator(re, self)
		v.setLocale(QLocale(QLocale.C))
		self.edit_wl.setValidator(v)

		self.link_signals()

		if len(self.dsr.get_error()) > 0:
			self.setDisabled(True)
			print(self.dsr.get_error())
		else:
			self.getWl.emit()
			self.getShutter.emit()

	def link_signals(self):
		if self.debug: print(f"DSRControl -> link_signals")

		self.edit_wl.returnPressed.connect(self.wl_pressed)
		self.edit_wl.textEdited   .connect(self.wl_edited)
		self.edit_wl.inputRejected.connect(self.wl_rejected)

		self.check_shutter.clicked.connect(self.shutter_clicked)

		self.getWl    .connect(self.dsr.getWl)
		self.setWl    .connect(self.dsr.setWl)
		self.dsr.newWl.connect(self.onNewWl)

		self.getShutter    .connect(self.dsr.getShutter)
		self.setShutter    .connect(self.dsr.setShutter)
		self.dsr.newShutter.connect(self.onNewShutter)

	def activate(self):
		if self.debug: print(f"DSRControl -> activate")
		if not self.activated:
			self.activated = True
			self.setDisabled(False)

	def deactivate(self):
		if self.debug: print(f"DSRControl -> deactivate")
		self.activated = False
		self.setDisabled(True)

	def wl_pressed(self):
		if self.debug: print(f"DSRControl -> wl_pressed")
		wl = float(self.edit_wl.text())
		if wl < 200.00 or wl > 2000.00:
			self.edit_wl.setStyleSheet("background: red; color: white")
		else:
			self.edit_wl.setStyleSheet("")
			self.setDisabled(True)
			self.setWl.emit(wl)

	def wl_edited(self, text):
		if self.debug: print(f"DSRControl -> wl_edited")
		if len(text) == 0 or self.wl != float(text):
			self.edit_wl.setStyleSheet("background: yellow")
		else:
			self.edit_wl.setStyleSheet("")

	def wl_rejected(self):
		if self.debug: print(f"DSRControl -> wl_rejected")
		self.edit_wl.setStyleSheet("background: red; color: white")

	@Slot(float)
	def onNewWl(self, wl: float):
		if self.debug: print(f"DSRControl -> newWl {wl}")
		self.wl = wl
		self.edit_wl.setStyleSheet("background: green; color: white")
		self.edit_wl.setText(f"{self.wl:.3f}")
		self.setDisabled(not self.activated)
		self.newWl.emit(self.wl)

	def shutter_clicked(self):
		if self.debug: print(f"DSRControl -> shutter_clicked")
		self.setDisabled(True)
		self.setShutter.emit(self.check_shutter.isChecked())

	@Slot(bool)
	def onNewShutter(self, shutter: bool):
		if self.debug: print(f"DSRControl -> newShutter {shutter}")
		self.shutter = shutter
		self.check_shutter.setCheckState(Qt.Checked if self.shutter else Qt.Unchecked)
		self.setDisabled(not self.activated)
		self.newShutter.emit(self.shutter)

	def closeEvent(self, event):
		if self.debug: print(f"DSRControl -> closeEvent")
		self.eThread.quit()
		self.eThread.wait()
		event.accept()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = DSRControl()
	w.show()
	app.exec()
