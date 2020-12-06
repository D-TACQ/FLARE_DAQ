#!/usr/bin/python3

import MDSplus
import numpy as np
import matplotlib.pyplot as plt
import sys


shot = int(sys.argv[1])
uuts = sys.argv[2:]#.split(" ")
#uuts = ["acq2106_201","acq2106_205"]

print(uuts)
for num, uut in enumerate(uuts):
	print(uut)
	#data = np.fromfile("/home/dt100/MR_DATA/{}.{}.dat".format(uut, shot))
	data = np.fromfile("/home/dt100/MR_DATA/{}.{}.dat".format(uut, shot), dtype=np.int16).astype(np.float)
	data = data.reshape((48,-1))
	CH01 = data[0]
	plt.plot(CH01, marker='x', label=uut)
	#if num == 3:
	#	break

plt.legend()
plt.grid(1)
plt.show()
