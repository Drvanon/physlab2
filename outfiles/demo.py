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
    """
    Show all data sets in one folder. Shortcut for 'demo.py show file1 -e file2 ....'
    """
    handles = []
    experiments = get_experiment_series(folder)
    for ex in experiments:
        handles.append(
            plt.plot(
                ex.distance,
                ex.weight,
                label=ex.height)[0]
            )
    plt.legend()
    plt.show()

@cli.command()
@click.option('--infile', '-i', type=click.Path(), multiple=True)
@click.option('--zero/--no-zero', '-z/-nz', default=False,
    help='Set the true zero to be the average of the last centimeter')
def show(infile, zero=False):
    """
    Render data in provided input file using row 2 and 3.
    """
    assert len(infile) > 0, "At least one inputfile must be provided"
    experiments = []
    for f in infile:
        experiments.append(Experiment(f))

    plt.xlabel(r'Distance in $mm$')
    plt.ylabel(r'Weight in $g$')
    handles = []
    for e in experiments:
        if zero:
            handles.append(
                plt.plot(e.distance, e.zeroed_weight)
                )
        else:
            handles.append(plt.plot(
                e.distance, e.weight, label=e.height)[0])
    plt.legend(handles=handles)
    plt.show()

@cli.command()
@click.argument('folder', type=click.Path())
def max(folder):
    """
    Find max value of every file in the provided folder.
    """
    experiments = get_experiment_series(folder)
    experiments = sorted(experiments, key=lambda x: x.height)
    plt.plot([ex.height for ex in experiments], [ex.maxWeight() for ex in experiments])
    plt.show()

@cli.command()
@click.argument('infile', type=click.Path())
@click.option('--dx', default=0.1)
@click.option('--minval', default=1, type=int)
@click.option('--plot/--no-plot', default=False)
@click.option('--fwmh', default=3)
def find_breaks(infile, dx, minval, plot, fwmh):
    """
    Find the breaking point of the provided graph
    """
    ex = Experiment(infile)
    ex.find_breaks(minval=minval, dx=dx, plot=plot)

if __name__=='__main__':
    cli()
