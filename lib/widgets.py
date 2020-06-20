#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FormEntry(QWidget): 

    def __init__(self,label_text,line_edit_text):
        super().__init__()
        self.form = QHBoxLayout()

        label_text = label_text + ':'
        self.form_line_label = QLabel(label_text)
        # self.form_line_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.form_line_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.form_line_label.setFixedSize(120, 40)
        self.form.addWidget(self.form_line_label)

        self.form_line_edit = QLineEdit()
        self.form_line_edit.setText(line_edit_text)
        self.form.addWidget(self.form_line_edit)
        
        self.setLayout(self.form)
    
class WorkoutField(QWidget):

    def __init__(self,text):
        super().__init__()
        self.form = QHBoxLayout()

        self.form_line_label = QLabel(text)
        self.form_line_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        # self.form_line_label.setFixedSize(120, 40)
        self.form.addWidget(self.form_line_label)

class RadioStack(QWidget):
    def __init__(self,radio_list):
        super().__init__()

        self.radio_layout = QHBoxLayout()

        self.radio_buttons = []
        for text in radio_list:
            radio_button = QRadioButton()
            radio_button.setText(text)

            self.radio_layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        self.radio_buttons[0].setChecked(True)
        
        self.setLayout(self.radio_layout)

    def get_checked_text(self):
        for button in self.radio_buttons:
            if button.isChecked():
                return button.text() 
    
    def connect_toggle(self,fn):
        for button in self.radio_buttons:
            button.toggled.connect(fn)
