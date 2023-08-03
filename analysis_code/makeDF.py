import glob
import os
import pickle
import numpy as np
import pandas as pd

# We assigned subjects IDs as 3-element integers beginning at 300. Change the following list to your subject IDs.

subs=['301','305','306','307','310','311','312','314','315','316','317','318','319','321','323','325','329','330','331','332','334','335','336','337','339','341','344','345','347','348','349','350','351','353','355','356','357']

#this is where the csv will output, i.e., wherever you saved/ran this programme
cdtmp = os.getcwd()

#change this to the directory the data are saved in
os.chdir('/change/to/directory/your/data/are/in')

sub=[]
sub_orig=[]
rt=[]
cue=[]
outcome=[]
crit=[]
init=[]
maxvel=[]
maxvelt=[]
maxacc=[]
maxacct=[]
acctrace=[]
veltrace=[]
init_x=[]
init_y=[]
init_dist=[]
quartacct_g=[]
quartacct_i=[]
post_error=[]
post_false_start=[]
hold=[]
run=[]
cue_times = []
reach_times = []
                        
for ind,participant in enumerate(subs):
    
    files = glob.glob(participant+'*')
    
    for file_no,file_in in enumerate(files):
        with open(file_in, "rb") as fp:
            b = pickle.load(fp)
            
            for trial in range(len(b)-2):
                
                sub.append(ind)
                sub_orig.append(int(participant))
                crit.append(b[-2]["RT_crit"])
                run.append(file_no+1)
                cue.append(b[trial]["cue"])
                hold.append(b[trial]["start_hold"])
                cue_times.append(b[trial]['onset_vbl'][0]-b[-2]['first_tr'])
                
                #trial history (if not first trial)
                #setting this up to contrast only:
                #post_error v post_correct
                #post_false_start v post_correct
                #i.e., same baseline
                if trial>0:
                    #previous trial jumped the gun, nan for post_error
                    if b[trial-1]["jumped_gun"]==1:
                        post_false_start.append(1)
                        post_error.append(np.nan)
                    else:
                        #previous trial was correct
                        if b[trial-1]["RT"]<b[-2]["RT_crit"]:
                            post_error.append(0)
                            post_false_start.append(0)
                        else:
                            #previous trial was error, nan for jumped_the gun
                            post_error.append(1)
                            post_false_start.append(np.nan)
                else:
                    post_false_start.append(np.nan)
                    post_error.append(np.nan)
                
                #If the jumped the gun we don't care about their data for that trial
                #outcome: 0 (jumped gun), 1 (correct), 2 (too slow)
                if b[trial]["jumped_gun"]==1:
                    rt.append(np.nan)
                    outcome.append(0)
                    init.append(np.nan)
                    maxvel.append(np.nan)
                    maxacc.append(np.nan)
                    maxvelt.append(np.nan)
                    maxacct.append(np.nan)
                    veltrace.append(np.repeat(np.nan,50))
                    acctrace.append(np.repeat(np.nan,50))
                    init_x.append(np.nan)
                    init_y.append(np.nan)
                    init_dist.append(np.nan)
                    quartacct_g.append(np.nan)
                    quartacct_i.append(np.nan)
                    reach_times.append(np.nan)
                else:
                    rt.append(b[trial]["RT"])
                    reach_times.append(b[trial]['reach_vbl'][0]-b[-2]['first_tr'])
                    #outcome; 1=success, 2=fail (too slow)
                    if b[trial]["RT"]<b[-2]["RT_crit"]:
                        outcome.append(1)
                    else:
                        outcome.append(2)
                    
                    #0th derivative, displacement of reach                            
                    d=np.sqrt(np.sum((np.array(b[trial]["reach_cursor"])-np.array(b[-1]["startxy"]))**2,axis=1))
                    #1st derivative, velocity of reach
                    v=np.diff(d)
                    #2nd derivative, acceleration of reach
                    a=np.diff(v)
                    
                    #"init" is a crude movement onset variable, i.e., at what point did the cursor leave the starting position
                    dist_test = d - b[-1]["radius"]
                    init_ind = np.where(dist_test>0)[0][0]
                    init.append(b[trial]["reach_vbl"][init_ind]-b[trial]["reach_vbl"][0])
                    
                    #max velocity and max acceleration
                    maxvel.append(np.max(v))
                    maxacc.append(np.max(a))
                    
                    #time of max velocity and max acceleration
                    max_vel_ind= np.where(v==np.max(v))[0][0]-1
                    max_acc_ind= np.where(a==np.max(a))[0][0]-2
                    maxvelt.append(b[trial]["reach_vbl"][max_vel_ind]-b[trial]["reach_vbl"][0])
                    maxacct.append(b[trial]["reach_vbl"][max_acc_ind]-b[trial]["reach_vbl"][0])
                    
                    #to make averagable plottable traces (given they are all different lengths)
                    #just taking the first 50 elements
                    ds_trace = np.diff(d[0:51])
                    veltrace.append(ds_trace)
                    acctrace.append(a[0:50])
                    
                    #starting position in spatial terms, i.e., where were they at the very beginning of trial
                    #can test if they drifted during the foreperiod, for e.g.
                    init_x.append(b[trial]["reach_cursor"][0][0])
                    init_y.append(b[trial]["reach_cursor"][0][1])
                    
                    #starting position in terms of distance from target, same idea
                    init_dist.append(np.sqrt(np.sum((np.array(b[trial]["reach_cursor"][0])-np.array(b[trial]["targetxy"]))**2)))
                    
                    #a slightly more robust measure of onset. in another model I figured out that 25% of the group
                    #accleeration was 0.023 units, so take the time on each trial to reach that acceleration
                    group_acc_ind = np.where(np.diff(np.diff(d))>=0.023)[0]
                    if group_acc_ind.any():
                        quartacct_g.append(b[trial]["reach_vbl"][group_acc_ind[0]-2]-b[trial]["reach_vbl"][0])
                    else:
                        quartacct_g.append(np.nan)
                    
                    #this is the same idea, but using a criterion that varies trial-by-trial, i.e., the time taken 
                    #to reach 1/4 the max acceleration as defined on that trial 
                    sorted_accs = -np.sort(-np.array(np.diff(np.diff(d))))
                    indiv_acc_thresh = sorted_accs[np.round(len(sorted_accs[sorted_accs>0])/4).astype(int)]
                    indiv_acc_ind = np.where(np.diff(np.diff(d))>indiv_acc_thresh)[0][0]                        
                    quartacct_i.append(b[trial]["reach_vbl"][indiv_acc_ind-2]-b[trial]["reach_vbl"][0])
                        

os.chdir(cdtmp)

#make a pandas dataframe and save to csv
pd.DataFrame({'sub':sub,
              'sub_orig':sub_orig,
              'run':run,
              'cue_t':cue_times,
              'reach_t':reach_times,
              'crit':crit,
              'cue':cue,
              'outcome':outcome,
              'rt':rt,
              'init':init,
              'maxvel':maxvel,
              'maxacc':maxacc,
              'maxvelt':maxvelt,
              'maxacct':maxacct,
              'init_x':init_x,
              'init_y':init_y,
              'init_dist':init_dist,
              'quartacct_g':quartacct_g,
              'quartacct_i':quartacct_i,
              'post_error':post_error,
              'post_false_start':post_false_start,
              'hold':hold}).to_csv('IVdata.csv',index=False)
