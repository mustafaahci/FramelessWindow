import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QLineEdit, QAction


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BROWSER")

        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.tab.setDocumentMode(True)

        self.tab.tabBarDoubleClicked.connect(self.newTabCTRL)
        self.tab.currentChanged.connect(self.tabChanged)
        self.tab.tabCloseRequested.connect(self.closeTab)

        self.setCentralWidget(self.tab)

        self.navbar = QToolBar()
        self.navbar.setIconSize(QSize(24, 24))
        self.navbar.setMovable(False)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.navbar)

        self.back = QAction(QIcon(os.path.join('images', 'back.png')), "GERİ", self)
        self.back.setStatusTip("Önceki Sayfa")
        self.back.triggered.connect(lambda: self.tab.currentWidget().back())
        self.navbar.addAction(self.back)

        self.forward = QAction(QIcon(os.path.join('images', 'forward.png')), "İLERİ", self)
        self.forward.setStatusTip("Sonraki Sayfa")
        self.forward.triggered.connect(lambda: self.tab.currentWidget().forward())
        self.navbar.addAction(self.forward)

        self.refresh = QAction(QIcon(os.path.join('images', 'refresh.png')), "YENİLE", self)
        self.refresh.setStatusTip("Yenile")
        self.refresh.triggered.connect(lambda: self.tab.currentWidget().reload())
        self.navbar.addAction(self.refresh)

        self.url = QLineEdit()
        self.navbar.addWidget(self.url)

        self.newTab(QUrl('http://www.google.com'))
        self.url.returnPressed.connect(self.openURL)

        self.navbar.addSeparator()

        self.show()

    def openURL(self):
        self.tab.currentWidget().setUrl(QUrl(self.url.text()))

    def newTabCTRL(self, p_int):
        if p_int == -1:
            self.newTab()

    def newTab(self, url=None):

        if url is None:
            url = QUrl("")

        browser = QWebEngineView()
        browser.setUrl(url)

        i = self.tab.addTab(browser, "about:blank")
        self.tab.setCurrentIndex(i)

        browser.urlChanged.connect(lambda url, browser=browser: self.update_url(url, browser))
        browser.loadFinished.connect(lambda: self.tab.setTabText(i, browser.page().title()))
    
    def tabChanged(self):
        url = self.tab.currentWidget().url()
        self.update_url(url, self.tab.currentWidget())
    
    def update_url(self, url, browser=None):
        if browser != self.tab.currentWidget():
            return
        self.url.setText(url.toString())

    def closeTab(self, i):
        if self.tab.count() < 2:
            return

        self.tab.removeTab(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
