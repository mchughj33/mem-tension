# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 16:14:25 2020
by Jeffrey Mc Hugh
mchughj3@tcd.ie

Analysis script for OT data taken from 3T3 fibroblasts

Notes:
For 10kPa 200201 11 there are NaN values at the end of the array so use these lines 
pulPt = pulPt[0:64122]
pulPx = pulPx[0:64122]
pulPy = pulPy[0:64122]

@author: jm2080
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import file_dialog2 as fd
import fileGet2 as fg
import TDMSfns2 as tdm
import jPlt

plt.close('all')

indir = fd.filedlg("C:/", "Choose folder of tdms files")
fileList = fg.fileGET(indir, '*_video_tweezers_*')
pzofileList = fg.fileGET(indir, '*_piezo_tweezers_*')
insavepath = fd.filedlg("C:/", "Choose save location")
insavepath = insavepath + '/'

d = []

GSSFvals = []
hPaSSFvals = []
kPaSSFvals = []
dkPaSSFvals = []
miscSSF = []

GPkFvals = []
hPaPkFvals = []
kPaPkFvals = []
dkPaPkFvals = []
miscPkF = []

ktrap = 0.1
px2nm = 214.56

i = len(fileList)
n = 0
foldnms = []

while n < i:
    file = fileList[n]
    foldnm = file.split('/')[-2]
    if foldnm not in foldnms:
        foldnms.append(foldnm)
    n = n + 1

i2 = len(foldnms)
n2 = 0

while n2 < i2:
    plt.close('all')
    i3 = len(fileList)
    n3 = 0
    anlyst = []
    pzolyst = []
    while n3 < i3:
        if foldnms[n2] in fileList[n3]:
            anlyst.append(fileList[n3])
            pzolyst.append(pzofileList[n3])
        n3 = n3 + 1
    i4 = len(anlyst)
    n4 = 1
    while n4 < i4:
        bsline = anlyst[0]
        
        basePt = tdm.tdmsLoad(bsline, 'Position Data', 'Time')
        btmin = np.amin(basePt)
        relbt = basePt - btmin
        
        basePx = tdm.tdmsLoad(bsline, 'Position Data', 'x-pos')
        baseFx = basePx * px2nm * ktrap
        baseFx = np.ma.array(baseFx, mask=np.isnan(baseFx))
        baseFxmean = np.mean(baseFx)
        
        basePy = tdm.tdmsLoad(bsline, 'Position Data', 'y-pos')
        baseFy = basePy * px2nm * ktrap
        baseFy = np.ma.array(baseFy, mask=np.isnan(baseFy))
        baseFymean = np.mean(baseFy)
    
        puldat = anlyst[n4]
        pulname = puldat.split('/')[-1]
        pultime = pulname.split('_')[3].split('.')[0]
        puldate = pulname.split('_')[0]
        pulfldr = puldat.split('/')[-2]
        
        pulPt = tdm.tdmsLoad(puldat, 'Position Data', 'Time')
        tmin = np.amin(pulPt)
        relt = pulPt - tmin
        smplt = relt[1]-relt[0]
        
        pulPx = tdm.tdmsLoad(puldat, 'Position Data', 'x-pos')
        pulFx = pulPx * px2nm * ktrap
        pulFx = np.ma.array(pulFx, mask=np.isnan(pulFx))
        
        pulPy = tdm.tdmsLoad(puldat, 'Position Data', 'y-pos')
        pulFy = pulPy * px2nm * ktrap
        pulFy = np.ma.array(pulFy, mask=np.isnan(pulFy))
        
        relt = relt.reshape(relt.size, 1)
        baseFxmean = baseFxmean.reshape(baseFxmean.size, 1)
        baseFymean = baseFymean.reshape(baseFymean.size, 1)
        nurelFx = pulFx - baseFxmean
        nurelFy = pulFy - baseFymean
        nurelFx = nurelFx.reshape(nurelFx.size, 1)
        nurelFy = nurelFy.reshape(nurelFy.size, 1)
        nurelF = np.sqrt(np.square(nurelFx) + np.square(nurelFy))
        ssrelF2 = np.mean(nurelF[-20000:-10000], axis=0)
        nurelFmax = np.amax(nurelF)
        stedstr2 = "Steady State Force = " + str(np.round(ssrelF2, 3))[1:-1] + '\n' + "Peak Force = " + str(np.round(nurelFmax, 3))
                    
        if 'glass' in pulfldr:
            GSSFvals.append(ssrelF2[0]) 
            GPkFvals.append(nurelFmax)
        elif '100Pa' in pulfldr:
            hPaSSFvals.append(ssrelF2[0]) 
            hPaPkFvals.append(nurelFmax)
        elif '1kPa' in pulfldr:
            kPaSSFvals.append(ssrelF2[0]) 
            kPaPkFvals.append(nurelFmax)
        elif '10kPa' in pulfldr:
            dkPaSSFvals.append(ssrelF2[0]) 
            dkPaPkFvals.append(nurelFmax)
        else:
            miscSSF.append(ssrelF2[0]) 
            miscPkF.append(nurelFmax)
            
        savepath = insavepath+pulfldr+'_'+pultime
        legstr = pulfldr+'_'+pultime+'\n'+stedstr2
        
        jPlt.jeffPlt(relt, nurelF, ymin=True, ybtm=-3, save=True, 
                    svpth=savepath, labl=legstr, filetyp='.jpg', 
                    rez=75)
        plt.close('all')
        
        #Create a dataframe of the results
        d.append({'Timestamp'           : puldate+"_"+pultime,
                  'Folder'              : pulfldr,
                  'SS Force'            : ssrelF2[0],
                  'Pk Force'            : nurelFmax,
                  })
        n4 = n4 + 1
    n2 = n2 + 1
plt.close('all')

GenDat = pd.DataFrame(d)

print('Data analysed!') 