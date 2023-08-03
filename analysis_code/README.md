# Extract behavioral and kinematic data

**BEFORE RUNNING CODE:**

- make sure the following dependencies are installed and accessible in your env: numpy, pandas, pickle, os, glob  
- change string in line 15 in makeDF.py to your local directory, where data are saved  

**RUNNING CODE:**
makeDF.py

**VARIABLES EXTRACTED**

makeDF.py will output a csv in tidydata format (fix url: https://vita.had.co.nz/papers/tidy-data.pdf) with the following columns:  

sub - enumerated subject number
sub_orig - original subject ID
rt - time taken to complete trial
cue - which cue (0: standard, 1: reward, 2: punish, 3: alternative standard)
outcome - success (1) or failure (2)
crit - what was the timelimit
init - time taken for subject to leave starting position
maxvel - maximum velocity reached in pixels per frame
maxvelt - time taken to reach maximum velocity
maxacc - maximum acceleration reached in pixels per frame squared
maxacct - time taken to reach maximum acceleration
init_x - initial position of cursor, x coords
init_y - initial position of cursor, y coords
init_dist - initial distance from starting position
quartacct_g - time taken to reach 1/4 acceleration using a group estimate from a subsample (you probably shouldn't use this)
quartacct_i - time taken to reach 1/4 acceleration relative to current participant (this one should be ok)
post_error - was this trial following an error (1) or not (0)
post_false_start - was this trial following a falase start (1) or not (0)
hold - what was the hold period between cue and action
run - what experimental run (or block)
cue_t - (mostly relevant for designing an fMRI GLM) time of each cue relative to the first registered TR of the sequence
reach_t - (mostly relevant for designing an fMRI GLM) time of each reach initiation relative to the first registered TR of the sequence

(final two variables require fmri=TRUE on line 20 of task_code/IV_Task.py.)
