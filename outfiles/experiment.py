import numpy as np
import os, re, itertools as it
from matplotlib import pyplot as plt

def get_experiment_series(folder):
    experiments = []
    for roots, dirs, files in os.walk(folder):
        for f in files:
            experiments.append(
                    Experiment(os.path.join(folder, f)))
    return experiments

class Experiment:
    def __init__(self, inf):
        with open(inf) as f:
            header = f.readline()
            prog = re.compile('\#(.*?)mm')
            try:
                self.height = prog.match(header).groups()[0]
            except:
                raise ValueError('File {} has no height in header'.format(inf))
        a = np.loadtxt(inf, skiprows=2, delimiter=',')
        self.distance = a[:, 1]
        self.weight = a[:, 2]
        self.trueZero()
        self.smooth()

    def smooth(self, fwhm=3):
        def fwhm2sigma(fwhm):
            return fwhm / np.sqrt(8 * np.log(2))

        sigma = fwhm2sigma(fwhm)
        smoothed_vals = np.zeros(self.weight.shape)
        for i, d in enumerate(self.distance):
            kernel = np.exp(-(self.distance - d) ** 2 / (2 * sigma ** 2))
            kernel = kernel / sum(kernel)
            smoothed_vals[i] = sum(self.weight * kernel)
        self.smoothed = smoothed_vals

    def find_breaks(self, fwmh=3, dx=0.1, offset=200, minval=1, plot=False):
        smooth_gradient = np.gradient(self.smoothed, dx)
        weight_at_break = breaks_at = left = right = 0
        for i, weight_gradient in enumerate(smooth_gradient[offset:]):
            if abs(weight_gradient) < minval:
                breaks_at = i+offset
                weight_at_break = self.weight[breaks_at]
                right = self.distance[breaks_at]
                break


        for i, val1, val2 in zip(it.count(), self.weight, self.weight[1:]):
            if abs(val1) < abs(weight_at_break) and abs(weight_at_break) < abs(val2):
                left = self.distance[i]
                break

        if plot:
            plt.plot([left]*2, [-50, 50], 'red')
            plt.plot([right]*2, [-50, 50], 'red')
            plt.plot([left-5, right+5], [weight_at_break]*2)
            plt.plot(self.distance, self.weight)
            plt.show()

        return right - left

    def trueZero(self):
        trueZero = []
        for i, val in enumerate(self.weight):
            if i > 500:
                trueZero.append(val)
        self.zeroed_weight = self.weight - np.average(trueZero)

    def maxWeight(self):
        return  np.min(self.weight)



