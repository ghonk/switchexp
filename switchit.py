from psychopy import visual, event, core, gui
import os, random as rnd, sys
from misc import *
from numpy import *
from socket import gethostname
from time import strftime

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#EXPERIMENT INFO
experimentname='switchit'
conditions=range(1,7)

##__________________________________|
##              SHJ2    SHJ3    SHJ4|
## classify     1       2       3   |
## switchit     4       5       6   |
##__________________________________|


## COSMETICS
fcolor=[-1,-1,-1]
ffont='Consolas'
fsize=22

imagestart=[0,150]
imagesizes=[[195, 231],[130,154]] # size of build image and option images, in pix
categorynames=['Lape','Tannet']
featurenamesorig = ['Color','Veining','Shape']

## STORE FILE LOCATIONS
if sys.platform=='darwin' or 'linux2':
    imagedirectories=[os.getcwd() + '/img/one/', 
        os.getcwd() + '/img/two/',
        os.getcwd() + '/img/three/']
    subjectfiles=os.getcwd() + '/subjects/'
    featurebalancelist= genfromtxt(
        os.getcwd() + '/img/balancefeatures.csv',delimiter=',',dtype='int').astype(int)
    dimensionbalancelist= genfromtxt(
        os.getcwd() + '/img/balancedimensions.csv',delimiter=',',dtype='int').astype(int)
else:
    imagedirectories=[os.getcwd() + '\\img\\one\\', 
        os.getcwd() + '\\img\\two\\',
        os.getcwd() + '\\img\\three\\']
    subjectfiles=os.getcwd() + '\\subjects\\'
    featurebalancelist= genfromtxt(
        os.getcwd() + '\\img\\balancefeatures.csv',delimiter=',',dtype='int').astype(int)
    dimensionbalancelist= genfromtxt(
        os.getcwd() +'\\img\\balancedimensions.csv',delimiter=',',dtype='int').astype(int)

#------------------------------------------------------------------------------------
##    GET SUBJECT INFORMATION & START WINDOW
[subjectnumber,condition,subjectfile]=  getsubjectinfo(
    experimentname,conditions,subjectfiles)

#create window and set logging option
if gethostname() not in ['klab1','klab2','klab3']:
    win=visual.Window(fullscr=True,units='pix',color=[1,1,1])
else:
    win=visual.Window(fullscr=True,units='pix',color=[1,1,1])
    checkdirectory(os.getcwd() + '\\logfiles\\')
    logfile=os.getcwd()+ '\\logfiles\\' + str(subjectnumber)+ '-logfile.txt'
    while os.path.exists(logfile):
       logfile=logfile+'_dupe.txt'
    logfile=open(logfile,'w')
    sys.stdout=logfile
    sys.stderr=logfile

##get current date and time
currenttime=strftime("%a, %d %b %Y %X")

##start mouse and timer
cursor = event.Mouse(visible=True, newPos=None, win=win)
timer=core.Clock() #clock

#------------------------------------------------------------------------------------
##    LOAD STIMULI AND ASSIGN FEATURES
stimuli=[]
for i in imagedirectories:
    temp=[]
    for j in os.listdir(i):
        if j[j.find('.'):] in ['.jpg','.png','.jpeg']:
            prop=str2prop(j[0:j.find('.')])
            stimuli.append ([
                visual.ImageStim(win,image=i+j,name=j,pos=imagestart),
                j, prop])

## counterbalance dimensions
[stimuli,balancecondition,featurenames,dimensionassignment] = counterbalance(subjectnumber,
    stimuli,featurebalancelist,dimensionbalancelist,featurenamesorig)

print '--------STIMULUS INFO--------'
for i in stimuli:
    print i

shjtypes=[
##  TYPE 2
    [[[0,0,0],[0,0,1],[1,1,1],[1,1,0]],
     [[0,1,0],[0,1,1],[1,0,0],[1,0,1]]],
##  TYPE 3    
    [[[0,0,0],[0,0,1],[0,1,0],[1,0,1]],
     [[1,1,1],[1,1,0],[0,1,1],[1,0,0]]],
##  TYPE 4
    [[[0,0,0],[0,0,1],[0,1,0],[1,0,0]],
     [[1,1,1],[1,1,0],[1,0,1],[0,1,1]]]]

#------------------------------------------------------------------------------------
##    RUN EXPERIMENT CONDITIONALS

## convert condition to specific variables
if condition in [1,4,7]:
    shjcondition=2
elif condition in [2,5,8]:
    shjcondition=3
elif condition in [3,6,9]:
    shjcondition=4
    
if condition <= 3:
    traincondition='classify'
else:
    traincondition='switchit'


validegs=shjtypes[shjcondition-2]

print '\n------------CONDITION INFO:------------'
print 'subjectnumber: ' + str(subjectnumber)
print 'exp condition: ' + str(condition)
print 'training condition: ' + traincondition
print 'shj condition: ' + str(shjcondition)
print 'stim condition: ' + str(balancecondition)

subjectdata=[[currenttime],[condition,subjectnumber,balancecondition]]

#------------------------------------------------------------------------------------
## LOAD INSTRUCTIONS
from instructs import *
instructions=visual.TextStim(win,text='',wrapWidth=2000,
         color=fcolor,font=ffont,height=fsize)
fixcross=visual.TextStim(win,text='+',pos=imagestart,
        wrapWidth=1000,color=fcolor,font=ffont,height=fsize)

continuestring='\n\
\n\
Click anywhere to continue.'


#------------------------------------------------------------------------------------
####  PASS TO TRAINING SCRIPTS
if traincondition=='classify':
    numtrainingblocks=15
    execfile('train_classify.py')
if traincondition=='switchit':
    numtrainingblocks=15
    execfile('train_switchit.py')
    
#------------------------------------------------------------------------------------
####  PASS TO TESTING SCRIPTS

execfile('test_classify.py')
execfile('test_inference.py')
execfile('test_switch.py')

# ---------------------------------------
# exit screen
instructions.setText(instructiontext[-1])
instructions.draw()
win.flip()
event.waitKeys()

print '\nExperiment completed'
if gethostname() in ['klab1','klab2','klab3']:
    copy2db(subjectfile,experimentname)
    logfile.close()
    os.system("TASKKILL /F /IM pythonw.exe")
