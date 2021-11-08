import os
from interface import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from cv_detection import Analyzer


class Interface(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Interface, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.files = []
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle('Track membrane analyzing')
        self.ui.action.setShortcut('Ctrl+O')
        self.ui.action.triggered.connect(self.open_files)
        self.ui.analyzeBtn.clicked.connect(self.analyze)
        self.ui.PlotLabel.setText('Тут будет диаграмма распределения диаметров!')
        self.setStyleSheet('''QPushButton {
                                border: 1px solid black;
                                border-radius: 7px;
                                background-color: ghostwhite;
                            }
                            QLineEdit {
                                border: 1px solid black;
                                border-radius: 5px;
                            }''')
        self.show()

    def open_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Выберите картинку:', './',
                                                          "Image (*.png *.jpg *.jpeg *.jfif")
        for i in files:
            if i not in self.files:
                self.files.append(i)
        text = ['<html><b>Вы открыли файлы:</b></html>', *self.files]
        self.ui.diameterText.setText('<br>'.join(text))

    def analyze(self):
        for file in os.listdir('results/correct'):
            os.remove(f'results/correct/{file}')
        for file in os.listdir('results/wrong'):
            os.remove(f'results/wrong/{file}')
        for file in os.listdir('results/not_a_hole'):
            os.remove(f'results/not_a_hole/{file}')
        analyzer = Analyzer(self.files)
        analyzer.detect_holes()
        holes_number, results = analyzer.sort_holes()
        text = ['<html><b>РЕЗУЛЬТАТЫ</b></html>']
        for i in results:
            text.append(f'Для <b>{i[0]}</b>:')
            text.extend([f'Правильные: {i[1]["correct"]}', f'Ошибочные: {i[1]["wrong"]}',
                         f'Не распознаны: {i[1]["not_a_hole"]}'])
        text.append('Таблица диаметров -- <b>results/diameters.xlsx!</b>')
        self.ui.diameterText.setText('<br>'.join(text))
        self.ui.PlotLabel.setPixmap(QtGui.QPixmap('results/plot.png'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_app = Interface()
    sys.exit(app.exec())
