"""
    This file is to check if the notch filter is working properly.
    This file uses matplotlib and also uses global site-packages to run.
"""

import numpy as np
from filters import notch_filter
import matplotlib.pyplot as plt

# Create a sine wave with multiple frequencies
t = np.linspace(0,10,0.1)
sin_wave = np.sin(t)

plt.plot(sin_wave)
