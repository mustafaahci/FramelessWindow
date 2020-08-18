import sys

from PyQt5.QtGui import QIcon

from timer import *

from settings import Settings

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QGraphicsOpacityEffect, QSystemTrayIcon, QMenu, QAction


class toolButton(QPushButton):

    def __init__(self, text=""):
        super().__init__()
        self.setMouseTracking(True)
        self.text = text
        self.setText(self.text)

    def enterEvent(self, a0: QtCore.QEvent):
        self.setCursor(Qt.PointingHandCursor)


class Window(QWidget):
    windowTwo: QWidget

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("Files/python.png"))
        self.setFixedWidth(250)
        self.setFixedHeight(110)

        self.mainLayout = QVBoxLayout()
        self.subLayout = QHBoxLayout()
        self.toolLayout = QVBoxLayout()

        self.trayIcon = QSystemTrayIcon(QIcon("Files/python.png"), self)
        self.trayMenu = QMenu()
        self.exit = QAction("Çıkış")
        self.trayMenu.addAction(self.exit)
        self.exit.triggered.connect(app.exit)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()

        self.timer = Timer()
        self.timer.setStyleSheet("color: white; background: rgba(0,0,0,.5); padding: 10px;"
                                 "font: 36px Bahnschrift;")
        self.timer.setAlignment(Qt.AlignCenter)

        # buttons
        buttonStyle = """
            QPushButton{
                font: 16px Comfortaa;
                background: rgba(0,0,0,.5);
                color: white;
            }
            
            QPushButton:hover{
                background: rgba(255,255,255,.5);
                border: 1px solid rgba(0,0,0,.5);
            }
        """
        self.addButton = toolButton("+")
        self.addButton.setFixedWidth(25)
        self.addButton.setStyleSheet(buttonStyle)
        self.addButton.clicked.connect(self.addTime)
        self.subtrButton = toolButton("-")
        self.subtrButton.setFixedWidth(25)
        self.subtrButton.setStyleSheet(buttonStyle)
        self.subtrButton.clicked.connect(self.subtrTime)
        self.resetButton = toolButton("⟲")
        self.resetButton.setFixedWidth(25)
        self.resetButton.setStyleSheet(buttonStyle)
        self.resetButton.clicked.connect(self.resetTime)

        # moving window
        self.move(self.screen().size().width() - self.width(), self.screen().size().height() - self.height() - 32)

        self.mainLayout.addLayout(self.subLayout)
        self.subLayout.addWidget(self.timer)
        self.subLayout.addLayout(self.toolLayout)

        # tool layour
        self.toolLayout.addWidget(self.addButton)
        self.toolLayout.addWidget(self.subtrButton)
        self.toolLayout.addWidget(self.resetButton)

        self.opacity = QGraphicsOpacityEffect(self)
        self.opacity.setOpacity(0.7)
        self.setGraphicsEffect(self.opacity)
        self.setAutoFillBackground(True)

        self.setLayout(self.mainLayout)
        self.show()

    def enterEvent(self, a0: QtCore.QEvent):
        self.opacity.setOpacity(1.0)

    def leaveEvent(self, a0: QtCore.QEvent):
        self.opacity.setOpacity(0.7)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.timer.isActive():
            self.timer.stop()
        elif self.timer.getTime() != (0, 0, 0):
            self.timer.start()
        self.timer.stopSound()

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        self.loadScreen()

    def loadScreen(self):
        self.windowTwo = Settings(self.timer)

    def addTime(self):
        self.timer.addMins(self.timer.getDefaultAdd())
        self.timer.updateText()

    def subtrTime(self):
        if self.timer.getMinutes() != 0:
            self.timer.addMins(-self.timer.getDefaultAdd())
            self.timer.updateText()

    def resetTime(self):
        self.timer.reset()
        self.timer.updateText()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
