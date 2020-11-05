# coding:utf-8
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm


def bayes_single_detector(t, s):
    with pm.Model() as abrupt_model:
        steppoint = pm.DiscreteUniform(
            "steppoint", lower=t[1], upper=t[-1], testval=200
        )
        early_mu = pm.Uniform("early_mu", -50, 50)
        late_mu = pm.Uniform("late_mu", -50, 50)
        mu = pm.math.switch(steppoint >= t, early_mu, late_mu)
        sigma = pm.Normal('sigma', mu=30, sigma=20)
        s_obs = pm.Normal("s_obs", mu=mu, sigma=sigma, observed=s)

    with abrupt_model:
        trace = pm.sample(5000)
        az.plot_trace(trace)
        plt.show()
    return trace