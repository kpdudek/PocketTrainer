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
    
class WorkoutField(QWidget):

    def __init__(self,text):
        super().__init__()
        self.form = QHBoxLayout()

        self.form_line_label = QLabel(text)
        self.form_line_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        # self.form_line_label.setFixedSize(120, 40)
        self.form.addWidget(self.form_line_label)
