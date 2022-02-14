from typing import *
import matplotlib.pyplot as plt
from matplotlib import gridspec


def mpl_shared_xaxis(y0: List[float], *args, yLabels: List[str] = None, colors: List[str] = None, xLabel: str = None, showGrid: bool = True) -> plt.Figure:
	"""
	Creates a figure with 1..n vertically aligned plots with a shared x axis.
	After calling this method, call matplotlib.pyplot.show() to show the figure.

	Parameters:
	y0 (List[float]): A list of y-values for the first plot

	*args (List[float]): Lists of y-values for any further plots

	yLabels (List[str]): Labels for the y-axes of the plots. The length of this list must match the number of plots.

	colors (List[str]): List of color-names for the plot colors. The length of this list must match the number of plots.

	xLabel (str): The label for the x axis of the figure. The x axis will be displayed below the very bottom plot.

	showGrid (bool): Toggles if a grid is turned on for all plots. By default this is True.

	Returns:
	Returns a matplotlib.pyplot.Figure containing the plots.
	The return value can be ignored unless you wish to make further changes to the figure.
	"""
	nEntries = 1 + len(args)
	if not yLabels:
		yLabels = ['Data ' + str(i) for i in range(nEntries)]
	if len(yLabels) != nEntries:
		raise ValueError(f"The length of the names list must match the number of entries ({nEntries} entries vs. {len(yLabels)} names given)")
	
	if colors is None:
		colors = ['r', 'g', 'b']
		if nEntries > 3:
			colors += ['b'] * (nEntries-3)
	if len(colors) < nEntries:
		raise ValueError(f"The length of the colors list must match the number of entries ({nEntries} entries vs. {len(colors)} colors given)")

	max_x_len = max([len(y0)] + [len(yn) for yn in args])
	x = list(range(max_x_len))
	
	# The majority of the following code is copied from this S.O. answer
	# https://stackoverflow.com/a/37738851/11998115
	fig = plt.figure()
	# set height ratios for subplots
	gs = gridspec.GridSpec(nEntries, 1, height_ratios=[1]*nEntries) 

	# the first subplot
	ax0 = plt.subplot(gs[0])
	line0, = ax0.plot(x, y0, color=colors[0])
	ax0.set_ylabel(yLabels[0])

	# the following  subplots
	axn = [ax0]
	linen = [line0]
	for i, yn in enumerate(args):
		# shared axis X
		axn.append(plt.subplot(gs[i+1], sharex = ax0))
		linen.append(axn[i+1].plot(x, yn, color=colors[i+1])[0])
		plt.setp(ax0.get_xticklabels(), visible=False)
		# remove last tick label for the second subplot
		yticks = axn[i+1].yaxis.get_major_ticks()
		yticks[-1].label1.set_visible(False)
		axn[i+1].set_ylabel(yLabels[i+1])

	if showGrid:
		for ax in axn:
			ax.grid()

	if xLabel:
		axn[-1].set_xlabel(xLabel)

	plt.subplots_adjust(hspace=.0)
	return fig


if __name__ == "__main__":
	import tkinter as tk
	from tkinter.filedialog import askopenfilename
	import csv

	def getFileName() -> str:
		root = tk.Tk()
		root.overrideredirect(True)
		root.attributes("-alpha", 0)
		path = askopenfilename(title="Select your data", filetypes=[("CSV files", "*.csv"), ("CSV files", "*.txt")])
		root.destroy()
		return path
	file = getFileName()
	if not file:
		exit()

	with open(file, 'r', newline='') as f:
		reader = csv.reader(f, delimiter=';')
	
		potentialheader = next(reader)

		nEntries = len(potentialheader)
		yn = []
		for _ in range(nEntries):
			yn.append([])

		ll = [x.replace('.','') for x in potentialheader]
		l = [h.isnumeric() for h in ll]
		b = all(l)
		if b:
			header = None
			line1 = [float(x) for x in potentialheader]
			for i,v in enumerate(line1):
				yn[i].append(float(v))
		else:
			header = potentialheader

		for row in reader:
			for i,v in enumerate(row):
				yn[i].append(float(v))

		fig = mpl_shared_xaxis(*yn, yLabels=header, xLabel='Time')
		plt.show()
