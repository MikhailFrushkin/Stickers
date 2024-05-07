import asyncio
import shutil
import threading
from pathlib import Path

import qdarkstyle
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QProgressBar, QFileDialog, QMessageBox
from loguru import logger

from Gui.main_window import Ui_MainWindow
from Gui.settings import Ui_Form
from config import config_prog, Config
from create_folders import create_folder_order, create_order_shk, create_bad_arts, upload_file
from db import db, Article, Orders, NotFoundArt
from read_order import read_excel_file
from update.search_stickers import main_search_sticker
from update.upadate_db import update_db_in_folder
from update.update import main_download_site


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.version = 2
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
        self.action_7.triggered.connect(self.update_db)

        # Ивенты на кнопки
        self.pushButton.clicked.connect(self.start_update_thread)
        self.pushButton_3.clicked.connect(self.evt_btn_open_file_clicked)
        self.pushButton_4.clicked.connect(self.evt_btn_create_files)
        self.pushButton_5.clicked.connect(self.evt_btn_create_shk)

        try:
            if config_prog.params.get('Автоматическое обновление'):
                self.update_timer = QTimer(self)
                self.update_timer.timeout.connect(self.start_update_thread)
                period = int(config_prog.params.get('Частота обновления', 120))
                self.update_timer.start(period * 60 * 1000)
        except Exception as ex:
            logger.error(ex)

        self.update_thread = UpdateDatabaseThread(parent=self)
        self.update_thread.progress_updated.connect(self.update_progress)
        self.update_thread.update_progress_message.connect(self.update_status_message)

    def update_db(self):
        try:
            update_db_in_folder(config_prog)
        except Exception as ex:
            logger.error(ex)

    def start_update_thread(self):
        # Останавливаем таймер, чтобы избежать параллельных запусков
        self.update_timer.stop()
        self.update_thread.start()
        # После завершения обновления снова запускаем таймер
        self.update_thread.finished.connect(self.update_timer.start)

    def stop_update_thread(self):
        self.update_timer.stop()

    def update_progress(self, current_value, total_value):
        progress = int(current_value / total_value * 100)
        self.progress_bar.setValue(progress)

    def setting_dialog(self):
        # Создаем диалоговое окно настроек
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Form()
        self.ui.setupUi(self.dialog)

        config = Config()
        params = config.params

        ui = self.ui
        ui.checkBox.setChecked(params.get("Автоматическое обновление", False))
        ui.checkBox_2.setChecked(params.get('categories', {}).get("Значки", False))
        ui.checkBox_4.setChecked(params.get('categories', {}).get("Попсокеты", False))
        ui.checkBox_5.setChecked(params.get('categories', {}).get("Зеркальца", False))
        ui.checkBox_3.setChecked(params.get('categories', {}).get("Постеры", False))
        ui.checkBox_6.setChecked(params.get('categories', {}).get("Кружки", False))
        ui.checkBox_8.setChecked(params.get('categories', {}).get("3D наклейки", False))
        ui.checkBox_7.setChecked(params.get('categories', {}).get("Наклейки на карту", False))
        ui.checkBox_10.setChecked(params.get('categories', {}).get("Брелки", False))
        ui.checkBox_9.setChecked(params.get('categories', {}).get("Наклейки квадратные", False))
        ui.checkBox_11.setChecked(params.get('categories', {}).get("Кружки-сердечко", False))
        ui.checkBox_12.setChecked(params.get('categories', {}).get("Попсокеты ДП", False))
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
            checkBox_12 = ui.checkBox_12.isChecked()
            update_frequency = int(ui.LineEdit.text())
            base_path = os.path.abspath(ui.LineEdit_2.text())
            sh_path = os.path.abspath(ui.LineEdit_3.text())
            token = ui.LineEdit_4.text()

            # Сохраняем настройки в конфигурационный файл
            config_prog.set_param("Автоматическое обновление", auto_update)
            config_prog.set_param("Значки", icons)
            config_prog.set_param("Попсокеты", popsockets)
            config_prog.set_param("Попсокеты ДП", checkBox_12)
            config_prog.set_param("Зеркальца", mirrors)
            config_prog.set_param("Постеры", posters)
            config_prog.set_param("Кружки", mugs)
            config_prog.set_param("3D наклейки", stickers_3d)
            config_prog.set_param("Наклейки на карту", map_stickers)
            config_prog.set_param("Брелки", keychains)
            config_prog.set_param("Наклейки квадратные", square_stickers)
            config_prog.set_param("Кружки-сердечко", heart_mugs)
            config_prog.set_param("Частота обновления", update_frequency)
            config_prog.set_param("Путь к базе", base_path)
            config_prog.set_param("Путь к шк", sh_path)
            config_prog.set_param("token", token)
            self.dialog.accept()
            config_prog.reload_settings()
        except Exception as ex:
            logger.error(ex)

    def update_status_message(self, text, current_value, total_value):
        proc = round(current_value / total_value * 100, 2)
        message = f'{text}: {proc}%'
        self.status_message.setText(message)

    def evt_btn_open_file_clicked(self):
        """Ивент на кнопку загрузить файл"""

        def get_download_path():
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
                create_bad_arts(self.not_found_arts, self.name_doc, self.version)
                try:
                    for file in os.listdir(os.path.join(config_prog.current_dir, 'Заказ')):
                        if file.startswith('Не найд'):
                            upload_file(os.path.join(config_prog.current_dir, 'Заказ', file))
                except Exception as ex:
                    logger.error(ex)

            except Exception as ex:
                logger.error(ex)

        filename = self.lineEdit.text()
        categories_dict = {}

        if filename:
            count_arts, count_images, stickers_count, popsocket_count = 0, 0, 0, 0
            if self.found_articles:
                try:
                    count_images, categories_dict = (
                        create_folder_order(self.found_articles, self.name_doc))
                except Exception as ex:
                    logger.error(ex)
            else:
                QMessageBox.warning(self, 'Ой', 'Ничего не найдено')

            if self.not_found_arts:
                # Запускаем функцию во втором потоке
                thread = threading.Thread(target=bad_arts_fix)
                thread.start()

            mess = f'\nАртикулов: {len(self.found_articles)}\nИзображений: {count_images}\n'
            for cat, value in categories_dict.items():
                if value['arts']:
                    mess += f'\n{cat}: {len(value["arts"])}'
                    shutil.copy2(os.path.join(config_prog.current_dir, 'Шаблоны', f'Шаблон {cat}.cdr'),
                                 os.path.join(config_prog.current_dir, 'Заказ'))

            QMessageBox.information(self, 'Завершено!', mess)

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
                    not_found_stickers = create_order_shk(self.arts, self.name_doc)
                except PermissionError as ex:
                    logger.error('Нужно закрыть документ')
                except Exception as ex:
                    logger.error(ex)
                else:
                    if not_found_stickers:
                        not_text = '\n'.join(not_found_stickers)
                        QMessageBox.information(self, '=(', f'Не найдены Шк для:\n{not_text}')

                    else:
                        QMessageBox.information(self, 'Ура!', f'Завершено!')
                    try:
                        path = os.path.join(config_prog.current_dir, 'Заказ')
                        os.startfile(path)
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
    def __init__(self, parent=None):
        super().__init__(parent)

    progress_updated = pyqtSignal(int, int)
    update_progress_message = pyqtSignal(str, int, int)

    def run(self):
        check_group = config_prog.params[
            'categories'
        ]
        self.progress_updated.emit(0, 100)
        self.update_progress_message.emit('Обновление', 0, 100)

        categories_list = []
        if check_group['3D наклейки']:
            categories_list.append(('Наклейки 3-D', None))
        if check_group['Наклейки квадратные']:
            categories_list.append(('Наклейки квадратные', None))
        if check_group['Наклейки на карту']:
            categories_list.append(('Наклейки на карту', None))
        if check_group['Попсокеты ДП']:
            categories_list.append(('Попсокеты', 'Дочке понравилось'))

        if categories_list:
            for item in categories_list:
                try:
                    main_download_site(category=item[0], config=config_prog, self=self, brand_request=item[1])
                except Exception as ex:
                    logger.error(ex)

        self.progress_updated.emit(100, 100)
        self.update_progress_message.emit('Обновление', 100, 100)

        # Обновление шк
        # try:
        #     self.progress_updated.emit(0, 100)
        #     self.update_progress_message.emit('Поиск шк', 0, 100)
        #     loop = asyncio.new_event_loop()
        #     asyncio.set_event_loop(loop)
        #     try:
        #         logger.debug('Поиск шк на яндекс диске')
        #         main_search_sticker(config_prog)
        #     except Exception as ex:
        #         logger.error(ex)
        #     self.progress_updated.emit(100, 100)
        #     self.update_progress_message.emit('Поиск шк', 100, 100)
        # except Exception as ex:
        #     logger.error(ex)
        #
        try:
            self.progress_updated.emit(0, 100)
            self.update_progress_message.emit('Поиск шк на CRM', 0, 100)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                logger.debug('Поиск шк на диск CRM')
                main_search_sticker(config_prog, folder_path='/Новая база (1)')
            except Exception as ex:
                logger.error(ex)
            self.progress_updated.emit(100, 100)
            self.update_progress_message.emit('Поиск шк на CRM', 100, 100)
        except Exception as ex:
            logger.error(ex)

        if self.parent():
            self.parent().start_update_thread()


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
