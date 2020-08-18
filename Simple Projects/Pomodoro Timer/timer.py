from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QLabel


class Timer(QLabel):

    DEFAULT_TIME = (00, 25, 00)

    def __init__(self, default_time=DEFAULT_TIME):
        super().__init__()
        self.hours = default_time[0]
        self.minutes = default_time[1]
        self.seconds = default_time[2]

        self._defaultAdd = 5

        self.sound = QSound("Files/Soft-alarm-tone.wav")

        self._timer = QTimer()
        self._timer.timeout.connect(self._updateTimer)

        self.updateText()

    def getTime(self):
        return self.hours, self.minutes, self.seconds

    def getHours(self):
        return self.hours

    def getMinutes(self):
        return self.minutes

    def getSeconds(self):
        return self.seconds

    def getDefaultAdd(self):
        return self._defaultAdd

    def setDefaultAdd(self, a):
        self._defaultAdd = a

    def __str__(self):
        return "{:02d}:{:02d}:{:02d}".format(self.hours, self.minutes, self.seconds)

    def setText(self, a0: str):
        full_time = a0.split(":")
        self.hours = int(full_time[0])
        self.minutes = int(full_time[1])
        self.seconds = int(full_time[2])
        super().setText(self.__str__())

    def setTime(self, h, m, s):
        self.hours = h
        self.minutes = m
        self.seconds = s

    def addHours(self, h):
        self.hours += h

    def addMins(self, m):
        if self.minutes + m > 59:
            self.hours += 1
            self.minutes = (self.minutes + m) - 60
        else:
            self.minutes += m

    def addSecs(self, s):
        if self.seconds + s > 59:
            self.minutes += 1
            self.seconds = (self.seconds + s) - 60
        else:
            self.seconds += s

    def reset(self):
        self.hours = self.DEFAULT_TIME[0]
        self.minutes = self.DEFAULT_TIME[1]
        self.seconds = self.DEFAULT_TIME[2]
        self._timer.stop()

    def setDefaultTime(self, h, m, s):
        self.DEFAULT_TIME = (h, m, s)

    def start(self, interval=1000):
        self._timer.start(interval)

    def stop(self):
        self._timer.stop()

    def _updateTimer(self):
        if self.seconds == 0:
            if self.minutes == 0:
                if self.hours == 0:
                    self.playSound()
                    self.stop()
                else:
                    self.hours -= 1
                    self.minutes += 59
            else:
                self.minutes -= 1
                self.seconds += 59
        else:
            self.seconds -= 1
        self.updateText()

    def updateText(self):
        self.setText(self.__str__())

    def isActive(self):
        return self._timer.isActive()

    def playSound(self):
        self.sound.play()

    def stopSound(self):
        self.sound.stop()