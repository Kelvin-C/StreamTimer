import sys
import time
import msvcrt
import win32api
import os
import Tkinter as Tk
import tkFileDialog
import numpy as np

version = '0.2.0'

year = time.localtime().tm_year
month = time.localtime().tm_mon
day = time.localtime().tm_mday

char_list = ['1','2','3','4','5','6','7','8','9','0',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            
############################### FUNCTIONS #####################################

def record():
        """
        Returns the current time of your computer
        """
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min
        second = time.localtime().tm_sec
        
        clock = [hour, minute, second]
        return np.array(clock)
        
def timecorrection(time):
    hour, minute, second = time
    while second >= 60:
        minute += 1
        second -= 60
    while second < 0:
        minute -= 1
        second += 60
    
    while minute >= 60:
        hour += 1
        minute -= 60
    while minute < 0:
        hour -= 1
        minute += 60
        
    time = [hour, minute, second]
        
    return time
    
	
def timeinput():
        """
        The user inputs the current time of the video. There are protection from inputting the wrong values.
        """
        i=0
        while i==0:
		hour = ''
		minute = ''
		second = ''
		
		while type(hour) is not int:
		    hourint = 0
		    hour = raw_input("Hours = ")
		    try:
      		        hour = int(hour)
      		    except ValueError:
      		        hourint = 1
      		        print 'Please input a number.'
      		    if hourint == 0:
      		        hour = int(hour)
		
		while minute >= 60 or minute < 0 or type(minute) is not int:
		    minint = 0
		    minute = raw_input("Minutes = ")
		    try:
      		        minute = int(minute)
      		    except ValueError:
      		        minint = 1
      		        print "Please input a number."
      		    if minint == 0:
      		        minute = int(minute)
      		        if minute >= 60 or minute < 0:
      		            print 'Please input a number between 0 and 59 inclusively.'
		  
		while second >= 60 or second < 0 or type(second) is not int:
		    secint = 0
	            second = raw_input("Seconds = ")
		    try:
      		        second = int(second)
      		    except ValueError:
      		        secint = 1
      		        print "Please input a number."
      		    if secint == 0:
      		        second = int(second)
      		        if second >= 60 or second < 0:
      		            print 'Please input a number between 0 and 59 inclusively.'
	       
		print "time = %i:%i:%i" %(hour,minute,second)
		
		correctrepeat = 0
		while correctrepeat == 0:
                    correct = raw_input("Is this time correct? y/n\n")
                    if correct in yes_answers:
                        i=1
                        correctrepeat = 1
                    elif correct in no_answers:
                        correctrepeat = 1
                        
	return np.array([hour, minute, second], dtype = 'int')
	
def configcheck(configline, checklist, checkline):
        """
        This function checks whether the config is correctly done.
        """
        if configline[-2] == ' ' or configline[-2] == ':':
            return False
        else:
            return True    
            
################################# SCRIPT #######################################    
    
print "VideoTimer ver: " + version
        
with open('config.ini', 'r') as config:
        """
        This opens the config.ini file. All of the script regarding this file is in this part.
        """
        no_answers = ['n', 'N']
        yes_answers = ['y', 'Y']
        yesno_answers = no_answers + yes_answers
                
        lines = config.readlines()
        if len(lines) > 9:
            lines = lines[:9]            
        
        old_folder = lines[-1]
        
        first = lines[0][10:-1]
        if first[0] == ' ':
            first = first[1:]
	
        changenumber = 0 #This number is used to define whether the user wants to change properties. Check line 215.
        
       	#Check
       	if first not in yes_answers:
            for checkline in range(6):
                linelengths = [10,17,12,10,25,23]
                checklist = [yesno_answers, char_list, char_list, yesno_answers]
                answertype = ['a y or n', 'a letter or number (not from numpad)', 'a letter or number (not from numpad)', 'y or n', 'a positive integer', 'a positive integer']
                
                configline = lines[checkline][:linelengths[checkline]]
                configanswer = lines[checkline][linelengths[checkline]:-1]
                if configanswer == '':
                    configanswer = '  '
                if configanswer[0] == ' ':
                    configanswer = configanswer[1:]                   
                if checkline <= 3:
                    if configanswer not in checklist[checkline]:
                        if checkline != 0:
                            print "Problem in 'config.ini', '%s' line. It must have %s at the end." %(configline, answertype[checkline])
                            lines[0] = 'First run: Y\n'
                            change = 'y'
                if checkline in [4,5]:
                    no_to_intfail = 0
                    try:
                        configanswer = int(configanswer)
                    except ValueError:
                        no_to_intfail = 1
                        print "Problem in 'config.ini', '%s' line. It must have %s at the end.\nIt wil be changed to 3 as default." %(configline, answertype[checkline])
                        if checkline == 4:
                            lines[checkline] = 'No. of presses to record: 3\n'
                        elif checkline == 5:
                            lines[checkline] = 'No. of presses to quit: 3\n'
                    if no_to_intfail == 0:
                        configanswer = int(configanswer)
                        if configanswer <= 0:
                            print "Problem in 'config.ini', '%s' line. It must have %s at the end.\nIt wil be changed to 3 as default." %(configline, answertype[checkline])
                            if checkline == 4:
                                lines[checkline] = 'No. of presses to record: 3\n'
                            elif checkline == 5:
                                lines[checkline] = 'No. of presses to quit: 3\n'
        else:
            lines[4] = 'No. of presses to record: 3\n'
            lines[5] = 'No. of presses to quit: 3\n'      
                                           
        if old_folder == '\n':
            old_folder = 'Bad folder : '    
        if old_folder[-2] in [':', ' ', 'y'] or old_folder in ['', 'Output Directory:']:
            old_folder = ''
            lines += ['']
            if first not in yes_answers:
                print '\nThere is no text file directory detected.'
            lines[0] = 'First run: Y\n'    
            change = 'y'
        #end of check
            
        no_to_record = int(lines[4][25:-1])
        no_to_quit = int(lines[5][23:-1])
        
        while changenumber == 0:
            first = lines[0][-2]
            if first not in no_answers:      #Run this if first run or if user wants to change properties.   
                    lines = [0,0,0,0, 'No. of presses to record: %i' %int(no_to_record), 'No. of presses to quit: %i\n' %int(no_to_quit), 0]     #Used to rewrite te lines
                    
                    #Prevents the recording button and the quit button to be the same.
                    temp = 0
                    while temp == 0:
                        recordrepeat = 0
                        print "\nWhich button do you want to record with? Only LETTERS or NUMBERS (NOT FROM NUMPAD).\nYou will need to rapidly press this %i times (change this in 'config.ini')." %no_to_record
                        while recordrepeat == 0:
                            recordbutton = msvcrt.getch()
                            if recordbutton.upper() in char_list:
                                print 'Recording button: ' + recordbutton + '\n'
                                lines[1] = 'Recording Button: ' + recordbutton
                                recordrepeat = 1
                            else:
                                print 'Please input only LETTERS or NUMBERS (NOT FROM NUMPAD)'
                                    
                        quitrepeat = 0    
                        print "Which button do you want to exit the application with? Only LETTERS or NUMBERS (NOT FROM NUMPAD).\nYou will need to rapidly press this %i times (change this in 'config.ini'.)" %no_to_quit
                        while quitrepeat == 0:
                            quitbutton = msvcrt.getch()
                            if quitbutton.upper() in char_list:
                                lines[2] = 'Quit Button: ' + quitbutton
                                print 'Quit button: ' + quitbutton
                                if quitbutton == recordbutton:
                                    print "\nThe record button and the exit button are the same. Please change one of them."
                                    quitrepeat = 1
                                else:
                                    temp = 1
                                    quitrepeat = 1
                            else:
                                print 'Please input only LETTERS or NUMBERS (NOT FROM NUMPAD)'
                    
                    #Keeps asking for a y or n answer. Repeats itself until satisfied.
                    auto_open = 'a'
                    print "\nThis application will open a text file, which will show the times.\nDo you want it to automatically open after closing this application? y/n"
                    while auto_open not in yesno_answers:
                        auto_open = msvcrt.getch()
                        print " " + auto_open + "\n"
                        if auto_open not in yesno_answers:
                            print "Please answer y or n"
                    lines[3] = 'Auto Open: ' + auto_open
                    
                    #Asks for text file output directory. If not given a directory, it will use the old one unless there was no old one.
                    output_dir = ''
                    print 'Where to do you want to save the text file? Press a button to continue.'
                    while output_dir == '':
                        print 'Please select a folder.'
                        msvcrt.getch()
                        Tk.Tk().withdraw()
                        output_dir = tkFileDialog.askdirectory()
                        if output_dir == '':
                            output_dir = old_folder

                    lines[-1] = 'Output Directory:\n' + output_dir
                    
                    lines[0] = 'First run: N'
                    
                    lines = np.array(lines)
                    np.savetxt('config.ini', lines, fmt='%s')
                    
                    print 'The text file will be saved in ' + output_dir +"\n"
                    
                    #converts to hexadecimal for win32api.GetKeyState()
                    #The reminders are used to remember the button used.
                    record_reminder = recordbutton
                    quit_reminder = quitbutton
                    recordbutton = ord(recordbutton.upper())
                    quitbutton = ord(quitbutton.upper())
                    
                    changenumber = 1
   	        
   	    else:
   	        change = 'a' #This is used to ask whether the user wants to change some properties.
   	          
                recordbutton = lines[1][-2]
                print '\nRecording button: ' + recordbutton
                record_reminder = recordbutton
                recordbutton = ord(recordbutton.upper())
                
                quitbutton = lines[2][-2]
                if quitbutton == recordbutton:
                    sys.exit("The record button and the exit button are the same. Please change one of them")
                print 'Quit button:' + quitbutton
                quit_reminder = quitbutton
                quitbutton = ord(quitbutton.upper())
                
                auto_open = lines[3][10:]
                print "Auto open text file? " + auto_open
                
                output_dir = lines[-1]
                print "Text file directory: " + output_dir
                
                #Keeps asking for the answer to be y or n. Stops when satisfied.
                while change not in yesno_answers:
                    change = raw_input("Do you want to keep these properties? y/n\n")
                    if change in yes_answers:
                        changenumber = 1
                    elif change in no_answers:
                        lines[0] = 'First run: Y\n'
                    else:
                        print "Please answer y or n"

print "Input your current recording time"
rec_initial = timeinput()
initial = record()
initial = initial - rec_initial

quit_status = win32api.GetKeyState(quitbutton)
record_status = win32api.GetKeyState(recordbutton)

print '\nRecording button: ' + record_reminder
print 'Quit button: ' + quit_reminder
print 'Number of presses to record: %i' %no_to_record
print 'Number of presses to quit: %i' %no_to_quit
print "\nThe program is now recording"
i=0
times = np.array([0,0,0])
quitpresses = 0
recpresses = 0

#Detects the button press. If the button is pressed more than 3 times in a second, then it will record or exit the program.
while i == 0:
    	current_rec_state = win32api.GetKeyState(recordbutton)
    	current_quit_state = win32api.GetKeyState(quitbutton)
	quit_diff = abs(current_quit_state - quit_status)
	rec_diff = abs(current_rec_state - record_status)
	
	if quit_diff == 1:
	    quit_status = current_quit_state
	    if quitpresses == 0:
                quittime = record()
            newquittime = record()
            quittime_diff = newquittime - quittime
            quittime_diff = timecorrection(quittime_diff)
	    if quittime_diff[-1] <= 1:
	         quitpresses += 1
                 if quitpresses >= no_to_quit:
                     newquittime = record()
                     i = 1
            else:
                quitpresses = 0

	elif rec_diff == 1:
	    record_status = current_rec_state
	    if recpresses == 0:
        	rec = record()
            newrectime = record()
            rectime_diff = newrectime - rec
            rectime_diff = timecorrection(rectime_diff)
            if rectime_diff[-1] <= 1:
                recpresses += 1
                if recpresses >= no_to_record:
                    recordtime = rec - initial
                    recordtime = timecorrection(recordtime)
                    times = np.vstack((times, recordtime))
                    print recordtime
                    recpresses = 0
            else:
                recpresses = 0

os.chdir(output_dir.split()[0]) #The split ignores \n at the end of the string

#prevents overwriting
filenumber = 0
while os.path.exists('%s-%s-%s' %(year, month, day) +' video times('+ str(filenumber) +').txt') == True:
    filenumber += 1
    
np.savetxt('%s-%s-%s' %(year, month, day) +' video times('+ str(filenumber) +').txt', times, fmt = '%i', header="Hours : Minutes : Seconds", delimiter = ':', comments = "Date is %s/%s/%s\n\n" %(day, month,year))

#automatically open the text file after exit program.
if auto_open == 'Y' or auto_open == 'y':
    os.startfile('%s-%s-%s' %(year, month, day) +' video times('+ str(filenumber) +').txt')
	
#CREDITS
print "\nThank you for using VideoTimer. This application is made by Orgasha."
time.sleep(2)