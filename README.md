# FLARE_DAQ

Supports Scripts for FLARE_DAQ

## Install:
./INSTALL

## MDSplus
Assume trees have been created, ideally with make_acq400_device.py

## Operation

```
UUTS="acq2106_180 acq2106_181 acq2106_182"
cd PROJECTS/acq400_hapi
python3 ./user_apps/special/acq2106_mr.py \
--trg0_src=WRTT0 --MR10DEC=32 --tune_si5326=1 \
--post=1M --set_arm=1 \
```
### 1. HOST_PULL with HAPI as per EMC#1
```
--save_data ./DATA/FLARE_DATA --plot_data=0 --trace_upload=1 \
```
### 2. HOST_PULL with MDSplus device
```
--get_mdsplus=mdsplus-new-shot-upload-uuts \
```
### 3. HOST_PULL fakes EPICS4 PVA
```
--get_epics4=fake-e4-blob-upload-all \
```
### 4. tidy up
```
--
```

## TODO
1. Scaleability: all uploads are in series. With MANY UUTS, a parallel upload will be required
