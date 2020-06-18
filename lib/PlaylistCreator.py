#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets import *
from utils import *

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import sys
import time
import datetime
import os
import json
import pwd
import random as rnd
import threading
import math

class PlaylistCreator(QWidget,FilePaths):
    '''
    A playlist contains the plugins required, workout settings, and the workouts
    '''

    go_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Playlist Creator')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,400,600)
            self.first_launch = False
            log('Set geometry of playlist creator window...',color='g')

        self.layout = QGridLayout()

        self.button = QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)

        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()