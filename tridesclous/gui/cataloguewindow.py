import numpy as np

from .myqt import QT
import pyqtgraph as pg

from .cataloguecontroller import CatalogueController
from .traceviewer import CatalogueTraceViewer
from .peaklists import PeakList, ClusterPeakList
from .ndscatter import NDScatter
from .waveformviewer import WaveformViewer
from .similarity import SimilarityView
from .pairlist import PairList
from .silhouette import Silhouette

from .tools import ParamDialog

from . import icons


import itertools
import datetime
import time

class CatalogueWindow(QT.QMainWindow):
    def __init__(self, catalogueconstructor):
        QT.QMainWindow.__init__(self)
        
        self.setWindowIcon(QT.QIcon(':/main_icon.png'))
        
        self.catalogueconstructor = catalogueconstructor
        self.controller = CatalogueController(catalogueconstructor=catalogueconstructor)
        
        self.traceviewer = CatalogueTraceViewer(controller=self.controller)
        self.peaklist = PeakList(controller=self.controller)
        self.clusterlist = ClusterPeakList(controller=self.controller)
        self.ndscatter = NDScatter(controller=self.controller)
        self.waveformviewer = WaveformViewer(controller=self.controller)
        self.similarityview = SimilarityView(controller=self.controller)
        self.pairlist = PairList(controller=self.controller)
        #~ self.silhouette = Silhouette(controller=self.controller)
        
        
        
        docks = {}

        docks['waveformviewer'] = QT.QDockWidget('waveformviewer',self)
        docks['waveformviewer'].setWidget(self.waveformviewer)
        #self.tabifyDockWidget(docks['ndscatter'], docks['waveformviewer'])
        self.addDockWidget(QT.Qt.RightDockWidgetArea, docks['waveformviewer'])
        
        #~ docks['silhouette'] = QT.QDockWidget('silhouette',self)
        #~ docks['silhouette'].setWidget(self.silhouette)
        #~ self.tabifyDockWidget(docks['waveformviewer'], docks['silhouette'])
        
        
        docks['traceviewer'] = QT.QDockWidget('traceviewer',self)
        docks['traceviewer'].setWidget(self.traceviewer)
        #self.addDockWidget(QT.Qt.RightDockWidgetArea, docks['traceviewer'])
        self.tabifyDockWidget(docks['waveformviewer'], docks['traceviewer'])
        
        docks['peaklist'] = QT.QDockWidget('peaklist',self)
        docks['peaklist'].setWidget(self.peaklist)
        self.addDockWidget(QT.Qt.LeftDockWidgetArea, docks['peaklist'])
        
        docks['pairlist'] = QT.QDockWidget('pairlist',self)
        docks['pairlist'].setWidget(self.pairlist)
        self.splitDockWidget(docks['peaklist'], docks['pairlist'], QT.Qt.Horizontal)
        
        docks['clusterlist'] = QT.QDockWidget('clusterlist',self)
        docks['clusterlist'].setWidget(self.clusterlist)
        self.tabifyDockWidget(docks['pairlist'], docks['clusterlist'])
        
        docks['similarityview'] = QT.QDockWidget('similarityview',self)
        docks['similarityview'].setWidget(self.similarityview)
        self.addDockWidget(QT.Qt.LeftDockWidgetArea, docks['similarityview'])
        
        docks['ndscatter'] = QT.QDockWidget('ndscatter',self)
        docks['ndscatter'].setWidget(self.ndscatter)
        self.tabifyDockWidget(docks['similarityview'], docks['ndscatter'])
        
        self.create_actions()
        self.create_toolbar()
        
        
    def create_actions(self):
        #~ self.act_save = QT.QAction(u'Save catalogue', self,checkable = False, icon=QT.QIcon.fromTheme("document-save"))
        self.act_save = QT.QAction(u'Save catalogue', self,checkable = False, icon=QT.QIcon(":/document-save.svg"))
        self.act_save.triggered.connect(self.save_catalogue)

        #~ self.act_refresh = QT.QAction(u'Refresh', self,checkable = False, icon=QT.QIcon.fromTheme("view-refresh"))
        self.act_refresh = QT.QAction(u'Refresh', self,checkable = False, icon=QT.QIcon(":/view-refresh.svg"))
        self.act_refresh.triggered.connect(self.refresh)

        #~ self.act_setting = QT.QAction(u'Settings', self,checkable = False, icon=QT.QIcon.fromTheme("preferences-other"))
        self.act_setting = QT.QAction(u'Settings', self,checkable = False, icon=QT.QIcon.fromTheme(":/preferences-other.svg"))
        self.act_setting.triggered.connect(self.open_settings)

        self.act_new_waveforms = QT.QAction(u'New waveforms', self,checkable = False, icon=QT.QIcon.fromTheme("TODO"))
        self.act_new_waveforms.triggered.connect(self.new_waveforms)

        #~ self.act_new_waveforms = QT.QAction(u'Yep', self,checkable = False, icon=QT.QIcon(":main_icon.png"))
        #~ self.act_new_waveforms.triggered.connect(self.new_waveforms)


    def create_toolbar(self):
        self.toolbar = QT.QToolBar('Tools')
        self.toolbar.setToolButtonStyle(QT.Qt.ToolButtonTextUnderIcon)
        self.addToolBar(QT.Qt.RightToolBarArea, self.toolbar)
        self.toolbar.setIconSize(QT.QSize(60, 40))
        
        self.toolbar.addAction(self.act_save)
        self.toolbar.addAction(self.act_refresh)
        self.toolbar.addAction(self.act_setting)
        #TODO with correct settings (left and right)
        self.toolbar.addAction(self.act_new_waveforms)
    

    def save_catalogue(self):
        self.catalogueconstructor.save_catalogue()
    
    def refresh(self):
        self.controller.reload_data()
        for w in self.controller.views:
            #~ print(w)
            w.refresh()
    
    def open_settings(self):
        _params = [{'name' : 'nb_waveforms', 'type' : 'int', 'value' : 10000}]
        dialog1 = ParamDialog(_params, title = 'Settings', parent = self)
        if not dialog1.exec_():
            return None, None
        
        self.settings = dialog1.get()
    
    def new_waveforms(self):
        pass
        #~ self.catalogueconstructor.extract_some_waveforms(n_left=-12, n_right=15, mode='rand', nb_max=10000)
        #~ self.controller.on_new_cluster()
        #~ self.refresh()

