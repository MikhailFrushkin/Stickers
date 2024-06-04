from PyQt6 import QtCore, QtGui, QtWidgets


class DeleteArticleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удалить артикул")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Введите артикул:", self)
        self.layout.addWidget(self.label)

        self.line_edit = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.line_edit)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.delete_button = QtWidgets.QPushButton("Удалить", self)
        self.delete_button.clicked.connect(self.delete_article)
        self.button_layout.addWidget(self.delete_button)

        self.cancel_button = QtWidgets.QPushButton("Отмена", self)
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

    def delete_article(self):
        article = self.line_edit.text()
        self.accept()
