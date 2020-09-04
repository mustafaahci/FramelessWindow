import ctypes
from ctypes import wintypes

import win32api
import win32con
import win32gui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtWinExtras import QtWin


class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved", wintypes.POINT),
        ("ptMaxSize", wintypes.POINT),
        ("ptMaxPosition", wintypes.POINT),
        ("ptMinTrackSize", wintypes.POINT),
        ("ptMaxTrackSize", wintypes.POINT),
    ]


class AnotherWidget(QWidget):

    def __init__(self):
        super().__init__()
        self._layout = QHBoxLayout()

        # set size
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(50)

        self.button = QPushButton("EXIT", clicked=app.exit)
        self.button.setStyleSheet("""
            QPushButton{
                border: none;
                outline: none;
                background-color: rgb(220,0,0);
                color: white;
                padding: 6px;
                width: 80px;
                font: 16px consolas;
            }
            
            QPushButton:hover{
            background-color: rgb(240,0,0);
            }
        """)

        # set background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#212121"))
        self.setPalette(p)

        self._layout.addStretch()
        self._layout.addWidget(self.button)
        self.setLayout(self._layout)


class Window(QWidget):
    BorderWidth = 5

    def __init__(self):
        super().__init__()
        # get the available resolutions without taskbar
        self._rect = QApplication.instance().desktop().availableGeometry(self)
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)

        # Create a thin frame
        style = win32gui.GetWindowLong(int(self.winId()), win32con.GWL_STYLE)
        win32gui.SetWindowLong(int(self.winId()), win32con.GWL_STYLE, style | win32con.WS_THICKFRAME)

        if QtWin.isCompositionEnabled():
            # Aero Shadow
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

        # Window Widgets
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.controlWidget = AnotherWidget()
        self.controlWidget.setObjectName("controlWidget")

        # main widget is here
        self.mainWidget = QWidget()
        self.mainWidgetLayout = QVBoxLayout()
        self.mainWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.mainWidget.setLayout(self.mainWidgetLayout)
        self.mainWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # set background color
        self.mainWidget.setAutoFillBackground(True)
        p = self.mainWidget.palette()
        p.setColor(self.mainWidget.backgroundRole(), QColor("#272727"))
        self.mainWidget.setPalette(p)

        self._layout.addWidget(self.controlWidget)
        self._layout.addWidget(self.mainWidget)
        self.setLayout(self._layout)
        self.show()

    def nativeEvent(self, eventType, message):
        retval, result = super().nativeEvent(eventType, message)

        # if you use Windows OS
        if eventType == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            # Get the coordinates when the mouse moves.
            x = win32api.LOWORD(ctypes.c_long(msg.lParam).value) - self.frameGeometry().x()
            y = win32api.HIWORD(ctypes.c_long(msg.lParam).value) - self.frameGeometry().y()

            # Determine whether there are other controls(i.e. widgets etc.) at the mouse position.
            if self.childAt(x, y) is not None and self.childAt(x, y) is not self.findChild(QWidget, "controlWidget"):
                # passing
                if self.width() - 5 > x > 5 and y < self.height() - 5:
                    return retval, result

            if msg.message == win32con.WM_NCCALCSIZE:
                # Remove system title
                return True, 0
            if msg.message == win32con.WM_GETMINMAXINFO:
                # This message is triggered when the window position or size changes.
                info = ctypes.cast(
                    msg.lParam, ctypes.POINTER(MINMAXINFO)).contents
                # Modify the maximized window size to the available size of the main screen.
                info.ptMaxSize.x = self._rect.width()
                info.ptMaxSize.y = self._rect.height()
                # Modify the x and y coordinates of the placement point to (0,0).
                info.ptMaxPosition.x, info.ptMaxPosition.y = 0, 0

            if msg.message == win32con.WM_NCHITTEST:
                w, h = self.width(), self.height()
                lx = x < self.BorderWidth
                rx = x > w - self.BorderWidth
                ty = y < self.BorderWidth
                by = y > h - self.BorderWidth
                if lx and ty:
                    return True, win32con.HTTOPLEFT
                if rx and by:
                    return True, win32con.HTBOTTOMRIGHT
                if rx and ty:
                    return True, win32con.HTTOPRIGHT
                if lx and by:
                    return True, win32con.HTBOTTOMLEFT
                if ty:
                    return True, win32con.HTTOP
                if by:
                    return True, win32con.HTBOTTOM
                if lx:
                    return True, win32con.HTLEFT
                if rx:
                    return True, win32con.HTRIGHT
                # Title
                return True, win32con.HTCAPTION

        return retval, result


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
