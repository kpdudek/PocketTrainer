import os
import sys
import time
import datetime
import pwd

def log(text):
    '''
    Display the text passed and append to the logs.txt file
    parameters:
        text: str
    '''
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