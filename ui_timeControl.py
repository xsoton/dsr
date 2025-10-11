# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'timeControl.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListView,
    QPlainTextEdit, QProgressBar, QPushButton, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_timeControl(object):
    def setupUi(self, timeControl):
        if not timeControl.objectName():
            timeControl.setObjectName(u"timeControl")
        timeControl.resize(300, 660)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(timeControl.sizePolicy().hasHeightForWidth())
        timeControl.setSizePolicy(sizePolicy)
        timeControl.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout = QVBoxLayout(timeControl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_meas = QFrame(timeControl)
        self.frame_meas.setObjectName(u"frame_meas")
        self.frame_meas.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_meas.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_meas)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.exp_edit = QPlainTextEdit(self.frame_meas)
        self.exp_edit.setObjectName(u"exp_edit")
        self.exp_edit.setMinimumSize(QSize(0, 100))

        self.gridLayout_11.addWidget(self.exp_edit, 2, 0, 1, 2)

        self.sample_edit = QLineEdit(self.frame_meas)
        self.sample_edit.setObjectName(u"sample_edit")
        self.sample_edit.setMaxLength(20)
        self.sample_edit.setFrame(True)
        self.sample_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.sample_edit, 0, 1, 1, 1)

        self.label_sample = QLabel(self.frame_meas)
        self.label_sample.setObjectName(u"label_sample")

        self.gridLayout_11.addWidget(self.label_sample, 0, 0, 1, 1)

        self.exp_button = QPushButton(self.frame_meas)
        self.exp_button.setObjectName(u"exp_button")

        self.gridLayout_11.addWidget(self.exp_button, 3, 0, 1, 2)


        self.verticalLayout.addWidget(self.frame_meas)

        self.frame_amp = QFrame(timeControl)
        self.frame_amp.setObjectName(u"frame_amp")
        self.frame_amp.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_amp.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_amp)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.voltage_check = QCheckBox(self.frame_amp)
        self.voltage_check.setObjectName(u"voltage_check")

        self.gridLayout_15.addWidget(self.voltage_check, 2, 0, 1, 1)

        self.label_average = QLabel(self.frame_amp)
        self.label_average.setObjectName(u"label_average")

        self.gridLayout_15.addWidget(self.label_average, 5, 1, 1, 1)

        self.voltage_edit = QLineEdit(self.frame_amp)
        self.voltage_edit.setObjectName(u"voltage_edit")
        self.voltage_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.voltage_edit, 2, 2, 1, 1)

        self.nplc_edit = QLineEdit(self.frame_amp)
        self.nplc_edit.setObjectName(u"nplc_edit")
        self.nplc_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.nplc_edit, 3, 2, 1, 1)

        self.label_channel = QLabel(self.frame_amp)
        self.label_channel.setObjectName(u"label_channel")

        self.gridLayout_15.addWidget(self.label_channel, 0, 1, 1, 1)

        self.label = QLabel(self.frame_amp)
        self.label.setObjectName(u"label")

        self.gridLayout_15.addWidget(self.label, 1, 1, 1, 1)

        self.label_nplc = QLabel(self.frame_amp)
        self.label_nplc.setObjectName(u"label_nplc")

        self.gridLayout_15.addWidget(self.label_nplc, 3, 1, 1, 1)

        self.label_voltage = QLabel(self.frame_amp)
        self.label_voltage.setObjectName(u"label_voltage")

        self.gridLayout_15.addWidget(self.label_voltage, 2, 1, 1, 1)

        self.average_edit = QLineEdit(self.frame_amp)
        self.average_edit.setObjectName(u"average_edit")
        self.average_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.average_edit, 5, 2, 1, 1)

        self.frame_channel = QFrame(self.frame_amp)
        self.frame_channel.setObjectName(u"frame_channel")
        self.frame_channel.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_channel.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_channel.setLineWidth(0)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_channel)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.channel1_radio = QRadioButton(self.frame_channel)
        self.channel1_radio.setObjectName(u"channel1_radio")
        self.channel1_radio.setChecked(True)

        self.horizontalLayout_5.addWidget(self.channel1_radio)

        self.channel2_radio = QRadioButton(self.frame_channel)
        self.channel2_radio.setObjectName(u"channel2_radio")
        self.channel2_radio.setChecked(False)

        self.horizontalLayout_5.addWidget(self.channel2_radio)


        self.gridLayout_15.addWidget(self.frame_channel, 0, 2, 1, 1)

        self.average_check = QCheckBox(self.frame_amp)
        self.average_check.setObjectName(u"average_check")

        self.gridLayout_15.addWidget(self.average_check, 5, 0, 1, 1)

        self.frame_current = QFrame(self.frame_amp)
        self.frame_current.setObjectName(u"frame_current")
        self.frame_current.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_current.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_current)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.current1_label = QLabel(self.frame_current)
        self.current1_label.setObjectName(u"current1_label")
        self.current1_label.setStyleSheet(u"color: white; background-color: green")
        self.current1_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.current1_label.setMargin(2)

        self.horizontalLayout.addWidget(self.current1_label)

        self.current2_label = QLabel(self.frame_current)
        self.current2_label.setObjectName(u"current2_label")
        self.current2_label.setStyleSheet(u"color: white; background-color: green")
        self.current2_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.current2_label.setMargin(2)

        self.horizontalLayout.addWidget(self.current2_label)


        self.gridLayout_15.addWidget(self.frame_current, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.frame_amp)

        self.frame_mono = QFrame(timeControl)
        self.frame_mono.setObjectName(u"frame_mono")
        self.frame_mono.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_mono.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_mono)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.label_shutter = QLabel(self.frame_mono)
        self.label_shutter.setObjectName(u"label_shutter")

        self.gridLayout_16.addWidget(self.label_shutter, 1, 0, 1, 1)

        self.wl_edit = QLineEdit(self.frame_mono)
        self.wl_edit.setObjectName(u"wl_edit")
        self.wl_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.wl_edit, 0, 1, 1, 1)

        self.shutter_check = QCheckBox(self.frame_mono)
        self.shutter_check.setObjectName(u"shutter_check")

        self.gridLayout_16.addWidget(self.shutter_check, 1, 1, 1, 1)

        self.label_setwl = QLabel(self.frame_mono)
        self.label_setwl.setObjectName(u"label_setwl")

        self.gridLayout_16.addWidget(self.label_setwl, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_mono)

        self.frame_control = QFrame(timeControl)
        self.frame_control.setObjectName(u"frame_control")
        self.frame_control.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_control.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_control)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.start_button = QPushButton(self.frame_control)
        self.start_button.setObjectName(u"start_button")

        self.gridLayout_17.addWidget(self.start_button, 0, 0, 1, 1)

        self.stop_button = QPushButton(self.frame_control)
        self.stop_button.setObjectName(u"stop_button")

        self.gridLayout_17.addWidget(self.stop_button, 0, 1, 1, 1)

        self.progress_bar = QProgressBar(self.frame_control)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.gridLayout_17.addWidget(self.progress_bar, 1, 0, 1, 2)


        self.verticalLayout.addWidget(self.frame_control)

        self.exp_list_view = QListView(timeControl)
        self.exp_list_view.setObjectName(u"exp_list_view")

        self.verticalLayout.addWidget(self.exp_list_view)

        self.load_button = QPushButton(timeControl)
        self.load_button.setObjectName(u"load_button")

        self.verticalLayout.addWidget(self.load_button)

        QWidget.setTabOrder(self.sample_edit, self.exp_edit)
        QWidget.setTabOrder(self.exp_edit, self.channel1_radio)
        QWidget.setTabOrder(self.channel1_radio, self.channel2_radio)
        QWidget.setTabOrder(self.channel2_radio, self.voltage_check)
        QWidget.setTabOrder(self.voltage_check, self.voltage_edit)
        QWidget.setTabOrder(self.voltage_edit, self.nplc_edit)
        QWidget.setTabOrder(self.nplc_edit, self.average_check)
        QWidget.setTabOrder(self.average_check, self.average_edit)
        QWidget.setTabOrder(self.average_edit, self.wl_edit)
        QWidget.setTabOrder(self.wl_edit, self.shutter_check)
        QWidget.setTabOrder(self.shutter_check, self.start_button)
        QWidget.setTabOrder(self.start_button, self.stop_button)
        QWidget.setTabOrder(self.stop_button, self.exp_list_view)
        QWidget.setTabOrder(self.exp_list_view, self.load_button)

        self.retranslateUi(timeControl)

        QMetaObject.connectSlotsByName(timeControl)
    # setupUi

    def retranslateUi(self, timeControl):
        timeControl.setWindowTitle(QCoreApplication.translate("timeControl", u"expControl", None))
        self.sample_edit.setText("")
        self.sample_edit.setPlaceholderText(QCoreApplication.translate("timeControl", u"sample_name", None))
        self.label_sample.setText(QCoreApplication.translate("timeControl", u"Sample", None))
        self.exp_button.setText(QCoreApplication.translate("timeControl", u"Set", None))
        self.voltage_check.setText("")
        self.label_average.setText(QCoreApplication.translate("timeControl", u"Average", None))
        self.voltage_edit.setText(QCoreApplication.translate("timeControl", u"0", None))
        self.voltage_edit.setPlaceholderText(QCoreApplication.translate("timeControl", u"voltage: \u00b110 V", None))
        self.nplc_edit.setText(QCoreApplication.translate("timeControl", u"1", None))
        self.nplc_edit.setPlaceholderText(QCoreApplication.translate("timeControl", u"0.01 - 10.00", None))
        self.label_channel.setText(QCoreApplication.translate("timeControl", u"Channel", None))
        self.label.setText(QCoreApplication.translate("timeControl", u"Current", None))
        self.label_nplc.setText(QCoreApplication.translate("timeControl", u"NPLC", None))
        self.label_voltage.setText(QCoreApplication.translate("timeControl", u"Voltage", None))
        self.average_edit.setText(QCoreApplication.translate("timeControl", u"1", None))
        self.average_edit.setPlaceholderText(QCoreApplication.translate("timeControl", u"1 - 100", None))
        self.channel1_radio.setText(QCoreApplication.translate("timeControl", u"1", None))
        self.channel2_radio.setText(QCoreApplication.translate("timeControl", u"2", None))
        self.average_check.setText("")
        self.current1_label.setText(QCoreApplication.translate("timeControl", u"0 pA", None))
        self.current2_label.setText(QCoreApplication.translate("timeControl", u"0 pA", None))
        self.label_shutter.setText(QCoreApplication.translate("timeControl", u"Shutter", None))
        self.wl_edit.setText("")
        self.wl_edit.setPlaceholderText(QCoreApplication.translate("timeControl", u"300 - 2000 nm", None))
        self.shutter_check.setText("")
        self.label_setwl.setText(QCoreApplication.translate("timeControl", u"Set  \u03bb", None))
        self.start_button.setText(QCoreApplication.translate("timeControl", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("timeControl", u"Stop", None))
        self.load_button.setText(QCoreApplication.translate("timeControl", u"Load", None))
    # retranslateUi

