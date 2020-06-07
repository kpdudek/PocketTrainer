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

class WorkoutPlayer(QWidget,FilePaths):
    '''
    This Widget is responsible for displaying the contents of a playlist
    A plugin must be loaded whenever the workout type switches
    '''
    go_home = pyqtSignal()

    pause = True

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Workout Player')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,1067,600)
            self.first_launch = False
            log('Set geometry of workout player window...')

        self.images_path = '%s/Images'%(self.user_path)
        self.play_path = '%s/play.png'%(self.images_path)
        self.pause_path = '%s/pause.png'%(self.images_path)

        self.layout = QGridLayout()

        self.get_playlists()

        self.button = QPushButton('Close')
        self.button.clicked.connect(self.switch_to_main_window)

        self.layout.addWidget(self.button,0,0)

        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()
    
    def get_playlists(self):
        '''
        This function loads every playlist JSON file from playlists folder
        The string with no json extension is displayed in the combo box in the constructor
        '''
        # self.user_name = pwd.getpwuid( os.getuid() ).pw_name
        # self.user_path = '/home/%s/PocketTrainer/'%self.user_name
        self.playlist_files = os.listdir('%sPlaylists/'%(self.user_path))
        log('{} playlists found...'.format(len(self.playlist_files)))

        self.first_get_playlists_call = True
        if self.first_get_playlists_call:
            self.spacer = QLabel()
            self.layout.addWidget(self.spacer,0,4,10,10)
            # self.first_get_playlists_call = False
        
        #Split the json extension of the plugin files for displaying in the QComboBox
        self.playlist_names = []
        for filename in self.playlist_files:
            self.playlist_names.append(filename.split('.')[0])
        
        for i in range(0,50):
            self.playlist_names.append('test_%d'%(i))


        self.select_playlist_widget = QWidget()
        self.select_playlist_stack = QVBoxLayout()

        newfont = QFont("Arial",18, QFont.Bold) 
        self.playlists_label = QLabel('Playlists')
        self.playlists_label.setFrameStyle(QFrame.Panel)
        self.playlists_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.playlists_label.setFont(newfont)
        self.select_playlist_stack.addWidget(self.playlists_label)

        self.playlist_list = QListWidget()
        self.playlist_list.addItems(self.playlist_names)
        self.select_playlist_stack.addWidget(self.playlist_list)

        self.select_playlist_button = QPushButton("Select Playlist")
        self.select_playlist_button.clicked.connect(self.load_playlist)
        self.select_playlist_stack.addWidget(self.select_playlist_button)

        self.select_playlist_widget.setLayout(self.select_playlist_stack)
        self.select_playlist_stack.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.select_playlist_widget,1,0,10,3)

    def load_playlist(self):
        '''
        The current text of the combo box gets a json extension and is then loaded from the playlists
        folder
        '''
        if self.first_get_playlists_call:
            try:
                self.layout.removeWidget(self.spacer)
                self.spacer.deleteLater()
                self.spacer = None
                self.first_get_playlists_call = False
            except:
                log("Tried to remove the workout player spacer, but it doesn't exist...")
        else:
            try:
                self.layout.removeWidget(self.workout_window_widget)
                self.workout_window_widget.deleteLater()
                self.workout_window_widget = None
            except:
                log("Tried to remove the workout window widget, but it doesn't exist...")

        self.workout_window_widget = QWidget()
        self.workout_window = QVBoxLayout()

        self.timer_label = QLabel('00 : 00 : 00.00')
        self.timer_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.workout_window.addWidget(self.timer_label)

        self.timer = QTimer()
        self.timer_count = 0.0
        self.timer_base = 100 # in milliseconds
        self.timer.setInterval(self.timer_base)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start()

        self.pause_play_button = QPushButton() 
        self.pause_play_button.setIcon(QIcon(self.play_path))
        self.pause_play_button.setIconSize(QSize(50,50))
        # self.pause_play_button.setFixedSize(100,100)
        self.pause_play_button.setStyleSheet("border-radius : 50; border : 0px solid black") 
        self.pause_play_button.clicked.connect(self.pause_play)
        self.workout_window.addWidget(self.pause_play_button)

        self.workout_window_widget.setLayout(self.workout_window)
        self.workout_window.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.workout_window_widget,0,4,10,10)

    def pause_play(self):
        if self.pause:
            self.pause = False
            self.pause_play_button.setIcon(QIcon(self.pause_path))
        else:
            self.pause = True
            self.pause_play_button.setIcon(QIcon(self.play_path))

    def update_timer(self):
        if not self.pause:
            self.timer_count += 1.0
            self.curr_time = self.timer_count*(float(self.timer_base)/1000.0)
            
            hours = self.curr_time/3600.0
            remain = hours - math.floor(hours)
            if hours < 0.01: # Get rid of e notation which screws up the coming split
                hours = 0.0

            minutes = remain * 60.0
            remain = minutes - math.floor(minutes)
            if minutes < 0.01: # Get rid of e notation which screws up the coming split
                minutes = 0.0

            seconds = remain * 60.0

            hours,scrap = str(hours).split('.')
            minutes,scrap = str(minutes).split('.')
            seconds,dec = str(seconds).split('.')

            time_vals = [hours,minutes,seconds]
            for count,val in enumerate(time_vals):
                if len(val) < 3:
                    try:
                        time_vals[count] = '0'*(2-len(val)) + val
                    except:
                        log('Couldnt format val...')
                        time_vals[count] = '00'
                else:
                    time_vals[count] = val[-2:]
                    log('Exceeded max session time of 60 hours')

            if len(dec) < 3:
                dec = dec + '0'*(2-len(dec))
            else:
                dec = dec[:2]

            time_label = time_vals[0] +' : '+time_vals[1]+' : '+time_vals[2]+'.'+dec
            self.timer_label.setText(time_label)
    
    def display_workout(self,workout):
        '''
        This function is called once for every workout in a playlist
        This function is responsible for:
            - displaying all characteristics in appropriate widgets
            - displaying a timer
        '''
        pass