"""
===============================
Legend using pre-defined labels
===============================

Defining legend labels with plots.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Make some fake data.
a = b = np.arange(0, 3, 0.02)
c = np.exp(a)
d = c[::-1]

# Create plots with pre-defined labels.
fig, ax = plt.subplots()
ax.plot(a, c, "k--", label="Model length")
ax.plot(a, d, "k:", label="Data length")
ax.plot(a, c + d, "k", label="Total message length")

legend = ax.legend(loc="upper center", shadow=True, fontsize="x-large")

# Put a nicer background color on the legend.
legend.get_frame().set_facecolor("C0")

plt.show()

#############################################################################
#
# ------------
#
# References
# """"""""""
#
# The use of the following functions, methods, classes and modules is shown
# in this example:


matplotlib.axes.Axes.plot
matplotlib.pyplot.plot
matplotlib.axes.Axes.legend
matplotlib.pyplot.legend
