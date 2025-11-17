# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ToolsPage.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ToolsPage(object):
    def setupUi(self, ToolsPage):
        if not ToolsPage.objectName():
            ToolsPage.setObjectName(u"ToolsPage")
        ToolsPage.resize(480, 640)
        self.verticalLayout = QVBoxLayout(ToolsPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tools_title_layout = QHBoxLayout()
        self.tools_title_layout.setObjectName(u"tools_title_layout")
        self.tools_title_layout.setContentsMargins(-1, -1, -1, 32)
        self.tools_title_label = QLabel(ToolsPage)
        self.tools_title_label.setObjectName(u"tools_title_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tools_title_label.sizePolicy().hasHeightForWidth())
        self.tools_title_label.setSizePolicy(sizePolicy)

        self.tools_title_layout.addWidget(self.tools_title_label)


        self.verticalLayout.addLayout(self.tools_title_layout)

        self.content_area = QWidget(ToolsPage)
        self.content_area.setObjectName(u"content_area")

        self.verticalLayout.addWidget(self.content_area)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(ToolsPage)

        QMetaObject.connectSlotsByName(ToolsPage)
    # setupUi

    def retranslateUi(self, ToolsPage):
        ToolsPage.setWindowTitle(QCoreApplication.translate("ToolsPage", u"Form", None))
        self.tools_title_label.setText(QCoreApplication.translate("ToolsPage", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">Tools</span></p></body></html>", None))
    # retranslateUi

