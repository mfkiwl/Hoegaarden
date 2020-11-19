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
        sigma = pm.Normal('sigma1', mu=0.02 * scala, sigma=0.015 * scala)
        # sigma = pm.Uniform('sigma', 5, 15)
        mu = pm.Uniform("mu1", -1.5 * scala, -1.4 * scala)
        tau = pm.DiscreteUniform("tau" + "1", t.min(), t.max())

        for i in np.arange(2, n + 2):
            _mu = pm.Uniform("mu" + str(i), -1.6 * scala, -1.4 * scala)
            mu = T.switch(tau >= t, mu, _mu)
            # _sigma = pm.Normal('sigma' + str(i), mu=0.02 * scala, sigma=0.015 * scala)
            # sigma = T.switch(tau >= t, sigma, _sigma)
            if i < (n + 1):
                # BoundedUniform = pm.Bound(pm.Uniform, lower=700)
                # dtau = BoundedUniform('dtau'+str(i), upper=t.max()-tau)
                ttau = pm.DiscreteUniform("tau" + str(i), tau, t.max())

                tau = ttau

        # add bound
        tau1 = abrupt_model["tau1"]
        tau2 = abrupt_model["tau2"]
        dtau = pm.DiscreteUniform('dtau', tau1 + 500, tau2)
        # BoundedUniform = pm.Bound(pm.HalfNormal, lower=300)
        # dtau = BoundedUniform('dtau', mu=(tau2-tau1)/2, sigma=30)
        # dtau = pm.Pareto("dtau", alpha=1, m=tau2 - tau1)
        # dtau = pm.Pareto("dtau", alpha=1.0/(tau2 - tau1), m=500)
        # d = tau2 - tau1
        # dv = T.switch(d < 700, 0, dtau)

        s_obs = pm.Normal("s_obs", mu=mu, sigma=sigma, observed=s)
    g = pm.model_to_graphviz(abrupt_model)
    g.view()
    with abrupt_model:
        pm.find_MAP()
        trace = pm.sample(20000, tune=5000)
        az.plot_trace(trace)
        az.to_netcdf(trace, getpath('tracepath') + 'bd9_4_each_sigma')
        plt.show()
        pm.summary(trace)
    return trace


if __name__ == '__main__':
    df = loadsol('rover_bd9_4_enu.pos')
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
    s = df.loc[650:, 'up'].to_numpy() * scala
    t = np.arange(0, len(s))
    plt.plot(t, s)
    plt.show()
    bayes_multiple_detector_each_sigma(t, s, 2)
