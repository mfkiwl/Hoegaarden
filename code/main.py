# coding:utf-8

import matplotlib.pyplot as plt
import arviz as az

from config.configutil import getpath
from ioext.gnss_sol_handler import loadsol
from proc.gnss_handler import bayes_multiple_detector

if __name__ == '__main__':
    df = loadsol('rover_bd9_3_enu.pos')
    t = df.loc[:, 'tow']-df.loc[0, 'tow']
    plt.subplot(3, 1, 1)
    plt.plot(t, df.loc[:, 'north'])
    plt.subplot(3, 1, 2)
    plt.plot(t, df.loc[:, 'east'])
    plt.subplot(3, 1, 3)
    plt.plot(t, df.loc[:, 'up'])
    plt.show()
    bayes_multiple_detector(t, df.loc[:, 'up'], 2)
    #
    # trace = az.from_netcdf(getpath('tracepath') + 'test')
    # az.plot_trace(trace)
    # plt.show()
