import arviz as az
import matplotlib.pyplot as plt

from config.configutil import getpath


def trace_plot(name):
    trace=az.from_netcdf(name)
    az.plot_trace(trace)
    plt.show()

if __name__ == '__main__':
    trace_plot(getpath('tracepath')+'sim_simple')