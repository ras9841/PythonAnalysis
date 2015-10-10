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
		args = fit parameters [tuple]
		label = label used for graphing [string]
		chi = chi-square of fit [float]
		pval = p-value of chi-squared[float].
		"""
		self.params = args
		self.label = label
		self.chi = chi
		self.pval = pval
	def __str__(self):
		""" String representation of a Fit """
		return self.label

