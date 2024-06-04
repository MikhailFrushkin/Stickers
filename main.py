import asyncio
import shutil
import threading
from pathlib import Path
from pprint import pprint

import qdarkstyle
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, QStringListModel
from PyQt6.QtWidgets import QProgressBar, QFileDialog, QMessageBox
from loguru import logger

from Gui.delete_art import DeleteArticleDialog
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
        self.version = 4.1
        self.name_doc = ''
        self.current_dir = Path.cwd()
        self.found_articles = []
        self.not_found_arts = []
        self.arts = []

        self.list_model = QStringListModel()
        self.listView.setModel(self.list_model)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 10, 100, 25)
        self.progress_bar.setMaximum(100)
        self.statusbar.addWidget(self.progress_bar, 1)

        self.status_message = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.status_message)

        # Создаем и добавляем действие для меню
        self.action.triggered.connect(self.setting_dialog)
        self.action_2.triggered.connect(self.close)
        self.action_5.triggered.connect(self.open_delete_article_dialog)
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

    def open_delete_article_dialog(self):
        dialog = DeleteArticleDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            art = dialog.line_edit.text()
            if Article.delete_by_art(art):
                QMessageBox.information(self, 'ВЫполнено!', 'Удаление выполнено!')
            else:
                QMessageBox.warning(self, 'Ошибка!', 'Ошибка удаления, проверте артикул!')

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
        try:
            self.dialog = QtWidgets.QDialog()
            self.ui = Ui_Form()
            self.ui.setupUi(self.dialog)

            config = Config()
            params = config.params

            ui = self.ui

            # Assign values to checkboxes based on config
            for text in self.ui.checkBox_texts:
                checkbox = self.dialog.findChild(QtWidgets.QCheckBox, f"checkBox_{self.ui.checkBox_texts.index(text)}")
                if text == "Автоматическое обновление":
                    checkbox.setChecked(params.get(text, False))
                else:
                    checkbox.setChecked(params.get('categories', {}).get(text, False))

            # Assign values to LineEdit fields based on config
            ui.LineEdit.setText(str(params.get("Частота обновления", 120)))
            ui.LineEdit_2.setText(str(params.get("Путь к базе", "C:\\База")))
            ui.LineEdit_3.setText(str(params.get("Путь к шк", "C:\\База\\ШК")))
            ui.LineEdit_4.setText(str(params.get("token", "")))
            ui.LineEdit_5.setText(str(params.get("machin_name", "")))

            ui.pushButton.clicked.connect(self.save_settings)  # Привязываем сохранение к кнопке "Сохранить"
            ui.pushButton_2.clicked.connect(self.dialog.close)  # Привязываем закрытие к кнопке "Выход"
            self.dialog.exec()
        except Exception as ex:
            logger.error(ex)

    def save_settings(self):
        try:
            ui = self.ui

            checkbox_states = {}

            for text in ui.checkBox_texts:
                checkbox = self.dialog.findChild(QtWidgets.QCheckBox, f"checkBox_{ui.checkBox_texts.index(text)}")
                checkbox_states[text] = checkbox.isChecked()

            # Fetch other settings from the UI widgets
            update_frequency = int(ui.LineEdit.text())
            base_path = os.path.abspath(ui.LineEdit_2.text())
            sh_path = os.path.abspath(ui.LineEdit_3.text())
            token = ui.LineEdit_4.text()
            machin_name = ui.LineEdit_5.text()

            # Save settings to the configuration file
            for key, value in checkbox_states.items():
                config_prog.set_param(key, value)
            config_prog.set_param("Частота обновления", update_frequency)
            config_prog.set_param("Путь к базе", base_path)
            config_prog.set_param("Путь к шк", sh_path)
            config_prog.set_param("token", token)
            config_prog.set_param("machin_name", machin_name)

            # Accept the dialog and reload settings
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
                            [str(quantity), "✅" if found else "❌", art]):
                        item = QtWidgets.QTableWidgetItem(text)
                        if col == 2:  # Если текущий столбец - это столбец "Артикул"
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
                    for file in os.listdir(os.path.join(config_prog.current_dir, 'logs')):
                        upload_file(os.path.join(config_prog.current_dir, 'logs', file), savefile_dir='Логи')
                except Exception as ex:
                    logger.error(ex)

            except Exception as ex:
                logger.error(ex)

        filename = self.lineEdit.text()
        categories_dict = {}

        if filename:
            self.add_to_list_view(self.name_doc)
            count_arts, count_images = 0, 0
            if self.found_articles:
                try:
                    count_images, categories_dict = (
                        create_folder_order(self.found_articles, self.name_doc, self.list_model,
                                            self.progress_bar))
                except Exception as ex:
                    logger.error(ex)
            else:
                QMessageBox.warning(self, 'Ой', 'Ничего не найдено')

            thread = threading.Thread(target=bad_arts_fix)
            thread.start()

            mess = f'\nАртикулов: {len(self.found_articles)}\nИзображений: {count_images}\n'
            for cat, value in categories_dict.items():
                if value['arts']:
                    arts = value["arts"]
                    total_quantity = sum(article.quantity for article in arts)
                    mess += f'\n{cat}\nАртикулов: {len(arts)}\tкол-во: {total_quantity if cat != "Зеркальца" else total_quantity * 2}\n'
                    if (cat != 'Брелки' and cat != 'Зеркальца' and cat != 'Попсокеты' and cat != 'Мини постеры'
                            and cat != 'Постеры' and cat != 'Маски' and cat != 'Кружки'):
                        try:
                            shutil.copy2(os.path.join(config_prog.current_dir, 'Шаблоны', f'Шаблон {cat}.cdr'),
                                         os.path.join(config_prog.current_dir, 'Заказ'))
                        except Exception as ex:
                            logger.error(ex)
                            QMessageBox.warning(self, 'Ошибка!', 'Возможно файл открыт')
            QMessageBox.information(self, 'Завершено!', mess)

            self.add_to_list_view(mess)

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

    def add_to_list_view(self, text):
        if text:
            display = self.list_model.stringList()
            display.append(text)
            self.list_model.setStringList(display)

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
        self.progress_updated.emit(0, 100)
        self.update_progress_message.emit('Обновление', 0, 100)

        check_group = config_prog.params[
            'categories'
        ]
        download_union_list = False
        categories_list = []
        if check_group['3D наклейки']:
            categories_list.append('Наклейки 3-D')
        if check_group['Наклейки квадратные']:
            categories_list.append('Наклейки квадратные')
        if check_group['Наклейки на карту']:
            categories_list.append('Наклейки на карту')
        if check_group['Попсокеты']:
            categories_list.append('Попсокеты')
        if check_group['Брелки']:
            categories_list.append('Брелки')
        if check_group['Зеркальца']:
            categories_list.append('Зеркальца')
        if check_group['Мини постеры']:
            categories_list.append('Мини постеры')
        if check_group['Постеры']:
            categories_list.append('Постеры')
        if check_group['Кружки']:
            categories_list.append(['Кружки', 'Кружки-сердечко'])
        if check_group['Маски']:
            categories_list.append('Маски')
            download_union_list = True
        if categories_list:
            for item in categories_list:
                try:
                    logger.warning(f'Обновление: {item}')
                    main_download_site(category=item, config=config_prog, self=self,
                                       download_union_list=download_union_list)
                except Exception as ex:
                    logger.error(ex)

        self.progress_updated.emit(100, 100)
        self.update_progress_message.emit('Обновление', 100, 100)

        try:
            self.progress_updated.emit(0, 100)
            self.update_progress_message.emit('Поиск шк на CRM', 0, 100)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                logger.warning('Поиск шк на дискe CRM')
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
        f"logs/{config_prog.params.get('machin_name', 'Не назван комп')}.log",
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
