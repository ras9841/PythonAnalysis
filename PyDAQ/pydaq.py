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
from scipy.stats import chi2
from scipy.odr import *
#from scipy.odr import ODR, Model, RealData

# Classes
class Graph:
	""" Represents an object used for fitting and plotting """
	def __init__(self, x, y, dx, dy):
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
		self.dy = dy
		self.dx = [0 for _ in x] if len(dx) == 0 else dx 
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
	def __init__(self, args, label="", chi=None, pval=None):
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
def reduced_chi_square(xvals, yvals, sigy, func, numparam):
	""" 
	Returns the reduced chi-squared, pvalue, and DOF of the fit.
	"""
	c = 0
	n = len(xvals) - numparam
	for x, y, s in zip(xvals, yvals, sigy):
		 c += (y-func(x))**2/(s**2)
	return c/n, float(1-chi2.cdf(c,n)), n 

def make_fit(graph, func, flabel="", x0=0, xf=0):
	""" 
	Returns a Fit for the Graph using the fitting function. 
	
	Keyword args
	graph  = contains data for the fit [Graph]
	func   = function with arguments (*args, x) [function]
	init   = initial guess of fit parameter values [array]
	flabel = label used to plot the function 
	x0 = fit starting point
	xf = fit ending point
	"""
	xf = len(graph.x) if xf == 0 else xf
	xdata = graph.x[x0:xf]
	ydata = graph.y[x0:xf]
	dxdata = graph.dx[x0:xf]
	dydata = graph.dy[x0:xf]

	print("*"*80)
	print("Fitting "+str(graph)+" from x=%f to x=%f."%(xdata[0],xdata[-1]))
	
	model = Model(func)
	data = RealData(xdata, ydata, sx=dxdata, sy=dydata)

	print(type(model))
	print(type(data))

	odr = ODR(data, model, beta0=[1.0,1.0])
	
	out = odr.run()
	f = lambda x: func(out.beta,x)
	chi, p, dof = reduced_chi_square(graph.x, graph.y, graph.dy, f, len(out.beta))
	fit = Fit(out.beta, label=flabel, chi=chi, pval=p)

	print("\nScipy ODR fit results...")
	out.pprint()
	print("\nSummary of results for "+str(graph)+" ...")
	print(fit)
	print("Reduced chi=%f\tp=%f\tDOF=%d"%(chi, p, dof))

	return fit
