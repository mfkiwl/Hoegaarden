import arviz as az
import matplotlib.pyplot as plt
import numpy as np
from config.configutil import getpath
import scipy.io as io


def trace_export_4_mat(srcname, destname, n):
    trace = az.from_netcdf(srcname)
    data = {}
    size = trace.posterior.sigma.data.size
    data['sigma'] = trace.posterior.sigma.data.reshape(size, 1)
    # data['dtau'] = trace.posterior.dtau.data.reshape(size, 1)


    for i in np.arange(1, n + 1):
        data['mu' + str(i)] = trace.posterior['mu' + str(i)].data.reshape(size, 1)
        data['tau' + str(i)] = trace.posterior['tau' + str(i)].data.reshape(size, 1)
    data['mu' + str(n + 1)] = trace.posterior['mu' + str(n + 1)].data.reshape(size, 1)
    io.savemat(destname, data, oned_as='column')


if __name__ == '__main__':
    # trace_export_4_mat(getpath('tracepath') + 'sim_simple', getpath('data4origin') + 'sim_simple_posterior.mat', 3)
    trace_export_4_mat(getpath('tracepath') + 'bd9_4', getpath('data4origin') + 'bd9_4_up.mat', 2)

