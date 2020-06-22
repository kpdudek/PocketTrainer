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

class WorkoutCreator(QWidget,FilePaths): 
    # Signals
    go_home = pyqtSignal()

    # Workout creator attributes
    plugins = None
    workout_types = None
    previous_workout_selected = None # Previous QComboBox value.

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Workout Creator')

        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,600,400)
            self.first_launch = False
            log('Set geometry of workout creator window...',color='g')

        self.layout = QVBoxLayout()
        self.starting_row = 2 # Starting row for the form
        self.width = 6 # Grid width used 
        self.height = 15

        # Set 'Home' button in top left corner
        self.home_layout = QHBoxLayout()
        self.button = QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)
        self.home_layout.addWidget(self.button)
        self.home_layout.addStretch()

        self.layout.addLayout(self.home_layout)

        self.workout_creator_title = QLabel('Workout Creator')
        self.workout_creator_title.setFrameStyle(QFrame.Panel)
        self.workout_creator_title.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.workout_creator_title.setStyleSheet("font:bold italic 24px; color: #353535; background-color: #ff9955")
        self.layout.addWidget(self.workout_creator_title)

        # Load plugins and display in combo box
        self.load_plugins()

        self.selector_layout = QHBoxLayout()

        self.workout_type_selector = QComboBox()
        self.workout_type_selector.addItems(self.workout_types)
        self.selector_layout.addWidget(self.workout_type_selector) 

        self.select_plugin_button = QPushButton('Select')
        self.select_plugin_button.clicked.connect(self.display_form)
        self.selector_layout.addWidget(self.select_plugin_button)

        self.layout.addLayout(self.selector_layout)

        # self.spacer = QLabel()
        # self.layout.addWidget(self.spacer,self.starting_row,0,self.height,self.width)

        self.add_workout_button = QPushButton('Add')
        self.add_workout_button.clicked.connect(self.add_workout)
        self.workout_button_added = False
        # self.layout.addWidget(self.add_workout_button,self.height+1,0,self.height+1,self.width)
        
        # Count the number of widgets added in the constructor. These cannot be deleted later on
        self.num_header_widgets = 3
        # Set layout of widget
        self.setLayout(self.layout)

        self.display_form()

    def switch_to_main_window(self):
        self.go_home.emit()
    
    def load_plugins(self):
        # Get plugins from folder and load into combo box
        # Load JSON into a class attribute
        # self.user_name = pwd.getpwuid( os.getuid() ).pw_name
        # self.user_path = '/home/%s/PocketTrainer/'%self.user_name
        self.plugins = os.listdir('%sPlugins/'%(self.user_path))
        log('{} plugins found...'.format(len(self.plugins)))

        # Split the json extension of the plugin files for displaying in the QComboBox
        self.workout_types = []
        for filename in self.plugins:
            self.workout_types.append(filename.split('.')[0])

    def display_form(self):
        '''
        On 'select_plugin_button' press
        Pull current selection from the plugin combo box and display the corresponding form
        '''
        # Get the selected workout from the QComboBox
        workout_selected = self.workout_type_selector.currentText()
        if self.previous_workout_selected == workout_selected:
            return

        # Delete the existing Form Widget in order to display the new selected workout        
        try:
            self.layout.removeWidget(self.form_widget)
            self.form_widget.deleteLater()
            self.form_widget = None
        except:
            log("Tried to remove the form entry, but it doesn't exist...")

        # Load the selected workouts plugin json file
        self.workout_selected_json = '%s.json'%(workout_selected)
        try:
            fp = open('%s/Plugins/%s'%(self.user_path,self.workout_selected_json),'r')
            self.workout_plugin = json.load(fp)
            log("Loaded plugin {%s}..."%(workout_selected))
        except:
            log("Failed to load plugin {%s}..."%(workout_selected))
        
        for key in self.workout_plugin:
            self.workout_name = key
            self.workout_template = self.workout_plugin[key]
        
        # Populating form lines with strings from the plugin template
        self.form_lines = []
        for key in self.workout_template:
            val = key
            self.form_lines.append(FormEntry(val,'Type here...'))
        
        # Stack the form lines in a QVBoxLayout
        self.form_widget = QWidget()
        form = QVBoxLayout()

        self.workout_name = FormEntry('Workout Name','Type here...')
        form.addWidget(self.workout_name)

        # Add form widget to the parent widget
        for count, key in enumerate(self.form_lines):
            form.addWidget(key)
        self.form_widget.setLayout(form)
        self.layout.addWidget(self.form_widget)

        form.addWidget(self.add_workout_button)
        self.previous_workout_selected = workout_selected

    def check_entries(self):
        # make sure all fields are valid based on expected type
        # check if type of workout template matches line entry
        #   if string: make sure its not 'Type here...'
        for line in self.form_lines:
            key = line.form_line_label.text()
            key,colon = key.split(':') # Split the colon from the label text
            entry = line.form_line_edit.text()
            data_type = self.workout_template[key]

            if data_type == 'string':
                if entry == 'Type here...':
                    log('Line edits not changed on line {%s}...'%(key))
                    return False

            elif data_type == 'float':
                try:
                    entry = float(entry)
                except:
                    log('Line {%s} was expecting a float but did not receive one...'%(key))
                    return False

            elif data_type == 'int':
                try:
                    entry = int(entry)
                except:
                    log('Line {%s} was expecting an int but did not receive one...'%(key))
                    return False

            elif data_type == "bool":
                trues = ['yes','Yes','YES','ya','yeet','yea','Yea','YEA','True','true','TRUE']
                falses = ['no','No','NO','False','false','FALSE']
                acceptable_responses = trues + falses
                if not entry in acceptable_responses:
                    log('Response in line {%s} could not be converted to a bool...'%(key))
                    return False
            else:
                log("Data type of template not recognized...")

        return True

    def add_workout(self):
        # Check if workout with the same name exists

        if self.check_entries():
            #Load json
            try:
                lp = open('%s/Library/%s'%(self.user_path,self.workout_selected_json),'r')
            except:
                log("Library file {%s}doesn't exist. Creating one..."%(self.workout_selected_json))
                lp = open('%s/Library/%s'%(self.user_path,self.workout_selected_json),'w')

            if not os.stat('%s/Library/%s'%(self.user_path,self.workout_selected_json)).st_size == 0:
                library = json.load(lp)
            else:
                lp.close()
                library = {}
                log('Library is empty. Skipping JSON load and closing file...')
            
            new_entry = {}
            for count, key in enumerate(self.workout_template):
                new_entry.update({key : self.form_lines[count].form_line_edit.text()})

            idx = len(library)
            workout_name = self.workout_name.form_line_edit.text()
            
            library.update({workout_name : new_entry})
            try:
                lp = open('%s/Library/%s'%(self.user_path,self.workout_selected_json),'w')
                json.dump(library, lp)
                log("Library appended successfully...",color='g')
            except:
                log("Library could not be appended...",color='r')

        else:
            log("Invalid entries...",color='r')
        pass