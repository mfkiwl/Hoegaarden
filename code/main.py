# coding:utf-8

import matplotlib.pyplot as plt

import numpy as np

from proc.simple_handler import bayes_single_detector, bayes_multiple_detector
from sim.sim_handler import sim_simple_steps

if __name__ == '__main__':
    # 1----bayes_single_detector(disp extraction)
    # l, noise, steps = 500, 10, np.array([[100, -30]])
    #
    # t, s = sim_simple_steps(l, noise, steps)
    # plt.plot(t, s)
    # plt.show()
    # bayes_single_detector(t, s)
    # 2----bayes_multiple_detector(disp extraction)
    l, noise, steps = 500, 10, np.array([[100, -30], [200, -30], [300, -30]])

    t, s = sim_simple_steps(l, noise, steps)
    plt.plot(t, s)
    plt.show()
    bayes_multiple_detector(t, s, 3)
