import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure



class MatplotlibWidget(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
	def __init__(self, parent=None, width=5, height=4, dpi=100, bgcolor=None):
		if bgcolor is None:
			bgcolor=parent.palette().window().color().getRgbF()
		fig = Figure(figsize=(width, height), dpi=dpi, facecolor=bgcolor, edgecolor=bgcolor)
		self.axes = fig.add_subplot(111)
		#self.axes.hold(False)
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
		FigureCanvas.updateGeometry(self)
	

	def setTitle(self, test):
		pass

























































































































































