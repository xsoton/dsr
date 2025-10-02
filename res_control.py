# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'res_control.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QListView,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_res_control(object):
    def setupUi(self, res_control):
        if not res_control.objectName():
            res_control.setObjectName(u"res_control")
        res_control.resize(300, 862)
        res_control.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout = QVBoxLayout(res_control)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_control = QFrame(res_control)
        self.frame_control.setObjectName(u"frame_control")
        self.frame_control.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_control.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_control)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.new_button = QPushButton(self.frame_control)
        self.new_button.setObjectName(u"new_button")

        self.gridLayout_5.addWidget(self.new_button, 0, 0, 1, 1)

        self.save_button = QPushButton(self.frame_control)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setEnabled(False)

        self.gridLayout_5.addWidget(self.save_button, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_control)

        self.res_list_view = QListView(res_control)
        self.res_list_view.setObjectName(u"res_list_view")

        self.verticalLayout.addWidget(self.res_list_view)


        self.retranslateUi(res_control)

        QMetaObject.connectSlotsByName(res_control)
    # setupUi

    def retranslateUi(self, res_control):
        res_control.setWindowTitle(QCoreApplication.translate("res_control", u"res_control", None))
        self.new_button.setText(QCoreApplication.translate("res_control", u"New", None))
        self.save_button.setText(QCoreApplication.translate("res_control", u"Save", None))
    # retranslateUi

