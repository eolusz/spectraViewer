# -*- coding: utf-8 -*-
import os
import sys
import time
import h5py
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
# Own modules
from .QCustomModels import ImagesModel
from .pyDevices import area_detector, instrument, dummy, detector
from .SpectraViewGUI import Ui_MainWindow
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NToolBar
from matplotlib.pyplot import Line2D
from .pyLogbook import LaserLogBook


QMessageBox=QtWidgets.QMessageBox


class  SpectraViewMain(QtWidgets.QMainWindow, Ui_MainWindow):
    shutter_signal = QtCore.Signal(int)
    trigger_signal = QtCore.Signal(int)
    index = 0
    acq = False
    scaling = True
    index = 0
    _lst = time.time()
    ccd = None
    _n = 0
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.onChangePlotTab(self.tabWidget.currentIndex())
        self.ccd=area_detector()
        self.shutter=instrument("ATAS:PUMPShutter:State")
        self.hhg=instrument("ATAS:HHGShutter:State")
        self.valve=instrument("ATAS:AttoValve:Run")
        self.trigger=instrument("ATAS:Trigger:State")        
        self._images=ImagesModel()
        self.MemorzView.setModel(self._images)
        
        # Required env variables 
        #self.waiting=True
        #self.waitingb=False
        self.cb=None
        self.cb2=None
        #self.accu=False
        self.on=False
        #self.acBusy=False
        self.diff=False
        self.na=True
        self.pon=None
        self.poff=None    
        # Adding the different toolbars
        self.tb=[]
        self.tb.append(NToolBar(self.mpl1,self.mpl1))
        self.tb.append(NToolBar(self.mpl2,self.mpl2))
        self.tb.append(NToolBar(self.mpl3,self.mpl3))

        # Plot related actions
        self.mpl3.figure.clear()
        self.mpl3.axes=self.mpl3.figure.add_subplot(211)
        self.mpl3.axes1=self.mpl3.figure.add_subplot(212)
        self.resetPlots()
        
        #Epics callbacks
        self.ccd.img_cb=self.plotImage
        self.ccd.minX_pv.add_callback(self.onRoiChange, ch=0)
        self.ccd.minY_pv.add_callback(self.onRoiChange, ch=1)
        self.ccd.sizeX_pv.add_callback(self.onRoiChange, ch=2)
        self.ccd.sizeY_pv.add_callback(self.onRoiChange, ch=3)
        self.ccd.binx_pv.add_callback(self.onRoiChange, ch=4)
        self.ccd.biny_pv.add_callback(self.onRoiChange, ch=5)
        self.ccd.ArraySizeX_pv.add_callback(self.arraySizeChange)
        self.ccd.ArraySizeY_pv.add_callback(self.arraySizeChange)
        self.ccd.expTime_pv.add_callback(self.expChange)
        self.ccd.acq_pv.add_callback(self.acqChange)
        self.ccd.accu_pv.add_callback(self.acuChange)
        self.ccd.imgMode_pv.add_callback(self.imageModeChange)
        self.ccd.readMode_pv.add_callback(self.readoutModeChange)
        self.ccd.adcSpeed_pv.add_callback(self.adcChange)
        self.ccd.preAmpGain_pv.add_callback(self.ampGainChange)
        self.ccd.dType_pv.add_callback(self.dTypeChange)

        #Slots and signals
        self.StartButton.clicked.connect(self.startAcq)
        self.AddButton.clicked.connect(self.addImage)
        self.RemoveButton.clicked.connect(self.removeImage)
        self.EntryButton.clicked.connect(self.toLogbook)
        self.PathButton.clicked.connect(self.select_path)        
        self.SaveButton.clicked.connect(self.saveAcq)
        self.BgButton_2.clicked.connect(self.takeBg)
        self.acuRestart.clicked.connect(self.restartAccu)    
        self.tabWidget.currentChanged.connect(self.onChangePlotTab)  
        self.ImagMin.textChanged.connect(self.imgCrange)
        self.ImagMax.textChanged.connect(self.imgCrange)
        self.ProyMin.textChanged.connect(self.proyYrange)
        self.ProyMax.textChanged.connect(self.proyYrange)
        self.LockBox.stateChanged.connect(self.lockChange)
        self.shutter_signal.connect(self.shutterSet)
        self.trigger_signal.connect(self.triggerSet)
        self.PumpButton.clicked.connect(self.setPump)
        self.HHGButton.clicked.connect(self.setHHG)
        self.pushButton.clicked.connect(self.setValve)
 
        self.popMenu = QtWidgets.QMenu( self )
        self.actionScale=self.popMenu.addAction("Fix scale", self.on_scale_action)
        self.initial_pvReadOut()

    #GUI related function--------------------------------------------------------------------------------------------
    def on_scale_action(self):
        self.scaling=not(self.scaling)
        txt="Autoscale"
        if self.scaling:
            txt="Fix scale"
        self.actionScale.setText(txt)

    def contextMenuEvent(self, event):
        self.popMenu.exec_( self.centralwidget.mapToGlobal(event.pos()))

    #Slots*-----------------------------------------------------------------------------------------

    def takeBg(self):
        if self.bg:
            self.bg=False
            self.BgButton_2.setText("Take Bg")
            return
        self.bg_image = self.dt
        self.bg=True
        self.BgButton_2.setText('Remove Bg')

    def select_path(self):
        self.PathEdit.setText(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))


    def onChangePlotTab(self, index):
		
        if self.ccd is None:
           return

        if index==0:
            self.ccd.img_cb = self.plotImage

        elif index==1:
            self.ccd.img_cb = self.plotProyection

        elif index==2:
            self.ccd.img_cb = self.plotAccu
            
        elif index==3:
            self.ccd.img_cb = self.takeBg
			
        elif index==4:
            self.ccd.img_cb = self.plotLocking
            
        else:
            self.ccd.img_cb = dummy

    def addImage(self):
        self._images.insertImage([self.dt],self._xaxis, self.mpl2.axes)
        self.mpl2.draw()

    def removeImage(self):
        index=self.MemorzView.currentIndex().row()
        self._images.removeRows(index ,1)

    def restartAccu(self):
        self.accuImg=np.zeros((self.ccd.sizey, self.ccd.sizex))

    def setPump(self):
        st=self.shutter.state.get()
        if st:
            self.shutter.state.put(0)
            self.PumpButton.setText("Pump (Open)")
        else:
            self.shutter.state.put(1)
            self.PumpButton.setText("Pump (Close)")

    def setHHG(self):
        st=self.hhg.state.get()
        if st:
            self.hhg.state.put(0)
            self.HHGButton.setText("HHG (Open)")
        else:
            self.hhg.state.put(1)
            self.HHGButton.setText("HHG (Close)")

    def setValve(self):
        st=self.valve.state.get()
        if st:
            self.valve.state.put(0)
            self.pushButton.setText("Valve (Open)")
        else:
            self.valve.state.put(1)
            self.pushButton.setText("Valve (Close)")
    
    #EPICS related functions--------------------------------------------------------------------------------------------
    def initial_pvReadOut(self):
        self.X0Edit.setText("%d"%self.ccd.minX_pv.get())
        self.Y0Edit.setText("%d"%self.ccd.minY_pv.get())
        self.X1Edit.setText("%d"%self.ccd.sizeX_pv.get())
        self.Y1Edit.setText("%d"%self.ccd.sizeY_pv.get())
        self.XBinningEdit.setText("%d"%self.ccd.binx_pv.get())
        self.YBinningEdit.setText("%d"%self.ccd.biny_pv.get())
        self.ExposureEdit.setValue(self.ccd.expTime_pv.get())
        self.AcuEdit.setValue(self.ccd.accu_pv.get())
        self.PreAmpBox.addItems(self.ccd.preAmpGain_pv.enum_strs)
        self.PreAmpBox.setCurrentIndex(self.ccd.preAmpGain_pv.get())
        self.ADCBox.addItems(self.ccd.adcSpeed_pv.enum_strs)
        self.ADCBox.setCurrentIndex(self.ccd.adcSpeed_pv.get())
        self.dTypeBox.addItems(self.ccd.dType_pv.enum_strs)
        self.dTypeBox.setCurrentIndex(self.ccd.dType_pv.get())

        self.ImageModeBox.addItems(self.ccd.imgMode_pv.enum_strs)
        self.ImageModeBox.setCurrentIndex(self.ccd.imgMode_pv.get())
        self.ReadoutModeBox.addItems(self.ccd.readMode_pv.enum_strs)
        self.ReadoutModeBox.setCurrentIndex(self.ccd.readMode_pv.get())

    def onRoiChange(self, **kw):
        if kw["ch"]==0:
            self.X0Edit.setText("%d"%kw['value'])
        elif kw["ch"]==1:
            self.Y0Edit.setText("%d"%kw['value'])
        elif kw["ch"]==2:
            self.X1Edit.setText("%d"%kw['value'])
        elif kw["ch"]==3:
            self.Y1Edit.setText("%d"%kw['value'])
        elif kw["ch"]==4:
            self.XBinningEdit.setText("%d"%kw['value'])
        elif kw["ch"]==5:
            self.YBinningEdit.setText("%d"%kw['value'])

    def arraySizeChange(self, **kw):
        self.bg=False
        self.reset_plots()
    
    def acqChange(self, **kw):
        if kw["value"]:
            self.StartButton.setText("Stop acq.")
            self.acq=True
        else:
            self.StartButton.setText("Acquire")
            self.acq=False

    def expChange(self, **kw):
        self.ExposureEdit.setValue(kw["value"])

    def acuChange(self, **kw):
        self.AcuEdit.setValue(kw["value"])
    
    def imageModeChange(self, **kw):
        self.ImageModeBox.setCurrentIndex(kw["value"])

    def readoutModeChange(self, **kw):
        self.ReadoutModeBox.setCurrentIndex(kw["value"])

    def adcChange(self, **kw):
        self.ADCBox.setCurrentIndex(kw["value"])

    def dTypeChange(self, **kw):
        self.dTypeBox.setCurrentIndex(kw["value"])

    def ampGainChange(self, **kw):
        self.PreAmpBox.setCurrentIndex(kw["value"])

    def shutterSet(self, value):
        self.shutter.state.put(value)
        time.sleep(0.5)
        self.toSet=False

    def triggerSet(self, value):
        self.trigger.state.put(value)
        
    def startAcq(self):
        if self.acq:
            self.ccd.acq_pv.put(0)
        else:
            self.ccd.acq_pv.put(1)


    def lockChange(self, state):
        self.diff=state
        self.on=self.shutter.getState()


    #plotting related functions----------------------------------------------------------------------------------- 
    def plotImage(self, dt):
        self.dt = dt
        if time.time()-self._lst<0.1:
            return
        self._lst = time.time()
        self.im.set_data(self.dt)
        if self.scaling:
            self.scaleImage()                
        self.mpl1.draw()

    def plotProyection(self, dt):
        if time.time()-self._lst<0.1:
            return
        self._lst = time.time()
        self.dt = dt
        self.prd = self.dt.mean(axis=0)
        self.pry.set_ydata(self.prd)
        if self.scaling:
            self.scaleProy()
        self.mpl2.draw()

    def plotAccu(self, dt):
        self.dt
        self.accuImg = (self.accuImg * self._n) + self.dt
        self._n += 1
        self.accuImg /= self._n
        if time.time()-self._lst<0.1:
            return
        self._lst = time.time()
        self.accuPry = self.accuImg.mean(axis=0)
        self.imA.set_data(self.accuImg)
        if self.scaling:
            self.scaleAccu()
        self.pryA.set_ydata(self.accuPry)
        self.mpl3.draw()


    def plotLockin(self, dt):
        self.dt = dt
        if self.on:                    
            self.pon = self.dt
            self.toSet = True
            self.shutter_signal.emit(0)
            while self.toSet:
                time.sleep(0.1)
            self.trigger_signal.emit(1)
            self.on = False
            
        else:
            self.poff = self.dt
            self.toSet = True
            self.shutter_signal.emit(1)
            while self.toSet:
                time.sleep(0.1)
            self.trigger_signal.emit(1)
            self.on = True

        if self.pon is None or self.poff is None:
            return True
            
        dt = np.log10(self.pon/self.poff)
        self.pon = None
        self.poff = None
        return False



    def plotOthers(self):
        for i in self._images._lines:
            self.mpl2.axes.add_line(i)

    def imgCrange(self):
        self.cb.set_clim(int(self.ImagMin.text()),int(self.ImagMax.text()))
        self.cb.draw_all()

    def proyYrange(self):
        if self.na:
            self.mpl2.axes.set_ylim(float(self.ProyMin.text()),float(self.ProyMax.text()))            

    def resetPlots(self,p=False):
        self.mpl1.axes.clear()
        self._xaxis=np.arange(self.ccd.sizex)
        self._yaxis=np.arange(self.ccd.sizey)
        if self.ccd.sizey<2:
            self.im=self.mpl1.axes.imshow(200* np.random.rand(self.ccd.sizey, self.ccd.sizex), aspect="auto")
        else:
            self.im=self.mpl1.axes.pcolorfast(self._xaxis, self._yaxis,200* np.random.rand(self.ccd.sizey, self.ccd.sizex))
        if self.cb is not None:
            self.cb.remove()            
        self.cb = self.mpl1.axes.figure.colorbar(self.im)
        self.pry = self.mpl2.axes.plot(self._xaxis, self._xaxis)[0]
        self.accuImg = np.zeros((self.ccd.sizey, self.ccd.sizex))
        self._n = 0
        if self.ccd.sizey<200:
            self.imA=self.mpl3.axes1.imshow(self.accuImg, aspect="auto")
        else:
            self.imA=self.mpl3.axes1.pcolormesh(self._xaxis, self._yaxis,self.accuImg)

        if self.cb2 is not None:
            self.cb2.remove()
        self.cb2=self.mpl3.axes1.figure.colorbar(self.imA)
        self.pryA=self.mpl3.axes.plot(self._xaxis, self._xaxis)[0]

    def scaleImage(self):
        m0=self.dt.min()
        m1=self.dt.max()
        self.cb.set_clim(vmin=m0, vmax=m1)
        self.cb.draw_all()
        self.ImagMin.setText("%d"%m0)
        self.ImagMax.setText("%d"%m1)
    
    def scaleAccu(self):
        m0=self.accuImg.min()
        m1=self.accuImg.max()
        self.cb2.set_clim(vmin=m0, vmax=m1)
        self.cb2.draw_all()
        self.ImagMin_2.setText("%.1f"%m0)
        self.ImagMax_2.setText("%.1f"%m1)
        self.mpl3.axes.set_ylim(self.accuPry.min(), self.accuPry.max())

    def scaleProy(self):
        m0=self.prd.min()
        m1=self.prd.max()
        self.mpl2.axes.set_ylim(m0, m1)
        self.na=False
        self.ProyMin.setText("%.2f"%m0)
        self.ProyMax.setText("%.2f"%m1)
        self.na=True


    
    #Saving related Slots---------------------------------------------------------------------------------------------------------
    def saveAcq(self, name=None):
        print("Saving...")
        self.ccd.img_cb=dummy
        path=self.PathEdit.text()
        if path[-1]=="/":
            path=path[:-1]

        self.fname=name
        if name==None or name==False:
            self.fname=self.NameEdit.text()
        if self.fname[-3:]==".h5":
            self.fname=self.fname[:-3]
        self.fh=h5py.File("%s/%s.h5"%(path,self.fname),"a")        
        self.fh.require_dataset("%s/LastData/Array"%self.dataSetEdit.text(), self.dt.shape, self.dt.dtype, data=self.dt )
        self.fh.require_dataset("%s/AccuData/Array"%self.dataSetEdit.text(), self.accuImg.shape, self.accuImg.dtype, data=self.accuImg)
        for i in self.ccd.pvs:
            self.fh["%s"%self.dataSetEdit.text()].attrs.create(i.pvname, np.string_(i.get(as_string=True)))
        self.fh["%s"%self.dataSetEdit.text()].attrs.create("Comments", self.CommentTextEdit.toPlainText().encode())
        self.fh.close()
        self.ccd.img_cb = self.plotImage

    def toLogbook(self):
        now=time.localtime()
        self.ccd.img_cb=dummy
        path=self.PathEdit.text()
        self.saveAcq(name="%4d-%02d-%02d_%02d%02d%02d"%(now[0],now[1],now[2],now[3],now[4],now[5]))
        self.logDialog=PyLogbook.LaserLogBook()
        self.mpl3.figure.savefig("%s/accu.png"%path)
        self.mpl2.figure.savefig("%s/proyections.png"%path)
        self.mpl1.figure.savefig("%s/image.png"%path)        
        self.logDialog.addAttachment("%s/image.png"%path)
        self.logDialog.addAttachment("%s/accu.png"%path)
        self.logDialog.addAttachment("%s/proyections.png"%path)
        self.logDialog.typeEdit.setText("Measurement")
        self.logDialog.subjectEdit.setText("SpectraViewer-Snapshot")
        self.logDialog.messageEdit.insertPlainText("Data saved on: %s/%s.h5\n"%(path,self.fname))
        self.logDialog.show()
        self.ccd.img_cb = self.plotImage
        
debug=False

class  SpectraViewMainB(QtWidgets.QMainWindow, Ui_MainWindow):
    shutter_signal = QtCore.Signal(int)
    trigger_signal = QtCore.Signal(int)
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

def run():
    ui = SpectraViewMain()
    ui.show()    

if debug:
    app = QtWidgets.QApplication(sys.argv)
    ui = SpectraViewMainB()
    ui.show()
    #from threading import Thread
    #r=Thread(target=run) 
    #r.start()
    #ui = SpectraViewMain()
    #ui.show()
    

if not(debug):
    app = QtWidgets.QApplication(sys.argv)
    print(sys.argv)
    confFile="current_conf.h5"    
    if sys.argv[1:]:
        print(sys.argv[1])
        confFile=sys.argv[1]
    ui = SpectraViewMain()
    ui.show()
    app.exec_()
    #sys.exit()
