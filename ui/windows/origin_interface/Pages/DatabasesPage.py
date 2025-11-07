# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DatabasesPage.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialogButtonBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_DatabasesPage(object):
    def setupUi(self, DatabasesPage):
        if not DatabasesPage.objectName():
            DatabasesPage.setObjectName(u"DatabasesPage")
        DatabasesPage.resize(760, 640)
        self.verticalLayout = QVBoxLayout(DatabasesPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.database_title_layout = QHBoxLayout()
        self.database_title_layout.setObjectName(u"database_title_layout")
        self.database_title_label = QLabel(DatabasesPage)
        self.database_title_label.setObjectName(u"database_title_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.database_title_label.sizePolicy().hasHeightForWidth())
        self.database_title_label.setSizePolicy(sizePolicy)

        self.database_title_layout.addWidget(self.database_title_label)


        self.verticalLayout.addLayout(self.database_title_layout)

        self.database_save_change_layout = QHBoxLayout()
        self.database_save_change_layout.setObjectName(u"database_save_change_layout")
        self.database_save_change_buttonBox = QDialogButtonBox(DatabasesPage)
        self.database_save_change_buttonBox.setObjectName(u"database_save_change_buttonBox")
        self.database_save_change_buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.database_save_change_layout.addWidget(self.database_save_change_buttonBox)


        self.verticalLayout.addLayout(self.database_save_change_layout)

        self.database_content_layout = QGridLayout()
        self.database_content_layout.setObjectName(u"database_content_layout")
        self.label = QLabel(DatabasesPage)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 14pt \"Segoe UI\";\n"
"align-text: center")

        self.database_content_layout.addWidget(self.label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.label_3 = QLabel(DatabasesPage)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 14pt \"Segoe UI\";")

        self.database_content_layout.addWidget(self.label_3, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.postgresql_service_dir_lineEdit = QLineEdit(DatabasesPage)
        self.postgresql_service_dir_lineEdit.setObjectName(u"postgresql_service_dir_lineEdit")

        self.horizontalLayout_5.addWidget(self.postgresql_service_dir_lineEdit)

        self.postgresql_service_dir_browseButton = QPushButton(DatabasesPage)
        self.postgresql_service_dir_browseButton.setObjectName(u"postgresql_service_dir_browseButton")

        self.horizontalLayout_5.addWidget(self.postgresql_service_dir_browseButton)


        self.database_content_layout.addLayout(self.horizontalLayout_5, 3, 3, 1, 1)

        self.mysql_version_comboBox = QComboBox(DatabasesPage)
        self.mysql_version_comboBox.setObjectName(u"mysql_version_comboBox")

        self.database_content_layout.addWidget(self.mysql_version_comboBox, 1, 1, 1, 1)

        self.mongodb_radio = QRadioButton(DatabasesPage)
        self.mongodb_radio.setObjectName(u"mongodb_radio")

        self.database_content_layout.addWidget(self.mongodb_radio, 4, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.mongodb_data_dir_lineEdit = QLineEdit(DatabasesPage)
        self.mongodb_data_dir_lineEdit.setObjectName(u"mongodb_data_dir_lineEdit")

        self.horizontalLayout_8.addWidget(self.mongodb_data_dir_lineEdit)

        self.mongodb_data_dir_browseButton = QPushButton(DatabasesPage)
        self.mongodb_data_dir_browseButton.setObjectName(u"mongodb_data_dir_browseButton")

        self.horizontalLayout_8.addWidget(self.mongodb_data_dir_browseButton)


        self.database_content_layout.addLayout(self.horizontalLayout_8, 4, 4, 1, 1)

        self.label_4 = QLabel(DatabasesPage)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"font: 14pt \"Segoe UI\";")

        self.database_content_layout.addWidget(self.label_4, 0, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.mysql_radio = QRadioButton(DatabasesPage)
        self.mysql_radio.setObjectName(u"mysql_radio")

        self.database_content_layout.addWidget(self.mysql_radio, 1, 0, 1, 1)

        self.mysql_port_lineEdit = QLineEdit(DatabasesPage)
        self.mysql_port_lineEdit.setObjectName(u"mysql_port_lineEdit")

        self.database_content_layout.addWidget(self.mysql_port_lineEdit, 1, 2, 1, 1)

        self.postgresql_radio = QRadioButton(DatabasesPage)
        self.postgresql_radio.setObjectName(u"postgresql_radio")

        self.database_content_layout.addWidget(self.postgresql_radio, 3, 0, 1, 1)

        self.mongodb_comboBox = QComboBox(DatabasesPage)
        self.mongodb_comboBox.setObjectName(u"mongodb_comboBox")

        self.database_content_layout.addWidget(self.mongodb_comboBox, 4, 1, 1, 1)

        self.label_5 = QLabel(DatabasesPage)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: 14pt \"Segoe UI\";")

        self.database_content_layout.addWidget(self.label_5, 0, 4, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.mongodb_port_lineEdit = QLineEdit(DatabasesPage)
        self.mongodb_port_lineEdit.setObjectName(u"mongodb_port_lineEdit")

        self.database_content_layout.addWidget(self.mongodb_port_lineEdit, 4, 2, 1, 1)

        self.label_2 = QLabel(DatabasesPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 14pt \"Segoe UI\";")

        self.database_content_layout.addWidget(self.label_2, 0, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.mariadb_port_lineEdit = QLineEdit(DatabasesPage)
        self.mariadb_port_lineEdit.setObjectName(u"mariadb_port_lineEdit")

        self.database_content_layout.addWidget(self.mariadb_port_lineEdit, 2, 2, 1, 1)

        self.mariadb_version_comboBox = QComboBox(DatabasesPage)
        self.mariadb_version_comboBox.setObjectName(u"mariadb_version_comboBox")

        self.database_content_layout.addWidget(self.mariadb_version_comboBox, 2, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.mariadb_service_dir_lineEdit = QLineEdit(DatabasesPage)
        self.mariadb_service_dir_lineEdit.setObjectName(u"mariadb_service_dir_lineEdit")

        self.horizontalLayout_3.addWidget(self.mariadb_service_dir_lineEdit)

        self.mariadb_service_dir_browseButton = QPushButton(DatabasesPage)
        self.mariadb_service_dir_browseButton.setObjectName(u"mariadb_service_dir_browseButton")

        self.horizontalLayout_3.addWidget(self.mariadb_service_dir_browseButton)


        self.database_content_layout.addLayout(self.horizontalLayout_3, 2, 3, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.mysql_data_dir_lineEdit = QLineEdit(DatabasesPage)
        self.mysql_data_dir_lineEdit.setObjectName(u"mysql_data_dir_lineEdit")

        self.horizontalLayout_2.addWidget(self.mysql_data_dir_lineEdit)

        self.mysql_data_dir_browseButton = QPushButton(DatabasesPage)
        self.mysql_data_dir_browseButton.setObjectName(u"mysql_data_dir_browseButton")

        self.horizontalLayout_2.addWidget(self.mysql_data_dir_browseButton)


        self.database_content_layout.addLayout(self.horizontalLayout_2, 1, 4, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.mongodb_service_dir_lineEdit = QLineEdit(DatabasesPage)
        self.mongodb_service_dir_lineEdit.setObjectName(u"mongodb_service_dir_lineEdit")

        self.horizontalLayout_7.addWidget(self.mongodb_service_dir_lineEdit)

        self.mongodb_service_dir_browseButton = QPushButton(DatabasesPage)
        self.mongodb_service_dir_browseButton.setObjectName(u"mongodb_service_dir_browseButton")

        self.horizontalLayout_7.addWidget(self.mongodb_service_dir_browseButton)


        self.database_content_layout.addLayout(self.horizontalLayout_7, 4, 3, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.mariadb_data_dir_lineEdit = QLineEdit(DatabasesPage)
        self.mariadb_data_dir_lineEdit.setObjectName(u"mariadb_data_dir_lineEdit")

        self.horizontalLayout_4.addWidget(self.mariadb_data_dir_lineEdit)

        self.mariadb_data_dir_browseButton = QPushButton(DatabasesPage)
        self.mariadb_data_dir_browseButton.setObjectName(u"mariadb_data_dir_browseButton")

        self.horizontalLayout_4.addWidget(self.mariadb_data_dir_browseButton)


        self.database_content_layout.addLayout(self.horizontalLayout_4, 2, 4, 1, 1)

        self.postgresql_version_comboBox = QComboBox(DatabasesPage)
        self.postgresql_version_comboBox.setObjectName(u"postgresql_version_comboBox")

        self.database_content_layout.addWidget(self.postgresql_version_comboBox, 3, 1, 1, 1)

        self.mariadb_radio = QRadioButton(DatabasesPage)
        self.mariadb_radio.setObjectName(u"mariadb_radio")

        self.database_content_layout.addWidget(self.mariadb_radio, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mysql_service_dir_lineEdit = QLineEdit(DatabasesPage)
        self.mysql_service_dir_lineEdit.setObjectName(u"mysql_service_dir_lineEdit")

        self.horizontalLayout.addWidget(self.mysql_service_dir_lineEdit)

        self.mysql_service_dir_browseButton = QPushButton(DatabasesPage)
        self.mysql_service_dir_browseButton.setObjectName(u"mysql_service_dir_browseButton")

        self.horizontalLayout.addWidget(self.mysql_service_dir_browseButton)


        self.database_content_layout.addLayout(self.horizontalLayout, 1, 3, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.postgresql_data_dir_lineEdit = QLineEdit(DatabasesPage)
        self.postgresql_data_dir_lineEdit.setObjectName(u"postgresql_data_dir_lineEdit")

        self.horizontalLayout_6.addWidget(self.postgresql_data_dir_lineEdit)

        self.postgresql_data_dir_browseButton = QPushButton(DatabasesPage)
        self.postgresql_data_dir_browseButton.setObjectName(u"postgresql_data_dir_browseButton")

        self.horizontalLayout_6.addWidget(self.postgresql_data_dir_browseButton)


        self.database_content_layout.addLayout(self.horizontalLayout_6, 3, 4, 1, 1)

        self.postgresql_port_lineEdit = QLineEdit(DatabasesPage)
        self.postgresql_port_lineEdit.setObjectName(u"postgresql_port_lineEdit")

        self.database_content_layout.addWidget(self.postgresql_port_lineEdit, 3, 2, 1, 1)

        self.mysql_config_pushButton = QPushButton(DatabasesPage)
        self.mysql_config_pushButton.setObjectName(u"mysql_config_pushButton")

        self.database_content_layout.addWidget(self.mysql_config_pushButton, 1, 5, 1, 1)

        self.mariadb_config_pushButton = QPushButton(DatabasesPage)
        self.mariadb_config_pushButton.setObjectName(u"mariadb_config_pushButton")

        self.database_content_layout.addWidget(self.mariadb_config_pushButton, 2, 5, 1, 1)

        self.postgresql_config_pushButton = QPushButton(DatabasesPage)
        self.postgresql_config_pushButton.setObjectName(u"postgresql_config_pushButton")

        self.database_content_layout.addWidget(self.postgresql_config_pushButton, 3, 5, 1, 1)

        self.mongodb_config_pushButton = QPushButton(DatabasesPage)
        self.mongodb_config_pushButton.setObjectName(u"mongodb_config_pushButton")

        self.database_content_layout.addWidget(self.mongodb_config_pushButton, 4, 5, 1, 1)

        self.database_content_layout.setColumnStretch(1, 1)
        self.database_content_layout.setColumnStretch(3, 2)
        self.database_content_layout.setColumnStretch(4, 2)

        self.verticalLayout.addLayout(self.database_content_layout)

        self.verticalSpacer_6 = QSpacerItem(20, 210, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.database_add_new_layout = QHBoxLayout()
        self.database_add_new_layout.setObjectName(u"database_add_new_layout")
        self.database_add_new_button = QPushButton(DatabasesPage)
        self.database_add_new_button.setObjectName(u"database_add_new_button")

        self.database_add_new_layout.addWidget(self.database_add_new_button)


        self.verticalLayout.addLayout(self.database_add_new_layout)


        self.retranslateUi(DatabasesPage)

        QMetaObject.connectSlotsByName(DatabasesPage)
    # setupUi

    def retranslateUi(self, DatabasesPage):
        DatabasesPage.setWindowTitle(QCoreApplication.translate("DatabasesPage", u"Form", None))
        self.database_title_label.setText(QCoreApplication.translate("DatabasesPage", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">Databases</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("DatabasesPage", u"Type", None))
        self.label_3.setText(QCoreApplication.translate("DatabasesPage", u"Port", None))
        self.postgresql_service_dir_browseButton.setText(QCoreApplication.translate("DatabasesPage", u"Browse", None))
        self.mongodb_radio.setText(QCoreApplication.translate("DatabasesPage", u"MongoDB", None))
        self.mongodb_data_dir_browseButton.setText(QCoreApplication.translate("DatabasesPage", u"Browse", None))
        self.label_4.setText(QCoreApplication.translate("DatabasesPage", u"Service Directory", None))
        self.mysql_radio.setText(QCoreApplication.translate("DatabasesPage", u"MySQL", None))
        self.postgresql_radio.setText(QCoreApplication.translate("DatabasesPage", u"PostgreSQL", None))
        self.label_5.setText(QCoreApplication.translate("DatabasesPage", u"Data Directory", None))
        self.label_2.setText(QCoreApplication.translate("DatabasesPage", u"Version", None))
        self.mariadb_service_dir_browseButton.setText(QCoreApplication.translate("DatabasesPage", u"Browse", None))
        self.mysql_data_dir_browseButton.setText(QCoreApplication.translate("DatabasesPage", u"Browse", None))
        self.mongodb_service_dir_browseButton.setText(QCoreApplication.translate("DatabasesPage", u"Browse", None))
        self.mariadb_data_dir_browseButton.setText(QCoreApplication.translate("DatabasesPage", u"Browse", None))
        self.mariadb_radio.setText(QCoreApplication.translate("DatabasesPage", u"MariaDB", None))
        self.mysql_service_dir_browseButton.setText(QCoreApplication.translate("DatabasesPage", u"Browse", None))
        self.postgresql_data_dir_browseButton.setText(QCoreApplication.translate("DatabasesPage", u"Browse", None))
        self.mysql_config_pushButton.setText(QCoreApplication.translate("DatabasesPage", u"Configuration", None))
        self.mariadb_config_pushButton.setText(QCoreApplication.translate("DatabasesPage", u"Configuration", None))
        self.postgresql_config_pushButton.setText(QCoreApplication.translate("DatabasesPage", u"Configuration", None))
        self.mongodb_config_pushButton.setText(QCoreApplication.translate("DatabasesPage", u"Configuration", None))
        self.database_add_new_button.setText(QCoreApplication.translate("DatabasesPage", u"Add New Databases", None))
    # retranslateUi

