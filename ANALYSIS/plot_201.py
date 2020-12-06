#!/usr/bin/python3

import MDSplus
import numpy as np
import matplotlib.pyplot as plt
import sys


shot = int(sys.argv[1])
uuts = sys.argv[2:]#.split(" ")
uuts = "acq2106_201"

print(uuts)
for chan in [1,2,3,4,25,26,27,28]:
	print(uuts)
	tree = MDSplus.Tree(uuts, shot)
	CH01 = getattr(tree.TRANSIENT1, "INPUT_{:03d}".format(chan)).CAL_INPUT.data()
	plt.plot(CH01[0:300000], marker='x', label=str(chan))
#	if num == 7:
#		break

plt.legend()
plt.grid(1)
plt.show()
