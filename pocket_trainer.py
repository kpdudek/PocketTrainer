#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import sys, os, pwd
import time, datetime
import json, math, threading
import importlib

user_name = pwd.getpwuid( os.getuid() ).pw_name
user_path = '/home/%s/PocketTrainer/lib'%(user_name)
sys.path.insert(1,user_path)
from utils import *
from widgets import *
from YogaMainWindow import *
from WorkoutCreator import *
from WorkoutPlayer import *
from PlaylistCreator import *

class Controller(object):
    '''
    This class instantiates all widgets in the app and listens to the 
    window switching signals from each.
    '''
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
        try:
            self.main_window_past_geom = self.main_window.geometry()
            self.main_window.hide()
        except:
            log("Tried to hide main window but failed...")

        self.workout_player.show()

def main():
    log('Session started...')

    app = QApplication(sys.argv)

    # Now use a palette to switch to dark colors:
    dark_mode = True
    if dark_mode:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 153, 85)) #Qt.white
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(255, 153, 85))
        palette.setColor(QPalette.Highlight, QColor(255, 153, 85))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)

    # Instantiate the controller to manage displaying windows and data management
    controller = Controller()
    controller.show_main_window()
    app.exec_()

if __name__ == '__main__':
    main()