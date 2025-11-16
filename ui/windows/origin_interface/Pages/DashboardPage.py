# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DashboardPage.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_DashboardPage(object):
    def setupUi(self, DashboardPage):
        if not DashboardPage.objectName():
            DashboardPage.setObjectName(u"DashboardPage")
        DashboardPage.resize(698, 642)
        self.verticalLayout = QVBoxLayout(DashboardPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.dashboard_title_layout = QHBoxLayout()
        self.dashboard_title_layout.setSpacing(6)
        self.dashboard_title_layout.setObjectName(u"dashboard_title_layout")
        self.dashboard_title_layout.setContentsMargins(-1, -1, -1, 32)
        self.dashboard_title_label_2 = QLabel(DashboardPage)
        self.dashboard_title_label_2.setObjectName(u"dashboard_title_label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dashboard_title_label_2.sizePolicy().hasHeightForWidth())
        self.dashboard_title_label_2.setSizePolicy(sizePolicy)

        self.dashboard_title_layout.addWidget(self.dashboard_title_label_2)


        self.verticalLayout.addLayout(self.dashboard_title_layout)

        self.dashboard_head_column_layout = QHBoxLayout()
        self.dashboard_head_column_layout.setObjectName(u"dashboard_head_column_layout")
        self.dashboard_service_label = QLabel(DashboardPage)
        self.dashboard_service_label.setObjectName(u"dashboard_service_label")

        self.dashboard_head_column_layout.addWidget(self.dashboard_service_label)

        self.dashboard_type_label = QLabel(DashboardPage)
        self.dashboard_type_label.setObjectName(u"dashboard_type_label")

        self.dashboard_head_column_layout.addWidget(self.dashboard_type_label)

        self.dashboard_version_label = QLabel(DashboardPage)
        self.dashboard_version_label.setObjectName(u"dashboard_version_label")

        self.dashboard_head_column_layout.addWidget(self.dashboard_version_label)

        self.dashboard_status_label = QLabel(DashboardPage)
        self.dashboard_status_label.setObjectName(u"dashboard_status_label")

        self.dashboard_head_column_layout.addWidget(self.dashboard_status_label)


        self.verticalLayout.addLayout(self.dashboard_head_column_layout)

        self.dashboard_content_layout = QGridLayout()
        self.dashboard_content_layout.setObjectName(u"dashboard_content_layout")
        self.tool_3_start_pushButton = QPushButton(DashboardPage)
        self.tool_3_start_pushButton.setObjectName(u"tool_3_start_pushButton")

        self.dashboard_content_layout.addWidget(self.tool_3_start_pushButton, 5, 3, 1, 1)

        self.startall_button = QPushButton(DashboardPage)
        self.startall_button.setObjectName(u"startall_button")

        self.dashboard_content_layout.addWidget(self.startall_button, 7, 1, 1, 2)

        self.language_version_label = QLabel(DashboardPage)
        self.language_version_label.setObjectName(u"language_version_label")
        self.language_version_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.language_version_label, 0, 2, 1, 1)

        self.tool_type_3_label = QLabel(DashboardPage)
        self.tool_type_3_label.setObjectName(u"tool_type_3_label")
        self.tool_type_3_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.tool_type_3_label, 5, 1, 1, 1)

        self.database_start_pushButton = QPushButton(DashboardPage)
        self.database_start_pushButton.setObjectName(u"database_start_pushButton")

        self.dashboard_content_layout.addWidget(self.database_start_pushButton, 1, 3, 1, 1)

        self.network_service_label = QLabel(DashboardPage)
        self.network_service_label.setObjectName(u"network_service_label")

        self.dashboard_content_layout.addWidget(self.network_service_label, 6, 0, 1, 1)

        self.webserver_start_pushButton = QPushButton(DashboardPage)
        self.webserver_start_pushButton.setObjectName(u"webserver_start_pushButton")

        self.dashboard_content_layout.addWidget(self.webserver_start_pushButton, 2, 3, 1, 1)

        self.tool_1_start_pushButton = QPushButton(DashboardPage)
        self.tool_1_start_pushButton.setObjectName(u"tool_1_start_pushButton")

        self.dashboard_content_layout.addWidget(self.tool_1_start_pushButton, 3, 3, 1, 1)

        self.network_version_label = QLabel(DashboardPage)
        self.network_version_label.setObjectName(u"network_version_label")
        self.network_version_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.network_version_label, 6, 2, 1, 1)

        self.tools_service_label = QLabel(DashboardPage)
        self.tools_service_label.setObjectName(u"tools_service_label")

        self.dashboard_content_layout.addWidget(self.tools_service_label, 3, 0, 1, 1)

        self.tool_2_start_pushButton = QPushButton(DashboardPage)
        self.tool_2_start_pushButton.setObjectName(u"tool_2_start_pushButton")

        self.dashboard_content_layout.addWidget(self.tool_2_start_pushButton, 4, 3, 1, 1)

        self.tool_type_2_label = QLabel(DashboardPage)
        self.tool_type_2_label.setObjectName(u"tool_type_2_label")
        self.tool_type_2_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.tool_type_2_label, 4, 1, 1, 1)

        self.language_start_pushButton = QPushButton(DashboardPage)
        self.language_start_pushButton.setObjectName(u"language_start_pushButton")

        self.dashboard_content_layout.addWidget(self.language_start_pushButton, 0, 3, 1, 1)

        self.network_start_pushButton = QPushButton(DashboardPage)
        self.network_start_pushButton.setObjectName(u"network_start_pushButton")

        self.dashboard_content_layout.addWidget(self.network_start_pushButton, 6, 3, 1, 1)

        self.network_type_label = QLabel(DashboardPage)
        self.network_type_label.setObjectName(u"network_type_label")
        self.network_type_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.network_type_label, 6, 1, 1, 1)

        self.language_type_label = QLabel(DashboardPage)
        self.language_type_label.setObjectName(u"language_type_label")
        self.language_type_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.language_type_label, 0, 1, 1, 1)

        self.database_service_label = QLabel(DashboardPage)
        self.database_service_label.setObjectName(u"database_service_label")

        self.dashboard_content_layout.addWidget(self.database_service_label, 1, 0, 1, 1)

        self.webserver_version_label = QLabel(DashboardPage)
        self.webserver_version_label.setObjectName(u"webserver_version_label")
        self.webserver_version_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.webserver_version_label, 2, 2, 1, 1)

        self.database_type_label = QLabel(DashboardPage)
        self.database_type_label.setObjectName(u"database_type_label")
        self.database_type_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.database_type_label, 1, 1, 1, 1)

        self.tool_version_2_label = QLabel(DashboardPage)
        self.tool_version_2_label.setObjectName(u"tool_version_2_label")
        self.tool_version_2_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.tool_version_2_label, 4, 2, 1, 1)

        self.language_service_label = QLabel(DashboardPage)
        self.language_service_label.setObjectName(u"language_service_label")

        self.dashboard_content_layout.addWidget(self.language_service_label, 0, 0, 1, 1)

        self.webserver_service_label = QLabel(DashboardPage)
        self.webserver_service_label.setObjectName(u"webserver_service_label")

        self.dashboard_content_layout.addWidget(self.webserver_service_label, 2, 0, 1, 1)

        self.tool_type_1_label = QLabel(DashboardPage)
        self.tool_type_1_label.setObjectName(u"tool_type_1_label")
        self.tool_type_1_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.tool_type_1_label, 3, 1, 1, 1)

        self.tool_version_1_label = QLabel(DashboardPage)
        self.tool_version_1_label.setObjectName(u"tool_version_1_label")
        self.tool_version_1_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.tool_version_1_label, 3, 2, 1, 1)

        self.webserver_type_label = QLabel(DashboardPage)
        self.webserver_type_label.setObjectName(u"webserver_type_label")
        self.webserver_type_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.webserver_type_label, 2, 1, 1, 1)

        self.tool_version_3_label = QLabel(DashboardPage)
        self.tool_version_3_label.setObjectName(u"tool_version_3_label")
        self.tool_version_3_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.tool_version_3_label, 5, 2, 1, 1)

        self.database_version_label = QLabel(DashboardPage)
        self.database_version_label.setObjectName(u"database_version_label")
        self.database_version_label.setMaximumSize(QSize(16777215, 16777215))
        self.database_version_label.setStyleSheet(u"word-break: break-all;")
        self.database_version_label.setTextFormat(Qt.TextFormat.PlainText)
        self.database_version_label.setWordWrap(True)

        self.dashboard_content_layout.addWidget(self.database_version_label, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.dashboard_content_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(DashboardPage)

        QMetaObject.connectSlotsByName(DashboardPage)
    # setupUi

    def retranslateUi(self, DashboardPage):
        DashboardPage.setWindowTitle(QCoreApplication.translate("DashboardPage", u"Form", None))
        self.dashboard_title_label_2.setText(QCoreApplication.translate("DashboardPage", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">Dashboard</span></p></body></html>", None))
        self.dashboard_service_label.setText(QCoreApplication.translate("DashboardPage", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Service</span></p></body></html>", None))
        self.dashboard_type_label.setText(QCoreApplication.translate("DashboardPage", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Type</span></p></body></html>", None))
        self.dashboard_version_label.setText(QCoreApplication.translate("DashboardPage", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Version</span></p></body></html>", None))
        self.dashboard_status_label.setText(QCoreApplication.translate("DashboardPage", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Status</span></p></body></html>", None))
        self.tool_3_start_pushButton.setText(QCoreApplication.translate("DashboardPage", u"Start", None))
        self.startall_button.setText(QCoreApplication.translate("DashboardPage", u"Start All", None))
        self.language_version_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.tool_type_3_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.database_start_pushButton.setText(QCoreApplication.translate("DashboardPage", u"Start", None))
        self.network_service_label.setText(QCoreApplication.translate("DashboardPage", u"Network", None))
        self.webserver_start_pushButton.setText(QCoreApplication.translate("DashboardPage", u"Start", None))
        self.tool_1_start_pushButton.setText(QCoreApplication.translate("DashboardPage", u"Start", None))
        self.network_version_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.tools_service_label.setText(QCoreApplication.translate("DashboardPage", u"Tools", None))
        self.tool_2_start_pushButton.setText(QCoreApplication.translate("DashboardPage", u"Start", None))
        self.tool_type_2_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.language_start_pushButton.setText(QCoreApplication.translate("DashboardPage", u"Start", None))
        self.network_start_pushButton.setText(QCoreApplication.translate("DashboardPage", u"Start", None))
        self.network_type_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.language_type_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.database_service_label.setText(QCoreApplication.translate("DashboardPage", u"Database", None))
        self.webserver_version_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.database_type_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.tool_version_2_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.language_service_label.setText(QCoreApplication.translate("DashboardPage", u"Language", None))
        self.webserver_service_label.setText(QCoreApplication.translate("DashboardPage", u"Webserver", None))
        self.tool_type_1_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.tool_version_1_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.webserver_type_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.tool_version_3_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
        self.database_version_label.setText(QCoreApplication.translate("DashboardPage", u"TextLabel", None))
    # retranslateUi

