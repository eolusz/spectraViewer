from epics import PV
import numpy as np
import time
from sys import stdout, platform

#if platform=='win32':
import configparser
#else:
#	import ConfigParser
import os
import threading

def dummy(*pa):
	pass


def default_writer(text):
	stdout.write("\r\x1b[K"+text.__str__())
	stdout.flush()

class instrument(object):
	def __init__(self, state_pv):
		self.state=PV(state_pv)
		self.writer=default_writer

	def write(self, text):
		self.writer("Instrument: %s"%text)

	def open(self):
		self.state.put(1)
	
	def close(self):
		self.state.put(0)
	
	def getState(self):
		return self.state.get()

	def checkPVs(self):
		if not(self.state.connected):
			print("Instrument:  state_pv is not connected")
			return True
		return False

	def setState(self, state):
		self.state.put(state)


class detector(object):
	def __init__(self, port="ATAS", cam="SENSI", array="", hdf1=""):
		"""Initilatization of a simple detector:
		acquire_pv: for starting acq
		status_pv:  to know acq is finish
		prefix_pv: prefix of data files"""
		#Detector pvs
		self.port=port
		self.cam=cam
		self.pvs=[]
		self.acq_pv=PV("%s:%s:ACQUIRE"%(port, cam))
		self.pvs.append(self.acq_pv)
		#self.expPeriod_pv=PV("%s:%s:AcquirePeriod_RBV"%(port, cam))
		#self.pvs.append(self.expPeriod_pv)				
		self.acqRBV_pv=PV("%s:%s:ACQUIRE_RB"%(port, cam))
		self.pvs.append(self.acqRBV_pv)
		self.expTime_pv=PV("%s:%s:EXPOSURE"%(port, cam))
		self.pvs.append(self.expTime_pv)
		#self.accu_pv=PV("%s:%s:NumExposures"%(port, cam))
		#self.pvs.append(self.accu_pv)
		self.numImages_pv=PV("%s:%s:ImageCounter"%(port, cam))
		self.pvs.append(self.numImages_pv)
		#self.imgMode_pv=PV("%s:%s:ImageMode"%(port, cam))
		#self.pvs.append(self.imgMode_pv)
		#self.readMode_pv=PV("%s:%s:AndorReadOutMode"%(port, cam))
		#self.pvs.append(self.readMode_pv)
		#self.trigger_pv=PV("%s:%s:TriggerMode"%(port, cam))
		#self.pvs.append(self.trigger_pv)
		self.sizeX_pv=PV("%s:%s:SIZEX"%(port, cam))
		self.pvs.append(self.sizeX_pv)
		self.sizeY_pv=PV("%s:%s:SIZEY"%(port, cam))
		self.pvs.append(self.sizeY_pv)
		self.minX_pv=PV("%s:%s:ROI_X1"%(port, cam))
		self.pvs.append(self.minX_pv)
		self.minY_pv=PV("%s:%s:ROI_Y1"%(port, cam))
		self.polling_pv=PV("%s:%s:POLLING"%(port, cam))
		#self.temp_pv=PV("%s:%s:TemperatureActual"%(port, cam))
		#self.pvs.append(self.temp_pv)
		self.binx_pv=PV("%s:%s:BINX"%(port, cam))
		self.pvs.append(self.binx_pv)
		self.biny_pv=PV("%s:%s:BINY"%(port, cam))
		self.pvs.append(self.biny_pv)
		#self.numExp_pv=PV("%s:%s:NumExposuresCounter_RBV"%(port,cam))
		#self.pvs.append(self.numExp_pv)
		self.sizex=2048
		self.sizey=512
		self.img_cb=dummy
		#NDArrayStd
		#self.dataType_pv=PV("%s:%s:DataType_RBV"%(port, array))
		#H5File
		#self.filePath_pv=PV("%s:%s:FilePath"%(port, hdf1))
		#self.filePathRBV_pv=PV("%s:%s:FilePathExits_RBV"%(port, hdf1))
		#self.fileName_pv=PV("%s:%s:FileName"%(port, hdf1))
		#self.sizex=self.sizeX_pv.get()
		#self.sizey=self.sizeY_pv.get()
		
		self.expTime_pv.add_callback(self.AutoSaveCallback)
		self.sizeX_pv.add_callback(self.change_sizeX)
		self.sizeY_pv.add_callback(self.change_sizeY)
		self.sizex=self.sizeX_pv.get()
		self.sizey=self.sizeY_pv.get()
		self.arrayData_pv.add_callback(self.newImage)
		self.acqRBV_pv.add_callback(self.StatusCallback)	
		self.arrayData_pv=PV("%s:%s:LASTIMAGE"%(port, cam), auto_monitor=True)
		self.writer=default_writer
		
		
		self.dtype=np.uint16
		
	def setDataCB(self):
		pass
		
		
	
	def write(self, text):
		self.writer("Detector: %s"%text)		

	def setEta(self):
		self.eta=self.expTime_pv.get()

	def change_sizeX(self, **kw):
		self.sizex=kw["value"]

	def change_sizeY(self, **kw):
		self.sizey=kw["value"]

	def getStatus(self):
		return self.status_pv.get()
	
	def StatusCallback(self, **kw):
		self.status=kw["value"]

	def AutoSaveCallback(self, **kw):
		self.autosave=kw["value"]

	def getImage(self):
		return self.arrayData_pv.get()

	def newImage(self, **kw):
		#self.polling_pv.put(0)		
		self.img=kw["value"].reshape(self.sizey, self.sizex)
		self.waiting=False
		self.img_cb(self.img)
		#self.polling_pv.put(1)


	def AcquireAndWait(self):
		#self.acq_pv.put(1)
		self.waiting=True
		while self.waiting:
			time.sleep(0.001)
			pass
		return True

	def WaitNew(self):
		self.waiting=True
		while self.waiting:
			pass
		return True

	def checkPVs(self):
		for i in self.pvs:
			if not(i.connected):
				self.write("%s is not connected"%i.pvname)
				return True		
		return False


class area_detector(object):
	def __init__(self, port="13ANDOR1", cam="cam1", array="image1", hdf1="HDF1"):
		"""Initilatization of a simple detector:
		acquire_pv: for starting acq
		status_pv:  to know acq is finish
		prefix_pv: prefix of data files"""
		#Detector pvs
		self.pvs=[]
		self.acq_pv=PV("%s:%s:Acquire"%(port, cam))
		self.pvs.append(self.acq_pv)
		self.acqRBV_pv=PV("%s:%s:AcquireBusy"%(port, cam))
		self.pvs.append(self.acqRBV_pv)

		self.expPeriod_pv=PV("%s:%s:AcquirePeriod_RBV"%(port, cam))
		self.pvs.append(self.expPeriod_pv)				
		self.expTime_pv=PV("%s:%s:AcquireTime"%(port, cam))
		self.pvs.append(self.expTime_pv)
		self.accu_pv=PV("%s:%s:NumExposures"%(port, cam))
		self.pvs.append(self.accu_pv)
		self.numExp_pv=PV("%s:%s:NumExposuresCounter_RBV"%(port,cam))
		self.pvs.append(self.numExp_pv)		
		self.numImages_pv=PV("%s:%s:NumImages"%(port, cam))
		self.pvs.append(self.numImages_pv)

		self.imgMode_pv=PV("%s:%s:ImageMode"%(port, cam))
		self.pvs.append(self.imgMode_pv)
		self.readMode_pv=PV("%s:%s:AndorReadOutMode"%(port, cam))
		self.pvs.append(self.readMode_pv)
		self.trigger_pv=PV("%s:%s:TriggerMode"%(port, cam))
		self.pvs.append(self.trigger_pv)

		self.minX_pv=PV("%s:%s:MinX"%(port, cam))
		self.pvs.append(self.minX_pv)
		self.minY_pv=PV("%s:%s:MinY"%(port, cam))
		self.pvs.append(self.minY_pv)		
		self.sizeX_pv=PV("%s:%s:SizeX_RBV"%(port, cam))
		self.pvs.append(self.sizeX_pv)
		self.sizeY_pv=PV("%s:%s:SizeY_RBV"%(port, cam))
		self.pvs.append(self.sizeY_pv)
		self.binx_pv=PV("%s:%s:BinX"%(port, cam))
		self.pvs.append(self.binx_pv)
		self.biny_pv=PV("%s:%s:BinY"%(port, cam))
		self.pvs.append(self.biny_pv)

		self.preAmpGain_pv=PV("%s:%s:AndorPreAmpGain_RBV"%(port, cam))
		self.pvs.append(self.preAmpGain_pv)
		self.adcSpeed_pv=PV("%s:%s:AndorADCSpeed_RBV"%(port, cam))
		self.pvs.append(self.adcSpeed_pv)
		
		self.temp_pv=PV("%s:%s:TemperatureActual"%(port, cam))
		self.pvs.append(self.temp_pv)



		#NDArrayStd
		self.img_cb=dummy
		self.ArraySizeX_pv=PV("%s:%s:ArraySizeX_RBV"%(port, cam))
		self.pvs.append(self.ArraySizeX_pv)
		self.ArraySizeY_pv=PV("%s:%s:ArraySizeY_RBV"%(port, cam))
		self.pvs.append(self.ArraySizeY_pv)
		self.sizex=self.ArraySizeX_pv.get()
		self.sizey=self.ArraySizeY_pv.get()
		self.arrayData_pv=PV("%s:%s:ArrayData"%(port, array),callback=self.newImage, auto_monitor=True)
		self.dType_pv=PV("%s:%s:DataType_RBV"%(port, cam))				
		self.pvs.append(self.dType_pv)

		self.filePath_pv=PV("%s:%s:FilePath"%(port, hdf1))
		self.filePathRBV_pv=PV("%s:%s:FilePathExits_RBV"%(port, hdf1))
		self.fileName_pv=PV("%s:%s:FileName"%(port, hdf1))
		
		self.expTime_pv.add_callback(self.AutoSaveCallback)
		self.ArraySizeX_pv.add_callback(self.change_sizeX)
		self.ArraySizeY_pv.add_callback(self.change_sizeY)
		self.acqRBV_pv.add_callback(self.StatusCallback)
		self.writer=default_writer
		if self.setDataType():
			self.write("Error obtaining data type")

	def setDataType(self):
		dtype=self.dType_pv.enum_strs[self.dType_pv.get()]
		if dtype=='UInt16':
			self.dtype=np.uint16
		elif dtype=='UInt32':
			self.dtype=np.uint32
		else:
			return True
		return False
		
		

	def write(self, text):
		self.writer("Detector: %s"%text)		

	def setEta(self):
		self.eta=self.expPeriod_pv.get()

	def change_sizeX(self, **kw):
		self.sizex=kw["value"]

	def change_sizeY(self, **kw):
		self.sizey=kw["value"]
		if kw["value"]<1:
			self.sizey=1		

	def getStatus(self):
		return self.status_pv.get()
	
	def StatusCallback(self, **kw):
		self.status=kw["value"]

	def AutoSaveCallback(self, **kw):
		self.autosave=kw["value"]

	def getImage(self):
		return self.arrayData_pv.get()

	def newImage(self, **kw):		
		self.img=kw["value"].reshape(self.sizey, self.sizex)
		self.waiting=False
		self.img_cb(self.img)


	def AcquireAndWait(self):
		self.acq_pv.put(1)
		self.waiting=True
		while self.waiting:
			pass
		return True

	def WaitNew(self):
		self.waiting=True
		while self.waiting:
			pass
		return True

	def checkPVs(self):
		for i in self.pvs:
			if not(i.connected):
				self.write("%s is not connected"%i.pvname)
				return True		
		return False
	



class detector_old(object):
	def __init__(self, pvs):
		"""Initilatization of a simple detector:
		acquire_pv: for starting acq
		status_pv:  to know acq is finish
		prefix_pv: prefix of data files"""
		self.writer=default_writer
		
		self.connect_pvs(pvs)
		self.connect_callbacks()

		self.sizex=self.sizex_pv.get()
		self.sizey=self.sizey_pv.get()
		self.n_acq=10	
		self.autosave=False

	def connect_pvs(self, pvs):
		self.writer("Connecting pvs...")
		self.acq_pv=PV(pvs[0])
		self.path_pv=PV(pvs[1])
		self.pathRB_pv=PV(pvs[2])
		self.fileName_pv=PV(pvs[3])
		self.fileNameRB_pv=PV(pvs[4])
		self.groupName_pv=PV(pvs[5])
		self.groupNameRB_pv=PV(pvs[6])
		self.status_pv=PV(pvs[7])
		self.fileIndex_pv=PV(pvs[8])
		self.autoSave_pv=PV(pvs[9])
		self.imgxstep_pv=PV(pvs[10])
		self.exposure_pv=PV(pvs[11])
		self.setAttr_pv=PV(pvs[12])
		self.lastImage_pv=PV(pvs[13])
		self.Image_pv=PV(pvs[14], auto_monitor=True)
		self.sizex_pv=PV(pvs[15])
		self.sizey_pv=PV(pvs[16])
		self.roix1_pv=PV(pvs[17])
		self.roix2_pv=PV(pvs[18])
		self.roiy1_pv=PV(pvs[19])
		self.roiy2_pv=PV(pvs[20])
		self.writer("Done...")

	def connect_callbacks(self):
		self.writer("Setting callbacks...")
		self.sizex_pv.add_callback(self.gsizex)
		self.sizey_pv.add_callback(self.gsizey)
		self.last_acq=self.fileIndex_pv.get()
		self.autoSave_pv.add_callback(self.AutoSaveCallback)
		self.status_pv.add_callback(self.StatusCallback)
		self.writer("Callbacks, Done.")
	
		

	def gsizex(self, **kw):
		self.sizex=kw['value']


	def gsizey(self, **kw):
		self.sizey=kw['value']


	def write(self, text):
		self.writer("Detector: %s"%text)		

	def setEta(self):
		self.eta=0.002*self.n_acq*self.exposure_pv.get()


	def getStatus(self):
		return self.status_pv.get()
	
	def StatusCallback(self, **kw):
		self.status=kw["value"]

	def AutoSaveCallback(self, **kw):
		self.autosave=kw["value"]


	def Wait(self): 
		t=time.time()
		while self.autosave:
			if time.time()>t+self.eta:
				t=time.time()
				self.write("Too long exposure, checking...")
				if (self.fileIndex_pv.get()>=self.n_acq-1):
					self.write("Yes, was done")
					self.set_autosave(False)
			pass	
		return False

	def createGroup(self, name):
		o=time.time()
		self.groupName_pv.put(name)
		if self.groupNameRB_pv.get()>1:
			self.write("Error creating group")
			return True			
		return False

	def set_autosave(self, val):	
			self.autoSave_pv.put(val, wait=True)



	def checkPVs(self):
		
		if not(self.fileIndex_pv.connected):
			self.write("fileIndex PV is not connected")
			return True

		if not(self.fileName_pv.connected):
			self.write("fileName PV is not connected")
			return True

		if not(self.status_pv.connected):
			self.write("status PV is not connected")
			return True

		if not(self.fileNameRB_pv.connected):
			self.write("openFilerb  PV is not connected")
			return True

		if not(self.groupNameRB_pv.connected):
			self.write("groupNameRB PV is not connected")
			return True


		if not(self.groupName_pv.connected):
			self.write("groupName PV is not connected")
			return True

		if not(self.autoSave_pv.connected):
			self.write("autoSave PV is not connected")
			return True			
			

		return False
	



class knob(object):
	def __init__(self, set_pv, read_pv, status_pv, settle=0.1):
		"""Initilatization of a simple knob:
		set_pv: for starting acq
		status_pv:  to know acq is finish
		read_pv: prefix of data files"""
		self.ready=False
		self.set_pv=PV(set_pv)
		self.read_pv=PV(read_pv)
		self.status_pv=PV(status_pv)
		self.settle=settle
		self.writer=default_writer

	def write(self, text):
		self.writer("Knob: %s"%text)

	
	def getPos(self):
		return self.read_pv.get()
	
	def moveWait(self, pos):
		self.set_pv.put(pos)
		while(self.status_pv.get()):
			time.sleep(self.settle)

	def checkPVs(self):
		if not(self.set_pv.connected):
			self.write("SetPos PV is not connected")
			return True
		
		if not(self.read_pv.connected):
			self.write("ReadPos PV is not connected")
			return True

		if not(self.status_pv.connected):
			self.write("Status PV is not connected")
			return True

		return False



class notebook(object):
	def __init__(self, fiberIn_pv, fiberOut_pv, fiberPressure_pv, generationMedium_pv, sample_pv, ffilter_pv, specFilter_pv, MCPvoltage_pv, screenVolatage_pv, valveDelay_pv, valveVoltage_pv, valveDuration_pv):
		self.fiberIn_pv          = PV(fiberIn_pv) 
		self.fiberOut_pv         = PV(fiberOut_pv)
		self.fiberPressure_pv    = PV(fiberPressure_pv)
		self.generationMedium_pv = PV(generationMedium_pv)
		self.sample_pv 		 = PV(sample_pv)
		self.ffilter_pv 	 = PV(ffilter_pv)
		self.specFilter_pv 	 = PV(specFilter_pv)
		self.MCPvoltage_pv 	 = PV(MCPvoltage_pv)
		self.screenVolatage_pv   = PV(screenVolatage_pv)
		self.valveDelay_pv 	 = PV(valveDelay_pv)
		self.valveVoltage_pv	 = PV(valveVoltage_pv)
		self.valveDuration_pv	 = PV(valveDuration_pv)
		self.writer=default_writer

	def write(self, text):
		self.writer("Notebook: %s"%text)


	def getFiberIn(self):
		return self.fiberIn_pv.get()

	def getFiberOut(self):
		return self.fiberOut_pv.get()

	def getFiberPressure(self):
		return self.fiberPressure_pv.get()

	def getGenMedium(self):
		return self.generationMedium_pv.get()

	def getSample(self):
		return self.sample_pv.get()

	def getFilter(self):
		return self.ffilter_pv.get()

	def getSpecFilter(self):
		return self.specFilter_pv.get()

	def getMCPvolt(self):
		return self.MCPvoltage_pv.get()

	def getScreenVolt(self):
		return self.screenVolatage_pv.get()

	def getScreenVolt(self):
		return self.screenVolatage_pv.get()

	def getScreenVolt(self):
		return self.screenVolatage_pv.get()

	def getValveDelay(self):
		return self.valveDelay_pv.get()

	def getValveVoltage(self):
		return self.valveVoltage_pv.get()

	def getValveDuration(self):
		return self.valveDuration_pv.get()
	
	def checkPVs(self):
		if not(self.fiberIn_pv.connected):
			self.write("FIBERINPUT is not connected: %s"%self.fiberIn_pv.pvname)
			return True
		if not(self.fiberOut_pv.connected):
			self.write("FIBEROUTPUT is not connected")
			return True
		if not(self.fiberPressure_pv.connected):
			self.write("FIBERPRESSURE is not connected")
			return True
		if not(self.generationMedium_pv.connected):
			self.write("GenerationMedium is not connected")
			return True
		if not(self.sample_pv.connected):
			self.write("SAMPLE is not connected")
			return True
		if not(self.ffilter_pv.connected):
			self.write("FFILTER is not connected")
			return True
		if not(self.specFilter_pv.connected):
			self.write("SPECFILTER is not connected")
			return True
		if not(self.MCPvoltage_pv.connected):
			self.write("MCPVOLTAGE is not connected")
			return True
		if not(self.screenVolatage_pv.connected):
			self.write("SCREENVOLTAGE is not connected")
			return True
		if not(self.valveVoltage_pv.connected):
			self.write("ValveDelay is not connected")
			return True
		if not(self.valveDuration_pv.connected):
			self.write("ValveVoltage is not connected")
			return True
		return False
	



		
def cb():
	pass



prefix="ATAS:"
detector_append=["ACQUIRE","PATH", "PATH_RB", "H5NAME","H5NAME_RB", "H5GROUPNAME", "H5GROUPNAME_RB", "Status", "FileIndex", "AUTOSAVE", "IMGXSTEP","EXPOSURE", "H5SETATTR", "LASTIMAGE", "IMAGE", "SIZEX", "SIZEY", "ROI_X1", "ROI_X2", "ROI_Y1", "ROI_Y2"]
camera_pvs=["ATAS:SENSI:%s"%i for i in detector_append]
knobs_pvs=["PIEZO:SetPos", "PIEZO:GetPos", "PIEZO:Status"]
shutter_pvs=["PUMPShutter:State"]
valve_pvs=["AttoValve:Run"]
notebook_pvs = ["NOTES:FIBERINPUT","NOTES:FIBEROUTPUT", "NOTES:FIBERPRESSURE","NOTES:GenerationMedium", "NOTES:SAMPLE", "NOTES:FFILTER", "NOTES:SPECFILTER", "NOTES:MCPVOLTAGE", "NOTES:SCREENVOLTAGE", "AttoValve:Delay", "AttoValve:Voltage", "AttoValve:Duration"]  
#	def __init__(self,  fileName_pv, fileNameRB_pv, groupName_pv, groupNameRB_pv,  status_pv, fileIndex_pv, autosave_pv):
#sensicam=detector(camera_pvs)
#piezo_e709=knob("%s%s"%(prefix,knobs_pvs[0]), "%s%s"%(prefix,knobs_pvs[1]), "%s%s"%(prefix,knobs_pvs[2]))
#PumpShutter=instrument("%s%s"%(prefix,shutter_pvs[0]))
#AttoValve=instrument("%s%s"%(prefix,valve_pvs[0]))
#instruments=[AttoValve, PumpShutter]

infobook=notebook("%s%s"%(prefix,notebook_pvs[0]), "%s%s"%(prefix,notebook_pvs[1]), "%s%s"%(prefix,notebook_pvs[2]), "%s%s"%(prefix,notebook_pvs[3]), "%s%s"%(prefix,notebook_pvs[4]), "%s%s"%(prefix,notebook_pvs[5]), "%s%s"%(prefix,notebook_pvs[6]), "%s%s"%(prefix, notebook_pvs[7]), "%s%s"%(prefix, notebook_pvs[8]), "%s%s"%(prefix, notebook_pvs[9]), "%s%s"%(prefix, notebook_pvs[10]), "%s%s"%(prefix, notebook_pvs[11]))  




