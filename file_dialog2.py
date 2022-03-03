# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 19:18:10 2018
by Jeffrey Mc Hugh
mchughj3@tcd.ie

@author: jm2080
"""

import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

def filedlg(idir, topname):
    return askdirectory(parent = root, initialdir = idir, title = topname)
root = tk.Tk()
root.lift()
root.attributes("-topmost", True)
root.withdraw()

def opnfile(idir, topname):
    return askopenfilename(initialdir = idir, filetypes=(("All Files","*.*"),("NPY File","*.npy"),("ABF File","*.abf"),("Comma Separated Values File","*.csv"),("TDMS File","*.tdms"),("Text File","*.txt")), title = topname)
root = tk.Tk()
root.lift()
root.attributes("-topmost", True)
root.withdraw()