"""
File: 	pydaq.py
Author:	Allen Sanford (ras9841@rit.edu)
Description:
	Module of python classes and functions build to aide
	in data acquisition. Fitting relies on scipy's odr 
	module.
"""
# Imports
import matplotlib.pyplot as plt
from numpy import linspace
from scipy.odr import ODR, Model, RealData

# Classes
class Graph:
	""" Represents an object used for fitting and plotting """
	def __init__(self, x, y, dx, dy=[]):
		"""
		Builds the graph.

		Keyword args
		x = data points for x-axis [array]
		y = data points for y-axis [array]
		dx = error in x data [array]
		dy = error in y data [array]
		"""
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy if len(dy) not 0 else [0 for _ in dx] 
		self.set_labels()
	
	def __str__(self):
		""" String representation of a Graph object """
		return self.title+": "+self.ylabel+" vs. "+self.xlabel

	def set_labels(self, title="", xlabel="", ylabel=""):
		""" Stores graphs labels """
		self.title = title
		self.xlabel = xlabel
		self.ylabel = ylabel

class Fit:
	""" Represents a fit of RealData to a Graph """
	def __init__(self, *args, label="", chi=None, pval=None):
		""" 
		Stores the fit information.

		Keyword args
		args  = fit parameters [tuple]
		label = label used for graphing [string]
		chi  = chi-square of fit [float]
		pval = p-value of chi-squared[float]
		"""
		self.params = args
		self.label = label
		self.chi = chi
		self.pval = pval
	def __str__(self):
		""" String representation of a Fit """
		return self.label

# Functions
def make_fit(graph, func, flabel="", init=[], x0=0, xf=len(graph.x)):
	""" 
	Returns a Fit for the Graph using the fitting function. 
	
	Keyword args
	graph  = contains data for the fit [Graph]
	func   = function with arguments (*args, x) [function]
	flabel = label used to plot the function 
	init   = initial guess of fit parameter values [array]
	x0 = fit starting point
	xf = fit ending point
	"""
	xdata = graph.x[x0:xf]
	ydata = graph.y[x0:xf]
	dxdata = graph.dx[x0:xf]
	dydata = graph.dy[x0:xf]

	print("*"*80)
	print("Fitting "+str(graph)+" from x=%f to x=%f."%(xdata[0],xdata[-1]))
	
	model = Model(func)
	data = RealData(xdata, ydata, sx=dxdata, sy=dydata)

	odr = None
	if len(init) not 0:
		odr = ODR(data, model, beta0=init)
	else:
		odr = ODR(data, model)
	
	out = odr.run()
	chi, p, dof = reduced_chi_square(graph.x, graph.y, graph.dy, func, len(out.beta))
	fit = Fit(output.beta, label=flabel, chi=chi, pval=p)

	print("\nScipy ODR fit results...")
	output.pprint()
	print("Summary of results for "+str(graph)+" :")
	print(fit)
	print("Reduced chi=%f\tp=%f\tDOF=%d"%(chi, p, dof))

	return fit
