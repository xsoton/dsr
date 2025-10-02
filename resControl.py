# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resControl.ui'
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
from PySide6.QtWidgets import (QApplication, QListView, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_resControl(object):
    def setupUi(self, resControl):
        if not resControl.objectName():
            resControl.setObjectName(u"resControl")
        resControl.resize(300, 300)
        resControl.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout = QVBoxLayout(resControl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.save_button = QPushButton(resControl)
        self.save_button.setObjectName(u"save_button")

        self.verticalLayout.addWidget(self.save_button)

        self.exp_list_view = QListView(resControl)
        self.exp_list_view.setObjectName(u"exp_list_view")

        self.verticalLayout.addWidget(self.exp_list_view)

        QWidget.setTabOrder(self.save_button, self.exp_list_view)

        self.retranslateUi(resControl)

        QMetaObject.connectSlotsByName(resControl)
    # setupUi

    def retranslateUi(self, resControl):
        resControl.setWindowTitle(QCoreApplication.translate("resControl", u"Form", None))
        self.save_button.setText(QCoreApplication.translate("resControl", u"Save", None))
    # retranslateUi

