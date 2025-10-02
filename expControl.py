# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'expControl.ui'
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

class Ui_expControl(object):
    def setupUi(self, expControl):
        if not expControl.objectName():
            expControl.setObjectName(u"expControl")
        expControl.resize(300, 1032)
        expControl.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout = QVBoxLayout(expControl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_meas = QFrame(expControl)
        self.frame_meas.setObjectName(u"frame_meas")
        self.frame_meas.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_meas.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_meas)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.start_edit = QLineEdit(self.frame_meas)
        self.start_edit.setObjectName(u"start_edit")
        self.start_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_edit.setDragEnabled(False)
        self.start_edit.setReadOnly(False)

        self.gridLayout_11.addWidget(self.start_edit, 1, 1, 1, 1)

        self.step_edit = QLineEdit(self.frame_meas)
        self.step_edit.setObjectName(u"step_edit")
        self.step_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.step_edit, 4, 1, 1, 1)

        self.label_start = QLabel(self.frame_meas)
        self.label_start.setObjectName(u"label_start")

        self.gridLayout_11.addWidget(self.label_start, 1, 0, 1, 1)

        self.delay_edit = QLineEdit(self.frame_meas)
        self.delay_edit.setObjectName(u"delay_edit")
        self.delay_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.delay_edit, 5, 1, 1, 1)

        self.label_stop = QLabel(self.frame_meas)
        self.label_stop.setObjectName(u"label_stop")

        self.gridLayout_11.addWidget(self.label_stop, 3, 0, 1, 1)

        self.label_delay = QLabel(self.frame_meas)
        self.label_delay.setObjectName(u"label_delay")
        self.label_delay.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_delay, 5, 0, 1, 1)

        self.label_step = QLabel(self.frame_meas)
        self.label_step.setObjectName(u"label_step")
        self.label_step.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_step, 4, 0, 1, 1)

        self.stop_edit = QLineEdit(self.frame_meas)
        self.stop_edit.setObjectName(u"stop_edit")
        self.stop_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.stop_edit, 3, 1, 1, 1)

        self.sample_edit = QLineEdit(self.frame_meas)
        self.sample_edit.setObjectName(u"sample_edit")
        self.sample_edit.setMaxLength(20)
        self.sample_edit.setFrame(True)
        self.sample_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.sample_edit, 0, 1, 1, 1)

        self.label_sample = QLabel(self.frame_meas)
        self.label_sample.setObjectName(u"label_sample")

        self.gridLayout_11.addWidget(self.label_sample, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_meas)

        self.frame_amp = QFrame(expControl)
        self.frame_amp.setObjectName(u"frame_amp")
        self.frame_amp.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_amp.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_amp)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.nplc_edit = QLineEdit(self.frame_amp)
        self.nplc_edit.setObjectName(u"nplc_edit")
        self.nplc_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.nplc_edit, 2, 2, 1, 1)

        self.average_edit = QLineEdit(self.frame_amp)
        self.average_edit.setObjectName(u"average_edit")
        self.average_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.average_edit, 4, 2, 1, 1)

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

        self.label_channel = QLabel(self.frame_amp)
        self.label_channel.setObjectName(u"label_channel")

        self.gridLayout_15.addWidget(self.label_channel, 0, 1, 1, 1)

        self.voltage_check = QCheckBox(self.frame_amp)
        self.voltage_check.setObjectName(u"voltage_check")

        self.gridLayout_15.addWidget(self.voltage_check, 1, 0, 1, 1)

        self.label_nplc = QLabel(self.frame_amp)
        self.label_nplc.setObjectName(u"label_nplc")

        self.gridLayout_15.addWidget(self.label_nplc, 2, 1, 1, 1)

        self.voltage_edit = QLineEdit(self.frame_amp)
        self.voltage_edit.setObjectName(u"voltage_edit")
        self.voltage_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.voltage_edit, 1, 2, 1, 1)

        self.average_check = QCheckBox(self.frame_amp)
        self.average_check.setObjectName(u"average_check")

        self.gridLayout_15.addWidget(self.average_check, 4, 0, 1, 1)

        self.label_average = QLabel(self.frame_amp)
        self.label_average.setObjectName(u"label_average")

        self.gridLayout_15.addWidget(self.label_average, 4, 1, 1, 1)

        self.label_voltage = QLabel(self.frame_amp)
        self.label_voltage.setObjectName(u"label_voltage")

        self.gridLayout_15.addWidget(self.label_voltage, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_amp)

        self.frame_mono = QFrame(expControl)
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

        self.frame_control = QFrame(expControl)
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

        self.exp_list_view = QListView(expControl)
        self.exp_list_view.setObjectName(u"exp_list_view")

        self.verticalLayout.addWidget(self.exp_list_view)

        QWidget.setTabOrder(self.sample_edit, self.start_edit)
        QWidget.setTabOrder(self.start_edit, self.stop_edit)
        QWidget.setTabOrder(self.stop_edit, self.step_edit)
        QWidget.setTabOrder(self.step_edit, self.delay_edit)
        QWidget.setTabOrder(self.delay_edit, self.channel1_radio)
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

        self.retranslateUi(expControl)

        QMetaObject.connectSlotsByName(expControl)
    # setupUi

    def retranslateUi(self, expControl):
        expControl.setWindowTitle(QCoreApplication.translate("expControl", u"expControl", None))
        self.start_edit.setText(QCoreApplication.translate("expControl", u"300", None))
        self.start_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"from, nm", None))
        self.step_edit.setText(QCoreApplication.translate("expControl", u"5", None))
        self.step_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"step, nm", None))
        self.label_start.setText(QCoreApplication.translate("expControl", u"Start \u03bb", None))
        self.delay_edit.setText(QCoreApplication.translate("expControl", u"0", None))
        self.delay_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"delay, s", None))
        self.label_stop.setText(QCoreApplication.translate("expControl", u"Stop \u03bb", None))
        self.label_delay.setText(QCoreApplication.translate("expControl", u"Delay", None))
        self.label_step.setText(QCoreApplication.translate("expControl", u"\u0394\u03bb", None))
        self.stop_edit.setText(QCoreApplication.translate("expControl", u"2000", None))
        self.stop_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"to, nm", None))
        self.sample_edit.setText("")
        self.sample_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"sample_name", None))
        self.label_sample.setText(QCoreApplication.translate("expControl", u"Sample", None))
        self.nplc_edit.setText(QCoreApplication.translate("expControl", u"1", None))
        self.nplc_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"0.01 - 10.00", None))
        self.average_edit.setText(QCoreApplication.translate("expControl", u"1", None))
        self.average_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"1 - 100", None))
        self.channel1_radio.setText(QCoreApplication.translate("expControl", u"1", None))
        self.channel2_radio.setText(QCoreApplication.translate("expControl", u"2", None))
        self.label_channel.setText(QCoreApplication.translate("expControl", u"Channel", None))
        self.voltage_check.setText("")
        self.label_nplc.setText(QCoreApplication.translate("expControl", u"NPLC", None))
        self.voltage_edit.setText(QCoreApplication.translate("expControl", u"0", None))
        self.voltage_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"voltage: \u00b110 V", None))
        self.average_check.setText("")
        self.label_average.setText(QCoreApplication.translate("expControl", u"Average", None))
        self.label_voltage.setText(QCoreApplication.translate("expControl", u"Voltage", None))
        self.label_shutter.setText(QCoreApplication.translate("expControl", u"Shutter", None))
        self.wl_edit.setText("")
        self.wl_edit.setPlaceholderText(QCoreApplication.translate("expControl", u"300 - 2000 nm", None))
        self.shutter_check.setText("")
        self.label_setwl.setText(QCoreApplication.translate("expControl", u"Set  \u03bb", None))
        self.start_button.setText(QCoreApplication.translate("expControl", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("expControl", u"Stop", None))
    # retranslateUi

