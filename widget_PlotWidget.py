from PySide6.QtCore import Slot
from PySide6.QtGui import QColor

from typing import Self, List

import sys
import pyqtgraph as pg
import numpy as np
from scipy.interpolate import interp1d

class PlotWidget(pg.PlotWidget):
	debug = False

	color_list = [QColor("black"), QColor("red"), QColor("green"), QColor("blue"),
		QColor(204, 204, 0), QColor(255, 0, 127), QColor(0, 204, 204), QColor(255, 128, 0)]

	styles = {"color": "black", "font-size": "16px", "font": "Calibri"}

	def __init__(self):
		super(PlotWidget, self).__init__()
		self.setBackground("w")
		self.setMinimumSize(700, 500)
		#self.setTitle("vac", color="b", size="20pt")
		self.setLabel("left", "Current, A", **self.styles)
		self.setLabel("bottom", "Wavelength, nm", **self.styles)
		self.addLegend()
		self.showGrid(x=True, y=True)
		# self.setXRange(300, 2000)
		# self.setYRange(0, 1)
		self.getPlotItem().enableAutoRange(axis=pg.ViewBox.XAxis)
		self.getPlotItem().enableAutoRange(axis=pg.ViewBox.YAxis)
		self.zero_axis_pen = pg.mkPen(color="black", width=1)
		self.v_line = pg.InfiniteLine(pos=0, angle=0, pen=self.zero_axis_pen)
		self.h_line = pg.InfiniteLine(pos=0, angle=90, pen=self.zero_axis_pen)
		self.addItem(self.v_line)
		self.addItem(self.h_line)

		self.items = []
		self.showItems = []
		self.color_index = 0

	@Slot()
	def newCurve(self):
		if self.debug: print(f"PlotWidget -> newCurve")
		color=self.color_list[self.color_index]
		self.color_index = self.color_index + 1
		if self.color_index >= len(self.color_list):
			self.color_list = 0
		pen = pg.mkPen(color=color, width=1)
		item = pg.PlotCurveItem(pen=pen)
		item.setPen(pen)
		self.items.append(item)
		self.showItems.append(item)
		self.addItem(item)

	@Slot(int, list, list)
	def updateDataIndex(self, index, x, y):
		if self.debug: print(f"PlotWidget -> updateDataIndex {index} {x} {y}")
		self.items[index].setData(x, y)
		self.getPlotItem().autoRange(items = self.showItems)

	@Slot(list, list)
	def updateData(self, x, y):
		if self.debug: print(f"PlotWidget -> updateData {x} {y}")
		self.updateDataIndex(-1, x, y)

	@Slot(int)
	def show(self, i):
		if self.debug: print(f"PlotWidget -> show {i}")
		item = self.items[i]
		item.show()
		if item not in self.showItems:
			self.showItems.append(item)
		self.getPlotItem().autoRange(items = self.showItems)

	@Slot()
	def showAll(self):
		if self.debug: print(f"PlotWidget -> showAll")
		for item in self.items:
			item.show()
			if item not in self.showItems:
				self.showItems.append(item)
		self.getPlotItem().autoRange(items = self.showItems)

	@Slot(int)
	def hide(self, i):
		if self.debug: print(f"PlotWidget -> hide {i}")
		item = self.items[i]
		item.hide()
		if item in self.showItems:
			self.showItems.remove(item)
		self.getPlotItem().autoRange(items = self.showItems)

	@Slot()
	def hideAll(self):
		if self.debug: print(f"PlotWidget -> hideAll")
		for item in self.items:
			item.hide()
			if item in self.showItems:
				self.showItems.remove(item)
		self.getPlotItem().autoRange(items = self.showItems)

	def setYLabel(self, label: str):
		self.setLabel("left", label, **self.styles)
