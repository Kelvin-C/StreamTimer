import win32api
import numpy as np

def process(button, stop, char_list):
    asciibutton = ord(button)
    print chr(asciibutton)
    stopstate = win32api.GetKeyState(stop)
    currentstate = win32api.GetKeyState(asciibutton)
    i = 0
    while i == 0:
        butstate = win32api.GetKeyState(asciibutton)
        ststate = win32api.GetKeyState(stop)
        if abs(ststate - stopstate) == 1:
            print '\nDid not work'
            return char_list
        elif abs(butstate - currentstate) == 1:
            print '\nWORKED!'
            char_list += [button]
            return char_list
            
n = 0
stopbutton = raw_input('\nSTOP = ')  
char_list = [stopbutton]
stop = ord(stopbutton.upper())

while n == 0:
    button = raw_input('INPUT = ')
    button = button.upper()
    char_list = process(button, stop, char_list)
    
    stopstate = win32api.GetKeyState(stop)
    
    question = raw_input('STOP?? y/n\n')
    if question == 'y':
        n = 1
        
char_list = np.array([char_list])
np.savetxt('char_list.txt', char_list, fmt = '%s', delimiter = ',')