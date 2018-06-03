import numpy as np
import os, re

def get_experiment_series(folder):
    experiments = []
    for roots, dirs, files in os.walk(folder):
        for f in files:
            experiments.append(Experiment(os.path.join(folder, f)))
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

    def plot(self, plotfunc, label=None):
        return plotfunc(self.distance, self.weight, label=label)

    def smooth(self, fwhm=3):
        def fwhm2sigma(fwhm):
            return fwhm / np.sqrt(8 * np.log(2))

        sigma = fwhm2sigma(fwhm)
        smoothed_force = np.zeros(self.force.shape)
        for i, d in enumerate(self.distance):
            kernel = np.exp(-(self.distance - d) ** 2 / (2 * sigma ** 2))
            kernel = kernel / sum(kernel)
            smoothed_vals[i] = sum(self.force * kernel)
        return distance, smoothed_force

    def trueZero(self):
        trueZero = []
        for i, val in enumerate(a[:, 2]):
            if i>500:
                trueZero.append(val)
        self.weight = self.weight[:, 2] - np.avg(trueZero)

    def maxWeight(self):
        return  np.min(self.weight)



