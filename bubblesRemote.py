# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 16:04:24 2017

@author: olgag

Modifed: davidre 7/20/2017
    -Added a zro wrapper to allow for remote interaction from Scheduler program

"""
# Developing bubble detection algorithm 
       
import os
import numpy as np
import tifffile
import cv2
import matplotlib.pyplot as plt

from PyQt4 import QtGui, QtCore
from zro import RemoteObject

import datetime

class RemoteInterface(RemoteObject):
    def __init__(self, rep_port, parent):
        super(RemoteInterface, self).__init__(rep_port=rep_port)
        print "opening Remote Interface on port:{}".format(rep_port)
        self.parent = parent

    def setDirectory(self, directory):
        print "setting directory to {}".format(directory)
        self.parent.setDirectory(directory)

    def setRibbon(self, ribbon):
        print "setting ribbon to {}".format(ribbon)
        self.parent.setRibbon(ribbon)

    def setSession(self, session):
        print "setting session to {}".format(session)
        self.parent.setSession(session)

    def setChannel(self, channel):
        print "setting channel to {}".format(channel)
        self.parent.setChannel(channel)

    def startDetection(self):
        print "starting Detection..."
        result = self.parent.startDetection()
        return result

    def test(self):
        print "TEST INCOMING"

class MyGui(QtGui.QWidget):
    def __init__(self):
        super(MyGui, self).__init__()

        self.dividerLabel = QtGui.QLabel(self)
        self.dividerLabel.setText("-- Select Directory for Bubble Detection --")
        self.dividerLabel.move(10,10)

        self.button = QtGui.QPushButton('Select Directory', self)
        self.button.clicked.connect(self.openSelection)
        self.button.resize(100, 30)
        self.button.move(10,30)

        self.fileSelectedLabel = QtGui.QLabel(self)
        self.fileSelectedLabel.setText("No Data Directory Selected")
        self.fileSelectedLabel.resize(600, 30)
        self.fileSelectedLabel.move(10,60)

        self.dataDirectoryLabel = QtGui.QLabel(self)
        self.dataDirectoryLabel.resize(600, 30)
        self.dataDirectoryLabel.setText("Data Directory: -na-")
        self.dataDirectoryLabel.move(10, 90)

        self.metaDirectoryLabel = QtGui.QLabel(self)
        self.metaDirectoryLabel.resize(600, 30)
        self.metaDirectoryLabel.setText("Meta Directory: -na-")
        self.metaDirectoryLabel.move(10, 120)

        self.setGeometry(300, 300, 300, 250)
        self.setWindowTitle('Bubble Detection')

        self.interface = RemoteInterface(rep_port=7778, parent=self)

        self.selectedDirectory = None

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._check_sock)
        self.timer.start(200)

        self.show()

    def _check_sock(self):
        self.interface._check_rep()

    def setDirectory(self, incomingDirectory):
        self.directoryLabel.setText("Directory: {}".format(incomingDirectory))
        self.selectedDirectory = incomingDirectory
        self.fileSelectedLabel.setText("Data Directory Remotely Selected:" + self.selectedDirectory)

    def setRibbon(self, incomingRibbon):
        self.ribbonLabel.setText("Ribbon: {}".format(incomingRibbon))
        self.ribbon = incomingRibbon

    def setSession(self, incomingSession):
        self.sessionLabel.setText("Session: {}".format(incomingSession))
        self.session = incomingSession

    def setChannel(self, incomingChannel):
        self.channelLabel.setText("Channel: {}".format(incomingChannel))
        self.channel = incomingChannel

    def startBubbleDetection(self):
        success = self.parent.startBubbleDetection()
        print "Bubble Detection Success:{}".format(success)

    def openSelection(self):
        print "opening selection"

        exptpath = r'\\synbionas1'

        self.selectedDirectory = QtGui.QFileDialog.getOpenFileName(self, 'Select File', exptpath)

        if self.selectedDirectory:
            print "selectedFilename:{}".format(self.selectedDirectory)
            self.fileSelectedLabel.setText("Data Directory Selected:" + self.selectedDirectory)
        else:
            self.fileSelectedLabel.setText("Data  Selected: No Directory Selected")

#select files
#data_files = data_files[0:320]
#metadata_files = metadata_files[0:320]

    # Read meatadata
    def read_metadata(self, filename):
        metafile = open(filename,'r')
        metafile.readline()
        line1 = metafile.readline()
        metafile.readline()
        line2 = metafile.readline()
        (xpos,ypos,zpos)=line2.split()
        xpos=float(xpos)
        ypos=float(ypos)
        zpos=float(zpos)
        (channel,width,height,mx,my,sx,sy,exposure)=line1.split()
        metafile.close()
        return (xpos,ypos,zpos)     

    # start the bubble detection routine
    def startBubbleDetection(self):
        # Specify data 
        # drive ='W:\\'
        # project = 'test_multi_ribbon\\SC_CM84FL_1'
        # ribbon = 'Ribbon0002'
        # session = 'session02'
        # channel = 'DAPI_2'

        # Sample
        # directory = C:\\data\test_multi_ribbon\\SC\\SC_CM84FL_1\\raw\\data\\ribbon\\session\\channel 

        if self.selectedDirectory:
            data_directory =  self.selectedDirectory
            metadata_directory =  self.selectedDirectory
        else:
            print "directory structure not defined yet..."
            return False

        #data_directory = 'W:\\data\\test_multi_ribbon\\SC_CM84FL_1\\raw\\data\\Ribbon0000\\session01\\DAPI_1\\'
        #metadata_directory = 'W:\\data\\test_multi_ribbon\\SC_CM84FL_1\\raw\\data\\Ribbon0000\\session01\\DAPI_1\\'

        print "Bubble Detection Started at {}".format(datetime.datetime.now())

        print "Data Directory:{}".format(data_directory)
        self.dataDirectoryLabel.setText("Data Directory: {}".format(data_directory))
        print "Metadata Directory:{}".format(metadata_directory)
        self.metaDirectoryLabel.setText("Metadata Directory:{}".format(metadata_directory))

        data_files = [os.path.join(data_directory,f)
                  for f in os.listdir(data_directory) if f.endswith('.tif') ]
        data_files.sort()

        metadata_files = [os.path.join(metadata_directory,os.path.splitext(f)[0]+'_metadata.txt')
                  for f in os.listdir(metadata_directory) if f.endswith('.tif') ]
        metadata_files.sort()

        section = np.zeros((len(metadata_files),), dtype=np.int)
        frame = np.zeros((len(metadata_files),), dtype=np.int)
        xpos = np.zeros((len(metadata_files),))
        ypos = np.zeros((len(metadata_files),))
        zpos = np.zeros((len(metadata_files),))

        for i, metapath in enumerate(metadata_files):
            (xpos[i],ypos[i],zpos[i])=self.read_metadata(metapath)
            fname = os.path.split(metapath)[1]
            f = os.path.splitext(fname)[0]
            (f,part,frame1)=f.partition('_F')
            (f,part,section1)=f.partition('_S')
            section[i] = int(section1)
            (sframe,part,sz) = frame1.partition('_Z')
            frame[i] = int(sframe)

        # Set up the SimpleBlobdetector
        params = cv2.SimpleBlobDetector_Params()
         
        # Change thresholds
        params.minThreshold = 0
        params.maxThreshold = 15
        params.thresholdStep = 1 

        # Filter by Area.
        params.filterByArea = True
        params.maxArea = 1e7
        params.minArea = 5e4
         
        # Filter by Circularity
        params.filterByCircularity = False
        params.minCircularity = 0.5
         
        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.97
         
        # Filter by Inertia
        params.filterByInertia = False
        params.minInertiaRatio = 0.4

        # Find bubbles
        score = np.zeros((len(data_files),),dtype='uint8')
        x = np.zeros((len(data_files),))
        y = np.zeros((len(data_files),))
        s = np.zeros((len(data_files),))
         
        for i, filename in enumerate(data_files):
            img = tifffile.imread(filename)    
            img = cv2.blur(img, (50,50))
            a = 255.0/(np.max(img) - np.min(img))
            b = np.min(img)*(-255.0)/(np.max(img)-np.min(img))
            img = cv2.convertScaleAbs(img,alpha=a,beta=b)      
            params.maxThreshold = int(round(np.min(img) + (np.min(img) + np.median(img))/4))   
            img[0,:]=img[-1,:]=img[:,0]=img[:,-1]=np.median(img)
            detector = cv2.SimpleBlobDetector_create(params)
            keypoints = detector.detect(img)
            if keypoints:
                score[i] = 1 
                x[i] = keypoints[0].pt[0] 
                y[i] = keypoints[0].pt[1]
                s[i] = keypoints[0].size 
                print i, params.maxThreshold, "found %d blobs" % len(keypoints)
            else:
                score[i] = 0        
                print i, params.maxThreshold, "no blobs"
        #    im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]),
        #                        (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)   
        #    plt.subplots(figsize=(10,10))
        #    plt.imshow(im_with_keypoints, cmap = 'gray')
        #    plt.colorbar()
        #    plt.title('i=%d'% i)

        # Plot score
        #plt.figure(figsize=(6,5)) 
        #plt.scatter(xpos, ypos, c = score, vmin=0, vmax=1, cmap='Reds', marker='o') # cmap='Reds'
        #plt.axis('scaled')    
        #plt.ylim(plt.ylim()[::-1])
        #plt.colorbar() 
        #plt.title('score_bubbles') 
        #plt.xlabel('xpos [$\mu$m]')
        #plt.ylabel('ypos [$\mu$m]') 

        plt.figure(figsize=(26,5)) 
        plt.scatter(xpos, ypos, c = s, vmin=None, vmax=None, cmap='Reds', marker='o') # cmap='Reds'
        plt.axis('scaled')    
        plt.ylim(plt.ylim()[::-1])
        plt.colorbar() 
        plt.title('blob size') 
        plt.xlabel('xpos [$\mu$m]')
        plt.ylabel('ypos [$\mu$m]') 

        #tile = np.arange(len(data_files))    
        #
        #plt.figure(figsize=(20,5))
        #plt.plot(tile, s, 'kx-')
        #plt.xlabel('tile')
        #plt.ylabel('size [pxl]')
        #plt.title('blob size')

        plt.figure(figsize=(26,5))
        plt.scatter(frame, section, c = s, vmin=None, vmax=None, cmap='Reds', marker='o') 
        plt.axis('scaled')    
        plt.grid() 
        plt.colorbar()    
        plt.xlabel('frame')
        plt.ylabel('section')
        plt.title('blob size') 

        #for keypoint in keypoints:
        #    x = keypoint.pt[0] #x-coordinate of blob
        #    y = keypoint.pt[1] #y-coordinate of blob
        #    s = keypoint.size #diameter of blob (diameter of the meaningful keypoint neighborhood)
        #    print "x", x, "y", y, "s", s

        return True

def main():
    app = QtGui.QApplication([])
    g = MyGui()
    g.show()
    app.exec_()

if __name__ == '__main__':
    main()
