# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RespControl.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_RespControl(object):
    def setupUi(self, RespControl):
        if not RespControl.objectName():
            RespControl.setObjectName(u"RespControl")
        RespControl.resize(303, 673)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RespControl.sizePolicy().hasHeightForWidth())
        RespControl.setSizePolicy(sizePolicy)
        RespControl.setMaximumSize(QSize(1000, 16777215))
        self.gridLayout = QGridLayout(RespControl)
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_load = QPushButton(RespControl)
        self.button_load.setObjectName(u"button_load")

        self.gridLayout.addWidget(self.button_load, 7, 0, 1, 2)

        self.label_sample = QLabel(RespControl)
        self.label_sample.setObjectName(u"label_sample")

        self.gridLayout.addWidget(self.label_sample, 0, 0, 1, 1)

        self.label_step = QLabel(RespControl)
        self.label_step.setObjectName(u"label_step")
        self.label_step.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_step, 3, 0, 1, 1)

        self.label_start = QLabel(RespControl)
        self.label_start.setObjectName(u"label_start")

        self.gridLayout.addWidget(self.label_start, 1, 0, 1, 1)

        self.edit_sample = QLineEdit(RespControl)
        self.edit_sample.setObjectName(u"edit_sample")
        self.edit_sample.setMaxLength(20)
        self.edit_sample.setFrame(True)
        self.edit_sample.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_sample, 0, 1, 1, 1)

        self.edit_stop = QLineEdit(RespControl)
        self.edit_stop.setObjectName(u"edit_stop")
        self.edit_stop.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_stop, 2, 1, 1, 1)

        self.edit_start = QLineEdit(RespControl)
        self.edit_start.setObjectName(u"edit_start")
        self.edit_start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_start.setDragEnabled(False)
        self.edit_start.setReadOnly(False)

        self.gridLayout.addWidget(self.edit_start, 1, 1, 1, 1)

        self.edit_step = QLineEdit(RespControl)
        self.edit_step.setObjectName(u"edit_step")
        self.edit_step.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_step, 3, 1, 1, 1)

        self.frame_control = QFrame(RespControl)
        self.frame_control.setObjectName(u"frame_control")
        self.frame_control.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_control.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_control)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.button_start = QPushButton(self.frame_control)
        self.button_start.setObjectName(u"button_start")

        self.gridLayout_17.addWidget(self.button_start, 0, 0, 1, 1)

        self.progress_bar = QProgressBar(self.frame_control)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.gridLayout_17.addWidget(self.progress_bar, 1, 0, 1, 2)

        self.button_stop = QPushButton(self.frame_control)
        self.button_stop.setObjectName(u"button_stop")

        self.gridLayout_17.addWidget(self.button_stop, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_control, 5, 0, 1, 2)

        self.label_delay = QLabel(RespControl)
        self.label_delay.setObjectName(u"label_delay")
        self.label_delay.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_delay, 4, 0, 1, 1)

        self.label_stop = QLabel(RespControl)
        self.label_stop.setObjectName(u"label_stop")

        self.gridLayout.addWidget(self.label_stop, 2, 0, 1, 1)

        self.edit_delay = QLineEdit(RespControl)
        self.edit_delay.setObjectName(u"edit_delay")
        self.edit_delay.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.edit_delay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.edit_delay, 4, 1, 1, 1)

        self.tableview_resp = QTableWidget(RespControl)
        self.tableview_resp.setObjectName(u"tableview_resp")
        self.tableview_resp.setMaximumSize(QSize(1000, 16777215))

        self.gridLayout.addWidget(self.tableview_resp, 6, 0, 1, 2)

        QWidget.setTabOrder(self.button_start, self.button_stop)

        self.retranslateUi(RespControl)

        QMetaObject.connectSlotsByName(RespControl)
    # setupUi

    def retranslateUi(self, RespControl):
        RespControl.setWindowTitle(QCoreApplication.translate("RespControl", u"RespControl", None))
        self.button_load.setText(QCoreApplication.translate("RespControl", u"Load", None))
        self.label_sample.setText(QCoreApplication.translate("RespControl", u"Sample", None))
        self.label_step.setText(QCoreApplication.translate("RespControl", u"\u0394\u03bb", None))
        self.label_start.setText(QCoreApplication.translate("RespControl", u"Start \u03bb", None))
        self.edit_sample.setText("")
        self.edit_sample.setPlaceholderText(QCoreApplication.translate("RespControl", u"sample_name", None))
        self.edit_stop.setText("")
        self.edit_stop.setPlaceholderText(QCoreApplication.translate("RespControl", u"to, nm", None))
        self.edit_start.setText("")
        self.edit_start.setPlaceholderText(QCoreApplication.translate("RespControl", u"from, nm", None))
        self.edit_step.setText("")
        self.edit_step.setPlaceholderText(QCoreApplication.translate("RespControl", u"step, nm", None))
        self.button_start.setText(QCoreApplication.translate("RespControl", u"Start", None))
        self.button_stop.setText(QCoreApplication.translate("RespControl", u"Stop", None))
        self.label_delay.setText(QCoreApplication.translate("RespControl", u"Delay", None))
        self.label_stop.setText(QCoreApplication.translate("RespControl", u"Stop \u03bb", None))
        self.edit_delay.setText("")
        self.edit_delay.setPlaceholderText(QCoreApplication.translate("RespControl", u"delay, s", None))
    # retranslateUi

