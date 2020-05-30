#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import sys
import time
import os

class YogaMainWindow(QtWidgets.QWidget):
    workout_creator_signal = pyqtSignal()
    playlist_creator_signal = pyqtSignal()
    workout_player_signal = pyqtSignal()

    def __init__(self):
        # QtWidgets.QWidget.__init__(self)
        super().__init__()
        self.setWindowTitle('Pocket Trainer')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,400,600)
            self.first_launch = False
            print('Set geometry of window...')

        layout = QVBoxLayout()

        # Workout Creator Button
        self.workout_creator_button = QtWidgets.QPushButton('Workout Creator')
        self.workout_creator_button.clicked.connect(self.switch_to_workout_creator)
        layout.addWidget(self.workout_creator_button)

        # Playlist Creator Button
        self.playlist_creator_button = QtWidgets.QPushButton('Playlist Creator')
        self.playlist_creator_button.clicked.connect(self.switch_to_playlist_creator)
        layout.addWidget(self.playlist_creator_button)

        # Workout Player Button
        self.workout_player_button = QtWidgets.QPushButton('Workout Player')
        self.workout_player_button.clicked.connect(self.switch_to_start_session)
        layout.addWidget(self.workout_player_button)

        self.setLayout(layout)

    def switch_to_workout_creator(self):
        self.workout_creator_signal.emit()
    def switch_to_playlist_creator(self):
        self.playlist_creator_signal.emit()
    def switch_to_start_session(self):
        self.workout_player_signal.emit()

class WorkoutCreator(QtWidgets.QWidget): 
    go_home = pyqtSignal()

    def __init__(self):
        # QtWidgets.QWidget.__init__(self)
        super().__init__()
        self.setWindowTitle('Workout Creator')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,400,600)
            self.first_launch = False
            print('Set geometry of window...')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)
        
        layout.addWidget(self.button)
        self.setLayout(layout)

    def switch_to_main_window(self):
        self.go_home.emit()

class PlaylistCreator(QtWidgets.QWidget):
    go_home = pyqtSignal()

    def __init__(self):
        # QtWidgets.QWidget.__init__(self)
        super().__init__()
        self.setWindowTitle('Playlist Creator')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,400,600)
            self.first_launch = False
            print('Set geometry of window...')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)

        layout.addWidget(self.button)

        self.setLayout(layout)

    def switch_to_main_window(self):
        self.go_home.emit()

class WorkoutPlayer(QtWidgets.QWidget):
    go_home = pyqtSignal()

    def __init__(self):
        # QtWidgets.QWidget.__init__(self)
        super().__init__()
        self.setWindowTitle('Workout Player')
        self.first_launch = True
        if self.first_launch:
            self.setGeometry(200,200,1920,1080)
            self.first_launch = False
            print('Set geometry of window...')


        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Home')
        self.button.clicked.connect(self.switch_to_main_window)

        layout.addWidget(self.button)

        self.setLayout(layout)

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