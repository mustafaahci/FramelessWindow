from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QLabel


class Timer(QLabel):
    DEFAULT_TIME = (0, 25, 0)

    def __init__(self, time=DEFAULT_TIME):
        super().__init__()
        self._hours = time[0]
        self._minutes = time[1]
        self._seconds = time[2]
        
        self._defaultAdd = 5

        self._sound = QSound("Files/Soft-alarm-tone.wav")

        self._timer = QTimer()
        self._timer.timeout.connect(self._updateTime)

        self.updateText()

    def getHours(self):
        return self._hours

    def getMinutes(self):
        return self._minutes

    def getSeconds(self):
        return self._seconds

    def getDefaultAdd(self):
        return self._defaultAdd

    def getTime(self):
        return self._hours, self._minutes, self._seconds

    def addHours(self, h):
        self._hours += h

    def addMins(self, m):
        if self._minutes + m > 59:
            self._hours += 1
            self._minutes = (self._minutes + m) - 60
        elif self._minutes + m < 0 and self._hours != 0:
            self._hours -= 1
            self._minutes = 60 + (self._minutes + m)
        elif self._minutes + m < 0 and self._hours == 0:
            return
        else:
            self._minutes += m

    def addSecs(self, s):
        if self._seconds + s > 59:
            self._minutes += 1
            self._seconds = (self._seconds + s) - 60
        else:
            self._seconds += s

    def reset(self):
        self._hours = self.DEFAULT_TIME[0]
        self._minutes = self.DEFAULT_TIME[1]
        self._seconds = self.DEFAULT_TIME[2]

    def updateText(self):
        self.setText(self.__str__())

    def _updateTime(self):
        if self._seconds == 0:
            if self._minutes == 0:
                if self._hours == 0:
                    self._timer.stop()
                    self._sound.play()
                else:
                    self._hours -= 1
                    self._minutes += 59
                    self._seconds += 59
            else:
                self._minutes -= 1
                self._seconds += 59
        else:
            self._seconds -= 1

        self.updateText()

    def start(self, interval=1000):
        self._timer.start(interval)

    def stop(self):
        self._timer.stop()

    def isActive(self):
        return self._timer.isActive()

    def setTime(self, h, m, s):
        self._hours = h
        self._minutes = m
        self._seconds = s

    def setDefaultTime(self, h, m, s):
        self.DEFAULT_TIME = (h, m, s)

    def setDefaultAdd(self, a):
        try:
            a = int(a)
            if a < 0:
                return
            else:
                self._defaultAdd = a
        except ValueError:
            return

    def playSound(self):
        self._sound.play()

    def stopSound(self):
        self._sound.stop()

    def __str__(self):
        return "{:02d}:{:02d}:{:02d}".format(self._hours, self._minutes, self._seconds)