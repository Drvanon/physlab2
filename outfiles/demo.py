#! /usr/bin/python3

import click, re, os, numpy as np
import matplotlib.pyplot as plt
from numpy import exp
import itertools as it

from experiment import Experiment, get_experiment_series

@click.group()
def cli():
    pass

@cli.command()
@click.argument('folder', type=click.Path())
def all(folder):
    '''Show all data sets in one folder. Shortcut for 'demo.py show file1 -e
    file2 ....' '''
    handles = []
    experiments = get_experiment_series(folder)
    for ex in experiments:
        handles.append(ex.plot(plt.plot, label=ex.height)[0])
    plt.legend()
    plt.show()

@cli.command()
@click.option('--infile', '-i', type=click.Path(), multiple=True)
@click.option('--zero/--no-zero', '-z/-nz', help='Set the true zero to be the \
average of the last centimeter', default=False)
def show(infile, zero=False):
    """Render data in provided input file using row 2 and 3."""
    assert len(infile) > 0, "At least one inputfile must be provided"
    experiments = []
    for f in infile:
        experiments.append(Experiment(f))

    plt.xlabel(r'Distance in $mm$')
    plt.ylabel(r'Weight in $g$')
    handles = []
    for e in experiments:
        if zero:
            e.trueZero()
        handles.append(e.plot(plt.plot, e.height)[0])
    plt.legend(handles=handles)
    plt.show()

@cli.command()
@click.argument('folder', type=click.Path())
def max(folder):
    '''Find max value of every file in the provided folder.'''
    experiments = get_experiment_series(folder)
    experiments = sorted(experiments, key=lambda x: x.height)
    plt.plot([ex.height for ex in experiments], [ex.maxWeight() for ex in experiments])
    plt.show()

@cli.command()
@click.argument('infile', type=click.Path())
@click.option('--dx', default=0.1)
@click.option('--minval', default=1, type=int)
def smooth(infile, dx=0.1, minval=1):
    a = np.loadtxt(inf, skiprows=2, delimiter=',')
    new_weight = smooth_values(a[:, 1], a[:, 2])
    smooth_gradient = np.gradient(new_weight, dx)

    handleold, = plt.plot(a[:, 1], a[:, 2], label='old')
    handlenew, = plt.plot(a[:, 1], new_weight, label='new')
    hgradold, = plt.plot(a[:, 1], np.gradient(a[:, 2], dx), label='gradient of data')
    hgradnew, = plt.plot(a[:, 1], np.gradient(new_weight, dx), label='gradient of smooth')

    # Find where the graph hits about zero
    breaks_at = 0
    weight_at_break = 0
    offset = 200
    right = 0
    for i, grad_of_weigth in enumerate(smooth_gradient[offset:]):
        if abs(grad_of_weigth) < minval:
            breaks_at = i
            right = a[offset+i, 1]
            weight_at_break = a[i+offset, 2]
            break
    plt.plot([a[offset+i, 1], a[offset+i, 1]], [-50, 50], 'red')

    print(weight_at_break)
    # Find where that zero is mirrored
    left = 0
    for i, val1, val2 in zip(it.count(), a[:,2], a[1:, 2]):
        if abs(val1) < abs(weight_at_break) and abs(weight_at_break) <= abs(val2):
            left = a[i, 1]
            plt.plot([a[i, 1], a[i, 1]], [-50, 50], 'red')
            break

    click.echo('Found difference {}'.format(right - left))
    plt.legend([handlenew, handleold])
    plt.show()

if __name__=='__main__':
    cli()
