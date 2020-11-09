# coding:utf-8
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
from theano import tensor as T


def bayes_single_detector(t, s):
    with pm.Model() as abrupt_model:
        steppoint = pm.DiscreteUniform(
            "steppoint", lower=t[1], upper=t[-1], testval=50
        )
        early_mu = pm.Uniform("early_mu", -50, 50)
        late_mu = pm.Uniform("late_mu", -50, 50)
        mu = pm.math.switch(steppoint >= t, early_mu, late_mu)
        sigma = pm.Normal('sigma', mu=30, sigma=20)
        s_obs = pm.Normal("s_obs", mu=mu, sigma=sigma, observed=s)

    with abrupt_model:
        trace = pm.sample(1000)
        az.plot_trace(trace)
        plt.show()
    return trace


def bayes_multiple_detector(t, s, n):
    with pm.Model() as abrupt_model:
        sigma = pm.Normal('sigma', mu=30, sigma=20)
        mu = pm.Uniform("mu1", 0, 1000)
        tau = pm.DiscreteUniform("tau" + "1", t.min(), t.max())

        for i in np.arange(2, n+1):
            _mu = pm.Uniform("mu" + str(i), 0, 1000)
            mu = T.switch(tau >= t, mu, _mu)
            tau = pm.DiscreteUniform("tau" + str(i), tau, t.max())
        s_obs = pm.Normal("s_obs", mu=mu, sigma=sigma, observed=s)

    with abrupt_model:
        trace = pm.sample(1000)
        az.plot_trace(trace)
        plt.show()
    return trace
