
# -*- coding: utf-8 -*-
# based on pyqtgraph\examples\ImageItem.py
from PyQt4 import QtCore, QtGui, uic
import numpy as np
import pyqtgraph as pg
import os
from imageSourceMM import imageSource
import pandas as pd
import tifffile
from functools import partial
import shutil
import multiprocessing as mp
from SaveThread import file_save_process
STOP_TOKEN = 'STOP!!!'


# class myHistographLUTItem(pg.HistogramLUTItem):
#     def __init__(self,*kargs,**kwargs):
#         super(myHistographLUTItem, self).__init__(*kargs,**kwargs)
#         self.plot.rotate(-90)
#         self.gradient.setOrientation('bottom')
viridis = [[ 0.26700401,  0.00487433,  0.32941519],
       [ 0.26851048,  0.00960483,  0.33542652],
       [ 0.26994384,  0.01462494,  0.34137895],
       [ 0.27130489,  0.01994186,  0.34726862],
       [ 0.27259384,  0.02556309,  0.35309303],
       [ 0.27380934,  0.03149748,  0.35885256],
       [ 0.27495242,  0.03775181,  0.36454323],
       [ 0.27602238,  0.04416723,  0.37016418],
       [ 0.2770184 ,  0.05034437,  0.37571452],
       [ 0.27794143,  0.05632444,  0.38119074],
       [ 0.27879067,  0.06214536,  0.38659204],
       [ 0.2795655 ,  0.06783587,  0.39191723],
       [ 0.28026658,  0.07341724,  0.39716349],
       [ 0.28089358,  0.07890703,  0.40232944],
       [ 0.28144581,  0.0843197 ,  0.40741404],
       [ 0.28192358,  0.08966622,  0.41241521],
       [ 0.28232739,  0.09495545,  0.41733086],
       [ 0.28265633,  0.10019576,  0.42216032],
       [ 0.28291049,  0.10539345,  0.42690202],
       [ 0.28309095,  0.11055307,  0.43155375],
       [ 0.28319704,  0.11567966,  0.43611482],
       [ 0.28322882,  0.12077701,  0.44058404],
       [ 0.28318684,  0.12584799,  0.44496   ],
       [ 0.283072  ,  0.13089477,  0.44924127],
       [ 0.28288389,  0.13592005,  0.45342734],
       [ 0.28262297,  0.14092556,  0.45751726],
       [ 0.28229037,  0.14591233,  0.46150995],
       [ 0.28188676,  0.15088147,  0.46540474],
       [ 0.28141228,  0.15583425,  0.46920128],
       [ 0.28086773,  0.16077132,  0.47289909],
       [ 0.28025468,  0.16569272,  0.47649762],
       [ 0.27957399,  0.17059884,  0.47999675],
       [ 0.27882618,  0.1754902 ,  0.48339654],
       [ 0.27801236,  0.18036684,  0.48669702],
       [ 0.27713437,  0.18522836,  0.48989831],
       [ 0.27619376,  0.19007447,  0.49300074],
       [ 0.27519116,  0.1949054 ,  0.49600488],
       [ 0.27412802,  0.19972086,  0.49891131],
       [ 0.27300596,  0.20452049,  0.50172076],
       [ 0.27182812,  0.20930306,  0.50443413],
       [ 0.27059473,  0.21406899,  0.50705243],
       [ 0.26930756,  0.21881782,  0.50957678],
       [ 0.26796846,  0.22354911,  0.5120084 ],
       [ 0.26657984,  0.2282621 ,  0.5143487 ],
       [ 0.2651445 ,  0.23295593,  0.5165993 ],
       [ 0.2636632 ,  0.23763078,  0.51876163],
       [ 0.26213801,  0.24228619,  0.52083736],
       [ 0.26057103,  0.2469217 ,  0.52282822],
       [ 0.25896451,  0.25153685,  0.52473609],
       [ 0.25732244,  0.2561304 ,  0.52656332],
       [ 0.25564519,  0.26070284,  0.52831152],
       [ 0.25393498,  0.26525384,  0.52998273],
       [ 0.25219404,  0.26978306,  0.53157905],
       [ 0.25042462,  0.27429024,  0.53310261],
       [ 0.24862899,  0.27877509,  0.53455561],
       [ 0.2468114 ,  0.28323662,  0.53594093],
       [ 0.24497208,  0.28767547,  0.53726018],
       [ 0.24311324,  0.29209154,  0.53851561],
       [ 0.24123708,  0.29648471,  0.53970946],
       [ 0.23934575,  0.30085494,  0.54084398],
       [ 0.23744138,  0.30520222,  0.5419214 ],
       [ 0.23552606,  0.30952657,  0.54294396],
       [ 0.23360277,  0.31382773,  0.54391424],
       [ 0.2316735 ,  0.3181058 ,  0.54483444],
       [ 0.22973926,  0.32236127,  0.54570633],
       [ 0.22780192,  0.32659432,  0.546532  ],
       [ 0.2258633 ,  0.33080515,  0.54731353],
       [ 0.22392515,  0.334994  ,  0.54805291],
       [ 0.22198915,  0.33916114,  0.54875211],
       [ 0.22005691,  0.34330688,  0.54941304],
       [ 0.21812995,  0.34743154,  0.55003755],
       [ 0.21620971,  0.35153548,  0.55062743],
       [ 0.21429757,  0.35561907,  0.5511844 ],
       [ 0.21239477,  0.35968273,  0.55171011],
       [ 0.2105031 ,  0.36372671,  0.55220646],
       [ 0.20862342,  0.36775151,  0.55267486],
       [ 0.20675628,  0.37175775,  0.55311653],
       [ 0.20490257,  0.37574589,  0.55353282],
       [ 0.20306309,  0.37971644,  0.55392505],
       [ 0.20123854,  0.38366989,  0.55429441],
       [ 0.1994295 ,  0.38760678,  0.55464205],
       [ 0.1976365 ,  0.39152762,  0.55496905],
       [ 0.19585993,  0.39543297,  0.55527637],
       [ 0.19410009,  0.39932336,  0.55556494],
       [ 0.19235719,  0.40319934,  0.55583559],
       [ 0.19063135,  0.40706148,  0.55608907],
       [ 0.18892259,  0.41091033,  0.55632606],
       [ 0.18723083,  0.41474645,  0.55654717],
       [ 0.18555593,  0.4185704 ,  0.55675292],
       [ 0.18389763,  0.42238275,  0.55694377],
       [ 0.18225561,  0.42618405,  0.5571201 ],
       [ 0.18062949,  0.42997486,  0.55728221],
       [ 0.17901879,  0.43375572,  0.55743035],
       [ 0.17742298,  0.4375272 ,  0.55756466],
       [ 0.17584148,  0.44128981,  0.55768526],
       [ 0.17427363,  0.4450441 ,  0.55779216],
       [ 0.17271876,  0.4487906 ,  0.55788532],
       [ 0.17117615,  0.4525298 ,  0.55796464],
       [ 0.16964573,  0.45626209,  0.55803034],
       [ 0.16812641,  0.45998802,  0.55808199],
       [ 0.1666171 ,  0.46370813,  0.55811913],
       [ 0.16511703,  0.4674229 ,  0.55814141],
       [ 0.16362543,  0.47113278,  0.55814842],
       [ 0.16214155,  0.47483821,  0.55813967],
       [ 0.16066467,  0.47853961,  0.55811466],
       [ 0.15919413,  0.4822374 ,  0.5580728 ],
       [ 0.15772933,  0.48593197,  0.55801347],
       [ 0.15626973,  0.4896237 ,  0.557936  ],
       [ 0.15481488,  0.49331293,  0.55783967],
       [ 0.15336445,  0.49700003,  0.55772371],
       [ 0.1519182 ,  0.50068529,  0.55758733],
       [ 0.15047605,  0.50436904,  0.55742968],
       [ 0.14903918,  0.50805136,  0.5572505 ],
       [ 0.14760731,  0.51173263,  0.55704861],
       [ 0.14618026,  0.51541316,  0.55682271],
       [ 0.14475863,  0.51909319,  0.55657181],
       [ 0.14334327,  0.52277292,  0.55629491],
       [ 0.14193527,  0.52645254,  0.55599097],
       [ 0.14053599,  0.53013219,  0.55565893],
       [ 0.13914708,  0.53381201,  0.55529773],
       [ 0.13777048,  0.53749213,  0.55490625],
       [ 0.1364085 ,  0.54117264,  0.55448339],
       [ 0.13506561,  0.54485335,  0.55402906],
       [ 0.13374299,  0.54853458,  0.55354108],
       [ 0.13244401,  0.55221637,  0.55301828],
       [ 0.13117249,  0.55589872,  0.55245948],
       [ 0.1299327 ,  0.55958162,  0.55186354],
       [ 0.12872938,  0.56326503,  0.55122927],
       [ 0.12756771,  0.56694891,  0.55055551],
       [ 0.12645338,  0.57063316,  0.5498411 ],
       [ 0.12539383,  0.57431754,  0.54908564],
       [ 0.12439474,  0.57800205,  0.5482874 ],
       [ 0.12346281,  0.58168661,  0.54744498],
       [ 0.12260562,  0.58537105,  0.54655722],
       [ 0.12183122,  0.58905521,  0.54562298],
       [ 0.12114807,  0.59273889,  0.54464114],
       [ 0.12056501,  0.59642187,  0.54361058],
       [ 0.12009154,  0.60010387,  0.54253043],
       [ 0.11973756,  0.60378459,  0.54139999],
       [ 0.11951163,  0.60746388,  0.54021751],
       [ 0.11942341,  0.61114146,  0.53898192],
       [ 0.11948255,  0.61481702,  0.53769219],
       [ 0.11969858,  0.61849025,  0.53634733],
       [ 0.12008079,  0.62216081,  0.53494633],
       [ 0.12063824,  0.62582833,  0.53348834],
       [ 0.12137972,  0.62949242,  0.53197275],
       [ 0.12231244,  0.63315277,  0.53039808],
       [ 0.12344358,  0.63680899,  0.52876343],
       [ 0.12477953,  0.64046069,  0.52706792],
       [ 0.12632581,  0.64410744,  0.52531069],
       [ 0.12808703,  0.64774881,  0.52349092],
       [ 0.13006688,  0.65138436,  0.52160791],
       [ 0.13226797,  0.65501363,  0.51966086],
       [ 0.13469183,  0.65863619,  0.5176488 ],
       [ 0.13733921,  0.66225157,  0.51557101],
       [ 0.14020991,  0.66585927,  0.5134268 ],
       [ 0.14330291,  0.66945881,  0.51121549],
       [ 0.1466164 ,  0.67304968,  0.50893644],
       [ 0.15014782,  0.67663139,  0.5065889 ],
       [ 0.15389405,  0.68020343,  0.50417217],
       [ 0.15785146,  0.68376525,  0.50168574],
       [ 0.16201598,  0.68731632,  0.49912906],
       [ 0.1663832 ,  0.69085611,  0.49650163],
       [ 0.1709484 ,  0.69438405,  0.49380294],
       [ 0.17570671,  0.6978996 ,  0.49103252],
       [ 0.18065314,  0.70140222,  0.48818938],
       [ 0.18578266,  0.70489133,  0.48527326],
       [ 0.19109018,  0.70836635,  0.48228395],
       [ 0.19657063,  0.71182668,  0.47922108],
       [ 0.20221902,  0.71527175,  0.47608431],
       [ 0.20803045,  0.71870095,  0.4728733 ],
       [ 0.21400015,  0.72211371,  0.46958774],
       [ 0.22012381,  0.72550945,  0.46622638],
       [ 0.2263969 ,  0.72888753,  0.46278934],
       [ 0.23281498,  0.73224735,  0.45927675],
       [ 0.2393739 ,  0.73558828,  0.45568838],
       [ 0.24606968,  0.73890972,  0.45202405],
       [ 0.25289851,  0.74221104,  0.44828355],
       [ 0.25985676,  0.74549162,  0.44446673],
       [ 0.26694127,  0.74875084,  0.44057284],
       [ 0.27414922,  0.75198807,  0.4366009 ],
       [ 0.28147681,  0.75520266,  0.43255207],
       [ 0.28892102,  0.75839399,  0.42842626],
       [ 0.29647899,  0.76156142,  0.42422341],
       [ 0.30414796,  0.76470433,  0.41994346],
       [ 0.31192534,  0.76782207,  0.41558638],
       [ 0.3198086 ,  0.77091403,  0.41115215],
       [ 0.3277958 ,  0.77397953,  0.40664011],
       [ 0.33588539,  0.7770179 ,  0.40204917],
       [ 0.34407411,  0.78002855,  0.39738103],
       [ 0.35235985,  0.78301086,  0.39263579],
       [ 0.36074053,  0.78596419,  0.38781353],
       [ 0.3692142 ,  0.78888793,  0.38291438],
       [ 0.37777892,  0.79178146,  0.3779385 ],
       [ 0.38643282,  0.79464415,  0.37288606],
       [ 0.39517408,  0.79747541,  0.36775726],
       [ 0.40400101,  0.80027461,  0.36255223],
       [ 0.4129135 ,  0.80304099,  0.35726893],
       [ 0.42190813,  0.80577412,  0.35191009],
       [ 0.43098317,  0.80847343,  0.34647607],
       [ 0.44013691,  0.81113836,  0.3409673 ],
       [ 0.44936763,  0.81376835,  0.33538426],
       [ 0.45867362,  0.81636288,  0.32972749],
       [ 0.46805314,  0.81892143,  0.32399761],
       [ 0.47750446,  0.82144351,  0.31819529],
       [ 0.4870258 ,  0.82392862,  0.31232133],
       [ 0.49661536,  0.82637633,  0.30637661],
       [ 0.5062713 ,  0.82878621,  0.30036211],
       [ 0.51599182,  0.83115784,  0.29427888],
       [ 0.52577622,  0.83349064,  0.2881265 ],
       [ 0.5356211 ,  0.83578452,  0.28190832],
       [ 0.5455244 ,  0.83803918,  0.27562602],
       [ 0.55548397,  0.84025437,  0.26928147],
       [ 0.5654976 ,  0.8424299 ,  0.26287683],
       [ 0.57556297,  0.84456561,  0.25641457],
       [ 0.58567772,  0.84666139,  0.24989748],
       [ 0.59583934,  0.84871722,  0.24332878],
       [ 0.60604528,  0.8507331 ,  0.23671214],
       [ 0.61629283,  0.85270912,  0.23005179],
       [ 0.62657923,  0.85464543,  0.22335258],
       [ 0.63690157,  0.85654226,  0.21662012],
       [ 0.64725685,  0.85839991,  0.20986086],
       [ 0.65764197,  0.86021878,  0.20308229],
       [ 0.66805369,  0.86199932,  0.19629307],
       [ 0.67848868,  0.86374211,  0.18950326],
       [ 0.68894351,  0.86544779,  0.18272455],
       [ 0.69941463,  0.86711711,  0.17597055],
       [ 0.70989842,  0.86875092,  0.16925712],
       [ 0.72039115,  0.87035015,  0.16260273],
       [ 0.73088902,  0.87191584,  0.15602894],
       [ 0.74138803,  0.87344918,  0.14956101],
       [ 0.75188414,  0.87495143,  0.14322828],
       [ 0.76237342,  0.87642392,  0.13706449],
       [ 0.77285183,  0.87786808,  0.13110864],
       [ 0.78331535,  0.87928545,  0.12540538],
       [ 0.79375994,  0.88067763,  0.12000532],
       [ 0.80418159,  0.88204632,  0.11496505],
       [ 0.81457634,  0.88339329,  0.11034678],
       [ 0.82494028,  0.88472036,  0.10621724],
       [ 0.83526959,  0.88602943,  0.1026459 ],
       [ 0.84556056,  0.88732243,  0.09970219],
       [ 0.8558096 ,  0.88860134,  0.09745186],
       [ 0.86601325,  0.88986815,  0.09595277],
       [ 0.87616824,  0.89112487,  0.09525046],
       [ 0.88627146,  0.89237353,  0.09537439],
       [ 0.89632002,  0.89361614,  0.09633538],
       [ 0.90631121,  0.89485467,  0.09812496],
       [ 0.91624212,  0.89609127,  0.1007168 ],
       [ 0.92610579,  0.89732977,  0.10407067],
       [ 0.93590444,  0.8985704 ,  0.10813094],
       [ 0.94563626,  0.899815  ,  0.11283773],
       [ 0.95529972,  0.90106534,  0.11812832],
       [ 0.96489353,  0.90232311,  0.12394051],
       [ 0.97441665,  0.90358991,  0.13021494],
       [ 0.98386829,  0.90486726,  0.13689671],
       [ 0.99324789,  0.90615657,  0.1439362 ]]

class RetakeView(QtGui.QWidget):

    def __init__(self,mp):
        super(RetakeView,self).__init__()

        self.mp = mp
        self.mp.imgSrc.set_binning(1)
        self.initial_offset = self.mp.imgSrc.get_autofocus_offset()
        self.initUI()
        #setup dummy variables of blanks for live and review data
        self.live_data = np.zeros((5,5))
        self.review_data = np.zeros((5,5))
        self.isLive = False
        #initialize section,frame, ch and  initialization state
        self.section = 0
        self.frame = 0
        self.ch = self.mp.cfg['ChannelSettings']['focusscore_chan']

        #get the outdirectory from mosaicplanner settings
        for key,value in self.mp.outdirdict.iteritems():
            self.outdir = self.mp.outdirdict[key]
        #load the focus score data
        self.loadFocusScoreData()
        ## Make all plots clickable
        self.archiveDir = self.outdir.replace('raw\\data','raw\\bad_data')
        if not os.path.isdir(self.archiveDir):
            os.makedirs(self.archiveDir)


    def initUI(self):
        #load the UI from layout file
        currpath=os.path.split(os.path.realpath(__file__))[0]
        filename = os.path.join(currpath,'Retake.ui')
        uic.loadUi(filename,self)

        #add a pyqtgraph image to graphics view
        self.img1 = pg.ImageItem()
        self.imageplot1 = self.image1_graphicsLayoutWidget.addPlot()
        self.imageplot1.setAspectLocked(True,ratio=1)
        self.imageplot1.addItem(self.img1)
        self.hist1 = pg.HistogramLUTItem()
        self.hist1.setImageItem(self.img1)
        self.image1_graphicsLayoutWidget.addItem(self.hist1,0,1)
        self.img1.setLevels(0,self.mp.imgSrc.get_max_pixel_value())
        self.hist1.setLevels(0,self.mp.imgSrc.get_max_pixel_value())

        #add a pyqtgraph image to graphics view
        self.img2 = pg.ImageItem()
        self.imageplot2 = self.image2_graphicsLayoutWidget.addPlot()
        self.imageplot2.setAspectLocked(True,ratio=1)
        self.imageplot2.addItem(self.img2)
        self.hist2 = pg.HistogramLUTItem()
        self.hist2.setImageItem(self.img2)
        self.image2_graphicsLayoutWidget.addItem(self.hist2,0,1)
        self.img2.setLevels(0,self.mp.imgSrc.get_max_pixel_value())
        self.hist2.setLevels(0,self.mp.imgSrc.get_max_pixel_value())

        self.dataplot = self.focusScore_graphicsLayoutWidget.addPlot()
        self.dataplot.setAspectLocked(True, ratio=1)
        self.dataplot.invertY(True)
        #setup the channel buttons 
        self.chnButtons=[]
        for i,ch in enumerate(self.mp.channel_settings.channels):
            btn=QtGui.QRadioButton(ch)
            self.chnButtons.append(btn)
            self.channel_verticalLayout.addWidget(btn)
            if ch == self.mp.cfg['ChannelSettings']['focusscore_chan']:
                btn.setChecked(True)
            btn.clicked.connect(partial(self.changeChannel,ch))

        #initialize AFCoffset UI, and connect valueChanged to setting it
        self.AFCoffset_doubleSpinBox.setValue(self.initial_offset)
        self.AFCoffset_doubleSpinBox.valueChanged[float].connect(self.mp.imgSrc.set_autofocus_offset)
        self.resetOffset_pushButton.clicked.connect(self.resetOffset)

        #connect various UI slots to their change functions
        self.section_spinBox.valueChanged[int].connect(self.changeSection)

        self.frame_spinBox.valueChanged[int].connect(self.changeFrame)
        
        self.move_pushButton.clicked.connect(self.moveToFrame)
        
        self.review_pushButton.clicked.connect(self.reviewFrame)
        self.retake_pushButton.clicked.connect(self.retakeFrame)
        self.hold_pushButton.clicked.connect(self.holdHere)
        self.softwareaf_pushButton.clicked.connect(self.mp.on_software_af_tool)
        self.snap_pushButton.clicked.connect(self.doSnap)
        self.livereview_pushButton.clicked[bool].connect(self.changeLiveReview)
        
        self.exit_pushButton.clicked.connect(self.exitClicked)

    def holdHere(self,evt=None):
        self.mp.imgSrc.set_autofocus_offset(-1)
        self.mp.imgSrc.set_hardware_autofocus_state(True)

    def retakeFrame(self,evt=None):
        currx, curry = self.mp.imgSrc.get_xy()
        currz = self.mp.imgSrc.get_z()
        x,y = self.getFramePos()
        assert(np.abs(x-currx)<2)
        assert(np.abs(y-curry)<2)
        self.archiveFrame()

        self.mp.imgSrc.set_binning(1)
        numchan, chrom_correction = self.mp.summarize_channel_settings()
        self.mp.dataQueue = mp.Queue()
        self.mp.messageQueue = mp.Queue()
        metadata_dictionary = {
            'channelname': self.mp.channel_settings.prot_names,
            '(height,width)': self.mp.imgSrc.get_sensor_size(),
            'ScaleFactorX': self.mp.imgSrc.get_pixel_size(),
            'ScaleFactorY': self.mp.imgSrc.get_pixel_size(),
            'exp_time': self.mp.channel_settings.exposure_times,
        }
        if self.mp.cfg['MosaicPlanner']['hardware_trigger']:
            #iterates over channels/exposure times in appropriate order
            channels = [ch for ch in self.mp.channel_settings.channels if self.mp.channel_settings.usechannels[ch]]
            exp_times = [self.mp.channel_settings.exposure_times[ch] for ch in self.mp.channel_settings.channels if self.mp.channel_settings.usechannels[ch]]
            success=self.mp.imgSrc.setup_hardware_triggering(channels,exp_times)

        ssh_opts = dict(self.mp.cfg['SSH'])
        ssh_opts['mount_point'] = self.mp.lookup_mountpoint(self.outdir)
        self.mp.saveProcess = mp.Process(target=file_save_process,
                                        args=(self.mp.dataQueue,
                                              self.mp.messageQueue,
                                              STOP_TOKEN,
                                              metadata_dictionary,
                                              ssh_opts))
        self.mp.saveProcess.start()

        self.mp.multiDacq(success, self.outdir, chrom_correction,
                          False, currx, curry, currz, self.section,
                          self.frame, hold_focus=True)

        self.mp.dataQueue.put(STOP_TOKEN)
        self.mp.saveProcess.join()
        if self.mp.cfg['MosaicPlanner']['hardware_trigger']:
            self.mp.imgSrc.stop_hardware_triggering()
        d = {'pos': (currx, curry), 'symbol': '+','pen': pg.mkPen('w', width=5)}
        self.retakesScatterPlot.addPoints([d])


    def archiveFrame(self):
        for ch in self.mp.channel_settings.channels:
           if self.mp.channel_settings.usechannels[ch]:
                prot_name = self.mp.channel_settings.prot_names[ch]
                ch_dir = os.path.join(self.outdir, prot_name)
                out_ch_dir = os.path.join(self.archiveDir,prot_name)
                if not os.path.isdir(out_ch_dir):
                    os.makedirs(out_ch_dir)

                tif_file = prot_name + "_S%04d_F%04d_Z%02d.tif" % (self.section, self.frame, 0)
                metadata_file =  prot_name + "_S%04d_F%04d_Z%02d_metadata.txt"%(self.section, self.frame, 0)
                focus_file = prot_name + "_S%04d_F%04d_Z%02d_focus.csv" %(self.section, self.frame, 0)

                if not os.path.exists(os.path.join(out_ch_dir,tif_file)):
                    shutil.move(os.path.join(ch_dir,tif_file),os.path.join(out_ch_dir,tif_file))
                    shutil.move(os.path.join(ch_dir,metadata_file),os.path.join(out_ch_dir,metadata_file))
                    if os.path.exists(os.path.join(out_ch_dir,focus_file)):
                        shutil.move(os.path.join(ch_dir,focus_file),os.path.join(out_ch_dir,focus_file))
                else:

                    try:
                        os.remove(os.path.join(ch_dir, tif_file))
                        os.remove(os.path.join(ch_dir, metadata_file))
                        if os.path.exists(os.path.join(out_ch_dir,focus_file)):
                            os.remove(os.path.join(ch_dir, focus_file))
                    except:
                        print "no data to remove"
                        pass

    def resetOffset(self,evt=None):
        self.AFCoffset_doubleSpinBox.setValue(self.initial_offset)
        self.mp.imgSrc.set_autofocus_offset(self.initial_offset)

    def loadFocusScoreData(self):
        score_ch=self.mp.cfg['ChannelSettings']['focusscore_chan']
        protName = self.mp.channel_settings.prot_names[score_ch]
        ch_dir = os.path.join(self.outdir,protName)
        data_files = [os.path.join(ch_dir,f) for f in os.listdir(ch_dir) if f.endswith('.csv') ]
        df = pd.DataFrame()
        data_files.sort()
        for data_file in data_files:
            dft = pd.read_csv(data_file)
            df = df.append(dft,ignore_index=True)
        

        frame_medians = df.groupby('frame_index')['score1_median'].median()
        frame_stds = df.groupby('frame_index')['score1_std'].median()

        for i,row in df.iterrows():
            df.loc[i,'score1_norm'] = (row.score1_median - frame_medians[row.frame_index])/frame_stds[row.frame_index]
        
        self.focus_df = df
        print self.focus_df.score1_norm
        cmap = pg.ColorMap(pos=np.linspace(start=-.04,stop=.04,num=256), color=viridis)
        colors = cmap.map(df.score1_norm)
        brushes = [pg.mkBrush(c) for c in colors]

        self.sp = pg.ScatterPlotItem(size=150)
        self.sp.sigClicked.connect(self.selectPoint)
        self.sp.setData(x=df.xpos, y=df.ypos, pxMode=False,brush=brushes,data=df.to_dict('records'))
        self.currPosScatterPlot = pg.ScatterPlotItem()
        self.currPointScatterPlot = pg.ScatterPlotItem()
        self.retakesScatterPlot = pg.ScatterPlotItem(size=150,pxMode=False)

        self.dataplot.addItem(self.sp)
        self.dataplot.addItem(self.retakesScatterPlot)
        self.dataplot.addItem(self.currPointScatterPlot)
        self.dataplot.addItem(self.currPosScatterPlot)

        self.updatePosition()

    def selectPoint(self,plot,points):
        lastClicked = points
        if len(points)==1:
            #for p in points:
            #    p.setPen('r', width=2)
            #self.lastClicked = points
            d=points[0].data()
            mode=self.clickMode_comboBox.currentText()
            if 'Review' in mode:
                self.section_spinBox.setValue(d['slide_index'])
                self.frame_spinBox.setValue(d['frame_index'])
            if 'Move' in mode:
                self.moveToFrame()

    def reviewFrame(self,evt=None):
        self.changeReviewData()
        self.changeLiveReview(isLive=False)


    def changeLiveReview(self,isLive=None):
        if isLive is None:
            isLive = self.isLive
        else:
            self.isLive = isLive
        self.livereview_pushButton.setDown(isLive)
        if isLive:
            self.livereview_pushButton.setText("Showing Live")
            self.loadLiveData()
        else:
            self.livereview_pushButton.setText("Showing Review")
            self.loadReviewData()

    def changeReviewData(self,evt=None):
        prot_name = self.mp.channel_settings.prot_names[self.ch]
        ch_dir = os.path.join(self.outdir,prot_name)
        tif_filepath = os.path.join(ch_dir, prot_name + "_S%04d_F%04d_Z%02d.tif" % (self.section, self.frame, 0))
        data = tifffile.imread(tif_filepath)
        self.review_data = data

        self.currPointScatterPlot.clear()
        x,y = self.getFramePos()
        d = {'pos': (x, y), 'symbol': 'o', 'pen': pg.mkPen('r', width=1)}
        self.currPointScatterPlot.addPoints([d])

    def changeChannel(self,ch):
        self.ch = ch
        if self.isLive == False:
            self.reviewFrame()

    def changeSection(self,section):
        self.section = section
        self.reviewFrame()

    def changeFrame(self,frame):
        self.frame = frame
        self.reviewFrame()

    def exitClicked(self,evt):
        self.hide()
 
    def loadLiveData(self,evt=None):
        self.img1.setImage(np.rot90(self.live_data,k=3))
        self.img1.setLevels((0, self.mp.imgSrc.get_max_pixel_value()))
        self.img2.setImage(np.rot90(self.live_data,k=3))
        self.img2.setLevels((0, self.mp.imgSrc.get_max_pixel_value()))
    def loadReviewData(self,evt=None):
        self.img1.setImage(np.rot90(self.review_data,k=3))
        self.img1.setLevels((0, self.mp.imgSrc.get_max_pixel_value()))
        self.img2.setImage(np.rot90(self.review_data,k=3))
        self.img2.setLevels((0, self.mp.imgSrc.get_max_pixel_value()))

    def doSnap(self,evt=None):
        self.mp.imgSrc.set_channel(self.ch)
        self.mp.imgSrc.set_exposure(self.mp.channel_settings.exposure_times[self.ch])
        data=self.mp.imgSrc.snap_image()
        self.live_data = data
        self.changeLiveReview(isLive=True)
        self.AFCoffset_doubleSpinBox.setValue(self.mp.imgSrc.get_autofocus_offset())

    def updatePosition(self):
        self.currPosScatterPlot.clear()
        x,y = self.mp.imgSrc.get_xy()
        d={'pos':(x,y),'symbol':'+','pen':pg.mkPen('m',width=2)}
        self.currPosScatterPlot.addPoints([d])

    def getFramePos(self):
        pos=self.mp.posList.slicePositions[self.section]
        frame=pos.frameList.slicePositions[self.frame]
        return (frame.x,frame.y)
        # issection = self.focus_df['slide_index'] == self.section
        # isframe = self.focus_df['frame_index'] == self.frame
        # goodpos = self.focus_df[issection & isframe]
        # for i, row in goodpos.iterrows():
        #     return row

    def moveToFrame(self,evt=None):
        x,y = self.getFramePos()
        self.mp.imgSrc.set_xy(x,y)
        self.updatePosition()