# read log file from water server and show a graph of watering over time as 
# well as a cumulative plot
# sample command line:
#
# scp user@waterserver:water/water.log /dev/stdout|python plot_water.py


from dateutil import parser
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import time


plt.close('all')

# stdin is one line per entry in this format:
#------------------------------------------------------------------------------
#time: Tue Jun 16 20:12:24 BST 2020	Payload: {Pulses:10 Nonce:0 Checksum:3}
#------------------------------------------------------------------------------
# parse out timestamp and pulses:
ts = []
ps = []
for line in sys.stdin:
  tuple = line.strip().split()
  date=parser.parse(" ".join(tuple[1:7]))
  pulses = int(tuple[8].split(':')[1])
  ts.append(date)
  ps.append(pulses)

data = pd.DataFrame(data={'t': ts, 'p': ps})
data['date']=pd.to_datetime(data["t"], unit='s')
data.plot(x='date',y='p')
plt.show()

# 'c' coluimn to show cumulative water use
data['c'] = data['p'].cumsum()
data.plot(x='date',y='c')
plt.show()
