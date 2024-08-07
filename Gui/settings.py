# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(550, 507)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.checkBox_texts = [
            "Печать на Мимаки",
            "Автоматическое обновление",
            "Значки",
            "Попсокеты",
            "Зеркальца",
            "Постеры",
            "Кружки",
            "3D наклейки",
            "Наклейки на карту",
            "Наклейки квадратные",
            "Брелки",
            "Мини постеры",
            "Маски"
        ]

        font = QtGui.QFont()
        font.setPointSize(12)

        for row, text in enumerate(self.checkBox_texts):
            checkbox = QtWidgets.QCheckBox(text, parent=Form)
            checkbox.setFont(font)
            checkbox.setObjectName(f"checkBox_{row}")
            self.gridLayout.addWidget(checkbox, row, 0, 1, 1)

        self.verticalLayout_4.addLayout(self.gridLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.Label_2 = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_2.setFont(font)
        self.Label_2.setObjectName("Label_2")
        self.verticalLayout.addWidget(self.Label_2)

        self.Label_3 = QtWidgets.QLabel(parent=Form)
        self.Label_3.setFont(font)
        self.Label_3.setObjectName("Label_3")
        self.verticalLayout.addWidget(self.Label_3)

        self.Label_4 = QtWidgets.QLabel(parent=Form)
        self.Label_4.setFont(font)
        self.Label_4.setObjectName("Label_4")
        self.verticalLayout.addWidget(self.Label_4)

        self.Label_5 = QtWidgets.QLabel(parent=Form)
        self.Label_5.setFont(font)
        self.Label_5.setObjectName("Label_5")
        self.verticalLayout.addWidget(self.Label_5)

        self.Label_6 = QtWidgets.QLabel(parent=Form)
        self.Label_6.setFont(font)
        self.Label_6.setObjectName("Label_6")
        self.verticalLayout.addWidget(self.Label_6)

        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.LineEdit = QtWidgets.QLineEdit(parent=Form)
        self.LineEdit.setFont(font)
        self.LineEdit.setText("")
        self.LineEdit.setObjectName("LineEdit")
        self.verticalLayout_2.addWidget(self.LineEdit)

        self.LineEdit_2 = QtWidgets.QLineEdit(parent=Form)
        self.LineEdit_2.setFont(font)
        self.LineEdit_2.setText("")
        self.LineEdit_2.setObjectName("LineEdit_2")
        self.verticalLayout_2.addWidget(self.LineEdit_2)

        self.LineEdit_3 = QtWidgets.QLineEdit(parent=Form)
        self.LineEdit_3.setFont(font)
        self.LineEdit_3.setText("")
        self.LineEdit_3.setObjectName("LineEdit_3")
        self.verticalLayout_2.addWidget(self.LineEdit_3)

        self.LineEdit_4 = QtWidgets.QLineEdit(parent=Form)
        self.LineEdit_4.setFont(font)
        self.LineEdit_4.setText("")
        self.LineEdit_4.setObjectName("LineEdit_4")
        self.verticalLayout_2.addWidget(self.LineEdit_4)

        self.LineEdit_5 = QtWidgets.QLineEdit(parent=Form)
        self.LineEdit_5.setFont(font)
        self.LineEdit_5.setText("")
        self.LineEdit_5.setObjectName("LineEdit_4")
        self.verticalLayout_2.addWidget(self.LineEdit_5)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Настройки"))
        self.Label_2.setText(_translate("Form", "Частота обновления (мин.)"))
        self.Label_3.setText(_translate("Form", "Путь к базе"))
        self.Label_4.setText(_translate("Form", "Путь к ШК"))
        self.Label_5.setText(_translate("Form", "Api token"))
        self.Label_6.setText(_translate("Form", "Имя компьютера"))
        self.pushButton.setText(_translate("Form", "Сохранить"))
        self.pushButton_2.setText(_translate("Form", "Выход"))

    def get_checkbox_states(self, Form):
        # Initialize an empty dictionary to store checkbox names and their states
        checkbox_states = {}

        # Iterate through checkBox_texts list
        for text in self.checkBox_texts:
            # Find the checkbox object based on object name
            checkbox = Form.findChild(QtWidgets.QCheckBox, f"checkBox_{self.checkBox_texts.index(text)}")
            # If checkbox object is found, append its text and state to checkbox_states dictionary
            if checkbox:
                checkbox_states[checkbox.text()] = checkbox.isChecked()

        return checkbox_states


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(window)
    window.show()

    # Get checkbox states by passing the Form as an argument
    checkbox_states = ui.get_checkbox_states(window)
    app.exec()