# coding:utf-8
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
from theano import tensor as T
import scipy.io as io

from config.configutil import getpath
from sim.sim_handler import sim_simple_steps, sim_gauss_randomwalk_steps


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


def bayes_multiple_detector(t, s, n, tracename):
    with pm.Model() as abrupt_model:
        sigma = pm.Normal('sigma', mu=30, sigma=5)
        # sigma = pm.Uniform('sigma', 5, 15)
        mu = pm.Uniform("mu1", -30, 30)
        tau = pm.DiscreteUniform("tau" + "1", t.min(), t.max())

        for i in np.arange(2, n + 2):
            _mu = pm.Uniform("mu" + str(i), -200, 0)
            mu = T.switch(tau >= t, mu, _mu)
            if (i < (n + 1)):
                tau = pm.DiscreteUniform("tau" + str(i), tau, t.max())
        s_obs = pm.Normal("s_obs", mu=mu, sigma=sigma, observed=s)
    g = pm.model_to_graphviz(abrupt_model)
    g.view()
    with abrupt_model:
        pm.find_MAP()
        trace = pm.sample(5000, tune=1000)
        az.plot_trace(trace)
        plt.show()
        az.plot_autocorr(trace)
        plt.show()
        az.to_netcdf(trace, getpath('tracepath') + tracename)
        pm.summary(trace)
    return trace


# add random walk
def bayes_multiple_detector_I(t, s, n, tracename):
    with pm.Model() as abrupt_model:
        sigma = pm.Normal('sigma', mu=30, sigma=5)
        # sigma = pm.Uniform('sigma', 5, 15)
        mu = pm.Uniform("mu1", -30, 30)
        tau = pm.DiscreteUniform("tau" + "1", t.min(), t.max())

        for i in np.arange(2, n + 2):
            _mu = pm.Uniform("mu" + str(i), -100, 0)
            mu = T.switch(tau >= t, mu, _mu)
            if (i < (n + 1)):
                tau = pm.DiscreteUniform("tau" + str(i), tau, t.max())
        # add random walk
        # sigma_rw = pm.Uniform("sigma_rw", 0, 10)
        g_rw = pm.GaussianRandomWalk("g_rw",
                                     tau=1,
                                     shape=len(s))
        s_obs = pm.Normal("s_obs", mu=g_rw+mu, sigma=sigma, observed=s)
    # g = pm.model_to_graphviz(abrupt_model)
    # g.view()
    with abrupt_model:
        pm.find_MAP()
        trace = pm.sample(5000, tune=1000)
        az.plot_trace(trace)
        plt.show()
        az.plot_autocorr(trace)
        plt.show()
        az.to_netcdf(trace, getpath('tracepath') + tracename)
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
    # l, noise, steps = 3600, 30, np.array([[1000, -50], [2500, -50], [3200, 100]])
    # t, s = sim_simple_steps(l, noise, steps)
    # io.savemat(getpath('data4origin') + 'sim_simple_raw.mat', {'t': t, 'x': s}, oned_as='column')
    # plt.plot(t, s)
    # plt.show()
    # bayes_multiple_detector(t, s, 3,'test')
    # 3----bayes_multiple_detector(disp extraction) gauss noise+ gauss random walk
    l, noise, randnoise, steps = 3600, 30, 5, np.array([[1000, -50], [2500, -50], [3200, 100]])
    t, s = sim_gauss_randomwalk_steps(l, noise, randnoise, steps)
    io.savemat(getpath('data4origin') + 'sim_gauss_randomwalk_raw.mat', {'t': t, 'x': s}, oned_as='column')
    plt.plot(t, s)
    plt.show()
    bayes_multiple_detector_I(t, s, 3, 'sim_gauss_randomwalk')
