from PyQt4 import QtGui, QtCore
from zro import RemoteObject

class RemoteInterface(RemoteObject):
    def __init__(self, rep_port, parent):
        super(RemoteInterface, self).__init__(rep_port=rep_port)
        print "opening Remote Interace on port:{}".format(rep_port)
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
        else:
            self.pause = True

        self.parent.pause_line_edit.setText(str(self.pause))
    

class MyGui(QtGui.QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()

        self.pause_line_edit = QtGui.QLineEdit(self)
        self.interface = RemoteInterface(rep_port=7777, parent=self)

        self.stagePositionX = 0
        self.stagePositionY = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._check_sock)
        self.timer.start(200)
         

    def _check_sock(self):
        self.interface._check_rep()
        #print("TEST")

    def getStagePosition(self):
        stagePosition = [self.stagePositionX, self.stagePositionY]
        return stagePosition

    def setStagePosition(self, newXPosition, newYPosition):
        self.stagePositionX = newXPosition
        self.stagePositionY = newYPosition
        print "stage Position updated"

def main():
    app = QtGui.QApplication([])
    g = MyGui()
    g.show()
    app.exec_()

if __name__ == '__main__':
    main()