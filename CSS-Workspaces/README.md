# cs-studio workspace

# FIRST, create a workspace using the method at:

https://github.com/D-TACQ/ACQ400CSS/blob/master/README.md

store at
CSS-Workspaces/FLARE1

Recommended method to create a workspace:
https://github.com/D-TACQ/ACQ400CSS/blob/master/README.md#httpsgithubcomd-tacqacq400cssblobmasteracq1001_acq430_quickstartpdf

# Use this opi set:
https://github.com/D-TACQ/ACQ400CSS/releases/tag/R201206

# Copy the workspace into 4 separate WS

```
cd CSS-Workspaces
for WS in FLARE_PRO_L1 FLARE_PRO_L2 FLARE_PRO_R1 FLARE_PRO_R2; do
    cp -a FLARE1 $WS
done
```
# Install properties shortcut

Setting up all the UUT properties can be tedious.
Assuming that you stack the boxes in numeric seqence as recommended:

acq2106_201 : Left Top
..
acq2106_214 : Left Bottom

acq2106_215 : Right Top
..
acq2106_227 : Right Bottom

.. then you could also use the same properties files, stored here:
```
cd CSS-Workspaces
tar xvf ../PROJECTS/FLARE_DAQ/CSS-Workspaces/FLARE_PRO_L1_props.tar -C FLARE_PRO_L1
tar xvf ../PROJECTS/FLARE_DAQ/CSS-Workspaces/FLARE_PRO_L2_props.tar -C FLARE_PRO_L2
tar xvf ../PROJECTS/FLARE_DAQ/CSS-Workspaces/FLARE_PRO_R1_props.tar -C FLARE_PRO_R1
tar xvf ../PROJECTS/FLARE_DAQ/CSS-Workspaces/FLARE_PRO_R2_props.tar -C FLARE_PRO_R2
```

## Open The WS

### look for Navigator
 + run open view8.opi [right click, open with Opi Display Workbench]
 + minimise all unwanted panes
 + press the top button Launch.., opens three Tabs

## Use the 3 tabs
 + view8 : shows active view of 8 UUT's, with launcheers for other OPI's
 + fp8   : front panel mimic for 8 UUT's, blinken LEDs match physical front panel
 + wr8   : shows WR status for 8 UUT's






