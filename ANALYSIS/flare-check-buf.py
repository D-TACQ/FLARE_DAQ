#!/usr/bin/python3


import numpy as np
import matplotlib.pyplot as plt


def load_blob_data(shot, uut):
    data = np.fromfile("/home/dt100/MR_DATA/{}.{}.dat".format(uut, shot), dtype=np.int16).astype(np.float)
    data = data.reshape((48,-1))
    return data[0]

plt.plot(np.array([True, False, True, True, True]))
plt.show()

uut = "acq2106_204"
shot = 3

bad_data = load_blob_data(shot, uut)

shot = 4
good_data = load_blob_data(shot, uut)

print("DEBUG")
closeness = np.isclose(bad_data, good_data, atol=0, rtol=0)
print(closeness)
print("DEBUG2")
plt.plot(closeness)
plt.grid(1)
print("DEBUG3")
plt.show()
