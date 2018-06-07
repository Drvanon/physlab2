#! /usr/bin/env python3

import sys
import os
import random
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from experiment import Experiment, get_experiment_series

import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.2"

class MyDynamicMplCanvas(FigureCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        experiments = []
        for f in self.window().selected_files:
            if f[-1] == '/':
                experiments += get_experiment_series(f)
            else:
                experiments.append(Experiment(f))

        handles = []
        for ex in experiments:
            handles.append(self.axes.plot(ex.distance, ex.weight, label="{}mm {}".format(ex.height, ex.inf))[0])
        self.axes.legend(handles=handles)
        self.draw()

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Setup window
        QtWidgets.QMainWindow.__init__(self)
        self.setGeometry(10, 10, 900, 900)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        # Setup menus'
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)
        self.main_widget = QtWidgets.QWidget(self)

        # Setup content
        self.horizontalGroupBox = QtWidgets.QGroupBox()
        h = QtWidgets.QHBoxLayout()

        # Setup file selector
        self.selected_files = []
        self.tree = QtWidgets.QTreeView()
        model = QtWidgets.QFileSystemModel()
        model.setRootPath('')

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        self.tree.setFixedWidth(300)

        self.tree.setModel(model)
        for i in range(1, model.columnCount()):
            self.tree.hideColumn(i)

        self.tree.setRootIndex(model.index(os.path.dirname(os.path.realpath(__file__))))
        self.tree.expandAll()
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tree.selectionModel().selectionChanged.connect(self.item_selection_changed_slot)
        h.addWidget(self.tree)

        self.verticalGroupBox = QtWidgets.QGroupBox()
        v = QtWidgets.QVBoxLayout()

        # Set up the plot
        self.main_widget.setLayout(h)
        self.dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        h.addWidget(self.dc)

        self.nav = NavigationToolbar(self.dc, self.dc, coordinates=False)
        self.nav.setMinimumWidth(300)
        self.nav.setStyleSheet("QToolBar { border: 0px }")

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)


    def item_selection_changed_slot(self, selection):
        self.statusBar().showMessage("Selection change")
        paths = []
        for i in self.tree.selectedIndexes():
            parents = []
            cur = i
            while not cur.parent().data() == os.path.split(os.getcwd())[-1]:
                cur = i.parent()
                parents.append(cur.data())
            if cur == i:
                paths.append(i.data() + '/')
            else:
                paths.append(os.path.join(*parents,  i.data()))
        self.selected_files = paths
        self.dc.update_figure()

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                """This program is based off:
embedding_in_qt5.py example

Copyright 2018 Robin A. Dorstijn
Intended for open source use only.
"""
                                )


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
