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
    start_time = datetime.datetime.now()
    curr_time = 0.0

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

        # Set base layout type for widget
        self.layout = QVBoxLayout()

        # Close button to return to the main window
        self.close_layout = QHBoxLayout()
        self.button = QPushButton('Close')
        self.button.clicked.connect(self.switch_to_main_window)
        self.close_layout.addWidget(self.button)
        self.close_layout.addStretch()
        self.layout.addLayout(self.close_layout)

        # Load all playlists and add them to the
        self.get_playlists()

        # Set base layout to the widget
        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()
    
    def get_playlists(self):
        '''
        This function loads every playlist JSON file from playlists folder
        The string with no json extension is displayed in the combo box in the constructor
        '''

        self.middle_layout = QHBoxLayout()

        # Spacer that reserves room for the workout window
        # self.first_get_playlists_call = True
        # if self.first_get_playlists_call:
        #     self.spacer = QLabel()
        #     self.layout.addWidget(self.spacer)
        #     # self.first_get_playlists_call = False

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
        # self.select_playlist_widget = QWidget()
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
        self.select_playlist_stack.setAlignment(Qt.AlignCenter)

        self.middle_layout.addLayout(self.select_playlist_stack)

        # self.select_playlist_widget.setLayout(self.select_playlist_stack)
        
        self.layout.addLayout(self.middle_layout)

    def load_playlist(self):
        '''
        The current text of the combo box gets a json extension and is then loaded from the playlists
        folder
        '''
        self.previous_plugin = None
        self.pause = True
        self.first_play = True
        self.workout_index = 0

        try:
            self.middle_layout.removeWidget(self.workout_window_widget)
            self.workout_window_widget.deleteLater()
            self.workout_window_widget = None
        except:
            log("Tried to remove the workout window, but it doesn't exist...")
        
        # if self.first_get_playlists_call:
        #     try:
        #         self.layout.removeWidget(self.spacer)
        #         self.spacer.deleteLater()
        #         self.spacer = None
        #         self.first_get_playlists_call = False
        #     except:
        #         log("Tried to remove the workout player spacer, but it doesn't exist...")
        # else:
        #     try:
        #         self.layout.removeWidget(self.workout_display_widget)
        #         self.workout_timer_widget.deleteLater()
        #         self.workout_timer_widget = None
        #     except:
        #         log("Tried to remove the workout window widget, but it doesn't exist...")

        #####################################################################
        ### Container widget for the workout viewer
        #####################################################################
        # self.workout_timer_widget = QWidget()
        self.workout_window_widget = QWidget()
        self.workout_window = QVBoxLayout()
        self.workout_window_widget.setLayout(self.workout_window)


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

        # Add widgets to the workout viewer
        # self.workout_timer_widget.setLayout(self.workout_timer)
        self.workout_timer.setAlignment(Qt.AlignCenter)
        self.workout_timer_buttons.setAlignment(Qt.AlignCenter)
        self.workout_timer.addLayout(self.workout_timer_buttons)

        # Add workout viewer to parent
        # self.layout.addWidget(self.workout_timer_widget)

        # Container for the workout information
        # The content of this container is determined based on the plugin specified
        #   in the playlist
        # self.workout_display_widget = QWidget()
        self.workout_display = QVBoxLayout()

        self.workout_window.addLayout(self.workout_display,3)
        self.workout_window.addLayout(self.workout_timer)
        # self.workout_display_widget.setLayout(self.workout_display)
        # self.workout_display.setAlignment(Qt.AlignVCenter)
        self.middle_layout.addWidget(self.workout_window_widget,3)
        # self.layout.addWidget(self.workout_display_widget)

        # Load selected playlist
        self.selected_playlist = self.playlist_names[self.playlist_list.currentRow()]
        playlist_file_name = self.selected_playlist + '.json'
        with open('%sPlaylists/%s'%(self.user_path,playlist_file_name)) as fp:
            self.playlist = json.load(fp)

        self.curr_idx = 0
        self.workout_idx = 0
        self.update_workout()
        self.workout_idx = 1

        # self.workout_player = WorkoutPlayer(playlist)
        # self.workout_player.current_workout_index = 0
        # self.workout_player.done_signal.connect(self.play_workout)

    def update_workout(self):
        '''
        This function takes the current workout index and loads that workout into a workout player object
        This function is called whenever play/pause is pressed, so it must be able to pause the workout currently playing
        When the workout is finished, the index is increased and the function recurses
        '''
        # Check the status of self.pause in workout_player
        # self.workout_player.play()

        if not self.curr_idx == self.workout_idx:
            for plugin in self.playlist:
                workout = self.playlist[plugin]
                plugin,index = plugin.split(',')

                # try:
                #     self.layout.removeWidget(self.workout_display_widget)
                #     self.workout_display_widget.deleteLater()
                #     self.workout_display_widget = None
                # except:
                #     log('Tried to remove the workout template but it doesnt exist...')

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
                
                # self.workout_display_widget = QWidget()
                # self.workout_display = QVBoxLayout()
                # self.workout_display_widget.setLayout(self.workout_display)
                # self.workout_display.setAlignment(Qt.AlignVCenter)
                
                # Populating form lines with strings from the plugin template
                self.workout_fields = []
                for key in self.workout_template:
                    val = key
                    self.workout_fields.append(WorkoutField(workout[key]))
                
                # Add form widget to the parent widget
                for count, key in enumerate(self.workout_fields):
                    self.workout_display.addLayout(self.workout_fields[count].form)

                # self.workout_display_widget.setLayout(self.workout_display)
                # self.workout_timer.addWidget(self.workout_display_widget)
                # self.workout_display.addLayout(self.workout_display)
                # self.workout_display_widget.update()

                # self.workout_window.addLayout(self.workout_display)
                self.previous_plugin = plugin

            self.curr_idx += 1

    def pause_play(self):
        '''
        When this function is called, the class attribute 'pause'
        is toggled
        '''
        if self.pause:
            self.pause = False
            self.pause_play_button.setIcon(QIcon(self.pause_path))
            
            # print(self.curr_time)
            self.update_workout()

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