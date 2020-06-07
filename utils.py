import os
import sys
import time
import datetime as dt
import pwd
from threading import Thread

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FilePaths(object):
    user_name = pwd.getpwuid( os.getuid() ).pw_name
    user_path = '/home/%s/PocketTrainer/'%user_name

def log(text):
    '''
    Display the text passed and append to the logs.txt file
    parameters:
        text: str
    '''
    curr_time = str(dt.datetime.now())
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

    