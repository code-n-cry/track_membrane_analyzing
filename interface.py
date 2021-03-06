from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 714)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.analyzeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.analyzeBtn.setGeometry(QtCore.QRect(10, 10, 191, 31))
        self.analyzeBtn.setObjectName("analyzeBtn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 20, 451, 21))
        self.label.setObjectName("label")
        self.diameterText = QtWidgets.QTextEdit(self.centralwidget)
        self.diameterText.setGeometry(QtCore.QRect(10, 70, 421, 561))
        self.diameterText.setObjectName("diameterText")
        self.PlotLabel = QtWidgets.QLabel(self.centralwidget)
        self.PlotLabel.setGeometry(QtCore.QRect(540, 70, 491, 551))
        self.PlotLabel.setText("")
        self.PlotLabel.setObjectName("PlotLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 18))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.analyzeBtn.setText(_translate("MainWindow", "???????????? ????????????"))
        self.label.setText(_translate("MainWindow", "???????????????????? ?????????? ?? ?????????? \"results\"!"))
        self.diameterText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">?????????? ?????????? ???????????????????????? ????????????????????!</span></p></body></html>"))
        self.menu.setTitle(_translate("MainWindow", "??????????????..."))
        self.action.setText(_translate("MainWindow", "????????(??)"))
        self.action_2.setText(_translate("MainWindow", "??????????"))
