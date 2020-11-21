# coding:utf-8
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
from pymc3 import save_trace
from theano import tensor as T
import scipy.io as io

from config.configutil import getpath
from ioext.gnss_sol_handler import loadsol


def bayes_multiple_detector_each_sigma(t, s, n):
    scala = 1000
    with pm.Model() as abrupt_model:
        sigma = pm.Normal('sigma', mu=0.02 * scala, sigma=0.015 * scala)
        # sigma = pm.Uniform('sigma', 5, 15)
        mu = pm.Uniform("mu1", -1.5 * scala, -1.4 * scala)
        tau = pm.DiscreteUniform("tau" + "1", t.min(), t.max())

        for i in np.arange(2, n + 2):
            _mu = pm.Uniform("mu" + str(i), -1.5 * scala, -1.4 * scala)
            mu = T.switch(tau >= t, mu, _mu)
            if i < (n + 1):
                ttau = pm.DiscreteUniform("tau" + str(i), tau, t.max())
                tau = ttau

        tau1 = abrupt_model["tau1"]
        tau2 = abrupt_model["tau2"]
        dtau = pm.DiscreteUniform('dtau', tau1 + 500, tau2)

        s_obs = pm.Normal("s_obs", mu=mu, sigma=sigma, observed=s)
    g = pm.model_to_graphviz(abrupt_model)
    g.view()
    with abrupt_model:
        # pm.find_MAP()
        trace = pm.sample(20000, tune=5000)
        az.plot_trace(trace)
        az.to_netcdf(trace, getpath('tracepath') + 'bd9_3_add_new_rule')
        plt.show()
        pm.summary(trace)
    return trace


if __name__ == '__main__':
    df = loadsol('rover_bd9_3_enu.pos')
    t = df.loc[:, 'tow'] - df.loc[0, 'tow']
    t = t.to_numpy()
    scala = 1000
    plt.subplot(3, 1, 1)
    plt.plot(t, df.loc[:, 'north'] * scala)
    plt.subplot(3, 1, 2)
    plt.plot(t, df.loc[:, 'east'] * scala)
    plt.subplot(3, 1, 3)
    plt.plot(t, df.loc[:, 'up'] * scala)
    plt.show()
    s = df.loc[:, 'up'].to_numpy() * scala
    t = np.arange(0, len(s))
    plt.plot(t, s)
    plt.show()
    bayes_multiple_detector_each_sigma(t, s, 2)
