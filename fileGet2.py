# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 09:45:20 2020
by Jeffrey Mc Hugh
mchughj3@tcd.ie

@author: jm2080
"""

import os
import glob

def fileGET(dirpath, idString):

    fileList = []
    for x in os.walk(dirpath):
        for y in glob.glob(os.path.join(x[0], idString).replace('\\', '/')):
            y.replace('\\', '/')
            fileList.append(y.replace('\\', '/'))
            
    return(fileList)