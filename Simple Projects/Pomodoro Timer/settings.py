from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
from timer import *


class Settings(QWidget):

    def __init__(self, timer: Timer):
        super().__init__()
        self.layout = QVBoxLayout()
        self.timer = timer

        self.section1 = QHBoxLayout()
        self.section2 = QHBoxLayout()

        self.setTime = QLineEdit()
        self.setTime.setPlaceholderText("00:25:00")
        self.setTimeBtn = QPushButton("SET")
        self.setTimeBtn.clicked.connect(self.setTimeFunc)
        self.setTime.returnPressed.connect(self.setTimeFunc)

        self.setDefaultAdd = QLineEdit()
        self.setDefaultAdd.setPlaceholderText("Default value for +, -")
        self.setDefaultAddBtn = QPushButton("SET")
        self.setDefaultAddBtn.clicked.connect(self.setDefaultAddFunc)
        self.setDefaultAdd.returnPressed.connect(self.setDefaultAddFunc)

        self.section1.addWidget(self.setTime)
        self.section1.addWidget(self.setTimeBtn)
        self.section2.addWidget(self.setDefaultAdd)
        self.section2.addWidget(self.setDefaultAddBtn)
        self.layout.addLayout(self.section1)
        self.layout.addLayout(self.section2)
        self.setLayout(self.layout)
        self.show()

    def setDefaultAddFunc(self):
        self.timer.setDefaultAdd(self.setDefaultAdd.text())

    def setTimeFunc(self):
        try:
            self.timer.setTime(*map(int, self.setTime.text().split(":")))
            self.timer.setDefaultTime(*map(int, self.setTime.text().split(":")))
            self.timer.updateText()
        except ValueError:
            return
