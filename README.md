# MPL-shared-xaxis

A python script to easily generate a matplotlib figure with 1..n plots that all share a single x-axis.

The x-axes of the plots are directly linked so that panning and zooming in the matplotlib window affects all plots.

Example figure with three plots:

![Example figure with three plots](https://i.imgur.com/LYR4MTT.png)

# Usage

## Directly executing the script

You can directly execute the script (`mpl_shared_xaxis.py`) to generate a plot from a csv file.

Your csv file has to look similar to this:

```
Temperature / °C;Pressure / mbar;Humidity / %RH
20.930;1014.619;49.220
20.940;1014.749;49.229
20.940;1014.700;49.209
20.940;1014.700;49.189
...
```

(Headers are optional and you can have as many rows and columns as you like.)

After executing the script, a tkinter filedialog will ask you for the file.
After pressing OK, a figure will be generated and shown immediately.

## Importing the method

The core of this script is the function `mpl_shared_xaxis`. 
You can import it from any other python environment.  
For documentation of this method, refer to the source code. I did my best at documenting the method in the docstring.

Example usage:

```
import matplotlib.pyplot as plt
from mpl_shared_xaxis import mpl_shared_xaxis

y0 = [0,1,2,3]
y1 = [3,2,4,1]

fig = mpl_shared_xaxis(y0, y1, yLabels = ['y0 label', 'y1 label'])
plt.show()
```


