#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import sys
import time
import os
import json
import pwd

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
            print('Set geometry of main window...')

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

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Workout Creator')

        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,400,600)
            self.first_launch = False
            print('Set geometry of workout creator window...')

        self.layout = QGridLayout()

        # Set 'Home' button in top left corner
        self.button = QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)
        self.layout.addWidget(self.button,0,0)

        # Load plugins and display in combo box
        self.load_plugins()
        self.workout_type_selector = QComboBox()
        self.workout_type_selector.addItems(self.workout_types)
        self.layout.addWidget(self.workout_type_selector,1,0,1,5)

        self.select_plugin_button = QPushButton('Select')
        self.select_plugin_button.clicked.connect(self.display_form)
        self.layout.addWidget(self.select_plugin_button,1,6)

        self.spacer = QLabel()
        self.layout.addWidget(self.spacer,2,0,15,6)
        
        # Set layout of widget
        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()
    
    def load_plugins(self):
        # Get plugins from folder and load into combo box
        # Load JSON into a class attribute

        name = pwd.getpwuid( os.getuid() ).pw_name
        user_path = '/home/%s/PocketTrainer/'%name
        plugins = os.listdir('%sPlugins/'%(user_path))
        print('{} plugins found...'.format(len(plugins)))

        workout_types = []
        for filename in plugins:
            workout_types.append(filename.split('.')[0])

        self.plugins = plugins
        self.workout_types = workout_types

    def display_form(self):
        # On 'select_plugin_button' press
        # Pull current selection from the plugin combo box and display the corresponding form
        try:
            self.layout.removeWidget(self.spacer)
        except:
            print("Tried to remove the spacer, but it doesn't exist")
        
        try:
            self.layout.removeWidget(self.form)
        except:
            print("Tried to remove the form entry, but it doesn't exist")
        
        self.form = QGridLayout()

        self.form_line_label = QLabel('Test Show')
        self.form.addWidget(self.form_line_label,0,0)

        self.form_line_edit = QLineEdit()
        self.form.addWidget(self.form_line_edit,0,1,0,6)
        
        # Add layout to the parent widget
        self.layout.addLayout(self.form,2,0,15,6)

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
    go_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Playlist Creator')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,400,600)
            self.first_launch = False
            print('Set geometry of playlist creator window...')

        self.layout = QGridLayout()

        self.button = QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)

        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def switch_to_main_window(self):
        self.go_home.emit()

class WorkoutPlayer(QWidget):
    go_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Workout Player')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,1920,1080)
            self.first_launch = False
            print('Set geometry of workout player window...')


        self.layout = QGridLayout()

        self.button = QPushButton('Home')
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
            print("Tried to hide workout creator but failed...")

        try:
            self.playlist_creator_past_geom = self.playlist_creator.geometry()
            self.playlist_creator.hide()
        except:
            print("Tried to hide playlist creator but failed...")

        try:
            self.workout_player_past_geom = self.workout_player.geometry()
            self.workout_player.hide()
        except:
            print("Tried to hide workout_player but failed...")

        self.main_window.setGeometry(self.main_window_past_geom)
        self.main_window.show()

    def show_workout_creator(self):
        self.workout_creator.go_home.connect(self.show_main_window)
        try:
            self.main_window_past_geom = self.main_window.geometry()
            self.main_window.hide()
        except:
            print("Tried to hide main window but failed...")

        self.workout_creator.show()
    
    def show_playlist_creator(self):
        self.playlist_creator.go_home.connect(self.show_main_window)
        try:
            self.main_window_past_geom = self.main_window.geometry()
            self.main_window.hide()
        except:
            print("Tried to hide main window but failed...")

        self.playlist_creator.show()
    
    def show_workout_player(self):
        self.workout_player.go_home.connect(self.show_main_window)
        self.workout_player.show()

def main():
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

    # Start 
    controller.show_main_window()
    app.exec_()

if __name__ == '__main__':
    main()