# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 13:04:34 2020
by Jeffrey Mc Hugh
mchughj3@tcd.ie

@author: jm2080
"""

import numpy as np
from nptdms import TdmsFile 

def tdmsLoad(filepath, dathdr, colnm):
    tdms_file = TdmsFile.read(filepath)
    group = tdms_file[dathdr]
    channel = group[colnm]
    datlist = channel[:]
    #converts the contents from lists to numpy arrays
    datarr = np.asarray(datlist)
    if colnm == 'Time':
        if np.amin(datarr) < 1.0e-02: 
            datarr[np.argmin(datarr):np.size(datarr)] += datarr[np.argmin(datarr)-1]
            #zero each time channel
    return(datarr)