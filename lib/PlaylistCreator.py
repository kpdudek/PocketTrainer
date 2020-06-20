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

        self.workouts_title = QLabel('Workouts')
        self.workouts_title.setFrameStyle(QFrame.Panel)
        self.workouts_title.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.workouts_title.setStyleSheet("font:bold italic 18px; color: #353535; background-color: #ff9955")
        self.workout_selector_layout.addWidget(self.workouts_title)

        ### Layout for playlist creation options like [new,load]
        self.playlist_create_options = QHBoxLayout()

        self.new_playlist_button = QPushButton('New')
        self.playlist_create_options.addWidget(self.new_playlist_button)
        self.new_playlist_button.clicked.connect(self.new_playlist)

        # self.load_playlist_button = QPushButton('Load')
        # self.playlist_create_options.addWidget(self.load_playlist_button)
        # self.load_playlist_button.clicked.connect(self.load_playlist)

        self.workout_selector_layout.addLayout(self.playlist_create_options)

        ### Layout for selecting what to load
        # radio buttons for [workouts, playlists]
        self.display_selection_layout = QHBoxLayout()

        self.radio_stack = RadioStack(['Workouts','Playlists'])
        self.radio_stack.connect_toggle(self.display_selection_selected)
        self.display_selection_layout.addWidget(self.radio_stack)

        # push button to load the selection option
        # self.display_selection_button = QPushButton('Select')
        # self.display_selection_button.clicked.connect(self.display_selection_selected)
        # self.display_selection_layout.addWidget(self.display_selection_button)

        self.workout_selector_layout.addLayout(self.display_selection_layout)

        ### Workout type selector. hstacked combo box and button
        self.workout_type_select_widget = QWidget()
        self.workout_type_select_layout = QHBoxLayout()

        self.workout_type_selector = QComboBox()
        self.workout_type_selector.addItems(self.workout_types)
        self.workout_type_select_layout.addWidget(self.workout_type_selector)

        self.workout_type_select_button = QPushButton('Select')
        self.workout_type_select_button.clicked.connect(self.display_selection_selected)
        self.workout_type_select_layout.addWidget(self.workout_type_select_button)

        self.workout_type_select_widget.setLayout(self.workout_type_select_layout)
        self.workout_selector_layout.addWidget(self.workout_type_select_widget)

        ### Workout list
        self.workout_list = QListWidget()
        self.workout_names = []
        self.workout_list.addItems(self.workout_names)
        self.workout_selector_layout.addWidget(self.workout_list)
        self.workout_list.hide()

        ### Playlist list
        self.playlist_list = QListWidget()
        self.playlist_names = []
        self.playlist_list.addItems(self.playlist_names)
        self.workout_selector_layout.addWidget(self.playlist_list)
        self.playlist_list.hide()

        ### Add Workout button
        self.add_workout_button = QPushButton('Add Workout')
        self.add_workout_button.clicked.connect(self.add_workout)
        self.workout_selector_layout.addWidget(self.add_workout_button)
        self.add_workout_button.hide()

        ### Playlist Select button
        self.select_playlist_button = QPushButton('Load Playlist')
        self.select_playlist_button.clicked.connect(self.load_playlist)
        self.workout_selector_layout.addWidget(self.select_playlist_button)
        self.select_playlist_button.hide()

        self.display_selection_selected()
        self.workout_selector_widget.setLayout(self.workout_selector_layout)
        self.middle_layout.addWidget(self.workout_selector_widget)

    def display_selection_selected(self):
        # if radio button is workouts:
        #     load workouts function
        # elif radio button is playlists:
        #     load playlists function

        selection = self.radio_stack.get_checked_text()

        if selection == 'Playlists':
            self.display_playlists()
        elif selection == 'Workouts':
            self.display_workouts()
        else:
            log('Failed to load a selection...',color='r')
    
    def new_playlist(self):
        # Wipe the workout list widget
        # Wipe the playlist editor list widget
        # Set a variable = 'new'
        # Wait for user to hit 'select'
        self.added_workouts.clear()
        self.playlist_name_form.form_line_edit.setText('Type here...')

        pass

    def load_playlist(self):
        # Wipe the workout list widget
        # Wipe the playlist editor list widget
        # Set a variable = 'edit'
        # Wait for user to hit 'select'

        self.selected_playlist = self.playlist_list.currentItem().text()
        self.playlist_file_name = self.selected_playlist + '.json'
        try:
            with open('%sPlaylists/%s'%(self.user_path,self.playlist_file_name)) as fp:
                self.playlist = json.load(fp)
            log('Loaded playlist {%s}'%(self.playlist_file_name))
        except:
            log('Failed to load playlist {%s}'%(self.playlist_file_name))
            return

        self.playlist_name_form.form_line_edit.setText(self.selected_playlist)

        for key,workout in self.playlist.items():
            plugin,name = key.split(',')

            self.added_workouts.addItems([name])

        
        pass

    def display_playlists(self):
        # Shows the 'select playlist' button
        # Hides the 'add workout' button
        # Loads all playlists from the combo box value to the list

        self.add_workout_button.hide()
        self.select_playlist_button.show()
        self.workout_type_select_widget.hide()

        self.workouts_title.setText('User Playlists')
        
        self.workout_list.hide()
        self.playlist_list.show()
        
        self.playlist_names = os.listdir('%sPlaylists/'%(self.user_path))

        if not len(self.playlist_names) > 0:
            log('No playlists found...',color='r')
            return

        self.playlist_list.clear()

        # Strip the json extension
        for count,name in enumerate(self.playlist_names):
            self.playlist_names[count] = name.split('.')[0]
        
        self.playlist_list.addItems(self.playlist_names)

        pass

    def display_workouts(self):
        # Hides the 'select playlist' button
        # Shows the 'add workout' button
        # Loads all workouts from the combo box value to the list

        self.select_playlist_button.hide()
        self.add_workout_button.show()
        self.workout_type_select_widget.show()

        self.workout_list.show()
        self.playlist_list.hide()

        self.workouts_title.setText('Workouts')

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
        selected_workout = self.workout_list.currentItem().text()
        self.added_workouts.addItem(selected_workout)

        # workout_path = '%sLibrary/%s'%(self.selected_workout_type_json)
        self.added_workout_names.append(selected_workout)
        self.added_workout_list.append(self.library[self.workout_list.currentItem().text()])
        self.added_workout_type.append(self.selected_workout_type)

        log('%s added to playlist...'%(selected_workout))

    def playlist_editor(self):
        self.playlist_editor_widget = QWidget()
        self.playlist_editor_layout = QVBoxLayout()
        self.playlist_editor_layout.setAlignment(Qt.AlignCenter)

        self.editor_title = QLabel('Playlist Editor')
        self.editor_title.setFrameStyle(QFrame.Panel)
        self.editor_title.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.editor_title.setStyleSheet("font:bold italic 18px; color: #353535; background-color: #ff9955")
        self.playlist_editor_layout.addWidget(self.editor_title)

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
                key = self.added_workout_type[workout_idx] + ',' + self.added_workout_names[workout_idx]
                playlist_dict.update({key:self.added_workout_list[workout_idx]})
                count += 1
            
            with open('%sPlaylists/%s'%(self.user_path,playlist_name_json),'w') as fp:
                json.dump(playlist_dict,fp)
            log('Saved playlist {%s}'%(playlist_name),color='g')
        
        except:
            log('Failed to save playlist {%s}'%(playlist_name),color='r')
            return



