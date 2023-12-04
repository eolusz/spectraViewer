import os
import sys
from PIL import Image
import glob
import matplotlib.pyplot as plt
from numpy import array, random 


class logbook_entryLinux:

    def __init__(self, host, port, logbook, user, pwd, extra=None):
        #os.chdir("c:\\Program Files (x86)\\ELOG")
        self._exe="elog "
        self._host=host
        self._port=port
        self._logbook=logbook
        self._user=user
        self._pass=pwd
        self._extra=extra
        self._fields={}
        self._attach=[]
        self._comment=""

    def add_field(self, name, value):
        self._fields[name]=value

    def add_attachment(self, file):
        if not os.path.isfile(file):
            print("File: %s not found. "%file)
            return 0
        self._attach.append(file)

    def add_to_comment(self, comment):
        self._comment+=comment

    def restart_entry(self):
        self._comment=""
        self._fields={}
        self._attach=[]

    def send_entry(self):
        cmd=self._exe
        cmd+="-h %s -p %d -l %s -u %s %s "%(self._host, self._port, self._logbook, self._user, self._pass)
        for i in self._fields:
            cmd+='-a "%s=%s" ' %(i,self._fields[i])
        for i in self._attach:
            cmd+='-f %s '%i
        cmd+="-n 2 '%s'"%self._comment
        self._cmd=cmd
        print(self._cmd)
        os.system("%s"%self._cmd)



class logbook_entryWindows:

    def __init__(self, host, port, logbook, user, pwd, extra=None):
        os.chdir("c:\\Program Files (x86)\\ELOG")
        self._exe="elog.exe "
        self._host=host
        self._port=port
        self._logbook=logbook
        self._user=user
        self._pass=pwd
        self._extra=extra
        self._fields={}
        self._attach=[]
        self._comment=""

    def add_field(self, name, value):
        self._fields[name]=value

    def add_attachment(self, file):
        if not os.path.isfile(file):
            print("File: %s not found. "%file)
            return 0
        self._attach.append(file)

    def add_to_comment(self, comment):
        self._comment+=comment

    def restart_entry(self):
        self._comment=""
        self._fields={}
        self._attach=[]

    def send_entry(self):
        cmd=self._exe
        cmd+="-h %s -p %d -l %s -u %s %s -n 2"%(self._host, self._port, self._logbook, self._user, self._pass)
        for i in self._fields:
            cmd+='-a "%s=%s" ' %(i,self._fields[i])
        for i in self._attach:
            cmd+='-f %s '%i
        cmd+=" '%s'"%self._comment
        self._cmd=cmd
        os.system("%s"%self._cmd)

def make_1d(image):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(image.T)
    ax.set_xlabel("Pixel [-]")
    ax.set_ylabel("Counts [-]")
    num=1000*random.rand(1)[0]
    name="temp_%d.png"%num
    fig.savefig(name)
    return os.path.abspath("%s\\%s"%(os.path.curdir,name))

def make_2d(image):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.imshow(image.T)
    ax.set_xlabel("Pixel [-]")
    ax.set_ylabel("Pixel [-]")
    num=1000*random.rand(1)[0]
    name="temp_%d.png"%num
    fig.savefig(name)
    return os.path.abspath("%s\\%s"%(os.path.curdir,name))

def create_avg_img(folder):
    files=glob.glob("%s/*.tiff"%folder)
    if len(files)<1:
        return ""
    im=[]
    for i in files:
        a=Image.open(i)
        im.append(array(a))
        a.close()        
    im=array(im).mean(axis=0)
    if im.shape[0]==1:
        return make_1d(im)
    else:
        return make_2d(im)
    
        
        
    

        
def main(argc, argv=[]):
    opts=[]
    comments='"No comments"'
    folder=""
    for i in range(argc):
        if argv[i]=="-h":
            host=argv[i+1]
        elif argv[i]=="-l":
            logbook=argv[i+1]
        elif argv[i]=="-p":
            port=argv[i+1]
        elif argv[i]=="-u":
            user=argv[i+1]
            pwd=argv[i+2]
        elif argv[i]=="-a":
            opts.append([argv[i+1],argv[i+2]])
        elif argv[i]=="-c":
            comments=argv[i+1]
        elif argv[i]=="/f":
            folder=argv[i+1]
            folder=create_avg_img(folder)
            print(folder)                

        
    entry=logbook_entry("192.168.88.248", 8080, "Matterhorn", "robot", "robot")
    entry.add_field('Type','Snapshot')
    for i in opts:
        entry.add_field(i[0],i[1])
    entry.add_to_comment(comments)
    entry.add_attachment(folder)
    entry.send_entry()
    print('%s'%entry._cmd)
    
    os.remove(folder)
    
if __name__=="__main__":
	main(len(sys.argv), sys.argv)
