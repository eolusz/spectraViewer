
from PyQt5 import QtCore
import numpy as np
from matplotlib.pyplot import Line2D
from itertools import cycle


class integration:

	def __init__(self, datas, pos, uniques, areas, I0=None):
		self.pos=pos
		self.uniques=uniques
		self.areas=areas
		self.na=len(self.areas)
		self.integrate_data(datas)
		self.norm=[1.0 for i in range(self.na)]
		self.I0area=I0

	def integrate_datab(self, datas):
		self.datas=[[] for i in range(self.na)]
		self.avg=[[] for i in range(self.na)]
		self.std=[[] for i in range(self.na)]
		for i in datas:
			for j in range(self.na):
				self.datas[j].append(i[self.areas[j][1],self.areas[j][0]].sum())
		self.datas=np.array(self.datas)

	def average_data(self):
		self.norm=[[] for i in range(self.na)]
		self.n_std=[[] for i in range(self.na)]
		self.norm_avg=[[] for i in range(self.na)]
		self.norm_std=[[] for i in range(self.na)]
		for i in range(self.na):
			for j in self.uniques:
				self.avg[i].append(np.average(self.datas[i][j],axis=0))
				self.std[i].append(np.std(self.datas[i][j],axis=0))
		self.avg=np.array(self.avg)
		self.std=np.array(self.std)


	def get_norm(self, beg, end, area):
		return self.avg[area][beg:end].mean(), self.avg[area][beg:end].std()

	def norm_data(self, norm, n_std, area):
		self.norm_avg[area]=self.avg[area]/(1.0*norm)
		self.norm_std[area]=np.power(np.power(self.std[area],2)+np.power(n_std*self.avg[area]/(1.0*norm),2),.5)/(1.0*norm)


	def integrate_data(self, datas):
		self.datas=[[] for i in range(self.na)]
		self.avg=[[] for i in range(self.na)]
		self.std=[[] for i in range(self.na)]
		for i in datas:
			for j in range(self.na):
				self.datas[j].append(0)
				for k in range(len(self.areas[j][0])):
					self.datas[j][-1]+=i[self.areas[j][1]].T[self.areas[j][0][k]].sum()
		self.datas=np.array(self.datas)

	def integrate_data_n(self, datas):
		self.datas=[[] for i in range(self.na)]
		self.I0=[]
		self.avg=[[] for i in range(self.na)]
		self.std=[[] for i in range(self.na)]
		for i in datas:
			self.I0.append(0)	
			for j in range(len(self.I0area[0])):
				self.I0[-1]+=i[self.I0area[1]].T[self.I0area[0][j]].sum()
			for j in range(self.na):
				self.datas[j].append(0)
				for k in range(len(self.areas[j][0])):
					self.datas[j][-1]+=i[self.areas[j][1]].T[self.areas[j][0][k]].sum()
				self.datas[j][-1]=self.datas[j][-1]/(1.0*self.I0[-1])
		self.datas=np.array(self.datas)
	 

	def area_avg(self):
		self.navg=np.average(self.norm_avg,axis=0)
		self.nstd=np.power(np.array([ np.power(self.norm_std[i],2) for i in range(self.na)]).sum(axis=0), .5 )











#-------------------------------------------------------------------
			
class dialogmodel(QtCore.QAbstractListModel):
	def __init__(self, parent = None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._ui=[]
		self._qdia=[]
		self._names=[]
		self.next=1

	def rowCount(self, parent = None):
		return len(self._ui)

	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

	def setData(self, index, value, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			#row = index.row()
			self._ui[index]=value
			self.dataChanged.emit(index,index)
			return True

	def data(self, index, role):
		row = index.row()
		if role ==  QtCore.Qt.DisplayRole:
			return "Data set: %d"%self._names[row]


	def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._ui.insert(position, '')
			self._qdia.insert(position, '')
			self._names.insert(position, '')
		self.endInsertRows()
		return True

	def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
		self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._qdia[position].close()
			self._qdia[position].destroy()
			value =self._qdia[position]
			self._qdia.remove(value)
			value = self._ui[position]
			self._ui.remove(value)
			value=self._names[position]
			self._names.remove(value)
			#self.updateNames()
		self.endRemoveRows()
		return True

	def updateNames(self):
		for i in range(self.rowCount()):
			self._qdia[i].setWindowTitle('Data set: %d'%(i+1))
			self._ui[i].dataSet=i+1
			self._names[i]=i+1
			self.dataChanged.emit(0, self.rowCount()-1)


	def insertDialog(self, dialogs, ui):
		position=self.rowCount()
		rows=len(dialogs)
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows)
		for i in range(rows):
			self._qdia.insert(position, dialogs[i])
			self._ui.insert(position, ui[i] )
			self._ui[position].setupUi(self._qdia[position])
			self._names.insert(position, self.next)
			self._qdia[position].setWindowTitle('Data set: %d'%self.next)
			self._ui[position].dataSet=self.rowCount()
			self.next+=1
		self.endInsertRows()
		return position

	def get_pos(self, name):
		return np.where(np.array(self._names)==name)[0]



#----------------------------------------------------------------------------------------------

class filemodel(QtCore.QAbstractListModel):
	def __init__(self, parent = None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._files=[]
		self._datas=[]
		self.fft=False

	def rowCount(self, parent = None):
		return len(self._files)

	def apply_filter(self, funct):
		for i in range(len(self._datas)):
			self._datas[i]=funct(self._datas[i])

	def apply_filter_2(self, funct):
		self._datas=funct(self._datas)

	def data(self, index, role):
		row = index.row()
		if role ==  QtCore.Qt.DisplayRole:
			return self._files[row].split('/')[-1].split('.SPE')[0]

	def get_position(self, index):
		a = self._files[index].split('_')[-1]
		a = a.split('.SPE')[0].split('-')
		if len(a) == 3:
			#This has a minus sign
			p=-1.0*np.float(a[1])
			sh=np.int(a[2].split('g')[0])
		elif len(a) == 2:
			#This is positive
			p=np.float(a[0])
			sh=np.int(a[1].split('g')[0])
		else:
			print(index)	
		return p, sh

	def get_uniques(self):
		p=[]
		for i in range(self.rowCount()):
			p.append(self.get_position(i)[0])
		uniques=np.unique(p)
		indexes=[]
		for i in uniques:
			indexes.append(np.where(p==i)[0])
		return np.array(uniques),np.array(indexes)
		


	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

	def setData(self, index, value, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			#row = index.row()
			self._files[index]=value
			self.dataChanged.emit(index,index)
			return True

	def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._files.insert(position, '')
			self._datas.insert(position, [])
		self.endInsertRows()
		return True

	def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
		self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			value =self._files[position]
			self._files.remove(value)
			self._datas[position]='a'
			self._datas.remove('a')
		self.endRemoveRows()
		return True

	def reload_datas(self):
		self._datas=[]
		for i in self._files:
			self._datas.append(spe.load(i))




	def insertFiles(self, files):
		position=self.rowCount()-1
		rows=len(files)
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._files.insert(position, files[i])
			self._datas.insert(position, spe.load(files[i]))
		self.endInsertRows()
		return True


#------------------------

class data_model(QtCore.QAbstractTableModel):
	def __init__(self, parent = None):
		QtCore.QAbstractTableModel.__init__(self, parent)
		self._xdata=None
		self._ydata=None
		self._zdata=None

	def rowCount(self, parent = None):
		return len(self._xdata[0])
	
	def columnCount(self, parent = None):
		return len(self._xdata)

	def data(self, index, role):
		row = index.row()
		column = index.column()
		if role ==  QtCore.Qt.DisplayRole:
			return "%s"%self._xdata[column][row]

	def setData(self, index, value, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			row = index.row()
			col = index.column()
			self._xdata[column][row]=value
			self.dataChanged.emit(index,index)
			return True
	
	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled 
	def get_z(self, index):
		row = index.row()
		col = index.column()
		return self._zdata[col][row]

	def get_y(self, index):
		row = index.row()
		col = index.column()
		return self._ydata[col]

	def get_yp(self):
		return self._ydata[1]

	def get_col(self, col):
		return self._zdata[col]

	def time_index(self, time):
		y=self.get_yp()
		return np.where(y==time)[0][0]



#------------------------------------------------



class calib_model(QtCore.QAbstractListModel):
	def __init__(self, parent = None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._calib=[]
		self._y_axis=[]
		self._t_data=[]

	def rowCount(self, parent = None):
		return len(self._calib)

	def load_from_h5(self, fh):
		grps=fh["Proc_data/configuration_0/calib"].items()
		calibs=[]
		for i in grps:
			name=i[0]
			yx=i[1].items()[0][1].value
			ep=i[1].items()[1][1].value
			tp=i[1].items()[2][1].value
			calibs.append([name, yx, tp, ep])
		self.insertCalib(calibs) 

	def data(self, index, role):
		row = index.row()
		if role ==  QtCore.Qt.DisplayRole:
			return self._calib[row]

	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

	def setData(self, index, value, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			#row = index.row()
			#self._files[index]=value
			self.dataChanged.emit(index,index)
			return True

	def get_eVs(self, index):
		return self._t_data[index.row()]._data[0],self._t_data[index.row()]._data[1]


	def insertCalib(self, calibs):
		position=self.rowCount()-1
		rows=len(calibs)
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._calib.insert(position, calibs[i][0])
			self._y_axis.insert(position, calibs[i][1])
			self._t_data.insert(position, tdata_model())
			self._t_data[position].load_data(calibs[i][2].tolist(),calibs[i][3].tolist())
			#self._t_data[position]._data[0]=calibs[i][2]
			#self._t_data[position]._data[1]=calibs[i][3]
		self.endInsertRows()
		return True

	def newCalib(self):
		position=self.rowCount()-1
		self.beginInsertRows(QtCore.QModelIndex(), position, position + 1 - 1)
		self._calib.insert(position, "%03d"%(position+2))
		self._y_axis.insert(position, [])
		self._t_data.insert(position, tdata_model())
		self._t_data[position]._data[0]=[]
		self._t_data[position]._data[1]=[]
		self.endInsertRows()
		return True



class tdata_model(QtCore.QAbstractTableModel):
	def __init__(self, parent = None):
		QtCore.QAbstractTableModel.__init__(self, parent)
		self._data=[[],[]]
		self._index=[]
		self._points=None

	def rowCount(self, parent = None):
		return len(self._data[0])
	
	def columnCount(self, parent = None):
		return len(self._data)

	def data(self, index, role):
		row = index.row()
		column = index.column()
		if role ==  QtCore.Qt.DisplayRole:
			return "%s"%self._data[column][row]
		if role == 32:
			return self._index[row]

	def setData(self, index, value, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			row = index.row()
			col = index.column()
			a=value.toFloat()
			if not a[1]:
				return False
			self._data[col][row]=a[0]
			if self._points is not None and col == 0:
				self._points[row].point.set_xdata(self._data[col][row])
				self._points[row].point.figure.canvas.draw()
			self.dataChanged.emit(index,index)
			return True
	
	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

	def insertPairs(self, pairs):
		position=self.rowCount()
		rows=len(pairs)
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
		l=self.rowCount()
		for i in range(rows):
			self._data[0].insert(position, pairs[i][0])
			self._data[1].insert(position, pairs[i][1])
			self._index.insert(position, l+i)
		self.endInsertRows()
		return True

	def get_pairs(self, index):
		row=index.row()
		return self._data[0][row], self._data[1][row]

	def get_all_pairs(self):
		return np.array(self._data).T

	def addPoint(self):
		position=self.rowCount()-1
		self.beginInsertRows(QtCore.QModelIndex(), position, position + 1 - 1)
		self._data[0].append(0)
		self._data[1].append(0)
		self.endInsertRows()
		return True

	def update_table(self, index, new):		
		self._data[0][index.row()]=new[0]
		self.dataChanged.emit(index, index)

	def load_data(self, x, y):
		if not len(x)==len(y):
			return -1
		self._data[0]=x
		self._data[1]=y
		self._index=range(len(x))



			


class sap_model(QtCore.QAbstractTableModel):
	def __init__(self, sap, parent = None):
		QtCore.QAbstractTableModel.__init__(self, parent)
		self._sap=sap

	def rowCount(self, parent = None):
		return len(self._sap.x_axes)
	
	def columnCount(self, parent = None):
		return 2

	def data(self, index, role):
		row = index.row()
		column = index.column()
		if role ==  QtCore.Qt.DisplayRole:
			return "%s"%self._sap.x_axes[row]

	def setData(self, index, value, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			row = index.row()
			col = index.column()
			self._xdata[column][row]=value
			self.dataChanged.emit(index,index)
			return True
	
	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

	def get_z(self, index):
		row = index.row()
		col = index.column()
		if col==0:
			return self._sap.s_data[row]
		if col==1:
			return self._sap.u_data[row]
		else:
			return "Hmm, wrong thiny"

	def get_y(self, index):
		row = index.row()
		col = index.column()
		return self._sap.y_sc

	def get_yp(self):
		return self._sap.y_sc

	def get_col(self, col):
		if col==0:
			return self._sap.s_data
		if col==1:
			return self._sap.u_data

	def time_index(self, time):
		y=self.get_yp()
		return np.where(y==time)[0][0]

#------------------------------------------------------

class ImagesModel(QtCore.QAbstractListModel):
	def __init__(self, parent = None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._names=[]
		self._images=[]
		self._bg=None
		self._show=[]
		self._iter=range(self.rowCount())
		self._lines=[]
		self.color=cycle(['r','g','y','c'])
	

	def rowCount(self, parent = None):
		return len(self._images)


	def data(self, index, role):
		row = index.row()
		if role ==  QtCore.Qt.DisplayRole:
			return self._names[row]

	def getImage(self, index):	
		return self._image[row]	

	def getProyection(self, index):
		if self._show[index]:		
			return self._image[row].sum(axis=0)
	

	def flags(self, index):
		return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

	"""def setData(self, index, value, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			#row = index.row()
			self._files[index]=value
			self.dataChanged.emit(index,index)
			return True"""

	def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._names.insert(position, 'Image %d'%i)
			self._images.insert(position, '')
			self._show.insert(position, '')
			self._line.insert(position, '')
		self.endInsertRows()
		self._iter=range(self.rowCount())
		return True

	def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
		self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._names[position]="???TBR"
			self._images[position]="???TBR"						
			self._images.remove('???TBR')
			self._show[position]='???TBR'
			self._show.remove('???TBR')
			self._lines[position].remove()
			self._lines[position]='???TBR'
			self._lines.remove('???TBR')
			if self._bg==i:
				self._bg=None
		self.endRemoveRows()
		self._iter=range(self.rowCount())
		return True


	def insertImage(self, imgs, x, ax):
		position=self.rowCount()-1
		rows=len(imgs)
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._images.insert(position, imgs[i])
			self._show.insert(position, True)			
			self._names.insert(position, "Image %d"%(position+1))
			self._lines.insert(position, Line2D(x, imgs[i].mean(axis=0), color=next(self.color)))
			ax.add_line(self._lines[position])
		self.endInsertRows()
		self._iter=range(self.rowCount())
		return True

	def toBeShow(self):
		return np.where(self._show)



class TextListModel(QtCore.QAbstractListModel):
	def __init__(self, parent = None):
		QtCore.QAbstractListModel.__init__(self, parent)
		self._pvs=[]

	def rowCount(self, parent = None):
		return len(self._pvs)


	def data(self, index, role):
		row = index.row()
		if role ==  QtCore.Qt.DisplayRole:
			return self._pvs[row]


	def setData(self, index, value, role = QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			self._pvs[index]=value
			self.dataChanged.emit(index,index)
			return True

	def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
		self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._pvs.insert(position, '')
		self.endInsertRows()
		return True

	def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
		self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
		for i in range(rows):
			self._pvs.remove(position)
		self.endRemoveRows()
		return True







	

	




