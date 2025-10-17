# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TimeControl.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_TimeControl(object):
    def setupUi(self, TimeControl):
        if not TimeControl.objectName():
            TimeControl.setObjectName(u"TimeControl")
        TimeControl.resize(306, 660)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TimeControl.sizePolicy().hasHeightForWidth())
        TimeControl.setSizePolicy(sizePolicy)
        TimeControl.setMaximumSize(QSize(1000, 16777215))
        self.formLayout = QFormLayout(TimeControl)
        self.formLayout.setObjectName(u"formLayout")
        self.label_sample = QLabel(TimeControl)
        self.label_sample.setObjectName(u"label_sample")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_sample)

        self.edit_sample = QLineEdit(TimeControl)
        self.edit_sample.setObjectName(u"edit_sample")
        self.edit_sample.setMaxLength(20)
        self.edit_sample.setFrame(True)
        self.edit_sample.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.edit_sample)

        self.label_exp = QLabel(TimeControl)
        self.label_exp.setObjectName(u"label_exp")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.label_exp)

        self.edit_exp = QPlainTextEdit(TimeControl)
        self.edit_exp.setObjectName(u"edit_exp")
        self.edit_exp.setMinimumSize(QSize(0, 100))
        self.edit_exp.setMaximumSize(QSize(16777215, 200))

        self.formLayout.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.edit_exp)

        self.button_exp = QPushButton(TimeControl)
        self.button_exp.setObjectName(u"button_exp")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.button_exp)

        self.frame_control = QFrame(TimeControl)
        self.frame_control.setObjectName(u"frame_control")
        self.frame_control.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_control.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_control)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.button_start = QPushButton(self.frame_control)
        self.button_start.setObjectName(u"button_start")

        self.gridLayout_17.addWidget(self.button_start, 0, 0, 1, 1)

        self.button_stop = QPushButton(self.frame_control)
        self.button_stop.setObjectName(u"button_stop")

        self.gridLayout_17.addWidget(self.button_stop, 0, 1, 1, 1)

        self.progress_bar = QProgressBar(self.frame_control)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.gridLayout_17.addWidget(self.progress_bar, 1, 0, 1, 2)


        self.formLayout.setWidget(4, QFormLayout.ItemRole.SpanningRole, self.frame_control)

        self.tableview_time = QTableWidget(TimeControl)
        self.tableview_time.setObjectName(u"tableview_time")
        self.tableview_time.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(5, QFormLayout.ItemRole.SpanningRole, self.tableview_time)

        self.button_load = QPushButton(TimeControl)
        self.button_load.setObjectName(u"button_load")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.SpanningRole, self.button_load)

        QWidget.setTabOrder(self.button_start, self.button_stop)
        QWidget.setTabOrder(self.button_stop, self.button_load)

        self.retranslateUi(TimeControl)

        QMetaObject.connectSlotsByName(TimeControl)
    # setupUi

    def retranslateUi(self, TimeControl):
        TimeControl.setWindowTitle(QCoreApplication.translate("TimeControl", u"TimeControl", None))
        self.label_sample.setText(QCoreApplication.translate("TimeControl", u"Sample", None))
        self.edit_sample.setText("")
        self.edit_sample.setPlaceholderText(QCoreApplication.translate("TimeControl", u"sample_name", None))
        self.label_exp.setText(QCoreApplication.translate("TimeControl", u"Time Voltage Shutter", None))
        self.button_exp.setText(QCoreApplication.translate("TimeControl", u"Set", None))
        self.button_start.setText(QCoreApplication.translate("TimeControl", u"Start", None))
        self.button_stop.setText(QCoreApplication.translate("TimeControl", u"Stop", None))
        self.button_load.setText(QCoreApplication.translate("TimeControl", u"Load", None))
    # retranslateUi

