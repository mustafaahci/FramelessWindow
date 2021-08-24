import ctypes
from ctypes import wintypes

import win32api
import win32con
import win32gui

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QColor
    from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QSizePolicy, QHBoxLayout
    from PyQt5.QtWinExtras import QtWin
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QColor
    from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QSizePolicy, QHBoxLayout
    from PySide2.QtWinExtras import QtWin


class TitleBar(QWidget):

    def __init__(self, parent):
        super().__init__()
        self._layout = QHBoxLayout()
        button_style = "QPushButton{{border: none;outline: none;background-color: {};color: white;padding: 6px;width: 80px;font: 16px consolas;}}QPushButton:hover{{background-color: {};}}"

        # set size
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(50)

        self.close_button = QPushButton("EXIT", clicked=app.exit)
        self.close_button.setStyleSheet(button_style.format('rgb(220, 0, 0)', 'rgb(240, 0, 0)'))

        self.maximize_button = QPushButton("Maximize", clicked=parent.showMaximized)
        self.maximize_button.setStyleSheet(button_style.format('rgb(25, 118, 210)', 'rgb(39, 136, 232)'))

        self.minimize_button = QPushButton("Minimize", clicked=parent.showMinimized)
        self.minimize_button.setStyleSheet(button_style.format('rgb(76, 175, 80)', 'rgb(92, 196, 96)'))

        # set background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#212121"))
        self.setPalette(p)

        self._layout.addStretch()
        self._layout.addWidget(self.minimize_button)
        self._layout.addWidget(self.maximize_button)
        self._layout.addWidget(self.close_button)

        self.setLayout(self._layout)


class Window(QWidget):
    BORDER_WIDTH = 5

    def __init__(self):
        super().__init__()
        # get the available resolutions without taskbar
        self.rect = QApplication.instance().desktop().availableGeometry(self)
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)

        # Create a thin frame
        self.hwnd = int(self.winId())
        style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_STYLE,
                               style | win32con.WS_POPUP | win32con.WS_THICKFRAME | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.WS_MAXIMIZEBOX | win32con.WS_MINIMIZEBOX)

        if QtWin.isCompositionEnabled():
            # Aero Shadow
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

        # Window Widgets
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.controlWidget = TitleBar(self)
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

    def nativeEvent(self, event, message):
        return_value, result = super().nativeEvent(event, message)

        # if you use Windows OS
        if event == b'windows_generic_MSG':
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            # Get the coordinates when the mouse moves.
            x = win32api.LOWORD(ctypes.c_long(msg.lParam).value)
            # converted an unsigned int to int (for dual monitor issue)
            if x & 32768: x = x | -65536
            y = win32api.HIWORD(ctypes.c_long(msg.lParam).value)
            if y & 32768: y = y | -65536

            x = x - self.frameGeometry().x()
            y = y - self.frameGeometry().y()

            # Determine whether there are other controls(i.e. widgets etc.) at the mouse position.
            if self.childAt(x, y) is not None and self.childAt(x, y) is not self.findChild(QWidget, "controlWidget"):
                # passing
                if self.width() - self.BORDER_WIDTH > x > self.BORDER_WIDTH and y < self.height() - self.BORDER_WIDTH:
                    return return_value, result

            if msg.message == win32con.WM_NCCALCSIZE:
                # Remove system title
                return True, 0

            if msg.message == win32con.WM_NCHITTEST:
                w, h = self.width(), self.height()
                lx = x < self.BORDER_WIDTH
                rx = x > w - self.BORDER_WIDTH
                ty = y < self.BORDER_WIDTH
                by = y > h - self.BORDER_WIDTH
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

        return return_value, result


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
