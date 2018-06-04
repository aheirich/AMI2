
## Existing AMI Clients

This page documents the existing clients from AMI-1.

### PS-Mon

<img src="clients/AMI1_screenshots/PS-Mon_001.png">

The initial UI lets the user choose from among several data sources
(Env, LineFit, yag3).

It also provides session control
(Folder, Progress, Run, Throttle, Setup, Data, Find Plot).
TODO: explain session control.


### Env

<img src="clients/AMI1_screenshots/Env_1d_histogram_UI_002.png">

The Env data source supports one of six modes for displaying data
(1D histogram, v Time, Mean v Var, Mean v Scan, 2D histogram, Mean v Var2D).
All of these modes support "Normalize" and "Weight by" as shown.


<img src="clients/AMI1_screenshots/1dhistogram_003.png">

All of the modes produce a small x-y plot like this one for the 1D histogram.

<img src="clients/AMI1_screenshots/1d_vtime_1_004.png">

Here is a plot from the "v Time" mode, it is similar to the 1D histogram plot.

<img src="clients/AMI1_screenshots/Env_Filter_005.png">

We can apply a filter to the data source like this.

The next images show the different modes:

<table style="width:100%">
<tr>
<th>
<img src="clients/AMI1_screenshots/Env_vtime_UI_006.png">
</th>
<th>
<img src="clients/AMI1_screenshots/Env_mean_v_var_UI_007.png">
</th>
<th>
<img src="clients/AMI1_screenshots/Env_mean_v_scan_UI_008.png">
</th>
<th>
<img src="clients/AMI1_screenshots/Env_2d_histogram_UI_009.png">
</th>
<th>
<img src="clients/AMI1_screenshots/Env_mean_v_var2D_UI_010.png">
</th>
</tr>
</table>

The only difference among these modes is the selection in the "Plot type" region.

### LineFit

LifeFit has 4 plotting modes.  Every mode selects source channels, fit method, and plot type.
The plots themselves look the same as for the Env modes.

<table style="width:100%">
<tr>
<th>
<img src="clients/AMI1_screenshots/LineFit_vTime_UI_011.png">
</th>
<th>
<img src="clients/AMI1_screenshots/LineFit_meanVVar_UI_012.png">
</th>
<th>
<img src="clients/AMI1_screenshots/LineFit_meanVScan_013.png">
</th>
<th>
<img src="clients/AMI1_screenshots/LineFit_meanVVar2D_014.png">
</th>
</tr>
</table>


Each plot make has different specifications.
