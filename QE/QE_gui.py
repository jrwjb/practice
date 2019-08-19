#-*- coding=utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import (QWidget, QMessageBox, QApplication, QDesktopWidget, QComboBox, QLabel,
QFileDialog, QPushButton, QLineEdit, QInputDialog, QFormLayout, QTextEdit, QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from QCandyUi import CandyWindow
from QCandyUi.CandyWindow import colorful
import QE


class Gui(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # self.resize(650, 450)
        # self.setFixedSize(650, 450)    ### 窗口固定大小
        self.setWindowTitle('QE工具')
        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)     ## 忽略放大按钮
        self.center()       ## 窗口居中

        ## 添加 label
        self.lbl = QLabel(u'请选择目录', self)
        self.lbl.setFont(QFont("Timers", 12))
        self.lbl.move(50, 120)
        self.lbl_1= QLabel('               ', self)
        self.lbl_1.setFont(QFont('Timers', 16))
        self.lbl_1.move(200, 200)

        ## 创建输入框
        self.le_1 = QLineEdit(self)
        self.le_1.resize(200, 32)
        self.le_1.move(150, 115)
        self.le_1.setFont(QFont("Timers", 12))

        ## 添加 按钮
        self.btn_1 = QPushButton('...', self)
        self.btn_1.resize(50, 32)
        self.btn_1.setFont(QFont("Timers", 12))
        self.btn_1.move(350, 115)
        self.btn_1.clicked.connect(self.chose_dir)

        self.btn_2 = QPushButton('Start', self)
        self.btn_2.setFont(QFont("Timers", 18))
        self.btn_2.move(200, 250)
        self.btn_2.clicked.connect(self.start)

        # self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def chose_dir(self):
        global dir
        dir = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        self.le_1.setText(str(dir))
        # return str(dir)


    def start(self):
        try:
            # self.lbl_1.setText('.....')
            QE.main(dir)
            self.lbl_1.setText(u'分析完成')
            # print('Done')
        except Exception as e:
            # print(e)
            self.lbl_1.setText(str(e))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = Gui()
    # gui = CandyWindow.createWindow(gui, 'blue', title=u'QE工具')
    # gui.resize(500, 450)
    gui.setFixedSize(500, 450)
    gui.show()
    sys.exit(app.exec_())
    # os.system('pause')
