import os
import xlsxwriter
import numpy
from PIL import Image
from interface import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import base64
import requests
import matplotlib.pyplot as plt


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
        try:
            self.request_to_api()
        except Exception as e:
            print(e)

    def request_to_api(self):
        fig, ax = plt.subplots()
        fig.set_figwidth(3)
        fig.set_figheight(6)
        for image_name in self.files:
            with open(image_name, 'rb') as photo:
                data = photo.read()
                b64_file = base64.urlsafe_b64encode(data).decode('ascii')
            response = requests.post('http://127.0.0.1:8000/analyze',
                                     json={'image': b64_file}).json()
            for data in response['results']['correct']:
                r = base64.urlsafe_b64decode(data[list(data.keys())[0]])
                print(r)
                with open(f'results/correct/{list(data.keys())[0]}', 'wb') as new_img:
                    new_img.write(r)
            for data in response['results']['wrong']:
                r = base64.urlsafe_b64decode(data[list(data.keys())[0]])
                with open(f'results/correct/{list(data.keys())[0]}', 'wb') as new_img:
                    new_img.write(r)
            workbook = xlsxwriter.Workbook('results/diameters.xlsx')
            worksheet = workbook.add_worksheet('Диаметры')
            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 20)
            bold = workbook.add_format({'bold': True})
            worksheet.write('A1', 'ИЗОБРАЖЕНИЕ', bold)
            worksheet.write('B1', 'ДИАМЕТР', bold)
            row = 2
            for i in range(len(response['diameters'])):
                img_name = list(response['results']['correct'][i].keys())[0]
                worksheet.write(row, 0, img_name)
                worksheet.write(row, 1, response['diameters'][i])
                ax.bar(i + 1, response['diameters'][i])
                row += 1
            workbook.close()
            plt.savefig('results/plot.png')
            worksheet.insert_image('C1', 'results/plot.png')
            text = ['<html><b>РЕЗУЛЬТАТЫ</b></html>']
            for i in range(len(response['results']['digits'])):
                text.append(f'Для <b>{self.files[i]}</b>:')
                text.extend([f'Правильные: {response["results"]["digits"][i]["correct"]}',
                             f'Ошибочные: {response["results"]["digits"][i]["wrong"]}',
                             f'Не распознаны: {response["results"]["digits"][i]["not_a_hole"]}'])
            text.append('Таблица диаметров -- <b>results/diameters.xlsx!</b>')
            self.ui.diameterText.setText('<br>'.join(text))
            self.ui.PlotLabel.setPixmap(QtGui.QPixmap('results/plot.png'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_app = Interface()
    sys.exit(app.exec())
