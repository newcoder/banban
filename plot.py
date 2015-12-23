import pylab
import numpy as np
from scipy.stats import norm
x = np.linspace(-50,50,1000)
y = norm.pdf(x, loc=-1.55, scale=8.66)    # for example
pylab.plot(x,y)
pylab.show()