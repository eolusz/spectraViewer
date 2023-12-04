import numpy 
from lmfit import minimize, Parameters
#import PyGnuplot as gnu
order=1.0
grating=1/1200.
pixel_size=13.5e-3


class rfl_spec():
  def __init__(self,distance,grating,incident_angle,order,pixel_size,zero,efficiency):
    self._i_angle=incident_angle
    self._order=order
    self._zero=zero
    self._efficiency=efficiency
    self._distance=distance
    self._gratting=grating
    self._pixel_size=pixel_size

  def px2nm_2(self,pixel):
    delta_a=(pixel-self._zero)*self._pixel_size/(1.0*self._distance)
    wl=1e6*self._grating*(numpy.sin(numpy.deg2rad(self._i_angle))+numpy.sin(numpy.arctan(delta_a)-numpy.deg2rad(self._i_angle)))/(self._order)
    return wl

  def px2nm(self,pixel):
    x=self._distance*np.tan(np.deg2rad(90-self._i_angle))
    xp=x+((pixel-self._zero)*self._pixel_size)
    orp=0.5*np.pi-np.arctan(xp/self._distance)
    wl=1e6*self._grating*(numpy.sin(numpy.deg2rad(self._i_angle))-numpy.sin(orp))/(self._order)
    return wl
    
  def nm2px(self,nm):
    return ((self._distance/self._pixel_size)/numpy.tan(numpy.arcsin((self._order*nm*1e-6/self._gratting)-numpy.sin(numpy.deg2rad(self._i_angle)))))+self._zero
    
  def nm2ev(self,nm):
    return 1240.0/(1.0*nm)
  
  def ev2nm(self,eV):
    return 1240.0/(1.0*eV)
  
  def px2ev(self,pixel):
    nm=self.px2nm(pixel)
    return self.nm2ev(nm)
    
  def ev2px(self,ev):
    nm=self.ev2nm(ev)
    return self.nm2px(nm)
  
  def set_zero(self,zero):
    self._zero=zero
  
  def set_order(self,order):
    self._order=order
  
  def set_distance(self,distance):
    self._distance=distance
  
  def set_gratting(self,grating):
    self._grating=grating
  
  def set_pixel_size(self,pxsize):
    self._pixel_size=pxsize
  
  def set_incident_angle(self,angle):
    self._i_angle=angle




class Spectrometer():
  """Spectrometer class length units are in mm execpt in the 2nm or nm2 function where are in nm, angles in radiant"""
  def __init__(self,distance,grating,incident_angle,order,pixel_size,zero,efficiency):
    self._i_angle=incident_angle
    self._order=order
    self._zero=zero
    self._efficiency=efficiency
    self._distance=distance
    self._gratting=grating
    self._pixel_size=pixel_size
    
  def px2nm_2(self,pixel):
    delta_a=(pixel-self._zero)*self._pixel_size/(1.0*self._distance)
    wl=1e6*self._grating*(numpy.sin(numpy.deg2rad(self._i_angle))+numpy.sin(numpy.arctan(delta_a)-numpy.deg2rad(self._i_angle)))/(self._order)
    return wl

  def px2nm(self,pixel):
    x=self._distance*numpy.tan(numpy.deg2rad(90-self._i_angle))
    xp=x+((pixel-self._zero)*self._pixel_size)
    wr=.5*numpy.pi-numpy.arctan(xp/self._distance) 
    wl=1e6*self._grating*(numpy.sin(numpy.deg2rad(self._i_angle))-numpy.sin(wr))/(self._order)
    return wl
    
  def nm2px(self,nm):
    return ((self._distance/self._pixel_size)/numpy.tan(numpy.arcsin((nm*1e-6/(self._order*self._gratting))-numpy.sin(numpy.deg2rad(self._i_angle)))))+self._zero
    
  def nm2ev(self,nm):
    return 1240.0/(1.0*nm)
  
  def ev2nm(self,eV):
    return 1240.0/(1.0*eV)
  
  def px2ev(self,pixel):
    nm=self.px2nm(pixel)
    return self.nm2ev(nm)
    
  def ev2px(self,ev):
    nm=self.ev2nm(ev)
    return self.nm2px(nm)
  
  def set_zero(self,zero):
    self._zero=zero
  
  def set_order(self,order):
    self._order=order
  
  def set_distance(self,distance):
    self._distance=distance
  
  def set_gratting(self,grating):
    self._grating=grating
  
  def set_pixel_size(self,pxsize):
    self._pixel_size=pxsize
  
  def set_incident_angle(self,angle):
    self._i_angle=angle
    
  def calibrate(self, pixels, orders, bounds):
        self.params = Parameters()
	
        rq_keys=["zero", "distance", "angle", "pump"]
        for i in rq_keys:
               if not bounds.has_key(i):
                  print("You forgot to specify the bound %s"%i)
                  return
		
        for i in bounds.iteritems():
               if len(i[1])==1:
                  self.params.add(i[0], value=i[1][0], vary=False)
               elif len(i[1])==2:
                  self.params.add(i[0], value=0.5*(i[1][0]+i[1][1]), min=i[1][0], max=i[1][1], vary=True)
               else:
                        print("Wrong bounds (L) for %s"%(i[0]))
                        return

        self.params.add('grating', value=self._grating, vary=False)
        self.params.add('order', value=self._order, vary=False)
        self.params.add('pxsz', value=self._pixel_size, vary=False)
	
        self.out=minimize(trans_simplex ,self.params , args=(pixels, orders))	
        return self.out
	

def trans_simplex(params, pixel, Y, typ):
	#print(params)
	zero=params['zero'].value
	distance=params['distance'].value
	angle=params['angle'].value
	grating=params['grating'].value
	pxsz=params['pxsz'].value	
	order=params['order'].value
	pump=params['pump'].value
	x=distance*np.tan(np.deg2rad(90-angle))
	xp=(pixel-zero)*pxsz+x
	wr=.5*np.pi-np.arctan(xp/distance)
	wl=1.e6*grating*(np.sin(np.deg2rad(angle))-np.sin(wr))/(order)
	e=1240./wl
	error=np.power(pump*Y-e,2)
	print(typ)
	#print ("angle: %f ->error: %f")%(angle,error)
	return error

     
