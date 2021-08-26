import ctypes
import win32api
import win32gui

from ctypes.wintypes import LONG

from win32con import WM_GETMINMAXINFO, WM_NCCALCSIZE, GWL_STYLE, WM_NCHITTEST, WS_MAXIMIZEBOX, WS_THICKFRAME, \
    WS_CAPTION, WS_OVERLAPPEDWINDOW, HTTOPLEFT, HTBOTTOMRIGHT, HTTOPRIGHT, HTBOTTOMLEFT, \
    HTTOP, HTBOTTOM, HTLEFT, HTRIGHT, HTCAPTION, WS_POPUP, WS_SYSMENU, WS_MINIMIZEBOX

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


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", LONG),
        ("top", LONG),
        ("right", LONG),
        ("bottom", LONG)
    ]


class TitleBar(QWidget):

    def __init__(self, parent):
        super().__init__()
        self._layout = QHBoxLayout()
        button_style = "QPushButton{{border: none;outline: none;background-color: {};color: white;padding: 6px;width: " \
                       "80px;font: 16px Consolas;}}QPushButton:hover{{background-color: {};}} "

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
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Create a thin frame
        self.hwnd = self.winId().__int__()
        window_style = win32gui.GetWindowLong(self.hwnd, GWL_STYLE)
        win32gui.SetWindowLong(self.hwnd, GWL_STYLE, window_style | WS_POPUP | WS_THICKFRAME | WS_CAPTION | WS_SYSMENU | WS_MAXIMIZEBOX | WS_MINIMIZEBOX)

        if QtWin.isCompositionEnabled():
            # Aero Shadow
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

        # Window Widgets
        self.resize(800, 600)
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.controlWidget = TitleBar(self)
        self.controlWidget.setObjectName("ControlWidget")

        # main widget is here
        self.mainWidget = QWidget()
        self.mainWidgetLayout = QVBoxLayout()
        self.mainWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.mainWidget.setLayout(self.mainWidgetLayout)
        self.mainWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # set background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#272727"))
        self.setPalette(p)

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
            x = win32api.LOWORD(LONG(msg.lParam).value)
            # converted an unsigned int to int (for dual monitor issue)
            if x & 32768: x = x | -65536
            y = win32api.HIWORD(LONG(msg.lParam).value)
            if y & 32768: y = y | -65536

            x -= self.frameGeometry().x()
            y -= self.frameGeometry().y()

            # Determine whether there are other controls(i.e. widgets etc.) at the mouse position.
            if self.childAt(x, y) is not None and self.childAt(x, y) is not self.findChild(QWidget, "ControlWidget"):
                # passing
                if self.width() - self.BORDER_WIDTH > x > self.BORDER_WIDTH and y < self.height() - self.BORDER_WIDTH:
                    return return_value, result

            if msg.message == WM_NCCALCSIZE:
                # Remove system title
                return True, 0

            if msg.message == WM_GETMINMAXINFO:
                # This message will be triggered when the position or size of the window changes

                if ctypes.windll.user32.IsZoomed(self.hwnd):
                    frame = RECT(0, 0, 0, 0)
                    ctypes.windll.user32.AdjustWindowRectEx(ctypes.byref(frame), WS_OVERLAPPEDWINDOW, False, 0)
                    frame.left = abs(frame.left)
                    frame.top = abs(frame.bottom)
                    self.setContentsMargins(frame.left, frame.top, frame.right, frame.bottom)
                else:
                    self.setContentsMargins(0, 0, 0, 0)

            if msg.message == WM_NCHITTEST:
                w, h = self.width(), self.height()
                lx = x < self.BORDER_WIDTH
                rx = x > w - self.BORDER_WIDTH
                ty = y < self.BORDER_WIDTH
                by = y > h - self.BORDER_WIDTH
                if lx and ty:
                    return True, HTTOPLEFT
                if rx and by:
                    return True, HTBOTTOMRIGHT
                if rx and ty:
                    return True, HTTOPRIGHT
                if lx and by:
                    return True, HTBOTTOMLEFT
                if ty:
                    return True, HTTOP
                if by:
                    return True, HTBOTTOM
                if lx:
                    return True, HTLEFT
                if rx:
                    return True, HTRIGHT
                # Title
                return True, HTCAPTION

        return return_value, result


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
