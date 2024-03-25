import shutil
import threading
import winreg
from pathlib import Path

import qdarkstyle
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QProgressBar, QFileDialog, QMessageBox
from loguru import logger

from config import Config
from create_folders import create_folder_order, create_order_shk, create_bad_arts, upload_file
from db import db, Article, Orders, NotFoundArt
from read_order import read_excel_file
from settings import Ui_Form
from update import main_download_site

config_prog = Config()


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
        self.name_doc = ''
        self.current_dir = Path.cwd()
        self.found_articles = []
        self.not_found_arts = []
        self.arts = []

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 10, 100, 25)
        self.progress_bar.setMaximum(100)
        self.statusbar.addWidget(self.progress_bar, 1)

        self.status_message = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.status_message)

        # Создаем и добавляем действие для меню
        self.action.triggered.connect(self.setting_dialog)
        self.action_2.triggered.connect(self.close)

        # Ивенты на кнопки
        self.pushButton.clicked.connect(self.start_update_thread)
        self.pushButton_3.clicked.connect(self.evt_btn_open_file_clicked)
        self.pushButton_4.clicked.connect(self.evt_btn_create_files)
        self.pushButton_5.clicked.connect(self.evt_btn_create_shk)

        self.update_thread = UpdateDatabaseThread()
        self.update_thread.progress_updated.connect(self.update_progress)
        self.update_thread.update_progress_message.connect(self.update_status_message)

    def update_progress(self, current_value, total_value):
        progress = int(current_value / total_value * 100)
        self.progress_bar.setValue(progress)

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
        ui.LineEdit_2.setText(str(params.get("Путь к базе", "C:\\База")))
        ui.LineEdit_3.setText(str(params.get("Путь к шк", "C:\\База\\ШК")))
        ui.LineEdit_4.setText(str(params.get("token", "")))

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
            base_path = os.path.abspath(ui.LineEdit_2.text())
            sh_path = os.path.abspath(ui.LineEdit_3.text())
            token = ui.LineEdit_4.text()

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
            config.set_param("Путь к базе", base_path)
            config.set_param("Путь к шк", sh_path)
            config.set_param("token", token)
            self.dialog.accept()
        except Exception as ex:
            logger.error(ex)

    def start_update_thread(self):
        self.update_thread.start()

    def update_status_message(self, text, current_value, total_value):
        proc = round(current_value / total_value * 100, 3)
        message = f'{text}: {proc}%'
        self.status_message.setText(message)

    def evt_btn_open_file_clicked(self):
        """Ивент на кнопку загрузить файл"""
        def get_download_path():
            if os.name == 'nt':
                sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
                downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                    location = winreg.QueryValueEx(key, downloads_guid)[0]
                return location
            else:
                return os.path.join(os.path.expanduser('~'), 'downloads')

        try:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Загрузить файл', get_download_path(),
                                                       'CSV файлы (*.csv *.xlsx)')
        except Exception as ex:
            logger.error(ex)
            file_name, _ = QFileDialog.getOpenFileName(self, 'Загрузить файл', str(self.current_dir),
                                                       'CSV файлы (*.csv *.xlsx)')
        if file_name:
            try:
                self.lineEdit.setText(file_name)
                self.name_doc = os.path.basename(file_name)
                tuples_list, self.found_articles, self.not_found_arts, self.arts = read_excel_file(self.lineEdit.text())
                self.tableWidget.setRowCount(0)
                # Установка выравнивания и шрифта для каждой ячейки в таблице
                font = QtGui.QFont()
                font.setPointSize(12)  # Устанавливаем размер шрифта
                font.setBold(True)  # Делаем шрифт жирным
                for idx, (art, quantity, found) in enumerate(tuples_list):
                    self.tableWidget.insertRow(idx)

                    # Заполняем значениями из списка tuples_list и устанавливаем выравнивание и шрифт
                    for col, text in enumerate(
                            [str(idx + 1), str(quantity), "✅" if found else "❌", art]):
                        item = QtWidgets.QTableWidgetItem(text)
                        if col == 3:  # Если текущий столбец - это столбец "Артикул"
                            item.setTextAlignment(QtCore.Qt.AlignLeft)  # Устанавливаем выравнивание по левому краю
                        else:
                            item.setTextAlignment(
                                QtCore.Qt.AlignCenter)  # Устанавливаем выравнивание по центру для остальных столбцов
                        item.setFont(font)  # Устанавливаем шрифт
                        self.tableWidget.setItem(idx, col, item)

            except Exception as ex:
                logger.error(f'ошибка чтения xlsx {ex}')
                QMessageBox.information(self, 'Инфо', f'ошибка чтения xlsx {ex}')

    def evt_btn_create_files(self):
        """Ивент на кнопку Создать файлы"""
        def bad_arts_fix():
            try:
                create_bad_arts(self.not_found_arts, self.name_doc)
                try:
                    for file in os.listdir(os.path.join(config_prog.current_dir, 'Заказ')):
                        if file.startswith('Не найд'):
                            upload_file(os.path.join(config_prog.current_dir, 'Заказ', file))
                except Exception as ex:
                    logger.error(ex)

            except Exception as ex:
                logger.error(ex)

        filename = self.lineEdit.text()

        if filename:
            if self.found_articles:
                try:
                    count_arts, count_image = create_folder_order(self.found_articles, self.name_doc)
                except Exception as ex:
                    logger.error(ex)
            else:
                QMessageBox.warning(self, 'Ой', 'Ничего не найдено')

            if self.not_found_arts:
                # Запускаем функцию во втором потоке
                thread = threading.Thread(target=bad_arts_fix)
                thread.start()
            QMessageBox.information(self, 'Ура!', 'Завершено!')

            try:
                shutil.copy2(os.path.join(config_prog.current_dir, 'Шаблоны', 'Шаблон 3d.cdr'),
                             os.path.join(config_prog.current_dir, 'Заказ'))
            except Exception as ex:
                logger.error(ex)
            try:
                path = os.path.join(config_prog.current_dir, 'Заказ')
                os.startfile(path)
            except Exception as ex:
                logger.error(ex)
        else:
            QMessageBox.information(self, 'Инфо', 'Загрузите заказ')

    def evt_btn_create_shk(self):
        """Ивент на кнопку Создать ШК"""
        filename = self.lineEdit.text()
        if filename:
            if self.arts:
                try:
                    create_order_shk(self.arts, self.name_doc)
                except PermissionError as ex:
                    logger.error('Нужно закрыть документ')
                except Exception as ex:
                    logger.error(ex)
            else:
                QMessageBox.information(self, 'Инфо', 'Не найденны шк')
        else:
            QMessageBox.information(self, 'Инфо', 'Загрузите заказ')

    def __enter__(self):
        db.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.close()


class UpdateDatabaseThread(QThread):
    progress_updated = pyqtSignal(int, int)
    update_progress_message = pyqtSignal(str, int, int)

    def run(self):
        try:
            self.progress_updated.emit(0, 100)
            self.update_progress_message.emit('Обновление', 0, 100)
            category = 'Наклейки 3-D'
            main_download_site(category=category, config=config_prog, self=self)
            self.progress_updated.emit(100, 100)
            self.update_progress_message.emit('Обновление', 100, 100)
        except Exception as ex:
            logger.error(ex)


if __name__ == '__main__':
    import sys
    import os

    logger.add(
        "logs/logs.log",
        rotation="20 MB",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file!s} | {line} | {message}"
    )

    directories = ['files', 'logs', 'base', 'Заказ', 'Файлы связанные с заказом']
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)

    db.connect()
    db.create_tables([Article, Orders, NotFoundArt])
    db.close()

    os.environ['QT_API'] = 'pyqt6'
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = MainWindow()
    w.show()

    sys.exit(app.exec())
