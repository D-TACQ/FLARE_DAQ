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
	tree = MDSplus.Tree(uut, shot)
	CH01 = tree.TRANSIENT1.INPUT_001.CAL_INPUT.data()
	plt.plot(CH01[0:300000], marker='x', label=uut)
	#if num == 3:
	#	break

plt.legend()
plt.grid(1)
plt.show()
