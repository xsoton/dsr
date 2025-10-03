from PySide6.QtCore import Qt, QDateTime, Signal, Slot, QItemSelection, QItemSelectionModel, QFile, QIODevice
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget

from typing import Self, List
import numpy as np
from scipy.interpolate import interp1d

from ui_resControl import Ui_resControl
from data import Data
from detectors import detectorSi as detVIS, detectorInGaAs as detIR

class ResControl(QWidget, Ui_resControl):
	expSelected: int
	expCheckedList = {}

	idVIS = -1
	idIR = -1

	sig_newCurve        = Signal()
	sig_updateData      = Signal(list, list)
	sig_updateDataIndex = Signal(int, list, list)
	sig_show            = Signal(int)
	sig_hide            = Signal(int)
	sig_showAll         = Signal()
	sig_hideAll         = Signal()

	def __init__(self, data: List[Data], parent=None):
		super(ResControl, self).__init__(parent)
		self.setupUi(self)

		self.data = data

		m = QStandardItemModel()
		m.itemChanged.connect(self.onItemChanged)
		self.exp_list_view.setModel(m)
		self.exp_list_view.selectionModel().selectionChanged.connect(self.onSelectionChanged)
		self.expSelected = -1
		self.expCheckedList = {}

		self.save_button.released.connect(self.save_button_slot)

	def addExpToListView(self):
		print("addExpToListView")
		e = self.data[2].expList[-1]
		i = len(self.data[2].expList)-1
		p = self.exp_list_view.model().invisibleRootItem()

		it = QStandardItem(f"{i} : {e.sampleName}")
		it.setCheckable(True)
		it.setSelectable(True)
		it.setEditable(False)
		it.setEnabled(False)
		self.exp_list_view.selectionModel().selectionChanged.disconnect(self.onSelectionChanged)
		p.appendRow(it)
		self.exp_list_view.selectionModel().select(it.index(), QItemSelectionModel.SelectionFlag.ClearAndSelect)
		self.exp_list_view.selectionModel().selectionChanged.connect(self.onSelectionChanged)

	@Slot()
	def onChecked(self):
		print(f"onChecked")

		l0 = self.data[0].expCheckedList
		if len(l0) > 0: self.idVIS = l0[-1]
		else:           self.idVIS = -1

		l1 = self.data[1].expCheckedList
		if len(l1) > 0: self.idIR  = l1[-1]
		else:           self.idIR  = -1

		cl = self.expCheckedList
		cd = self.data[2].expCheckedList

		a = self.idVIS >=0 and self.idIR >= 0
		for i in range(len(self.data[2].expList)):
			if i in cl and i not in cd: del cl[i]

			it = self.exp_list_view.model().item(i)

			self.exp_list_view.model().itemChanged.disconnect(self.onItemChanged)
			it.setEnabled(i in cd and a)
			it.setCheckState(Qt.Checked if i in cl and a else Qt.Unchecked)
			self.exp_list_view.model().itemChanged.connect(self.onItemChanged)

	@Slot()
	def onEnded(self):
		print("onEnded")
		self.addExpToListView()

	# !!!!!!!!!!!!!!
	def save_button_slot(self):
		print("save_button_slot")
		self.save_button.setDisabled(True)

		dateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		for i,d in self.expCheckedList.items():
			d1 = self.data[0].expList[self.idVIS]
			d2 = self.data[1].expList[self.idIR]
			d3 = self.data[2].expList[i]

			fileName = f"{dateTime}_responsivity_{i}-{d3.sampleName}.dat"
			file = QFile(fileName)
			file.open(QIODevice.ReadWrite)
			file.write(f"# DSR600: Spectrum Responsivity Experiment\n".encode())
			file.write(f"# dateTime: {dateTime}\n".encode())
			file.write(f"# VIS: {d1.fileName}\n".encode())
			file.write(f"#  IR: {d2.fileName}\n".encode())
			file.write(f"# SAM: {d3.fileName}\n".encode())
			file.write(f"# Columns:\n".encode())
			file.write(f"#   1 - Wavelength, nm\n".encode())
			file.write(f"#   2 - Responsivity, A/W\n".encode())

			for j in range(len(d[0])):
				file.write(f"{d[0][j]:.2f}\t{d[1][j]:+.9e}\n".encode())

			file.flush()
			file.close()

		self.save_button.setDisabled(False)

	@Slot(QStandardItem)
	def onItemChanged(self, item: QStandardItem):
		i = item.row()
		c = (item.checkState() == Qt.Checked)
		print(f"onItemChanged i = {i}, checked = {c}")
		s = self.expSelected
		l = self.expCheckedList

		if i not in l:
			if c:
				l[i] = self.calc(i)
				self.sig_updateDataIndex.emit(i, l[i][0], l[i][1])
				if i != s:
					self.sig_show.emit(i)
		else:
			if not c:
				del l[i]
				if i != s:
					self.sig_hide.emit(i)

	@Slot(QItemSelection, QItemSelection)
	def onSelectionChanged(self, s1: QItemSelection, s2: QItemSelection):
		l = self.expCheckedList

		for idx in s1.indexes():
			i = idx.row()
			self.expSelected = i
			if i not in l:
				d = self.calc(i)
				self.sig_updateDataIndex.emit(i, d[0], d[1])
				self.sig_show.emit(i)

		for idx in s2.indexes():
			i = idx.row()
			if i not in l:
				self.sig_hide.emit(i)

		print(f"onSelectionChanged {self.expSelected}")

	@Slot()
	def onExit(self):
		print(f"onExit")
		return

	def calc(self, index: int):
		print(f"calc {index}")

		visRes = detVIS
		visSp  = self.data[0].expList[self.idVIS].data

		# VIS
		rx = np.array(visRes[0])
		ry = np.array(visRes[1])
		sx = np.array(visSp[0])
		sy = np.array(visSp[1])

		x1 = np.min(sx)
		x2 = np.max(sx)
		x = []
		y = []
		for i in range(rx.size):
			if x1 <= rx[i] and rx[i] <= x2 and rx[i] < 1100.0:
				x.append(rx[i])
				y.append(ry[i])

		vx = np.array(x)
		vr = np.array(y)
		vi = interp1d(sx, sy, kind='linear')

		# IR
		irRes  = detIR
		irSp   = self.data[1].expList[self.idIR].data

		rx = np.array(irRes[0])
		ry = np.array(irRes[1])
		sx = np.array(irSp[0])
		sy = np.array(irSp[1])

		x1 = np.min(sx)
		x2 = np.max(sx)
		x = []
		y = []
		for i in range(rx.size):
			if x1 <= rx[i] and rx[i] <= x2 and rx[i] >= 1100.0:
				x.append(rx[i])
				y.append(ry[i])

		ix = np.array(x)
		ir = np.array(y)
		ii = interp1d(sx, sy, kind='linear')

		# SAM

		d = self.data[2].expList[index].data
		sx = np.array(d[0])
		sy = np.array(d[1])
		si = interp1d(sx, sy, kind='linear')

		x1 = np.min(sx)
		x2 = np.max(sx)
		x = []
		y = []
		for i in range(vx.size):
			if x1 <= vx[i] and vx[i] <= x2 and vx[i] < 1100.0:
				x.append(vx[i])
				y.append(vr[i])

		svx = np.array(x)
		svr = np.array(y)

		x = []
		y = []
		for i in range(ix.size):
			if x1 <= ix[i] and ix[i] <= x2 and ix[i] >= 1100.0:
				x.append(ix[i])
				y.append(ir[i])

		six = np.array(x)
		sir = np.array(y)

		x = np.append(svx, six)
		y = np.append(svr * si(svx) / vi(svx), sir * si(six) / ii(six))

		return [x, y]
