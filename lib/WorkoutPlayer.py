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

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # Set base layout type for widget
        self.layout = QGridLayout()

        # Load all playlists and add them to the
        self.get_playlists()

        # Close button to return to the main window
        self.button = QPushButton('Close')
        self.button.clicked.connect(self.switch_to_main_window)
        self.layout.addWidget(self.button,0,0)

        # Set base layout to the widget
        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()
    
    def get_playlists(self):
        '''
        This function loads every playlist JSON file from playlists folder
        The string with no json extension is displayed in the combo box in the constructor
        '''
        # Spacer that reserves room for the workout window
        self.first_get_playlists_call = True
        if self.first_get_playlists_call:
            self.spacer = QLabel()
            self.layout.addWidget(self.spacer,0,4,10,10)
            # self.first_get_playlists_call = False

        # Get all files in the Playlists folder
        self.playlist_files = os.listdir('%sPlaylists/'%(self.user_path))
        log('{} playlists found...'.format(len(self.playlist_files)))
        
        #Split the json extension of the plugin files for displaying in the QComboBox
        self.playlist_names = []
        for filename in self.playlist_files:
            self.playlist_names.append(filename.split('.')[0])

        #####################################################################
        ### Container widget for the playlist viewer
        #####################################################################
        self.select_playlist_widget = QWidget()
        self.select_playlist_stack = QVBoxLayout()

        self.playlists_label = QLabel('Playlists') #'Playlists'
        self.playlists_label.setFrameStyle(QFrame.Panel)
        self.playlists_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.playlists_label.setStyleSheet("font:bold italic 24px; color: #353535; background-color: #ff9955")
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

        #####################################################################
        ### Container widget for the workout viewer
        #####################################################################
        self.workout_window_widget = QWidget()
        self.workout_window = QVBoxLayout()

        # Container for the workout information
        # The content of this container is determined based on the plugin specified
        #   in the playlist
        self.workout_template_widget = QWidget()
        self.workout_template = QVBoxLayout()
        self.workout_template_widget.setLayout(self.workout_template)
        self.workout_template.setAlignment(Qt.AlignVCenter)
        self.workout_window.addWidget(self.workout_template_widget)

        # Set the label to display time
        self.timer_label = QLabel('00 : 00 : 00.00')
        self.timer_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.workout_window.addWidget(self.timer_label)

        # Create a timer widget
        self.timer = QTimer()
        self.timer_count = 0.0
        self.timer_base = 100 # in milliseconds
        self.timer.setInterval(self.timer_base)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start()

        # Button that toggles the pause attribute
        self.pause_play_button = QPushButton() 
        self.pause_play_button.setIcon(QIcon(self.play_path))
        self.pause_play_button.setIconSize(QSize(50,50))
        self.pause_play_button.setStyleSheet("border-radius : 25") 
        self.pause_play_button.clicked.connect(self.pause_play)
        self.workout_window.addWidget(self.pause_play_button)

        # gibberish labels for testing
        self.workout_name = QLabel('Workout Name')
        self.workout_template.addWidget(self.workout_name)
        self.workout_image = QLabel('IMG')
        self.workout_template.addWidget(self.workout_image)
        self.body_half = QLabel('Body Half')
        self.workout_template.addWidget(self.body_half)

        # Add widgets to the workout viewer
        self.workout_window_widget.setLayout(self.workout_window)
        self.workout_window.setAlignment(Qt.AlignCenter)
        # Add workout viewer to parent
        self.layout.addWidget(self.workout_window_widget,0,4,10,10)

        #####################################################################
        ### Play workout
        #####################################################################
        self.selected_playlist = self.playlist_names[self.playlist_list.currentRow()]
        playlist_file_name = self.selected_playlist + '.json'
        with open('%sPlaylists/%s'%(self.user_path,playlist_file_name)) as fp:
            playlist = json.load(fp)

        for workout in playlist:
            print(workout)
            pass

    def done_script(self):
        print('thread doing nothing...')
        pass

    def pause_play(self):
        '''
        When this function is called, the class attribute 'pause'
        is toggled
        '''
        if self.pause:
            self.pause = False
            self.pause_play_button.setIcon(QIcon(self.pause_path))
        else:
            self.pause = True
            self.pause_play_button.setIcon(QIcon(self.play_path))

    def update_timer(self):
        '''
        If the pause attribute is True, alter the global time
        If the pause attribute is False, alter the workout time
        '''
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
    

class WorkoutSignals(QObject):
    done = pyqtSignal()

class DisplayWorkouts(QRunnable):
    '''
    This function is called once for every workout in a playlist
    This function is responsible for:
        - displaying all characteristics in appropriate widgets
        - displaying a timer
    '''
    def __init__(self, playlist,layout):
        super().__init__()

        self.signals = WorkoutSignals()          

    @pyqtSlot()
    def run(self):
        for i in range(10):
            print('thread doing nothing...')
            time.sleep(1)
            self.signals.done.emit()