import visa
import numpy as np
from struct import unpack
import pylab
import math
import xlsxwriter
import array

rm = visa.ResourceManager()
scope = rm.open_resource('USB0::0x0699::0x03A4::C030230::INSTR')

def acquire(cha, Volts, Time):

	scope.write("DATA:SOU CH%s" %cha)
	scope.write('DATA:WIDTH 1')
	scope.write('DATA:ENC RPB')

	ymult = float(scope.query('WFMPRE:YMULT?'))
	yzero = float(scope.query('WFMPRE:YZERO?'))
	yoff = float(scope.query('WFMPRE:YOFF?'))
	xincr = float(scope.query('WFMPRE:XINCR?'))

	scope.write('CURVE?')
	data = scope.read_raw()
	headerlen = 2 + int(data[1])
	header = data[:headerlen]
	ADC_wave = data[headerlen:-1]

	ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))

	Volts = (ADC_wave - yoff) * ymult  + yzero

	Time = np.arange(0, xincr * len(Volts), xincr)

def measure(cha, amp, freq, dur, stops):

	slp_time = dur/stops

	scope.write("MEASUrement:IMMed:SOU%s" %cha)

	scope.write('MEASU:IMM:TYPE FREQ')	
	freq_meas = float(scope.query('MEASUrement:IMMed:VALue?'))
	freq.append(freq_meas)
	

	scope.write('MEASU:IMM:TYPE AMP')	
	amp_meas = float(scope.query('MEASUrement:IMMed:VALue?'))
	amp.append(amp_meas)
	

 

		
	



