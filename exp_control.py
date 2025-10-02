# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exp_control.ui'
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
    QProgressBar, QPushButton, QRadioButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_exp_control(object):
    def setupUi(self, exp_control):
        if not exp_control.objectName():
            exp_control.setObjectName(u"exp_control")
        exp_control.resize(300, 812)
        exp_control.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout = QVBoxLayout(exp_control)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_meas = QFrame(exp_control)
        self.frame_meas.setObjectName(u"frame_meas")
        self.frame_meas.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_meas.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_meas)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.start_edit = QLineEdit(self.frame_meas)
        self.start_edit.setObjectName(u"start_edit")
        self.start_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_edit.setDragEnabled(False)
        self.start_edit.setReadOnly(False)

        self.gridLayout_5.addWidget(self.start_edit, 1, 1, 1, 1)

        self.step_edit = QLineEdit(self.frame_meas)
        self.step_edit.setObjectName(u"step_edit")
        self.step_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.step_edit, 4, 1, 1, 1)

        self.label_start = QLabel(self.frame_meas)
        self.label_start.setObjectName(u"label_start")

        self.gridLayout_5.addWidget(self.label_start, 1, 0, 1, 1)

        self.delay_edit = QLineEdit(self.frame_meas)
        self.delay_edit.setObjectName(u"delay_edit")
        self.delay_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.delay_edit, 5, 1, 1, 1)

        self.label_stop = QLabel(self.frame_meas)
        self.label_stop.setObjectName(u"label_stop")

        self.gridLayout_5.addWidget(self.label_stop, 3, 0, 1, 1)

        self.label_delay = QLabel(self.frame_meas)
        self.label_delay.setObjectName(u"label_delay")
        self.label_delay.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_delay, 5, 0, 1, 1)

        self.label_step = QLabel(self.frame_meas)
        self.label_step.setObjectName(u"label_step")
        self.label_step.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_step, 4, 0, 1, 1)

        self.stop_edit = QLineEdit(self.frame_meas)
        self.stop_edit.setObjectName(u"stop_edit")
        self.stop_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.stop_edit, 3, 1, 1, 1)

        self.sample_edit = QLineEdit(self.frame_meas)
        self.sample_edit.setObjectName(u"sample_edit")
        self.sample_edit.setMaxLength(20)
        self.sample_edit.setFrame(True)
        self.sample_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.sample_edit, 0, 1, 1, 1)

        self.label_sample = QLabel(self.frame_meas)
        self.label_sample.setObjectName(u"label_sample")

        self.gridLayout_5.addWidget(self.label_sample, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_meas)

        self.frame_amp = QFrame(exp_control)
        self.frame_amp.setObjectName(u"frame_amp")
        self.frame_amp.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_amp.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_amp)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.nplc_edit = QLineEdit(self.frame_amp)
        self.nplc_edit.setObjectName(u"nplc_edit")
        self.nplc_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.nplc_edit, 2, 2, 1, 1)

        self.average_edit = QLineEdit(self.frame_amp)
        self.average_edit.setObjectName(u"average_edit")
        self.average_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.average_edit, 4, 2, 1, 1)

        self.frame_channel = QFrame(self.frame_amp)
        self.frame_channel.setObjectName(u"frame_channel")
        self.frame_channel.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_channel.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_channel.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_channel)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.channel1_radio = QRadioButton(self.frame_channel)
        self.channel1_radio.setObjectName(u"channel1_radio")
        self.channel1_radio.setChecked(True)

        self.horizontalLayout_2.addWidget(self.channel1_radio)

        self.channel2_radio = QRadioButton(self.frame_channel)
        self.channel2_radio.setObjectName(u"channel2_radio")
        self.channel2_radio.setChecked(False)

        self.horizontalLayout_2.addWidget(self.channel2_radio)


        self.gridLayout_6.addWidget(self.frame_channel, 0, 2, 1, 1)

        self.label_channel = QLabel(self.frame_amp)
        self.label_channel.setObjectName(u"label_channel")

        self.gridLayout_6.addWidget(self.label_channel, 0, 1, 1, 1)

        self.voltage_check = QCheckBox(self.frame_amp)
        self.voltage_check.setObjectName(u"voltage_check")

        self.gridLayout_6.addWidget(self.voltage_check, 1, 0, 1, 1)

        self.label_nplc = QLabel(self.frame_amp)
        self.label_nplc.setObjectName(u"label_nplc")

        self.gridLayout_6.addWidget(self.label_nplc, 2, 1, 1, 1)

        self.voltage_edit = QLineEdit(self.frame_amp)
        self.voltage_edit.setObjectName(u"voltage_edit")
        self.voltage_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.voltage_edit, 1, 2, 1, 1)

        self.average_check = QCheckBox(self.frame_amp)
        self.average_check.setObjectName(u"average_check")

        self.gridLayout_6.addWidget(self.average_check, 4, 0, 1, 1)

        self.label_average = QLabel(self.frame_amp)
        self.label_average.setObjectName(u"label_average")

        self.gridLayout_6.addWidget(self.label_average, 4, 1, 1, 1)

        self.label_voltage = QLabel(self.frame_amp)
        self.label_voltage.setObjectName(u"label_voltage")

        self.gridLayout_6.addWidget(self.label_voltage, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_amp)

        self.frame_mono = QFrame(exp_control)
        self.frame_mono.setObjectName(u"frame_mono")
        self.frame_mono.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_mono.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_mono)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_shutter = QLabel(self.frame_mono)
        self.label_shutter.setObjectName(u"label_shutter")

        self.gridLayout_2.addWidget(self.label_shutter, 1, 0, 1, 1)

        self.wl_edit = QLineEdit(self.frame_mono)
        self.wl_edit.setObjectName(u"wl_edit")
        self.wl_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.wl_edit, 0, 1, 1, 1)

        self.shutter_check = QCheckBox(self.frame_mono)
        self.shutter_check.setObjectName(u"shutter_check")

        self.gridLayout_2.addWidget(self.shutter_check, 1, 1, 1, 1)

        self.label_setwl = QLabel(self.frame_mono)
        self.label_setwl.setObjectName(u"label_setwl")

        self.gridLayout_2.addWidget(self.label_setwl, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_mono)

        self.frame_control = QFrame(exp_control)
        self.frame_control.setObjectName(u"frame_control")
        self.frame_control.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_control.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_control)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.start_button = QPushButton(self.frame_control)
        self.start_button.setObjectName(u"start_button")

        self.gridLayout_7.addWidget(self.start_button, 0, 0, 1, 1)

        self.stop_button = QPushButton(self.frame_control)
        self.stop_button.setObjectName(u"stop_button")

        self.gridLayout_7.addWidget(self.stop_button, 0, 1, 1, 1)

        self.progress_bar = QProgressBar(self.frame_control)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.gridLayout_7.addWidget(self.progress_bar, 1, 0, 1, 2)


        self.verticalLayout.addWidget(self.frame_control)

        self.exp_list_view = QListView(exp_control)
        self.exp_list_view.setObjectName(u"exp_list_view")

        self.verticalLayout.addWidget(self.exp_list_view)


        self.retranslateUi(exp_control)

        QMetaObject.connectSlotsByName(exp_control)
    # setupUi

    def retranslateUi(self, exp_control):
        exp_control.setWindowTitle(QCoreApplication.translate("exp_control", u"exp_control", None))
        self.start_edit.setText(QCoreApplication.translate("exp_control", u"300", None))
        self.start_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"from, nm", None))
        self.step_edit.setText(QCoreApplication.translate("exp_control", u"5", None))
        self.step_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"step, nm", None))
        self.label_start.setText(QCoreApplication.translate("exp_control", u"Start \u03bb", None))
        self.delay_edit.setText(QCoreApplication.translate("exp_control", u"0", None))
        self.delay_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"delay, s", None))
        self.label_stop.setText(QCoreApplication.translate("exp_control", u"Stop \u03bb", None))
        self.label_delay.setText(QCoreApplication.translate("exp_control", u"Delay", None))
        self.label_step.setText(QCoreApplication.translate("exp_control", u"\u0394\u03bb", None))
        self.stop_edit.setText(QCoreApplication.translate("exp_control", u"2000", None))
        self.stop_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"to, nm", None))
        self.sample_edit.setText("")
        self.sample_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"sample_name", None))
        self.label_sample.setText(QCoreApplication.translate("exp_control", u"Sample", None))
        self.nplc_edit.setText(QCoreApplication.translate("exp_control", u"1", None))
        self.nplc_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"0.01 - 10.00", None))
        self.average_edit.setText(QCoreApplication.translate("exp_control", u"1", None))
        self.average_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"1 - 100", None))
        self.channel1_radio.setText(QCoreApplication.translate("exp_control", u"1", None))
        self.channel2_radio.setText(QCoreApplication.translate("exp_control", u"2", None))
        self.label_channel.setText(QCoreApplication.translate("exp_control", u"Channel", None))
        self.voltage_check.setText("")
        self.label_nplc.setText(QCoreApplication.translate("exp_control", u"NPLC", None))
        self.voltage_edit.setText(QCoreApplication.translate("exp_control", u"0", None))
        self.voltage_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"voltage: \u00b110 V", None))
        self.average_check.setText("")
        self.label_average.setText(QCoreApplication.translate("exp_control", u"Average", None))
        self.label_voltage.setText(QCoreApplication.translate("exp_control", u"Voltage", None))
        self.label_shutter.setText(QCoreApplication.translate("exp_control", u"Shutter", None))
        self.wl_edit.setText("")
        self.wl_edit.setPlaceholderText(QCoreApplication.translate("exp_control", u"300 - 2000 nm", None))
        self.shutter_check.setText("")
        self.label_setwl.setText(QCoreApplication.translate("exp_control", u"Set  \u03bb", None))
        self.start_button.setText(QCoreApplication.translate("exp_control", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("exp_control", u"Stop", None))
    # retranslateUi

