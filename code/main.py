# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt

from proc.simple_handler import bayes_single_detector
from sim.sim_handler import sim_simple_steps

if __name__ == '__main__':
    l, noise, steps = 1000, 10, np.array([[300, -10],[500, -30],[700, -20]])

    t, s = sim_simple_steps(l, noise, steps)
    plt.plot(t, s)
    plt.show()
    bayes_single_detector(t, s)
