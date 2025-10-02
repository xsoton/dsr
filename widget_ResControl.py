from PySide6.QtCore import Qt, Signal, Slot, QItemSelection, QItemSelectionModel
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
	expCheckedList = []
	expCalculatedList = []

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
		self.expCheckedList = []
		self.expCalculatedList = []

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
			if i in cl and i not in cd: cl.remove(i)

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

		# dateTime = QDateTime.currentDateTime().toString("yyyy-MM-dd_HH-mm-ss")
		# fileName = f"{dateTime}_responsivity.dat"
		# file = QFile(fileName)
		# file.open(QIODevice.ReadWrite)
		# file.write(f"# DSR600: Spectrum Responsivity Experiment\n".encode())
		# file.write(f"# dateTime: {dateTime}\n".encode())
		# file.write(f"# Columns:\n".encode())
		# file.write(f"#   1 - wavelength, nm\n".encode())
		# file.write(f"#   2 - current, A\n".encode())
		# file.flush()

		self.save_button.setDisabled(False)

	@Slot(QStandardItem)
	def onItemChanged(self, item: QStandardItem):
		i = item.row()
		c = (item.checkState() == Qt.Checked)
		print(f"onItemChanged i = {i}, checked = {c}")
		s = self.expSelected
		l = self.expCheckedList
		lc = self.expCalculatedList

		if i not in l:
			if c:
				l.append(i)
				d = self.calc(i)
				self.sig_updateDataIndex.emit(i, d[0], d[1])

				if i != s:
					self.sig_show.emit(i)
		else:
			if not c:
				l.remove(i)
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
		irRes  = detIR
		visSp  = self.data[0].expList[self.idVIS].data
		irSp   = self.data[1].expList[self.idIR].data

		# VIS

		vrx = np.array(visRes[0])
		vry = np.array(visRes[1])
		vsx = np.array(visSp[0])
		vsy = np.array(visSp[1])

		s1 = np.min(vsx)
		s2 = np.max(vsx)
		x = []
		y = []
		for i in range(vrx.size):
			if s1 <= vrx[i] and vrx[i] <= s2 and vrx[i] < 1100.0:
				x.append(vrx[i])
				y.append(vry[i])

		vx = np.array(x)
		vr = np.array(y)
		vi = interp1d(vsx, vsy, kind='linear')
		# vs = fi(vx)

		# IR

		irx = np.array(irRes[0])
		iry = np.array(irRes[1])
		isx = np.array(irSp[0])
		isy = np.array(irSp[1])

		s1 = np.min(isx)
		s2 = np.max(isx)
		x = []
		y = []
		for i in range(irx.size):
			if s1 <= irx[i] and irx[i] <= s2 and irx[i] >= 1100.0:
				x.append(irx[i])
				y.append(iry[i])

		ix = np.array(x)
		ir = np.array(y)
		ii = interp1d(isx, isy, kind='linear')
		# is = fi(ix)

		# SP

		d = self.data[2].expList[index].data
		sx = np.array(d[0])
		sy = np.array(d[1])
		si = interp1d(sx, sy, kind='linear')

		s1 = np.min(sx)
		s2 = np.max(sx)
		x = []
		y = []
		for i in range(vx.size):
			if s1 <= vx[i] and vx[i] <= s2 and vx[i] < 1100.0:
				x.append(vx[i])
				y.append(vr[i])

		svx = np.array(x)
		svr = np.array(y)

		x = []
		y = []
		for i in range(ix.size):
			if s1 <= ix[i] and ix[i] <= s2 and ix[i] >= 1100.0:
				x.append(ix[i])
				y.append(ir[i])

		six = np.array(x)
		sir = np.array(y)

		x = np.append(svx, six)
		y = np.append(svr * si(svx) / vi(svx), sir * si(six) / ii(six))

		return [x, y]
