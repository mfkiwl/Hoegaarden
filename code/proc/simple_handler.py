# coding:utf-8
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
from theano import tensor as T

from sim.sim_handler import sim_simple_steps


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
        sigma = pm.Normal('sigma', mu=10, sigma=5)
        # sigma = pm.Uniform('sigma', 5, 15)
        mu = pm.Uniform("mu1", -30, 30)
        tau = pm.DiscreteUniform("tau" + "1", t.min(), t.max())

        for i in np.arange(2, n + 2):
            _mu = pm.Uniform("mu" + str(i), -100, 0)
            mu = T.switch(tau >= t, mu, _mu)
            if (i < (n + 1)):
                tau = pm.DiscreteUniform("tau" + str(i), tau, t.max())
        s_obs = pm.Normal("s_obs", mu=mu, sigma=sigma, observed=s)

    with abrupt_model:
        # pm.find_MAP()
        trace = pm.sample(5000, tune=2000)
        az.plot_trace(trace)
        plt.show()
        az.plot_autocorr(trace)
        plt.show()
        pm.summary(trace)
    return trace


if __name__ == '__main__':
    # 1----bayes_single_detector(disp extraction) gauss noise only
    # l, noise, steps = 500, 10, np.array([[100, -30]])
    #
    # t, s = sim_simple_steps(l, noise, steps)
    # plt.plot(t, s)
    # plt.show()
    # bayes_single_detector(t, s)
    # 2----bayes_multiple_detector(disp extraction) gauss noise only
    l, noise, steps = 3600, 10, np.array([[1000, -30], [2500, -30], [3200, 30]])
    t, s = sim_simple_steps(l, noise, steps)
    plt.plot(t, s)
    plt.show()
    bayes_multiple_detector(t, s, 3)
