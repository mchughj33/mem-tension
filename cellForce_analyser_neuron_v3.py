# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 16:14:25 2019
by Jeffrey Mc Hugh
mchughj3@tcd.ie

@author: jm2080
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import file_dialog2 as fd
import TDMSfns2 as tdm

plt.close('all')

indir = fd.filedlg("C:/", "Choose folder of tdms files")
path = glob.glob(indir + '/' + '*_video_tweezers_*.tdms')
insavepath = fd.filedlg("C:/", "Choose save location")
savepath = insavepath + '/'

SSFkeyvals = []
PkFvals = []
d = []

i = len(path)
n = 0

while n < i:

    plt.close('all')
    
    name = os.path.basename(path[n])
    s1 = name.split('_')[0]
    s2 = name.split('_')[3].split('.')[0]
    
    tdms_file = path[n]
    dataPt = tdm.tdmsLoad(tdms_file, 'Position Data', 'Time')
    #converts the contents from lists to numpy arrays
    if np.amin(dataPt) < 1.0e-02: 
        dataPt[np.argmin(dataPt):np.size(dataPt)] += dataPt[np.argmin(dataPt)-1]
    #zero each time channel
    tmin = np.amin(dataPt)
    relt = dataPt - tmin
    delt = relt[1] - relt[0]
    
    dataPx = tdm.tdmsLoad(tdms_file, 'Position Data', 'x-pos')
    #convert pixels to nm, 1 pixel = 214.56 nm
    dataPxnm = dataPx * 214.56
    #convert to force knowing laser power and using calibration curve
    Fx = dataPxnm * 0.08
    Fx = np.ma.array(Fx, mask=np.isnan(Fx))
    Fmax = np.amax(Fx)
    relFx = Fx - Fx[0]
    
    dataPy = tdm.tdmsLoad(tdms_file, 'Position Data', 'y-pos')
    dataPynm = dataPy * 214.56
    Fy = dataPynm * 0.08
    Fy = np.ma.array(Fy, mask=np.isnan(Fy))
    Fymax = np.amax(Fy)
    relFy = Fy - Fy[0]
    
    puldat = tdms_file
    pulname = puldat.split('/')[-1]
    pultime = pulname.split('_')[3].split('.')[0]
    puldate = pulname.split('_')[0]
    pulfldr = puldat.split('/')[-2]
    
    #These are the "Tableau 20" colors as RGB.    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120), 
         (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
         (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
         (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
         (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
      
    #Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for z in range(len(tableau20)):    
        r, g, b = tableau20[z]    
        tableau20[z] = (r / 255., g / 255., b / 255.)
        
    relt = relt.reshape(relt.size, 1)
    relFx = relFx.reshape(relFx.size, 1)
    relFy = relFy.reshape(relFy.size, 1)
    relF = np.sqrt(np.square(relFx) + np.square(relFy))
    relF = relF.reshape(relF.size, 1)
    farr = np.concatenate((relt, relFx, relFy, relF),axis=1)
    ssrelF = np.mean(relF[-20000:-10000], axis=0)
    relFmax = np.amax(relF)
    stedstr = "Steady State Force = " + str(np.round(ssrelF, 3))[1:-1] + '\n' + "Peak Force = " + str(np.round(relFmax, 3))
    
    SSFkeyvals.append(ssrelF[0])
    PkFvals.append(relFmax)
    
    fignuj = plt.figure(figsize=(12.6, 9.72))
    axnuj = fignuj.add_subplot(111)
    axnuj.set_xlabel('Time (s)', fontname='Arial', fontsize=28)
    axnuj.set_ylabel('Force (pN)', fontname='Arial', fontsize=28)
    axnuj.plot(relt, relF, color=tableau20[6], linewidth=2.0, label=stedstr)
    axnuj.legend(loc='best', fancybox=True, fontsize=12, framealpha=0.5)
    axnuj.locator_params(nbins=6)
    axnuj.tick_params(direction='in', length=7, width=2)
    axnuj.xaxis.set_ticks_position('both')
    axnuj.yaxis.set_ticks_position('both')
    for tick in axnuj.get_xticklabels():
        tick.set_fontname('Arial')
    for tick in axnuj.get_xticklabels():
        tick.set_fontsize(28)
    for tick in axnuj.get_yticklabels():
        tick.set_fontname('Arial')
    for tick in axnuj.get_yticklabels():
        tick.set_fontsize(28)
    for axis in ['top','bottom','left','right']:
        axnuj.spines[axis].set_linewidth(2)
    fignuj.savefig(savepath+"NeuronPullCurve_"+str(s1)+"_"+str(s2)+".jpg", bbox_inches='tight', dpi=75)

    d.append({'Timestamp' : str(s1)+"_"+str(s2),
              'SS Force' : ssrelF[0],
              'Pk Force' : relFmax,
              })
    
    plt.close('all')

    n = n + 1
ForceDat = pd.DataFrame(d)

print('Data analysed!')