from timer import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit


class Settings(QWidget):

    def __init__(self, timer: Timer):
        super().__init__()
        self.timer = timer

        self.layout = QVBoxLayout()
        self.section1 = QHBoxLayout()
        self.section2 = QHBoxLayout()

        self.setTime = QLineEdit()
        self.setTime.setPlaceholderText("00:25:00")
        self.setTimeBtn = QPushButton("Ayarla")
        self.setTimeBtn.clicked.connect(self.setTimeFunc)

        self.setDefaultAdd = QLineEdit()
        self.setDefaultAdd.setPlaceholderText("+, - için değer belirleyin")
        self.setDefaultAddBtn = QPushButton("Ayarla")
        self.setDefaultAddBtn.clicked.connect(self.setDefaultAddFunc)

        self.layout.addLayout(self.section1)
        self.layout.addLayout(self.section2)
        self.section1.addWidget(self.setTime)
        self.section1.addWidget(self.setTimeBtn)
        self.section2.addWidget(self.setDefaultAdd)
        self.section2.addWidget(self.setDefaultAddBtn)
        self.setLayout(self.layout)
        self.show()

    def setTimeFunc(self):
        try:
            self.timer.setTime(*map(int, self.setTime.text().split(":")))
            self.timer.setDefaultTime(*map(int, self.setTime.text().split(":")))
            self.timer.updateText()
        except ValueError as e:
            print(e)

    def setDefaultAddFunc(self):
        try:
            self.timer.setDefaultAdd(int(self.setDefaultAdd.text()))
        except ValueError as e:
            print(e)