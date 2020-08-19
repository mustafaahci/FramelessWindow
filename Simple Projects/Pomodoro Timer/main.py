import sys

from PyQt5 import QtCore, QtGui

from timer import *
from settings import *

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QSystemTrayIcon, QMenu, QAction, QLabel, QVBoxLayout, QPushButton, \
    QHBoxLayout, QGraphicsOpacityEffect


class Window(QWidget):
    settingsScreen: QWidget

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.subLayout = QHBoxLayout()
        self.toolLayout = QVBoxLayout()

        # WINDOW
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.Tool)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Pomodoro Timer")
        self.setFixedWidth(250)
        self.setFixedHeight(110)

        # SYSTEM TRAY
        self.trayIcon = QSystemTrayIcon(QIcon("Files/python.png"))
        self.trayIconMenu = QMenu()
        self.exit = QAction("ÇIKIŞ")
        self.trayIconMenu.addAction(self.exit)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.exit.triggered.connect(app.exit)
        self.trayIcon.show()

        self.move(self.screen().size().width() - self.size().width() - 10, self.screen().size().height() - self.size().height() - 47 )

        self.timer = Timer()
        self.timer.setStyleSheet("color: white; background: rgba(0,0,0,.5); font: 36px Bahnschrift;")
        self.timer.setAlignment(Qt.AlignCenter)

        self.opacity = QGraphicsOpacityEffect()
        self.opacity.setOpacity(0.7)
        self.setGraphicsEffect(self.opacity)

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

        self.addButton = QPushButton("+")
        self.addButton.setFixedWidth(25)
        self.addButton.setStyleSheet(buttonStyle)
        self.addButton.setCursor(Qt.PointingHandCursor)
        self.addButton.clicked.connect(self.addTime)
        self.subtrButton = QPushButton("-")
        self.subtrButton.setFixedWidth(25)
        self.subtrButton.setStyleSheet(buttonStyle)
        self.subtrButton.setCursor(Qt.PointingHandCursor)
        self.subtrButton.clicked.connect(self.subtrTime)
        self.resetButton = QPushButton("⟲")
        self.resetButton.setFixedWidth(25)
        self.resetButton.setStyleSheet(buttonStyle)
        self.resetButton.setCursor(Qt.PointingHandCursor)
        self.resetButton.clicked.connect(self.resetTime)

        self.layout.addLayout(self.subLayout)
        self.subLayout.addWidget(self.timer)
        self.subLayout.addLayout(self.toolLayout)
        self.toolLayout.addWidget(self.addButton)
        self.toolLayout.addWidget(self.subtrButton)
        self.toolLayout.addWidget(self.resetButton)
        self.setLayout(self.layout)
        self.show()

    def addTime(self):
        self.timer.addMins(self.timer.getDefaultAdd())
        self.timer.updateText()

    def subtrTime(self):
        self.timer.addMins(-self.timer.getDefaultAdd())
        self.timer.updateText()

    def resetTime(self):
        self.timer.reset()
        self.timer.updateText()

    def enterEvent(self, a0: QtCore.QEvent):
        self.opacity.setOpacity(1)

    def leaveEvent(self, a0: QtCore.QEvent):
        self.opacity.setOpacity(0.7)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.timer.isActive():
            self.timer.stop()
        elif self.timer.getTime() != (0, 0, 0):
            self.timer.start()
        self.timer.stopSound()

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        self.settingsScreen = Settings(self.timer)


if __name__ == "__main__":
   app =  QApplication(sys.argv)
   window = Window()
   sys.exit(app.exec_())