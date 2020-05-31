#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets import *

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import sys
import time
import datetime
import os
import json
import pwd
import random as rnd

def log(text):
    curr_time = str(datetime.datetime.now())
    curr_time = '[%s]'%(curr_time)
    log_msg = curr_time + ' ' + text
    print(log_msg)

    name = pwd.getpwuid( os.getuid() ).pw_name
    user_path = '/home/%s/PocketTrainer/'%name

    with open('%slogs.txt'%(user_path),'a') as fp:
        if not os.stat('%slogs.txt'%(user_path)).st_size == 0:
            if text == 'Session started...':
                fp.write('\n\n\n'+ log_msg)
            else:
                fp.write('\n'+ log_msg)
        else:
            fp.write(log_msg)

    try:    
        fp.close()
    except:
        print('Error closing log file...')

class YogaMainWindow(QWidget):
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
            log('Set geometry of main window...')

        self.layout = QVBoxLayout()

        # Workout Creator Button
        self.workout_creator_button = QPushButton('Workout Creator')
        self.workout_creator_button.clicked.connect(self.switch_to_workout_creator)
        self.layout.addWidget(self.workout_creator_button)

        # Playlist Creator Button
        self.playlist_creator_button = QPushButton('Playlist Creator')
        self.playlist_creator_button.clicked.connect(self.switch_to_playlist_creator)
        self.layout.addWidget(self.playlist_creator_button)

        # Workout Player Button
        self.workout_player_button = QPushButton('Workout Player')
        self.workout_player_button.clicked.connect(self.switch_to_start_session)
        self.layout.addWidget(self.workout_player_button)

        self.setLayout(self.layout)

    def switch_to_workout_creator(self):
        self.workout_creator_signal.emit()
    def switch_to_playlist_creator(self):
        self.playlist_creator_signal.emit()
    def switch_to_start_session(self):
        self.workout_player_signal.emit()

class WorkoutCreator(QWidget): 
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
            self.setGeometry(200,200,400,600)
            self.first_launch = False
            log('Set geometry of workout creator window...')

        self.layout = QGridLayout()
        self.starting_row = 2 # Starting row for the form
        self.width = 6 # Grid width used 
        self.height = 15

        # Set 'Home' button in top left corner
        self.button = QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)
        self.layout.addWidget(self.button,0,0)

        # Load plugins and display in combo box
        self.load_plugins()
        self.workout_type_selector = QComboBox()
        self.workout_type_selector.addItems(self.workout_types)
        self.layout.addWidget(self.workout_type_selector,1,0,1,self.width-1) 

        self.select_plugin_button = QPushButton('Select')
        self.select_plugin_button.clicked.connect(self.display_form)
        self.layout.addWidget(self.select_plugin_button,1,self.width)

        self.spacer = QLabel()
        self.layout.addWidget(self.spacer,self.starting_row,0,self.height,self.width)
        
        # Count the number of widgets added in the constructor. These cannot be deleted later on
        self.num_header_widgets = 3
        # Set layout of widget
        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()
    
    def load_plugins(self):
        # Get plugins from folder and load into combo box
        # Load JSON into a class attribute
        self.user_name = pwd.getpwuid( os.getuid() ).pw_name
        self.user_path = '/home/%s/PocketTrainer/'%self.user_name
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
        
        # Remove the spacer if it exists
        try:
            self.layout.removeWidget(self.spacer)
        except:
            log("Tried to hide the spacer, but it doesn't exist...")

        # Delete the existing Form Widget in order to display the new selected workout        
        try:
            self.layout.removeWidget(self.form_widget)
            self.form_widget.deleteLater()
            self.form_widget = None
        except:
            log("Tried to remove the form entry, but it doesn't exist...")

        # Load the selected workouts plugin json file
        workout_selected_json = '%s.json'%(workout_selected)
        try:
            fp = open('%s/Plugins/%s'%(self.user_path,workout_selected_json),'r')
            workout_plugin = json.load(fp)
            log("Loaded plugin {%s}..."%(workout_selected))
        except:
            log("Failed to load plugin {%s}..."%(workout_selected))
        
        for key in workout_plugin:
            workout_name = key
            workout_template = workout_plugin[key]
        
        # Populating form lines with strings from the plugin template
        form_lines = []
        for key in workout_template:
            val = key
            form_lines.append(FormEntry('%s:'%(val),'Type here...'))
        
        # Stack the form lines in a QVBoxLayout
        self.form_widget = QWidget()
        form = QVBoxLayout()
        # Add form widget to the parent widget
        for count, key in enumerate(form_lines):
            form.addLayout(key.form)
        self.form_widget.setLayout(form)
        self.layout.addWidget(self.form_widget,self.starting_row,0,self.height,self.width+2)

        self.previous_workout_selected = workout_selected

    def show_form(self):
        # Loop through plugin workout template and display a form entry for each
        pass

    def check_entries(self):
        # make sure all fields are valid based on expected type
        pass

    def add_workout(self):
        # Check if it exists
        pass

class PlaylistCreator(QWidget):
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
            log('Set geometry of playlist creator window...')

        self.layout = QGridLayout()

        self.button = QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)

        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()



class WorkoutPlayer(QWidget):
    '''
    This Widget is responsible for displaying the contents of a playlist
    A plugin must be loaded whenever the workout type switches
    '''
    go_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Workout Player')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,1920,1080)
            self.first_launch = False
            log('Set geometry of workout player window...')


        self.layout = QGridLayout()

        self.button = QPushButton('Close')
        self.button.clicked.connect(self.switch_to_main_window)

        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()

class Controller(object):

    def __init__(self):
        self.main_window = YogaMainWindow()
        self.main_window_past_geom = self.main_window.geometry()

        self.workout_creator = WorkoutCreator()
        self.workout_creator_past_geom = self.workout_creator.geometry()

        self.workout_player = WorkoutPlayer()
        self.workout_player_past_geom = self.workout_player.geometry()

        self.playlist_creator = PlaylistCreator()
        self.playlist_creator_past_geom = self.playlist_creator.geometry()

    def show_main_window(self):
        self.main_window.workout_creator_signal.connect(self.show_workout_creator)
        self.main_window.playlist_creator_signal.connect(self.show_playlist_creator)
        self.main_window.workout_player_signal.connect(self.show_workout_player)
        try:
            self.workout_creator_past_geom = self.workout_creator.geometry()
            self.workout_creator.hide()
        except:
            log("Tried to hide workout creator but failed...")

        try:
            self.playlist_creator_past_geom = self.playlist_creator.geometry()
            self.playlist_creator.hide()
        except:
            log("Tried to hide playlist creator but failed...")

        try:
            self.workout_player_past_geom = self.workout_player.geometry()
            self.workout_player.hide()
        except:
            log("Tried to hide workout_player but failed...")

        self.main_window.setGeometry(self.main_window_past_geom)
        self.main_window.show()

    def show_workout_creator(self):
        self.workout_creator.go_home.connect(self.show_main_window)
        try:
            self.main_window_past_geom = self.main_window.geometry()
            self.main_window.hide()
        except:
            log("Tried to hide main window but failed...")

        self.workout_creator.show()
    
    def show_playlist_creator(self):
        self.playlist_creator.go_home.connect(self.show_main_window)
        try:
            self.main_window_past_geom = self.main_window.geometry()
            self.main_window.hide()
        except:
            log("Tried to hide main window but failed...")

        self.playlist_creator.show()
    
    def show_workout_player(self):
        self.workout_player.go_home.connect(self.show_main_window)
        self.workout_player.show()

def main():
    log('Session started...')

    app = QApplication(sys.argv)

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    # Instantiate the controller to manage displaying windows and data management
    controller = Controller()
    controller.show_main_window()
    app.exec_()

if __name__ == '__main__':
    main()