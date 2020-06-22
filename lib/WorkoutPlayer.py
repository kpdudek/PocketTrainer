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

    pause = None # pause and play the workout
    previous_plugin = None

    workout_split_start = 0.0

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Workout Player')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,1067,600)
            self.first_launch = False
            log('Set geometry of workout player window...',color='g')

        self.images_path = '%s/Images'%(self.user_path)
        self.play_path = '%s/play.png'%(self.images_path)
        self.pause_path = '%s/pause.png'%(self.images_path)

        # Set base layout type for widget
        self.layout = QVBoxLayout()

        # Close button to return to the main window
        self.close_layout = QHBoxLayout()

        self.button = QPushButton('Close')
        self.button.clicked.connect(self.switch_to_main_window)
        self.close_layout.addWidget(self.button)
        self.close_layout.addStretch()

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh)
        self.close_layout.addWidget(self.refresh_button)

        self.layout.addLayout(self.close_layout)

        # Load all playlists and add them to the list
        self.get_playlists()

        # Set base layout to the widget
        self.setLayout(self.layout)

    def switch_to_main_window(self):
        '''
        This function emits the top level widget's go home signal
        The controller which is managing the top level widgets connects to this signal and will hide
            this widget
        '''
        self.go_home.emit()

    def refresh(self):
        # Get all files in the Playlists folder
        self.playlist_files = os.listdir('%sPlaylists/'%(self.user_path))
        log('{} playlists found...'.format(len(self.playlist_files)))
        
        #Split the json extension of the plugin files for displaying in the QComboBox
        self.playlist_names = []
        for filename in self.playlist_files:
            self.playlist_names.append(filename.split('.')[0])

        self.playlist_list.clear()
        self.playlist_list.addItems(self.playlist_names)
    
    def get_playlists(self):
        '''
        This function loads every playlist JSON file from playlists folder
        The string with no json extension is displayed in the combo box in the constructor
        '''

        # Middle layout contains the playlist selector and the playlist player
        self.middle_layout = QHBoxLayout()

        # Get all files in the Playlists folder
        self.playlist_files = os.listdir('%sPlaylists/'%(self.user_path))
        log('{} playlists found...'.format(len(self.playlist_files)))
        
        #Split the json extension of the plugin files for displaying in the QComboBox
        self.playlist_names = []
        for filename in self.playlist_files:
            self.playlist_names.append(filename.split('.')[0])

        # Layout for selecting a playlist. Contains:
        #   - Title label
        #   - Filters (TODO)
        #   - Playlists list
        #   - Select button
        self.select_playlist_stack = QVBoxLayout()

        # Title label
        self.playlists_label = QLabel('Playlists')
        self.playlists_label.setFrameStyle(QFrame.Panel)
        self.playlists_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.playlists_label.setStyleSheet("font:bold italic 24px; color: #353535; background-color: #ff9955")
        self.select_playlist_stack.addWidget(self.playlists_label)

        # List of all/filtered playlists
        self.playlist_list = QListWidget()
        self.playlist_list.addItems(self.playlist_names)
        self.select_playlist_stack.addWidget(self.playlist_list)

        # Select playlist button. This button loads the playlist into the player
        self.select_playlist_button = QPushButton("Select Playlist")
        self.select_playlist_button.clicked.connect(self.load_playlist)
        self.select_playlist_stack.addWidget(self.select_playlist_button)
        self.select_playlist_stack.setAlignment(Qt.AlignCenter)

        # Add playlist selector into the middle layout and then add middle to the top level layout
        self.middle_layout.addLayout(self.select_playlist_stack)
        self.layout.addLayout(self.middle_layout)

    def load_playlist(self):
        '''
        The current text of the combo box gets a json extension and is then loaded from the playlists
        folder
        '''
        try:
            self.middle_layout.removeWidget(self.workout_window_widget)
            self.workout_window_widget.deleteLater()
            self.workout_window_widget = None
        except:
            log("Tried to remove the workout window, but it doesn't exist...")

        #####################################################################
        ### Container widget for the workout viewer
        #####################################################################
        self.workout_window_widget = QWidget()
        self.workout_window = QVBoxLayout()
        self.workout_window_widget.setLayout(self.workout_window)

        # Layout for all timing aspects
        #   - label to display workout time
        #   - buttons for play/pause, skip
        self.workout_timer = QVBoxLayout()
        self.workout_timer_buttons = QHBoxLayout()

        # Set the label to display time
        self.timer_label = QLabel('00 : 00 : 00.00')
        self.timer_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.workout_timer.addWidget(self.timer_label)

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
        self.workout_timer_buttons.addWidget(self.pause_play_button)

        # Center justify and add timing buttons layout to the timing layout
        self.workout_timer.setAlignment(Qt.AlignCenter)
        self.workout_timer_buttons.setAlignment(Qt.AlignCenter)
        self.workout_timer.addLayout(self.workout_timer_buttons)

        # Container for the workout information
        # The content of this container is determined based on the plugin specified
        #   in the playlist
        self.workout_display = QVBoxLayout()

        self.workout_window.addLayout(self.workout_display,3)
        self.workout_window.addLayout(self.workout_timer)

        self.middle_layout.addWidget(self.workout_window_widget,3)

        # Load selected playlist
        # self.selected_playlist = self.playlist_names[self.playlist_list.currentRow()]
        self.selected_playlist = self.playlist_list.currentItem().text()
        self.playlist_file_name = self.selected_playlist + '.json'
        try:
            with open('%sPlaylists/%s'%(self.user_path,self.playlist_file_name)) as fp:
                self.playlist = json.load(fp)
            log('Loaded playlist {%s}'%(self.playlist_file_name))
        except:
            log('Failed to load playlist {%s}'%(self.playlist_file_name))
            return

        # Set playlist values and load the first workout
        # Starting state is paused
        self.start_time = datetime.datetime.now() # When the workout started
        self.curr_time = 0.0

        self.curr_idx = -1
        self.workout_idx = 0

        self.pause = True

        # print(self.playlist)
        self.playlist_enum = enumerate(self.playlist)
        # print(self.playlist_enum)

        # g = next(self.playlist_enum)
        # print(g)

        self.curr_workout_duration = 0.0
        self.workout_split_start = self.curr_time

        self.first_play = True
        self.pause = True
        # self.pause = False
        self.update_workout()
        # self.pause = True

        self.workout_idx = 1

    def update_workout(self):
        '''
        This function takes the current workout index and loads that workout into a workout player object
        This function is called whenever play/pause is pressed, so it must be able to pause the workout currently playing
        When the workout is finished, the index is increased and the function recurses
        '''

        if self.first_play:
            self.refresh_workout()
            self.first_play = False

        elif ((self.curr_time - self.workout_split_start) > self.curr_workout_duration) and (not self.pause):
            # self.workout_idx += 1
        
        # if (not self.curr_idx == self.workout_idx) and (not self.pause):
            self.curr_idx += 1
            self.workout_idx += 1

            self.workout_split_start = self.curr_time

            self.refresh_workout()

    def refresh_workout(self):
        try:
            self.curr_playlist_idx = next(self.playlist_enum)
        except:
            log('Reached end of playlist {%s}'%(self.playlist_file_name))
            return
        
        try:
            self.workout_display.removeWidget(self.workout_fields_widget)
            self.workout_fields_widget.deleteLater()
            self.workout_fields_widget = None
        except:
            log("Tried to remove the workout fields widget, but it doesn't exist...")
        
        self.workout_fields_widget = QWidget()
        self.workout_fields_layout = QVBoxLayout()

        self.curr_workout = self.playlist[self.curr_playlist_idx[1]]
        log('Starting workout {%s}'%(self.curr_playlist_idx[1]))

        self.curr_workout_duration = float(self.curr_workout['Duration'])
        log('Current workout duration')

        # workout = self.playlist[plugin]
        plugin  = self.curr_playlist_idx[1]
        plugin,index = plugin.split(',')

        if not (plugin == self.previous_plugin):
            # Load the selected workouts plugin json file
            self.plugin_json = '%s.json'%(plugin)
            try:
                fp = open('%s/Plugins/%s'%(self.user_path,self.plugin_json),'r')
                self.workout_plugin = json.load(fp)
                log("Loaded plugin {%s}..."%(plugin))
            except:
                log("Failed to load plugin {%s}..."%(plugin))
            
            for key in self.workout_plugin:
                self.workout_name = key
                self.workout_template = self.workout_plugin[key]
        
        # Populating form lines with strings from the plugin template
        self.workout_fields = []
        for key in self.workout_template:
            val = key
            self.workout_fields.append(WorkoutField(self.curr_workout[key]))
        
        # Add form widget to the parent widget
        for count, key in enumerate(self.workout_fields):
            self.workout_fields_layout.addLayout(self.workout_fields[count].form)

        self.workout_fields_widget.setLayout(self.workout_fields_layout)
        self.workout_display.addWidget(self.workout_fields_widget)
        self.previous_plugin = plugin            

    def pause_play(self):
        '''
        When this function is called, the class attribute 'pause'
        is toggled and then the workout is updated
        '''
        # Play the workout
        if self.pause:
            self.pause = False
            self.pause_play_button.setIcon(QIcon(self.pause_path))
            self.update_workout()

            log('Split time: ' + str(self.curr_time).split('.')[0]+'.'+ str(self.curr_time).split('.')[1][0])

        # Pause the workout
        else:
            self.pause = True
            self.pause_play_button.setIcon(QIcon(self.play_path))
            self.update_workout()

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

        self.update_workout()