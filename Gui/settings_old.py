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
        self.Label = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Label.setFont(font)
        self.Label.setObjectName("Label")
        self.verticalLayout_4.addWidget(self.Label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox = QtWidgets.QCheckBox(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_2 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy)
        self.checkBox_2.setSizeIncrement(QtCore.QSize(0, 10))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setTabletTracking(False)
        self.checkBox_2.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        self.checkBox_2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.checkBox_2.setAcceptDrops(False)
        self.checkBox_2.setStyleSheet("QCheckBox {\n"
                                      "    padding-left:20px;\n"
                                      "}")
        self.checkBox_2.setShortcut("")
        self.checkBox_2.setChecked(False)
        self.checkBox_2.setAutoRepeat(False)
        self.checkBox_2.setAutoExclusive(False)
        self.checkBox_2.setTristate(False)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_3.addWidget(self.checkBox_2)
        self.checkBox_4 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_4.sizePolicy().hasHeightForWidth())
        self.checkBox_4.setSizePolicy(sizePolicy)
        self.checkBox_4.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setTabletTracking(False)
        self.checkBox_4.setStyleSheet("QCheckBox {\n"
                                      "    padding-left:20px;\n"
                                      "}")
        self.checkBox_4.setShortcut("")
        self.checkBox_4.setChecked(False)
        self.checkBox_4.setAutoRepeat(False)
        self.checkBox_4.setAutoExclusive(False)
        self.checkBox_4.setTristate(False)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_3.addWidget(self.checkBox_4)
        self.checkBox_5 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_5.sizePolicy().hasHeightForWidth())
        self.checkBox_5.setSizePolicy(sizePolicy)
        self.checkBox_5.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setTabletTracking(False)
        self.checkBox_5.setStyleSheet("QCheckBox {\n"
                                      "    padding-left:20px;\n"
                                      "}")
        self.checkBox_5.setShortcut("")
        self.checkBox_5.setChecked(False)
        self.checkBox_5.setAutoRepeat(False)
        self.checkBox_5.setAutoExclusive(False)
        self.checkBox_5.setTristate(False)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_3.addWidget(self.checkBox_5)
        self.checkBox_3 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_3.sizePolicy().hasHeightForWidth())
        self.checkBox_3.setSizePolicy(sizePolicy)
        self.checkBox_3.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setTabletTracking(False)
        self.checkBox_3.setStyleSheet("QCheckBox {\n"
                                      "    padding-left:20px;\n"
                                      "}")
        self.checkBox_3.setShortcut("")
        self.checkBox_3.setChecked(False)
        self.checkBox_3.setAutoRepeat(False)
        self.checkBox_3.setAutoExclusive(False)
        self.checkBox_3.setTristate(False)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_3.addWidget(self.checkBox_3)
        self.checkBox_6 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_6.sizePolicy().hasHeightForWidth())
        self.checkBox_6.setSizePolicy(sizePolicy)
        self.checkBox_6.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_6.setFont(font)
        self.checkBox_6.setTabletTracking(False)
        self.checkBox_6.setStyleSheet("QCheckBox {\n"
                                      "    padding-left:20px;\n"
                                      "}")
        self.checkBox_6.setShortcut("")
        self.checkBox_6.setChecked(False)
        self.checkBox_6.setAutoRepeat(False)
        self.checkBox_6.setAutoExclusive(False)
        self.checkBox_6.setTristate(False)
        self.checkBox_6.setObjectName("checkBox_6")
        self.verticalLayout_3.addWidget(self.checkBox_6)
        self.checkBox_11 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_11.sizePolicy().hasHeightForWidth())
        self.checkBox_11.setSizePolicy(sizePolicy)
        self.checkBox_11.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_11.setFont(font)
        self.checkBox_11.setTabletTracking(False)
        self.checkBox_11.setStyleSheet("QCheckBox {\n"
                                       "    padding-left:20px;\n"
                                       "}\n"
                                       "")
        self.checkBox_11.setShortcut("")
        self.checkBox_11.setChecked(False)
        self.checkBox_11.setAutoRepeat(False)
        self.checkBox_11.setAutoExclusive(False)
        self.checkBox_11.setTristate(False)
        self.checkBox_11.setObjectName("checkBox_11")
        self.verticalLayout_3.addWidget(self.checkBox_11)
        self.checkBox_8 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_8.sizePolicy().hasHeightForWidth())
        self.checkBox_8.setSizePolicy(sizePolicy)
        self.checkBox_8.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_8.setFont(font)
        self.checkBox_8.setTabletTracking(False)
        self.checkBox_8.setStyleSheet("QCheckBox {\n"
                                      "    padding-left:20px;\n"
                                      "}")
        self.checkBox_8.setShortcut("")
        self.checkBox_8.setChecked(False)
        self.checkBox_8.setAutoRepeat(False)
        self.checkBox_8.setAutoExclusive(False)
        self.checkBox_8.setTristate(False)
        self.checkBox_8.setObjectName("checkBox_8")
        self.verticalLayout_3.addWidget(self.checkBox_8)
        self.checkBox_7 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_7.sizePolicy().hasHeightForWidth())
        self.checkBox_7.setSizePolicy(sizePolicy)
        self.checkBox_7.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_7.setFont(font)
        self.checkBox_7.setTabletTracking(False)
        self.checkBox_7.setStyleSheet("QCheckBox {\n"
                                      "    padding-left:20px;\n"
                                      "}")
        self.checkBox_7.setShortcut("")
        self.checkBox_7.setChecked(False)
        self.checkBox_7.setAutoRepeat(False)
        self.checkBox_7.setAutoExclusive(False)
        self.checkBox_7.setTristate(False)
        self.checkBox_7.setObjectName("checkBox_7")
        self.verticalLayout_3.addWidget(self.checkBox_7)
        self.checkBox_9 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_9.sizePolicy().hasHeightForWidth())
        self.checkBox_9.setSizePolicy(sizePolicy)
        self.checkBox_9.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_9.setFont(font)
        self.checkBox_9.setTabletTracking(False)
        self.checkBox_9.setStyleSheet("QCheckBox {\n"
                                      "    padding-left:20px;\n"
                                      "}")
        self.checkBox_9.setShortcut("")
        self.checkBox_9.setChecked(False)
        self.checkBox_9.setAutoRepeat(False)
        self.checkBox_9.setAutoExclusive(False)
        self.checkBox_9.setTristate(False)
        self.checkBox_9.setObjectName("checkBox_9")
        self.verticalLayout_3.addWidget(self.checkBox_9)
        self.checkBox_10 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_10.sizePolicy().hasHeightForWidth())
        self.checkBox_10.setSizePolicy(sizePolicy)
        self.checkBox_10.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_10.setFont(font)
        self.checkBox_10.setTabletTracking(False)
        self.checkBox_10.setStyleSheet("QCheckBox {\n"
                                       "    padding-left:20px;\n"
                                       "}")
        self.checkBox_10.setShortcut("")
        self.checkBox_10.setChecked(False)
        self.checkBox_10.setAutoRepeat(False)
        self.checkBox_10.setAutoExclusive(False)
        self.checkBox_10.setTristate(False)
        self.checkBox_10.setObjectName("checkBox_10")
        self.verticalLayout_3.addWidget(self.checkBox_10)

        self.checkBox_12 = QtWidgets.QCheckBox(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_12.sizePolicy().hasHeightForWidth())
        self.checkBox_12.setSizePolicy(sizePolicy)
        self.checkBox_12.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_12.setFont(font)
        self.checkBox_12.setTabletTracking(False)
        self.checkBox_12.setStyleSheet("QCheckBox {\n"
                                       "    padding-left:20px;\n"
                                       "}")
        self.checkBox_12.setShortcut("")
        self.checkBox_12.setChecked(False)
        self.checkBox_12.setAutoRepeat(False)
        self.checkBox_12.setAutoExclusive(False)
        self.checkBox_12.setTristate(False)
        self.checkBox_12.setObjectName("checkBox_10")
        self.verticalLayout_3.addWidget(self.checkBox_12)


        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
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
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_3.setFont(font)
        self.Label_3.setObjectName("Label_3")
        self.verticalLayout.addWidget(self.Label_3)
        self.Label_4 = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_4.setFont(font)
        self.Label_4.setObjectName("Label_4")
        self.verticalLayout.addWidget(self.Label_4)
        self.Label_5 = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label_5.setFont(font)
        self.Label_5.setObjectName("Label_5")
        self.verticalLayout.addWidget(self.Label_5)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.LineEdit = QtWidgets.QLineEdit(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LineEdit.setFont(font)
        self.LineEdit.setText("")
        self.LineEdit.setObjectName("LineEdit")
        self.verticalLayout_2.addWidget(self.LineEdit)
        self.LineEdit_2 = QtWidgets.QLineEdit(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LineEdit_2.setFont(font)
        self.LineEdit_2.setText("")
        self.LineEdit_2.setObjectName("LineEdit_2")
        self.verticalLayout_2.addWidget(self.LineEdit_2)
        self.LineEdit_3 = QtWidgets.QLineEdit(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LineEdit_3.setFont(font)
        self.LineEdit_3.setText("")
        self.LineEdit_3.setObjectName("LineEdit_3")
        self.verticalLayout_2.addWidget(self.LineEdit_3)
        self.LineEdit_4 = QtWidgets.QLineEdit(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LineEdit_4.setFont(font)
        self.LineEdit_4.setText("")
        self.LineEdit_4.setObjectName("LineEdit_4")
        self.verticalLayout_2.addWidget(self.LineEdit_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Настройки"))
        self.Label.setText(_translate("Form", "Настройка обновления:"))
        self.checkBox.setText(_translate("Form", "Автоматичесчкое обновление"))
        self.checkBox_2.setText(_translate("Form", "Значки", "0"))
        self.checkBox_4.setText(_translate("Form", "Попсокеты", "0"))
        self.checkBox_5.setText(_translate("Form", "Зеркальца", "0"))
        self.checkBox_3.setText(_translate("Form", "Постеры", "0"))
        self.checkBox_6.setText(_translate("Form", "Кружки", "0"))
        self.checkBox_11.setText(_translate("Form", "Кружки-сердечко", "0"))
        self.checkBox_8.setText(_translate("Form", "3D наклейки", "0"))
        self.checkBox_7.setText(_translate("Form", "Наклейки на карту", "0"))
        self.checkBox_9.setText(_translate("Form", "Наклейки квадратные", "0"))
        self.checkBox_10.setText(_translate("Form", "Брелки", "0"))
        self.checkBox_12.setText(_translate("Form", "Попсокеты ДП", "0"))
        self.Label_2.setText(_translate("Form", "Частота обновления (мин.)"))
        self.Label_3.setText(_translate("Form", "Путь к базе"))
        self.Label_4.setText(_translate("Form", "Путь к ШК"))
        self.Label_5.setText(_translate("Form", "Api token"))
        self.pushButton.setText(_translate("Form", "Сохранить"))
        self.pushButton_2.setText(_translate("Form", "Выход"))
