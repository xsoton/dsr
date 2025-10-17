# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'K6482Control.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QRadioButton,
    QSizePolicy, QWidget)

class Ui_K6482Control(object):
    def setupUi(self, K6482Control):
        if not K6482Control.objectName():
            K6482Control.setObjectName(u"K6482Control")
        K6482Control.setEnabled(True)
        K6482Control.resize(335, 168)
        self.formLayout = QFormLayout(K6482Control)
        self.formLayout.setObjectName(u"formLayout")
        self.label_channel = QLabel(K6482Control)
        self.label_channel.setObjectName(u"label_channel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_channel)

        self.frame_channel = QFrame(K6482Control)
        self.frame_channel.setObjectName(u"frame_channel")
        self.frame_channel.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_channel.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_channel.setLineWidth(0)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_channel)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.radio_channel1 = QRadioButton(self.frame_channel)
        self.radio_channel1.setObjectName(u"radio_channel1")
        self.radio_channel1.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radio_channel1)

        self.radio_channel2 = QRadioButton(self.frame_channel)
        self.radio_channel2.setObjectName(u"radio_channel2")
        self.radio_channel2.setChecked(False)

        self.horizontalLayout_5.addWidget(self.radio_channel2)


        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.frame_channel)

        self.label_current = QLabel(K6482Control)
        self.label_current.setObjectName(u"label_current")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_current)

        self.frame_current = QFrame(K6482Control)
        self.frame_current.setObjectName(u"frame_current")
        self.frame_current.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_current.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_current)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_current1 = QLabel(self.frame_current)
        self.label_current1.setObjectName(u"label_current1")
        self.label_current1.setStyleSheet(u"color: white; background-color: green")
        self.label_current1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_current1.setMargin(2)

        self.horizontalLayout.addWidget(self.label_current1)

        self.label_current2 = QLabel(self.frame_current)
        self.label_current2.setObjectName(u"label_current2")
        self.label_current2.setStyleSheet(u"color: white; background-color: green")
        self.label_current2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_current2.setMargin(2)

        self.horizontalLayout.addWidget(self.label_current2)


        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.frame_current)

        self.label_voltage = QLabel(K6482Control)
        self.label_voltage.setObjectName(u"label_voltage")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_voltage)

        self.label_nplc = QLabel(K6482Control)
        self.label_nplc.setObjectName(u"label_nplc")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_nplc)

        self.edit_nplc = QLineEdit(K6482Control)
        self.edit_nplc.setObjectName(u"edit_nplc")
        self.edit_nplc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.edit_nplc)

        self.label_average = QLabel(K6482Control)
        self.label_average.setObjectName(u"label_average")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_average)

        self.edit_average = QLineEdit(K6482Control)
        self.edit_average.setObjectName(u"edit_average")
        self.edit_average.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.edit_average)

        self.check_output = QCheckBox(K6482Control)
        self.check_output.setObjectName(u"check_output")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.check_output)

        self.edit_voltage = QLineEdit(K6482Control)
        self.edit_voltage.setObjectName(u"edit_voltage")
        self.edit_voltage.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.edit_voltage)

        self.check_average = QCheckBox(K6482Control)
        self.check_average.setObjectName(u"check_average")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.check_average)


        self.retranslateUi(K6482Control)

        QMetaObject.connectSlotsByName(K6482Control)
    # setupUi

    def retranslateUi(self, K6482Control):
        K6482Control.setWindowTitle(QCoreApplication.translate("K6482Control", u"K6482Control", None))
        self.label_channel.setText(QCoreApplication.translate("K6482Control", u"Channel", None))
        self.radio_channel1.setText(QCoreApplication.translate("K6482Control", u"1", None))
        self.radio_channel2.setText(QCoreApplication.translate("K6482Control", u"2", None))
        self.label_current.setText(QCoreApplication.translate("K6482Control", u"Current", None))
        self.label_current1.setText(QCoreApplication.translate("K6482Control", u"0 pA", None))
        self.label_current2.setText(QCoreApplication.translate("K6482Control", u"0 pA", None))
        self.label_voltage.setText(QCoreApplication.translate("K6482Control", u"Voltage", None))
        self.label_nplc.setText(QCoreApplication.translate("K6482Control", u"NPLC", None))
        self.edit_nplc.setText("")
        self.edit_nplc.setPlaceholderText(QCoreApplication.translate("K6482Control", u"0.01 - 10.00", None))
        self.label_average.setText(QCoreApplication.translate("K6482Control", u"Average", None))
        self.edit_average.setText("")
        self.edit_average.setPlaceholderText(QCoreApplication.translate("K6482Control", u"1 - 100", None))
        self.check_output.setText(QCoreApplication.translate("K6482Control", u"Enable Output", None))
        self.edit_voltage.setText("")
        self.edit_voltage.setPlaceholderText(QCoreApplication.translate("K6482Control", u"voltage: \u00b110 V", None))
        self.check_average.setText(QCoreApplication.translate("K6482Control", u"Enable Average", None))
    # retranslateUi

