# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
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
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1167, 924)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setMinimumSize(QSize(572, 0))
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabs.setElideMode(Qt.TextElideMode.ElideNone)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(False)
        self.tabs.setMovable(False)
        self.tab_si = QWidget()
        self.tab_si.setObjectName(u"tab_si")
        self.tabs.addTab(self.tab_si, "")
        self.tab_ingaas = QWidget()
        self.tab_ingaas.setObjectName(u"tab_ingaas")
        self.tabs.addTab(self.tab_ingaas, "")
        self.tab_sample = QWidget()
        self.tab_sample.setObjectName(u"tab_sample")
        self.tabs.addTab(self.tab_sample, "")

        self.horizontalLayout.addWidget(self.tabs)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMaximumSize(QSize(300, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 298, 862))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_meas = QFrame(self.scrollAreaWidgetContents)
        self.frame_meas.setObjectName(u"frame_meas")
        self.frame_meas.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_meas.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_meas)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.start_edit = QLineEdit(self.frame_meas)
        self.start_edit.setObjectName(u"start_edit")
        self.start_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_edit.setDragEnabled(False)
        self.start_edit.setReadOnly(False)

        self.gridLayout_3.addWidget(self.start_edit, 1, 1, 1, 1)

        self.step_edit = QLineEdit(self.frame_meas)
        self.step_edit.setObjectName(u"step_edit")
        self.step_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.step_edit, 4, 1, 1, 1)

        self.label_start = QLabel(self.frame_meas)
        self.label_start.setObjectName(u"label_start")

        self.gridLayout_3.addWidget(self.label_start, 1, 0, 1, 1)

        self.delay_edit = QLineEdit(self.frame_meas)
        self.delay_edit.setObjectName(u"delay_edit")
        self.delay_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.delay_edit, 5, 1, 1, 1)

        self.label_stop = QLabel(self.frame_meas)
        self.label_stop.setObjectName(u"label_stop")

        self.gridLayout_3.addWidget(self.label_stop, 3, 0, 1, 1)

        self.label_delay = QLabel(self.frame_meas)
        self.label_delay.setObjectName(u"label_delay")
        self.label_delay.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_delay, 5, 0, 1, 1)

        self.label_step = QLabel(self.frame_meas)
        self.label_step.setObjectName(u"label_step")
        self.label_step.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_step, 4, 0, 1, 1)

        self.stop_edit = QLineEdit(self.frame_meas)
        self.stop_edit.setObjectName(u"stop_edit")
        self.stop_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.stop_edit, 3, 1, 1, 1)

        self.sample_edit = QLineEdit(self.frame_meas)
        self.sample_edit.setObjectName(u"sample_edit")
        self.sample_edit.setMaxLength(20)
        self.sample_edit.setFrame(True)
        self.sample_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.sample_edit, 0, 1, 1, 1)

        self.label_sample = QLabel(self.frame_meas)
        self.label_sample.setObjectName(u"label_sample")

        self.gridLayout_3.addWidget(self.label_sample, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_meas)

        self.frame_amp = QFrame(self.scrollAreaWidgetContents)
        self.frame_amp.setObjectName(u"frame_amp")
        self.frame_amp.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_amp.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_amp)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.nplc_edit = QLineEdit(self.frame_amp)
        self.nplc_edit.setObjectName(u"nplc_edit")
        self.nplc_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.nplc_edit, 2, 2, 1, 1)

        self.average_edit = QLineEdit(self.frame_amp)
        self.average_edit.setObjectName(u"average_edit")
        self.average_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.average_edit, 4, 2, 1, 1)

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


        self.gridLayout_4.addWidget(self.frame_channel, 0, 2, 1, 1)

        self.label_channel = QLabel(self.frame_amp)
        self.label_channel.setObjectName(u"label_channel")

        self.gridLayout_4.addWidget(self.label_channel, 0, 1, 1, 1)

        self.voltage_check = QCheckBox(self.frame_amp)
        self.voltage_check.setObjectName(u"voltage_check")

        self.gridLayout_4.addWidget(self.voltage_check, 1, 0, 1, 1)

        self.label_nplc = QLabel(self.frame_amp)
        self.label_nplc.setObjectName(u"label_nplc")

        self.gridLayout_4.addWidget(self.label_nplc, 2, 1, 1, 1)

        self.voltage_edit = QLineEdit(self.frame_amp)
        self.voltage_edit.setObjectName(u"voltage_edit")
        self.voltage_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.voltage_edit, 1, 2, 1, 1)

        self.average_check = QCheckBox(self.frame_amp)
        self.average_check.setObjectName(u"average_check")

        self.gridLayout_4.addWidget(self.average_check, 4, 0, 1, 1)

        self.label_average = QLabel(self.frame_amp)
        self.label_average.setObjectName(u"label_average")

        self.gridLayout_4.addWidget(self.label_average, 4, 1, 1, 1)

        self.label_voltage = QLabel(self.frame_amp)
        self.label_voltage.setObjectName(u"label_voltage")

        self.gridLayout_4.addWidget(self.label_voltage, 1, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_amp)

        self.frame_mono = QFrame(self.scrollAreaWidgetContents)
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


        self.verticalLayout_2.addWidget(self.frame_mono)

        self.frame_control = QFrame(self.scrollAreaWidgetContents)
        self.frame_control.setObjectName(u"frame_control")
        self.frame_control.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_control.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_control)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.start_button = QPushButton(self.frame_control)
        self.start_button.setObjectName(u"start_button")

        self.gridLayout_5.addWidget(self.start_button, 0, 0, 1, 1)

        self.stop_button = QPushButton(self.frame_control)
        self.stop_button.setObjectName(u"stop_button")

        self.gridLayout_5.addWidget(self.stop_button, 0, 1, 1, 1)

        self.progress_bar = QProgressBar(self.frame_control)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.gridLayout_5.addWidget(self.progress_bar, 1, 0, 1, 2)


        self.verticalLayout_2.addWidget(self.frame_control)

        self.exp_list_view = QListView(self.scrollAreaWidgetContents)
        self.exp_list_view.setObjectName(u"exp_list_view")

        self.verticalLayout_2.addWidget(self.exp_list_view)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1167, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.tabs, self.sample_edit)
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
        QWidget.setTabOrder(self.exp_list_view, self.scrollArea)

        self.retranslateUi(MainWindow)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_si), QCoreApplication.translate("MainWindow", u"Si", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_ingaas), QCoreApplication.translate("MainWindow", u"InGaAs", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_sample), QCoreApplication.translate("MainWindow", u"Sample", None))
        self.start_edit.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.start_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"from, nm", None))
        self.step_edit.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.step_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"step, nm", None))
        self.label_start.setText(QCoreApplication.translate("MainWindow", u"Start \u03bb", None))
        self.delay_edit.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.delay_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"delay, s", None))
        self.label_stop.setText(QCoreApplication.translate("MainWindow", u"Stop \u03bb", None))
        self.label_delay.setText(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.label_step.setText(QCoreApplication.translate("MainWindow", u"\u0394\u03bb", None))
        self.stop_edit.setText(QCoreApplication.translate("MainWindow", u"2000", None))
        self.stop_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"to, nm", None))
        self.sample_edit.setText("")
        self.sample_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"sample_name", None))
        self.label_sample.setText(QCoreApplication.translate("MainWindow", u"Sample", None))
        self.nplc_edit.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.nplc_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"0.01 - 10.00", None))
        self.average_edit.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.average_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"1 - 100", None))
        self.channel1_radio.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.channel2_radio.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.label_channel.setText(QCoreApplication.translate("MainWindow", u"Channel", None))
        self.voltage_check.setText("")
        self.label_nplc.setText(QCoreApplication.translate("MainWindow", u"NPLC", None))
        self.voltage_edit.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.voltage_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"voltage: \u00b110 V", None))
        self.average_check.setText("")
        self.label_average.setText(QCoreApplication.translate("MainWindow", u"Average", None))
        self.label_voltage.setText(QCoreApplication.translate("MainWindow", u"Voltage", None))
        self.label_shutter.setText(QCoreApplication.translate("MainWindow", u"Shutter", None))
        self.wl_edit.setText("")
        self.wl_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"300 - 2000 nm", None))
        self.shutter_check.setText("")
        self.label_setwl.setText(QCoreApplication.translate("MainWindow", u"Set  \u03bb", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
    # retranslateUi

