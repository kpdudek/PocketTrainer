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

    plugins = None
    workout_types = None
    previous_workout_selected = None # Previous QComboBox value.

    added_workout_list = []
    added_workout_type = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Playlist Creator')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,800,600)
            self.first_launch = False
            log('Set geometry of playlist creator window...',color='g')

        # Set base layout type for widget
        self.layout = QVBoxLayout()

        # Close button to return to the main window
        self.close_layout = QHBoxLayout()
        self.button = QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)
        self.close_layout.addWidget(self.button)
        self.close_layout.addStretch()
        self.layout.addLayout(self.close_layout)

        self.middle_layout = QHBoxLayout()
        self.layout.addLayout(self.middle_layout)

        # Set base layout to the widget
        self.setLayout(self.layout)

        # Load form entries
        self.load_plugins()
        self.workout_selector()
        self.playlist_editor()

    def switch_to_main_window(self):
        self.go_home.emit()

    def load_plugins(self):
        self.plugins = os.listdir('%sPlugins/'%(self.user_path))
        log('{} plugins found...'.format(len(self.plugins)))

        # Split the json extension of the plugin files for displaying in the QComboBox
        self.workout_types = []
        for filename in self.plugins:
            self.workout_types.append(filename.split('.')[0])
    
    def workout_selector(self):
        self.workout_selector_widget = QWidget()
        self.workout_selector_layout = QVBoxLayout()
        self.workout_selector_layout.setAlignment(Qt.AlignCenter)
        
        # Workout type selector. hstacked combo box and button
        self.workout_type_select_layout = QHBoxLayout()

        self.workout_type_selector = QComboBox()
        self.workout_type_selector.addItems(self.workout_types)
        self.workout_type_select_layout.addWidget(self.workout_type_selector)

        self.workout_type_select_button = QPushButton('Select')
        self.workout_type_select_button.clicked.connect(self.display_workouts)
        self.workout_type_select_layout.addWidget(self.workout_type_select_button)

        self.workout_selector_layout.addLayout(self.workout_type_select_layout)

        # Workout list
        self.workout_list = QListWidget()
        self.workout_names = []
        self.workout_list.addItems(self.workout_names)
        self.workout_selector_layout.addWidget(self.workout_list)

        # Workout add button
        self.add_workout_button = QPushButton('Add Workout')
        self.add_workout_button.clicked.connect(self.add_workout)
        self.workout_selector_layout.addWidget(self.add_workout_button)

        self.workout_selector_widget.setLayout(self.workout_selector_layout)
        self.middle_layout.addWidget(self.workout_selector_widget)

    def display_workouts(self):
        self.selected_workout_type = self.workout_type_selector.currentText()
        log('Selected workout type {%s}'%(self.selected_workout_type))

        self.selected_workout_type_json = self.selected_workout_type + '.json'

        try:
            is_empty = os.stat('%s/Library/%s'%(self.user_path,self.selected_workout_type_json)).st_size == 0
        except:
            log('Library {%s} is empty.'%(self.selected_workout_type),color='y')
            self.workout_list.clear()
            return
        
        try:
            lp = open('%s/Library/%s'%(self.user_path,self.selected_workout_type_json),'r')
        except:
            log("Library file {%s} doesn't exist. Creating one..."%(self.selected_workout_type_json),color='y')
            lp = open('%s/Library/%s'%(self.user_path,self.selected_workout_type_json),'w')

        if not is_empty:
            self.library = json.load(lp)
        else:
            lp.close()
            self.library = {}
            log('Library {%s} is empty. Skipping JSON load and closing file...'%(self.selected_workout_type),color='y')
        
        self.workout_names = []
        self.workout_list.clear()

        for name,workout in self.library.items():
            # for workout_field,value in self.library[idx].items():
            #     self.workout_names
            self.workout_names.append(name)
        self.workout_list.addItems(self.workout_names)
    
    def add_workout(self):
        selected_workout = [self.workout_list.currentItem().text()]
        self.added_workouts.addItems(selected_workout)

        # workout_path = '%sLibrary/%s'%(self.selected_workout_type_json)
        self.added_workout_list.append(self.library[self.workout_list.currentItem().text()])
        self.added_workout_type.append(self.selected_workout_type)

        log('%s added to playlist...'%(selected_workout))

    def playlist_editor(self):
        self.playlist_editor_widget = QWidget()
        self.playlist_editor_layout = QVBoxLayout()
        self.playlist_editor_layout.setAlignment(Qt.AlignCenter)

        # Playlist name form
        self.playlist_name_form = FormEntry('Playlist Name','Type here...')
        self.playlist_editor_layout.addWidget(self.playlist_name_form)

        # Workout list
        self.added_workouts = QListWidget()
        self.added_workout_names = []
        self.added_workouts.addItems(self.added_workout_names)
        self.playlist_editor_layout.addWidget(self.added_workouts)

        # Save Playlist
        self.save_playlist_button = QPushButton('Save Playlist')
        self.save_playlist_button.clicked.connect(self.save_playlist)
        self.playlist_editor_layout.addWidget(self.save_playlist_button)
        
        ### Set layout of playlist editor widget and add to middle layout
        self.playlist_editor_widget.setLayout(self.playlist_editor_layout)
        self.middle_layout.addWidget(self.playlist_editor_widget)

    def save_playlist(self):

        playlist_name = self.playlist_name_form.form_line_edit.text()
        playlist_name_json = playlist_name + '.json'

        num_workouts = self.added_workouts.count()
        log('Adding %d workouts to the %s playlist...'%(num_workouts,playlist_name))

        count = 0
        try:
            playlist_dict = {}
            for workout_idx in range(0,len(self.added_workout_list)):
                key = self.added_workout_type[workout_idx] + ',%d'%(count)
                playlist_dict.update({key:self.added_workout_list[workout_idx]})
                count += 1
            
            with open('%sPlaylists/%s'%(self.user_path,playlist_name_json),'w') as fp:
                json.dump(playlist_dict,fp)
            log('Saved playlist {%s}'%(playlist_name))
        
        except:
            log('Failed to save playlist {%s}'%(playlist_name),color='r')
            return



