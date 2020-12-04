Sean's FLARE analysis workflow
==============================


MDSplus
-------
There are two options for offloading FLARE data saved to MDSplus to a CSV.

1: flare-summary-csv.py
2: flare-live-csv-offload.py

flare-live-csv-offload.py is the recommended method of offload as it runs 
alongside the capture loop.


Blob offload
------------
There is currently only one method of offloading blob data and that is with 
flare-summary-csv.py. There is an argument option for blob offload.


CSV analysis
------------
Once the data has been saved to a CSV there is a small (quite basic) script 
called flare_csv.py that loads the CSV data into pandas so it can check for any 
errors.

The analysis is configured to only print total errors rather than where they 
occurred. There are lines commented out that print the errors in the relevant
functions (if there are any).


Plotting CH01 on all UUTs
-------------------------
To plot CH01 on whichever UUTs the user wishes then the plot_ch01.py script
should be used. This is a very simple python script that loads data from MDSplus
trees and plots the CH01s on top of one another. Any subset of UUTs can be used.
Usage: 
./plot_ch01.py shot uuts
e.g.
./plot_ch01.py 12345 acq2106_201 acq2106_203
or
./plot_ch01.py 12345 $UUTS
