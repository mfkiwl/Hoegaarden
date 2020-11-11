# coding:utf-8
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
from pymc3 import save_trace
from theano import tensor as T

from config.configutil import getpath


def bayes_multiple_detector(t, s, n):
    with pm.Model() as abrupt_model:
        sigma = pm.Normal('sigma', mu=0.03, sigma=0.015)
        # sigma = pm.Uniform('sigma', 5, 15)
        mu = pm.Uniform("mu1", -1.5, -1.4)
        tau = pm.DiscreteUniform("tau" + "1", t.min(), t.max())

        for i in np.arange(2, n + 2):
            _mu = pm.Uniform("mu" + str(i),-1.5, -1.4)
            mu = T.switch(tau >= t, mu, _mu)
            if (i < (n + 1)):
                tau = pm.DiscreteUniform("tau" + str(i), tau, t.max())
        s_obs = pm.Normal("s_obs", mu=mu, sigma=sigma, observed=s)

    with abrupt_model:
        pm.find_MAP()
        trace = pm.sample(5000)
        az.plot_trace(trace)
        az.to_netcdf(trace, getpath('tracepath')+'test')
        plt.show()
        pm.summary(trace)
    return trace