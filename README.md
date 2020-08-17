# FLARE_DAQ

Supports Scripts for FLARE_DAQ

Recommended FW release:
https://github.com/D-TACQ/ACQ400RELEASE/releases/tag/v245

git clone to PROJECTS/FLARE_DAQ
eg
```
mkdir -p PROJECTS;
cd PROJECTS;
git clone https://github.com/D-TACQ/FLARE_DAQ.git
```
## Install:
./INSTALL

## MDSplus : OPTIONAL but RECOMMENDED.
Assume trees have been created, ideally with make_acq400_device.py

## RUN A SHOT : UUTS, ACTIONS, CONTROL

* summary:
```
source ./bin/FLARE3  
source ./bin/FLARE_CONFIG
./bin/run-3-way $UUTS
```
* more detail below:

### Configuration

#### UUTS
```
[flare@andros ~]$ cat ./bin/FLARE3 
export UUTS="acq2106_182 acq2106_181 acq2106_200"
```


#### Actions

Customise this file on site;
```
[flare@andros ~]$ cat bin/FLARE_CONFIG 
export UUTS="acq2106_182 acq2106_181 acq2106_200 acq2106_201"
# export FL_XXX=  DISABLES a feature
# to ENABLE the feature with defaults, COMMENT the line OUT
# to ENABLE the feature with special value, enter FL_XXX=special-value
#export FL_MDS=
export FL_EP4=
export FL_GET=
export SITECLIENT_TRACE=0
# for MR example uncomment this:
#export FL_STL=--stl=STL/acq2106_test10.stl
# for default rate ("RUN"), uncomment this:
unset FL_STL
# for TERM11 fiber trigger, uncomment this:
#FL_TRG=--trg0_src=WRTT0,RP
# For FP TTL trigger, uncomment this:
unset FL_TRG
```

## Operation
Script supports all 3 data upload.
```
./bin/run-3-way $UUTS
...

python3 PROJECTS/acq400_hapi/user_apps/special/acq2106_mr.py \
--trg0_src=WRTT0 --MR10DEC=32 --tune_si5326=1 \
--post=1M --set_arm=1 $UUTS
```
* 1. HOST_PULL with HAPI as per EMC#1
```
--save_data ./DATA/FLARE_DATA --plot_data=0 --trace_upload=1 \
```
* 2. HOST_PULL with MDSplus device
```
--get_mdsplus=mdsplus-new-shot-upload-uuts \
```
* 3. HOST_PULL fakes EPICS4 PVA
```
--get_epics4=fake-e4-blob-upload-all \
```
* 4. MR demo
```
--stl PROJECTS/acq400_hapi/user_apps/STL/acq2106_test10.stl \
```
* 5. tidy up
```
-- $UUTS
```


## TODO
1. Scaleability: all uploads are in series. With MANY UUTS, a parallel upload will be required
