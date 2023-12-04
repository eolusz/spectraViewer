import h5py
import numpy






class scan:
	def __init__(self, filename="/home/atto/Desktop/data/2019/2019-03-25/methaneII.h5"):				
		self._fname=filename
		self.load(self._fname)
		self._rf=False
		

	def load(self, filename):
		self.f=h5py.File(filename,"r")
		keys_0=self.f["state_0"].keys()
		keys_1=self.f["state_1"].keys()
		keys_2=self.f["state_2"].keys()

		self.xsize=1280
		self.ysize=self.f["state_0"].items()[0].items()[0][1].value.shape[0]/self.xsize
		sets=self.f["state_0/%s"%keys_0]
		
		if keys_0!=keys_1:
			print("Error: state_0 not same points that state_1")
			return
	
		self.arr_data=np.empty((2,len(keys_0), xsize*ysize))
		self.buf_data=np.empty(xsize*ysize)
		for i in keys_0:
			self.load_group("state_0/%s"%i)
			self.avg[0]=self.buf_data.reshape(xsize,ysize)
			self.load_group("state_1/%s"%i)
			self.avg[1]=self.buf_data.reshape(xsize,ysize)


	def load_group(self, grp_name):
		self.buf_data=self.buf_data*0
		for j in self.f[grp_name]:
			self.buf_data+=j.value()
		
		
