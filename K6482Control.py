from PySide6.QtCore import Qt, QThread, QTimer, Signal, Slot, QLocale, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QDoubleValidator
from PySide6.QtWidgets import QApplication, QWidget

import sys

from ui_K6482Control import Ui_K6482Control
from K6482 import K6482

class K6482Control(QWidget, Ui_K6482Control):
	debug = True

	getCurrent     = Signal()
	getChannel     = Signal()
	setChannel     = Signal(int)
	getOutput      = Signal()
	setOutput      = Signal(bool)
	getVoltage     = Signal()
	setVoltage     = Signal(float)
	getNplc        = Signal()
	setNplc        = Signal(float)
	getAverageFlag = Signal()
	setAverageFlag = Signal(bool)
	getAverage     = Signal()
	setAverage     = Signal(int)

	newCurrent     = Signal(float, float)
	newChannel     = Signal(int)
	newOutput      = Signal(bool)
	newVoltage     = Signal(float)
	newNplc        = Signal(float)
	newAverageFlag = Signal(bool)
	newAverage     = Signal(int)

	def __init__(self, parent=None):
		super(K6482Control, self).__init__(parent)
		self.setupUi(self)

		self.activated = False

		self.channel     = 1
		self.output      = False
		self.voltage     = 0.0
		self.nplc        = 1.0
		self.averageFlag = False
		self.average     = 1

		self.k6482 = K6482("GPIB0::25::INSTR")
		self.k6482.open()

		self.eThread = QThread()
		self.eThread.finished.connect(self.eThread.deleteLater)
		self.eThread.finished.connect(self.k6482.close)
		self.eThread.finished.connect(self.k6482.deleteLater)
		self.eThread.start()
		self.k6482.moveToThread(self.eThread)

		re = QRegularExpression(r"[\+\-]?((10(\.0{0,2})?)|(\d(\.\d{,2})?))")
		v = QRegularExpressionValidator(re, self)
		v.setLocale(QLocale(QLocale.C))
		self.edit_voltage.setValidator(v)
		self.edit_voltage.setStyleSheet("background: yellow")

		re = QRegularExpression(r"(10(\.0{0,2})?)|(\d(\.\d{,2})?)")
		v = QRegularExpressionValidator(re, self)
		v.setLocale(QLocale(QLocale.C))
		self.edit_nplc.setValidator(v)
		self.edit_nplc.setStyleSheet("background: yellow")

		re = QRegularExpression(r"(10{2})|([1-9]\d{0,1})")
		v = QRegularExpressionValidator(re, self)
		v.setLocale(QLocale(QLocale.C))
		self.edit_average.setValidator(v)
		self.edit_average.setStyleSheet("background: yellow")

		self.link_signals()

		if len(self.k6482.get_error()) > 0:
			self.setDisabled(True)
			print(self.k6482.get_error())
		else:
			self.getCurrent    .emit()
			self.getChannel    .emit()
			self.getOutput     .emit()
			self.getVoltage    .emit()
			self.getNplc       .emit()
			self.getAverageFlag.emit()
			self.getAverage    .emit()

	def link_signals(self):
		if self.debug: print(f"K6482Control -> link_signals")
		self.radio_channel1.clicked      .connect(self.channel1_clicked)
		self.radio_channel2.clicked      .connect(self.channel2_clicked)
		self.check_output  .clicked      .connect(self.output_clicked)
		self.edit_voltage  .returnPressed.connect(self.voltage_pressed)
		self.edit_voltage  .textEdited   .connect(self.voltage_edited)
		self.edit_voltage  .inputRejected.connect(self.voltage_rejected)
		self.edit_nplc     .returnPressed.connect(self.nplc_pressed)
		self.edit_nplc     .textEdited   .connect(self.nplc_edited)
		self.edit_nplc     .inputRejected.connect(self.nplc_rejected)
		self.check_average .clicked      .connect(self.average_clicked)
		self.edit_average  .returnPressed.connect(self.average_pressed)
		self.edit_average  .textEdited   .connect(self.average_edited)
		self.edit_average  .inputRejected.connect(self.average_rejected)

		self.getCurrent    .connect(self.k6482.getCurrent)
		self.getChannel    .connect(self.k6482.getChannel)
		self.setChannel    .connect(self.k6482.setChannel)
		self.getOutput     .connect(self.k6482.getOutput)
		self.setOutput     .connect(self.k6482.setOutput)
		self.getVoltage    .connect(self.k6482.getVoltage)
		self.setVoltage    .connect(self.k6482.setVoltage)
		self.getNplc       .connect(self.k6482.getNplc)
		self.setNplc       .connect(self.k6482.setNplc)
		self.getAverageFlag.connect(self.k6482.getAverageFlag)
		self.setAverageFlag.connect(self.k6482.setAverageFlag)
		self.getAverage    .connect(self.k6482.getAverage)
		self.setAverage    .connect(self.k6482.setAverage)

		self.k6482.newCurrent    .connect(self.onNewCurrent)
		self.k6482.newChannel    .connect(self.onNewChannel)
		self.k6482.newOutput     .connect(self.onNewOutput)
		self.k6482.newVoltage    .connect(self.onNewVoltage)
		self.k6482.newNplc       .connect(self.onNewNplc)
		self.k6482.newAverageFlag.connect(self.onNewAverageFlag)
		self.k6482.newAverage    .connect(self.onNewAverage)

	def activate(self):
		if self.debug: print(f"K6482Control -> activate")
		if self.activated:
			self.getCurrent.emit()

	def deactivate(self):
		if self.debug: print(f"K6482Control -> deactivate")
		self.activated = False

	@Slot(float, float)
	def onNewCurrent(self, c1: float, c2: float):
		if self.debug: print(f"K6482Control -> onNewCurrent {c1=} {c2=}")
		self.label_current1.setText(f"{c1:+.5e}")
		self.label_current2.setText(f"{c2:+.5e}")
		self.newCurrent.emit(c1, c2)
		if self.activated:
			self.getCurrent.emit()

	def voltage_pressed(self):
		if self.debug: print(f"K6482Control -> voltage_pressed")
		voltage = float(self.edit_voltage.text())
		if voltage < -10.00 or voltage > 10.00:
			self.voltage_rejected()
		else:
			self.edit_voltage.setStyleSheet("")
			self.setDisabled(True)
			self.setVoltage.emit(voltage)
	def voltage_edited(self, text):
		if self.debug: print(f"K6482Control -> voltage_edited")
		if len(text) == 0 or text[0] == "+" or text[0] == "-" or self.voltage != float(text):
			self.edit_voltage.setStyleSheet("background: yellow")
		else:
			self.edit_voltage.setStyleSheet("")
	def voltage_rejected(self):
		if self.debug: print(f"K6482Control -> voltage_rejected")
		self.edit_voltage.setStyleSheet("background: red; color: white")
	@Slot(float)
	def onNewVoltage(self, voltage: float):
		if self.debug: print(f"K6482Control -> onNewVoltage {voltage=}")
		self.voltage = voltage
		self.edit_voltage.setStyleSheet("background: green; color: white")
		self.edit_voltage.setText(f"{self.voltage:.2f}")
		self.setDisabled(False)
		self.newVoltage.emit(self.voltage)

	def nplc_pressed(self):
		if self.debug: print(f"K6482Control -> nplc_pressed")
		nplc = float(self.edit_nplc.text())
		if nplc < -0.01 or nplc > 10.00:
			self.nplc_rejected()
		else:
			self.edit_nplc.setStyleSheet("")
			self.setDisabled(True)
			self.setNplc.emit(nplc)
	def nplc_edited(self, text):
		if self.debug: print(f"K6482Control -> nplc_edited")
		if len(text) == 0 or self.nplc != float(text):
			self.edit_nplc.setStyleSheet("background: yellow")
		else:
			self.edit_nplc.setStyleSheet("")
	def nplc_rejected(self):
		if self.debug: print(f"K6482Control -> nplc_rejected")
		self.edit_nplc.setStyleSheet("background: red; color: white")
	@Slot(float)
	def onNewNplc(self, nplc: float):
		if self.debug: print(f"K6482Control -> onNewNplc {nplc=}")
		self.nplc = nplc
		self.edit_nplc.setStyleSheet("background: green; color: white")
		self.edit_nplc.setText(f"{self.nplc:.2f}")
		self.setDisabled(False)
		self.newNplc.emit(self.nplc)

	def average_pressed(self):
		if self.debug: print(f"K6482Control -> average_pressed")
		average = int(self.edit_average.text())
		if average < 1 or average > 100:
			self.average_rejected()
		else:
			self.edit_average.setStyleSheet("")
			self.setDisabled(True)
			self.setAverage.emit(average)
	def average_edited(self, text):
		if self.debug: print(f"K6482Control -> average_edited")
		if len(text) == 0 or self.average != int(text):
			self.edit_average.setStyleSheet("background: yellow")
		else:
			self.edit_average.setStyleSheet("")
	def average_rejected(self):
		if self.debug: print(f"K6482Control -> average_rejected")
		self.edit_average.setStyleSheet("background: red; color: white")
	@Slot(int)
	def onNewAverage(self, average: int):
		if self.debug: print(f"K6482Control -> onNewAverage {average=}")
		self.average = average
		self.edit_average.setStyleSheet("background: green; color: white")
		self.edit_average.setText(f"{self.average}")
		self.setDisabled(False)
		self.newAverage.emit(self.average)

	def channel1_clicked(self):
		if self.debug: print(f"K6482Control -> channel1_clicked")
		channel = 1 if self.radio_channel1.isChecked() else 2
		self.setDisabled(True)
		self.setChannel.emit(channel)
		self.getOutput     .emit()
		self.getVoltage    .emit()
		self.getNplc       .emit()
		self.getAverageFlag.emit()
		self.getAverage    .emit()
	def channel2_clicked(self):
		if self.debug: print(f"K6482Control -> channel2_clicked")
		channel = 2 if self.radio_channel2.isChecked() else 1
		self.setDisabled(True)
		self.setChannel.emit(channel)
		self.getOutput     .emit()
		self.getVoltage    .emit()
		self.getNplc       .emit()
		self.getAverageFlag.emit()
		self.getAverage    .emit()
	@Slot(int)
	def onNewChannel(self, channel: int):
		if self.debug: print(f"K6482Control -> onNewChannel {channel=}")
		self.channel = channel
		self.radio_channel1.setChecked(True if channel == 1 else False)
		self.setDisabled(False)
		self.newChannel.emit(self.channel)

	def output_clicked(self):
		if self.debug: print(f"K6482Control -> output_clicked")
		output = self.check_output.isChecked()
		self.setDisabled(True)
		self.setOutput.emit(output)
	@Slot(bool)
	def onNewOutput(self, output: bool):
		if self.debug: print(f"K6482Control -> onNewOutput {output=}")
		self.output = output
		self.check_output.setChecked(self.output)
		self.setDisabled(False)
		self.newOutput.emit(self.output)

	def average_clicked(self):
		if self.debug: print(f"K6482Control -> average_clicked")
		averageFlag = self.check_average.isChecked()
		self.setDisabled(True)
		self.setAverageFlag.emit(averageFlag)
	@Slot(bool)
	def onNewAverageFlag(self, averageFlag: bool):
		if self.debug: print(f"K6482Control -> onNewAverageFlag {averageFlag=}")
		self.averageFlag = averageFlag
		self.check_average.setChecked(self.averageFlag)
		self.setDisabled(False)
		self.newAverageFlag.emit(self.averageFlag)

	def closeEvent(self, event):
		if self.debug: print(f"K6482Control -> closeEvent")
		self.eThread.quit()
		self.eThread.wait()
		event.accept()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = K6482Control()
	w.show()
	app.exec()
