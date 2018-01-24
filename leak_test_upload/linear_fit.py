import time
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from least_square_linear import *

#create import of weighted linear least squar fit

PPM = []
PPM_err = []
timestamp = []
starttime = 0
with open('C:\\Users\\mu2e\\Desktop\\Why_not_testme_chamber1.txt') as f:
    for line in f:
        numbers_float = map(float, line.split()[:3])
        print numbers_float
        if starttime == 0 :
            starttime = numbers_float[0]
        eventtime = numbers_float[0] - starttime
        PPM.append(numbers_float[2])
        PPM_err.append(numbers_float[2]*0.02)
        timestamp.append(eventtime)
        
slope = get_slope(timestamp, PPM, PPM_err)
slope_err = get_slope_err(timestamp,PPM,PPM_err)
intercept = get_intercept(timestamp, PPM, PPM_err)
intercept_err = get_intercept_err(timestamp,PPM,PPM_err)

#print PPM
print "our fit slope is %f +- %f" % (slope,slope_err)
print "our fit intercept is %f +- %f" % (intercept,intercept_err)

x = np.linspace(0,max(timestamp))
y = slope*x + intercept
plt.plot(timestamp,PPM,'bo')
plt.plot(x,y,'r')
plt.show()
