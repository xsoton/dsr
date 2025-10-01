# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'control2.ui'
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
    QPushButton, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_scrollArea(object):
    def setupUi(self, scrollArea):
        if not scrollArea.objectName():
            scrollArea.setObjectName(u"scrollArea")
        scrollArea.setEnabled(True)
        scrollArea.resize(300, 864)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(scrollArea.sizePolicy().hasHeightForWidth())
        scrollArea.setSizePolicy(sizePolicy)
        scrollArea.setMaximumSize(QSize(300, 16777215))
        scrollArea.setWidgetResizable(True)
        scrollArea.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 298, 862))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_control = QFrame(self.scrollAreaWidgetContents)
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


        self.verticalLayout_2.addWidget(self.frame_control)

        self.res_list_view = QListView(self.scrollAreaWidgetContents)
        self.res_list_view.setObjectName(u"res_list_view")

        self.verticalLayout_2.addWidget(self.res_list_view)

        scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(scrollArea)

        QMetaObject.connectSlotsByName(scrollArea)
    # setupUi

    def retranslateUi(self, scrollArea):
        self.new_button.setText(QCoreApplication.translate("scrollArea", u"New", None))
        self.save_button.setText(QCoreApplication.translate("scrollArea", u"Save", None))
        pass
    # retranslateUi

