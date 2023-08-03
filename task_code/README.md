**BEFORE RUNNING CODE:**

- install the [latest version of PsychoPy](https://www.psychopy.org/)  
- make sure the following dependencies are installed and accessible in your env: numpy, pandas, pickle, os  
- change string in line 19 in IV_task.py to your local directory  
- set the desired trial time limit on line 35 of IV_task.py, we use 1.87 seconds for our setup ("RT_crit":1.87)

**RUNNING THE TASK:**

Practice trials with gradually increasing difficulty to a deadline of 2 seconds:  
IV_practice.py

100 experimental trials:  
IV_task.py

Data from each file output to ./Data (you might need to make this directory yourself).

**fMRI Compatibility**

The IV_task.py code's default on line 20 is fmri=False, i.e., testing in a behavioural suite with no requirement to wait for scanner TRs before experiment starts.  
If you set fmri=True, the code will wait for the first TR to be received from the scanner before beginning the experiment, and records its timestamp.  
This allows cue and reach times to be timestamped relative to the images, for calculating design matrices for a GLM (see ./analysis_code/README.md).  
Our aquisition computer receives triggers through a serial port. The relevant functions to do this are get_serial_port and wait4tr_start in the IV_functions.py  
You will need to change these functions, for e.g., if you use a USB-based system.
