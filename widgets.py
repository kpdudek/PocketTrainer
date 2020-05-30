#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FormEntry(QWidget): 

    def __init__(self,label_text,line_edit_text):
        super().__init__()
        self.form = QGridLayout()

        self.form_line_label = QLabel(label_text)
        self.form.addWidget(self.form_line_label,0,0)

        self.form_line_edit = QLineEdit()
        self.form_line_edit.setText(line_edit_text)
        self.form.addWidget(self.form_line_edit,0,1,0,6)
