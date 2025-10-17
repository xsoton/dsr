# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DSRControl.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QLabel,
    QLineEdit, QSizePolicy, QWidget)

class Ui_DSRControl(object):
    def setupUi(self, DSRControl):
        if not DSRControl.objectName():
            DSRControl.setObjectName(u"DSRControl")
        DSRControl.resize(300, 61)
        DSRControl.setMaximumSize(QSize(1000, 16777215))
        self.formLayout = QFormLayout(DSRControl)
        self.formLayout.setObjectName(u"formLayout")
        self.label_wl = QLabel(DSRControl)
        self.label_wl.setObjectName(u"label_wl")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_wl)

        self.edit_wl = QLineEdit(DSRControl)
        self.edit_wl.setObjectName(u"edit_wl")
        self.edit_wl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.edit_wl)

        self.label_shutter = QLabel(DSRControl)
        self.label_shutter.setObjectName(u"label_shutter")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_shutter)

        self.check_shutter = QCheckBox(DSRControl)
        self.check_shutter.setObjectName(u"check_shutter")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.check_shutter)


        self.retranslateUi(DSRControl)

        QMetaObject.connectSlotsByName(DSRControl)
    # setupUi

    def retranslateUi(self, DSRControl):
        DSRControl.setWindowTitle(QCoreApplication.translate("DSRControl", u"DSRControl", None))
        self.label_wl.setText(QCoreApplication.translate("DSRControl", u"\u03bb", None))
        self.edit_wl.setText("")
        self.edit_wl.setPlaceholderText(QCoreApplication.translate("DSRControl", u"300 - 2000 nm", None))
        self.label_shutter.setText(QCoreApplication.translate("DSRControl", u"Shutter", None))
        self.check_shutter.setText("")
    # retranslateUi

