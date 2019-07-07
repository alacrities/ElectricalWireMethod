import visa
import pyvisa
from Instruments import function_generator
from Instruments import oscilloscope 
import time
import pylab
import array
import fitter
import numpy as np



cha = 1
sweep_function = "SQU"
sweep_amp = 3
sweep_freq_start = 15
sweep_freq_stop = 100
sweep_duration = 20
sweep_stops = 6

Output = []
Frequency = []

x = np.linspace(0, 110, 500)

y_fit = []
y_ifit = []
parameters = []
par = [1,2,0.3,500]


function_generator.sweep_meas(cha, sweep_function, sweep_amp, sweep_freq_start, sweep_freq_stop, sweep_duration, sweep_stops, Output, Frequency)
fitter.bipolar_reso(Output, Frequency, par, y_fit, y_ifit, parameters)

mu = 1.6*(10**(-4))
omega = parameters[3]
wire_len = 1 

tension = 4*mu*(omega*wire_len/(2*np.pi))**2
print(tension)


pylab.plot(Frequency, Output, 'bo')
pylab.plot(Frequency, y_fit, 'ro')
pylab.plot(x, fitter.resonance(x, parameters[0] , parameters[1], parameters[2], parameters[3]), 'r')

pylab.title('Frequency Spectrum')
pylab.xlabel('Hz')
pylab.ylabel('V')
 
pylab.ylim(0.8*min(Output),1.2*max(Output))
pylab.xlim(0.8*min(Frequency),1.2*max(Frequency))

pylab.show()


