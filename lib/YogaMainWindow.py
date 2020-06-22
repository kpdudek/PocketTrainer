#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
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

class YogaMainWindow(QWidget,FilePaths):
    workout_creator_signal = pyqtSignal()
    playlist_creator_signal = pyqtSignal()
    workout_player_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pocket Trainer')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,400,600)
            self.first_launch = False
            log('Set geometry of main window...',color='g')

        self.layout = QVBoxLayout()

        # Title image
        # self.main_title = QLabel() 
        # self.main_title.setPixmap(QPixmap('%sImages/main.png'%(self.user_path)))
        # self.main_title.setFixedSize(400,200)
        # self.layout.addWidget(self.main_title)

        self.layout.addStretch()

        # Title label
        self.title = QLabel('\nPocket Trainer\nV1.0\n')
        self.title.setFrameStyle(QFrame.Panel)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.title.setStyleSheet("font:bold italic 48px; color: #353535; background-color: #ff9955")
        self.layout.addWidget(self.title)

        self.layout.addStretch()

        self.options = QVBoxLayout()
        # Workout Creator Button
        self.workout_creator_button = QPushButton('Workout Creator')
        # self.workout_creator_button.setFixedSize(350,100)
        self.workout_creator_button.clicked.connect(self.switch_to_workout_creator)
        self.workout_creator_button.setStyleSheet("font:bold 18px")
        self.options.addWidget(self.workout_creator_button)

        # Playlist Creator Button
        self.playlist_creator_button = QPushButton('Playlist Editor')
        # self.playlist_creator_button.setFixedSize(350,100)
        self.playlist_creator_button.clicked.connect(self.switch_to_playlist_creator)
        self.playlist_creator_button.setStyleSheet("font:bold 18px")
        self.options.addWidget(self.playlist_creator_button)

        # Workout Player Button
        self.workout_player_button = QPushButton('Workout Player')
        # self.workout_player_button.setFixedSize(350,100)
        self.workout_player_button.clicked.connect(self.switch_to_start_session)
        self.workout_player_button.setStyleSheet("font:bold 18px")
        self.options.addWidget(self.workout_player_button)

        # self.options.setAlignment(Qt.AlignCenter)

        self.layout.addLayout(self.options)

        self.layout.addStretch()

        # self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def switch_to_workout_creator(self):
        self.workout_creator_signal.emit()

    def switch_to_playlist_creator(self):
        self.playlist_creator_signal.emit()

    def switch_to_start_session(self):
        self.workout_player_signal.emit()