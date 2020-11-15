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
     Examples
    --------
    l, noise, steps = 1000, 30, np.array([[500, -30]])
    t, s = sim_simple_steps(l, noise, steps)
    Returns
    -------
    append : ndarray
        [time,value]
    """
    np.random.seed(1)
    s = np.random.normal(0, noise, l)
    sshape = steps.shape
    for i in np.arange(0, sshape[0]):
        s[steps[i, 0]:l] = s[steps[i, 0]:l] + steps[i, 1]
    t = np.arange(0, l)
    return t, s


def sim_gauss_randomwalk_steps(l, noise, walknoise, steps):
    """
    Append values to the end of an array.

    Parameters
    ----------
    l : int
        data length
    noise : float
        noise level.
    walknoise: float
        gauss random walk noise level.
    steps : array_like
        [time1,step1]
        [time2,step2]

     Examples
    --------
    l, noise, steps = 1000, 30, np.array([[500, -30]])
    t, s = sim_simple_steps(l, noise, steps)
    Returns
    -------
    append : ndarray
        [time,value]
    """
    np.random.seed(1)
    s = np.random.normal(0, noise, l)
    randwalk = np.random.normal(0, walknoise, l)
    s = s + np.cumsum(randwalk)
    sshape = steps.shape
    for i in np.arange(0, sshape[0]):
        s[steps[i, 0]:l] = s[steps[i, 0]:l] + steps[i, 1]
    t = np.arange(0, l)
    return t, s
