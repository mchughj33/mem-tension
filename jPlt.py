# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 15:35:03 2020
by Jeffrey Mc Hugh
mchughj3@tcd.ie

@author: jm2080
"""

import matplotlib.pyplot as plt

def jeffPlt(x, y, ymin=False, ybtm=0, save=False, 
            svpth='C:/Users/jm2080/OneDrive - University Of Cambridge/savaccidnt/', 
            widt=12.96, lent=9.72, xnam='Time(s)', ynam='Force (pN)',fnt='Arial', 
            fntsz=28, colour=6, linwidt=2.0, labl='legtxt', ntik=6,
            tikdir='in', tiklen=7.0, tikwid=2.0, xtiks='both', ytiks='both',
            legend=True, lgfntsz=14, filetyp='.jpg', rez=75):
    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120), 
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
          
        #Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for z in range(len(tableau20)):
        r, g, b = tableau20[z]    
        tableau20[z] = (r / 255., g / 255., b / 255.)
    
    fig = plt.figure(figsize=(widt, lent))
    ax = fig.add_subplot(111)
    ax.set_xlabel(xnam, fontname=fnt, fontsize=fntsz)
    ax.set_ylabel(ynam, fontname=fnt, fontsize=fntsz)
    ax.plot(x, y, color=tableau20[colour], linewidth=linwidt, label=labl)
    if legend:
        ax.legend(loc='best', fancybox=True, fontsize=lgfntsz, framealpha=0.5)
    ax.locator_params(nbins=ntik)
    ax.tick_params(direction=tikdir, length=tiklen, width=tikwid)
    ax.xaxis.set_ticks_position(xtiks)
    ax.yaxis.set_ticks_position(ytiks)
    if ymin:
        plt.gca().set_ylim(bottom=ybtm)
    for tick in ax.get_xticklabels():
        tick.set_fontname(fnt)
    for tick in ax.get_xticklabels():
        tick.set_fontsize(fntsz-2)
    for tick in ax.get_yticklabels():
        tick.set_fontname(fnt)
    for tick in ax.get_yticklabels():
        tick.set_fontsize(fntsz-2)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(linwidt)
    if save:
        fig.savefig(svpth+filetyp, bbox_inches='tight', dpi=rez)