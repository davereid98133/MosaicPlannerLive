from PyQt4 import QtGui, QtCore
from zro import RemoteObject
from random import randint

class RemoteInterface(RemoteObject):
    def __init__(self, rep_port, parent):
        super(RemoteInterface, self).__init__(rep_port=rep_port)
        print "opening Remote Interace on port:{}".format(rep_port)
        self.parent = parent
        self.pause = False

    def returnStagePosition(self):
        print "getting stage position..."
        (x, y) = self.parent.getStagePosition()
        self.parent.pause_line_edit.setText("stage:" + str((x,y)))        
        return (x,y)

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

        self.randomXPos = 20
        self.randomYPos = 50

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._check_sock)
        self.timer.start(200)
         

    def _check_sock(self):
        self.interface._check_rep()
        #print("TEST")

    def getStagePosition(self):
        self.randomXPos = randint(0, 100)
        self.randomYPos = randint(0, 100)

        # newStagePosition = [self.randomXPos, self.randomYPos]
        return self.randomXPos, self.randomYPos

def main():
    app = QtGui.QApplication([])
    g = MyGui()
    g.show()
    app.exec_()

if __name__ == '__main__':
    main()