from PyQt4 import QtGui, QtCore
from zro import RemoteObject

import datetime

class RemoteInterface(RemoteObject):
    def __init__(self, rep_port, parent):
        super(RemoteInterface, self).__init__(rep_port=rep_port)
        print "opening Remote Interface on port:{}".format(rep_port)
        self.parent = parent
        self.pause = False

    def getStagePosition(self):
        print "getting stage position..."
        currentStagePosition = self.parent.getStagePosition()
        self.parent.pause_line_edit.setText("X:" + str(currentStagePosition[0]) + "Y:" + str(currentStagePosition[1]))        

    def setStagePosition(self, incomingStagePosition):
        print "setting new stage position to x:{}, y:{}".format(incomingStagePosition[0], incomingStagePosition[1])
        self.parent.setStagePosition(incomingStagePosition[0], incomingStagePosition[1])

    def set_pause(self):
        if self.pause is True:
            self.pause = False
            self.parent.setPause(False)
        else:
            self.pause = True
            self.parent.setPause(True)

        self.parent.pauseLabel.setText("Pause:{}".format(str(self.pause)))
    
    def setZPosition(self, incomingZPosition):
        print "setting Z Position to z:{}".format(incomingZPosition)
        self.parent.setZPosition(incomingZPosition)

    def getZPosition(self):
        print "getting Z position..."
        zPos = self.parent.getZPosition()
        print "Z Position:{}".format(zPos)

    def startAcq(self):
        print "Starting Acquisition..."
        success = self.parent.startAcquisition()
        return success

    def stopAcq(self):
        print "Stopping Acquisition..."
        success = self.parent.stopAcquisition()
        return success

    def getRemainingImagingTime(self):
        remainingTime = self.parent.getRemainingImagingTime()
        print "remainingTime:{}".format(remainingTime)
        return remainingTime

    def remoteSavePositionListJSON(self, filename, trans=None):
        print "saving position list to {}".format(filename)
        self.parent.remoteSavePositionListJSON(filename, trans=trans)

    def remoteLoadPositionListJSON(self, filename):
        print "loading position list from {}".format(filename)
        self.parent.remoteLoadPositionListJSON(filename)

class MyGui(QtGui.QWidget):
    def __init__(self):
        super(MyGui, self).__init__()

        self.pauseLabel = QtGui.QLabel(self)
        self.pauseLabel.resize(600, 40)
        self.pauseLabel.setText("Remote Pause: ")
        self.pauseLabel.move(10, 10)

        self.timeRemainingLabel = QtGui.QLabel(self)
        self.timeRemainingLabel.resize(600, 40)
        self.timeRemainingLabel.setText("Time Remaining: -na-")
        self.timeRemainingLabel.move(10, 50)

        self.stagePositionLabel = QtGui.QLabel(self)
        self.stagePositionLabel.resize(600, 40)
        self.stagePositionLabel.setText("Stage X:    Stage Y:    Z position: ")
        self.stagePositionLabel.move(10, 100)

        self.saveFileLabel = QtGui.QLabel(self)
        self.saveFileLabel.resize(600, 40)
        self.saveFileLabel.setText("Saved File: -na-")
        self.saveFileLabel.move(10, 150)

        self.loadFileLabel = QtGui.QLabel(self)
        self.loadFileLabel.resize(600, 40)
        self.loadFileLabel.setText("Loaded File: -na-")
        self.loadFileLabel.move(10, 200)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Dummy MosaicPlanner')

        self.interface = RemoteInterface(rep_port=7777, parent=self)

        self.stagePositionX = 0
        self.stagePositionY = 0
        self.zPosition = 0


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._check_sock)
        self.timer.start(200)

        self.acqTimer = QtCore.QTimer()
        self.acqTimer.timeout.connect(self.acqCountdown)

        self.acqCount = 60 #60 seconds, for now

        self.show()
         
    def _check_sock(self):
        self.interface._check_rep()
        #print("TEST")

    def getStagePosition(self):
        stagePosition = [self.stagePositionX, self.stagePositionY]
        return stagePosition

    def setStagePosition(self, newXPosition, newYPosition):
        self.stagePositionX = newXPosition
        self.stagePositionY = newYPosition
        self.stagePositionLabel.setText("Stage X: {} Stage Y: {} Z position: {}".format(self.stagePositionX, self.stagePositionY, self.zPosition))
        print "stage Position updated"

    def setZPosition(self, newZPosition):
        self.zPosition = newZPosition
        self.stagePositionLabel.setText("Stage X: {} Stage Y: {} Z position: {}".format(self.stagePositionX, self.stagePositionY, self.zPosition))
        print "z position updated"

    def getZPosition(self):
        return self.zPosition

    def startAcquisition(self):
        self.acqTimer.start(1000)
        self.startTime =  datetime.datetime.now()
        print "starting acq timer at {}".format(self.startTime)
        return True

    def stopAcquisition(self):
        self.acqTimer.stop()
        self.acqCount = 60
        self.timeRemainingLabel.setText("Seconds Remaining: {}".format("Acq stopped remotely"))

    def acqCountdown(self):
        if self.acqCount < 1:
            self.timeRemainingLabel.setText("Seconds Remaining: {}".format("Acq complete"))
            self.acqTimer.stop()
            self.acqCount = 60
        else:
            self.timeRemainingLabel.setText("Seconds Remaining: {}".format(self.acqCount))
            self.acqCount = self.acqCount - 1

    def setPause(self, incomingCmd):
        if incomingCmd:
            print "pausing Acquisition at {} remaining".format(self.acqCount)
            self.acqTimer.stop()
            self.timeRemainingLabel.setText("Seconds Remaining: {} -Remotely Paused".format(self.acqCount))
        else:
            self.timeRemainingLabel.setText("Seconds Remaining: {} -Remotely UnPaused".format(self.acqCount))
            self.acqTimer.start(1000)

    def getRemainingImagingTime(self):
        remainingTime = self.acqCount
        return remainingTime

    def remoteSavePositionListJSON(self, filename, trans=None):
        self.saveFileLabel.setText("Saved to {}".format(filename))

    def remoteLoadPositionListJSON(self, filename):
        self.loadFileLabel.setText("Loaded from {}".format(filename))

def main():
    app = QtGui.QApplication([])
    g = MyGui()
    g.show()
    app.exec_()

if __name__ == '__main__':
    main()