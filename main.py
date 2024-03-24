from pathlib import Path

import qdarkstyle
from PyQt6 import QtCore, QtGui, QtWidgets
from loguru import logger

from config import Config
from settings import Ui_Form


class ProgressBar:
    def __init__(self, total, progress_bar, current=0):
        self.current = current
        self.total = total
        self.progress_bar = progress_bar

    def update_progress(self):
        self.current += 1
        self.progress_bar.update_progress(self.current, self.total)

    def __str__(self):
        return str(self.current)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(604, 734)

        font_button = QtGui.QFont()
        font_button.setFamily("Times New Roman")
        font_button.setPointSize(15)
        font_button.setBold(True)
        font_button.setItalic(False)
        font_button.setWeight(75)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)

        self.pushButton.setFont(font_button)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)

        self.pushButton_2.setFont(font_button)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setFrame(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.centralwidget)

        self.pushButton_3.setFont(font_button)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setMouseTracking(False)
        self.tableWidget.setTabletTracking(False)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)

        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(75)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(10)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tableWidget)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setHorizontalSpacing(20)
        self.gridLayout_2.setVerticalSpacing(7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.centralwidget)

        self.pushButton_5.setFont(font_button)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 0, 3, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.centralwidget)

        self.pushButton_4.setFont(font_button)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 604, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(parent=self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menuBar)
        self.action = QtGui.QAction(parent=MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(parent=MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(parent=MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtGui.QAction(parent=MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtGui.QAction(parent=MainWindow)
        self.action_5.setObjectName("action_5")
        self.action_6 = QtGui.QAction(parent=MainWindow)
        self.action_6.setObjectName("action_6")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu_2.addAction(self.action_3)
        self.menu_2.addAction(self.action_4)
        self.menu_3.addAction(self.action_6)
        self.menu_3.addAction(self.action_5)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_3.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Печать"))
        self.pushButton.setText(_translate("MainWindow", "Обновить базу"))
        self.pushButton_2.setText(_translate("MainWindow", "Статистика"))
        self.pushButton_3.setText(_translate("MainWindow", "Загрузить файл"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "#"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Кол-во"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Статус"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Артикул"))
        self.pushButton_5.setText(_translate("MainWindow", "Создать файл ШК"))
        self.pushButton_4.setText(_translate("MainWindow", "Создать файлы"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Справка"))
        self.menu_3.setTitle(_translate("MainWindow", "Правка"))
        self.action.setText(_translate("MainWindow", "Настройки"))
        self.action_2.setText(_translate("MainWindow", "Выход"))
        self.action_3.setText(_translate("MainWindow", "Написать администратору"))
        self.action_4.setText(_translate("MainWindow", "О программе"))
        self.action_5.setText(_translate("MainWindow", "Удалить артикул"))
        self.action_6.setText(_translate("MainWindow", "Создать артикул"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.version = 0.1
        self.current_dir = Path.cwd()

        # Создаем и добавляем действие для меню
        self.action.triggered.connect(self.setting_dialog)
        self.action_2.triggered.connect(self.close)

    def setting_dialog(self, s):
        # Создаем диалоговое окно настроек
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Form()
        self.ui.setupUi(self.dialog)

        config = Config()
        params = config.params

        ui = self.ui
        ui.checkBox.setChecked(params.get("Автоматическое обновление", False))
        ui.checkBox_2.setChecked(params.get("Значки", False))
        ui.checkBox_4.setChecked(params.get("Попсокеты", False))
        ui.checkBox_5.setChecked(params.get("Зеркальца", False))
        ui.checkBox_3.setChecked(params.get("Постеры", False))
        ui.checkBox_6.setChecked(params.get("Кружки", False))
        ui.checkBox_8.setChecked(params.get("3D наклейки", False))
        ui.checkBox_7.setChecked(params.get("Наклейки на карту", False))
        ui.checkBox_10.setChecked(params.get("Брелки", False))
        ui.checkBox_9.setChecked(params.get("Квадратные наклейки", False))
        ui.checkBox_11.setChecked(params.get("Кружки-сердечко", False))
        ui.LineEdit.setText(str(params.get("Частота обновления", 120)))

        self.ui.pushButton.clicked.connect(self.save_settings)  # Привязываем сохранение к кнопке "Сохранить"
        self.ui.pushButton_2.clicked.connect(self.dialog.close)  # Привязываем закрытие к кнопке "Выход"
        self.dialog.exec()

    def save_settings(self):
        try:
            # Получаем экземпляр класса Ui_Form из диалогового окна
            ui = self.ui

            # Получаем текущие значения настроек из виджетов диалогового окна
            auto_update = ui.checkBox.isChecked()
            icons = ui.checkBox_2.isChecked()
            popsockets = ui.checkBox_4.isChecked()
            mirrors = ui.checkBox_5.isChecked()
            posters = ui.checkBox_3.isChecked()
            mugs = ui.checkBox_6.isChecked()
            stickers_3d = ui.checkBox_8.isChecked()
            map_stickers = ui.checkBox_7.isChecked()
            keychains = ui.checkBox_10.isChecked()
            square_stickers = ui.checkBox_9.isChecked()
            heart_mugs = ui.checkBox_11.isChecked()
            update_frequency = int(ui.LineEdit.text())

            # Сохраняем настройки в конфигурационный файл
            config = Config()
            config.set_param("Автоматическое обновление", auto_update)
            config.set_param("Значки", icons)
            config.set_param("Попсокеты", popsockets)
            config.set_param("Зеркальца", mirrors)
            config.set_param("Постеры", posters)
            config.set_param("Кружки", mugs)
            config.set_param("3D наклейки", stickers_3d)
            config.set_param("Наклейки на карту", map_stickers)
            config.set_param("Брелки", keychains)
            config.set_param("Квадратные наклейки", square_stickers)
            config.set_param("Кружки-сердечко", heart_mugs)
            config.set_param("Частота обновления", update_frequency)
            self.dialog.accept()
        except Exception as ex:
            logger.error(ex)


if __name__ == '__main__':
    import sys
    import os

    directories = ['files', 'logs']
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)

    logger.add(
        "logs/logs.log",
        rotation="20 MB",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file!s} | {line} | {message}"
    )

    config = Config()
    print("Текущие параметры конфигурации:")
    print(config.params)
    config.set_param("Автоматическое обновление", True)
    print("\nОбновленные параметры конфигурации:")
    print(config.params)

    os.environ['QT_API'] = 'pyqt6'
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = MainWindow()
    w.show()

    sys.exit(app.exec())
