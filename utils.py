import os
import sys
import time
import datetime as dt
import pwd

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

class StopWatch(object):
    # Time parameters
    start_time = None
    end_time = None
    lap_times = []
    paused_time = None
    paused_split = None

    # Flags
    ended = False
    paused = False

    def __init__(self):
        pass

    def start(self):
        self.start_time = dt.datetime.now()
        pass
    
    def pause(self):
        if not self.paused:
            self.paused = True
            self.paused_split = dt.datetime.now()
        else:
            log('Tried to pause timer, but it already is...')
        pass

    def play(self):
        if self.paused:
            self.paused = False
            self.paused_time += dt.datetime.now()-self.paused_split
            self.paused_split = None
        else:
            log('Tried to play timer, but it already is...')
        pass

    def lap(self):
        self.lap_times.append(dt.datetime.now()-self.start_time)
        pass
    
    def stop(self):
        self.end_time = dt.datetime.now()
        self.ended = True
        pass

    def get_time(self):
        '''
        Returns the time since the timer began
        Parameters:
            None
        Returns:
            hours (int)
            minutes (int)
            seconds (float)
        '''
        delt = dt.datetime.now()-self.start_time
        hours,minutes,seconds = str(delt).split(':')
        return int(hours),int(minutes),seconds
    