# coding:utf-8
import numpy as np
from matplotlib import pyplot as plt


def sim_simple_steps(l, noise, steps):
    """
    Append values to the end of an array.

    Parameters
    ----------
    l : int
        data length
    noise : float
        noise level.
    steps : array_like
        [time1,step1]
        [time2,step2]


    Returns
    -------
    append : ndarray
        [time,value]
    """
    s = np.random.normal(0, noise, l)
    sshape = steps.shape
    for i in np.arange(0, sshape[0]):
        s[steps[i, 0]:l] = s[steps[i, 0]:l] + steps[i, 1]
    t = np.arange(0, l)
    return t, s


l, noise, steps = 1000, 30, np.array([[500, -30]])
t, s = sim_simple_steps(l, noise, steps)
plt.plot(t, s)
plt.show()
