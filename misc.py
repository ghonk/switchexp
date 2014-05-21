from psychopy import visual, event, core, gui
import os, random as rnd, socket, sys, shutil, datetime
from numpy import *


#------------------------------------------------------------------------------------
# creates folder if it doesnt exist
def checkdirectory(dir): 
    if not os.path.exists(dir):
        os.makedirs(dir)

#------------------------------------------------------------------------------------    
# copies the data file to a series of dropbox folders
def copy2db(filename,experimentname):
    copyfolders=[ #add your own!
        'C:\\Users\\klab\\Dropbox\\PSYCHOPY DATA\\'+experimentname+'\\',
        'C:\\Users\\klab\\Dropbox\\garrett\\PSYCHOPY DATA\\'+experimentname+'\\']

    for i in copyfolders:
        checkdirectory(i)
        shutil.copy(filename,i)
        
#------------------------------------------------------------------------------------    
# writes list to file
def writefile(filename,data,delim):
    datafile=open(filename,'w')
    for line in data: #iterate over items in data list
        currentline='\n' #start each line with a newline
        for j in line: #add each item onto the current line

            if isinstance(j, (list, tuple)): #check if item is a list
                for k in j:
                    currentline=currentline+str(k)+delim
            else:
                currentline=currentline+str(j)+delim
                
##        write current line
        datafile.write(currentline)
    datafile.close()  


#------------------------------------------------------------------------------------        
# do a dialouge and return subject info 
def getsubjectinfo(experimentname,conditions,datalocation):
    ss_info=[]
    pc=socket.gethostname()
    myDlg = gui.Dlg(title=experimentname)
    myDlg.addText('Subject Info')
    myDlg.addField('ID:', tip='or subject code')
    myDlg.addField('Condition:', rnd.choice(conditions),choices=conditions)
    myDlg.show()
    if not myDlg.OK:
        print 'User Terminated'
        core.quit()
        
    subjectinfo = [str(i) for i in myDlg.data]
    
    if subjectinfo[0]=='':
        core.quit()
    else: 
        id=subjectinfo[0]
        condition=subjectinfo[1]
        subjectfile=datalocation+pc+'-'+experimentname+'-'+condition+'-'+id+'.csv'
        while os.path.exists(subjectfile) == True:
            subject_file=datalocation+pc+'-'+experimentname+'-'+condition+'-'+id+'.csv' + '_dupe'
        return [int(id),int(condition),subjectfile]
        
#------------------------------------------------------------------------------------    
#takes in 1 or 2-d lists of objects and draws them in the window
def drawall(win,objects):
    for i in objects:
        if isinstance(i, (list, tuple)):
            for j in i:
                j.draw()
        else:
            i.draw()
    win.flip()

#------------------------------------------------------------------------------------   
def presentinstructions(win,stim,text,phase):
    event.clearEvents()
    originalposition=stim.pos
    stim.setPos=[0.0,0.0]
    stim.alignVert='center'
    
    #search text for instructions matching phase
    for i in text:
        if i[0]==phase:
            instructs=i[1]
            break
            
    #draw text and wait for key press
    stim.setText(instructs)
    stim.draw()
    win.flip()
    core.wait(2)
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()
    
    stim.alignVert='top'
    stim.setPos=originalposition
    event.clearEvents() 

#-----------------------------------------------------------------------------------
## program waits for a mouse click to continue
def clicktocontinue(cursor):
    event.clearEvents()
    cursor.clickReset() 
    while cursor.getPressed()==[False,False,False]:
        cursor.getPressed()
        if event.getKeys(keyList='q'):
            print 'User Terminated'
            core.quit()

#------------------------------------------------------------------------------------    
# does the initial blankcreen-fixcross start to a trial
def starttrial(win,isi,fixcross):
    fixcross.draw()
    win.flip()
    core.wait(isi)                

#------------------------------------------------------------------------------------                
# return a randomized list of all possible pairs of items in a list
def list2pairs(mylist):    
    pairs=[]
    for i in mylist:
        for j in mylist[mylist.index(i)+1:]:
            p=[i,j]
            rnd.shuffle(p)
            pairs.append(p)
    rnd.shuffle(pairs)
    return pairs

#------------------------------------------------------------------------------------
# takes in a string and return a list of integers
#   a=0, b=1,....  #_=nan
def str2prop(string):
    features=tile(nan,[1,len(string)])[0]
    for dimension in range(0,len(string)):
        character=string[dimension]
        if character != '_':
             features[dimension]=(ord(character)-ord('a'))
    return features

#------------------------------------------------------------------------------------
#re-assigns dimension and feature values based on counterbalance lists
def counterbalance(subjectnumber,stimuli,featurebalancelist,
                    dimensionbalancelist,featurenames):

    # select a counterbalance condition based on subject
    nconditions=len(featurebalancelist)
    condition=subjectnumber%nconditions
    
    ## balance features
    featureassignment=featurebalancelist[condition]==1
    print ['FLIPPED FEATURES:',featureassignment]
    for i in stimuli:
        features=i[2]
        features[featureassignment] = 1-features[featureassignment]
        stimuli[stimuli.index(i)][2]=features
    ## balance dimensions and create labels    
    dimensionassignment=dimensionbalancelist[condition]-1
    origfeaturenames = list(featurenames)
    count = 0
    for i in dimensionassignment:
        featurenames[count] = origfeaturenames[i]
        count = count + 1
    print ['DIMENSION SHUFFLE:', dimensionassignment,featurenames]
    for i in stimuli:
        features=i[2]
        stimuli[stimuli.index(i)][2]=features[dimensionassignment]
       
    print ''
    return [stimuli,condition,featurenames,dimensionassignment]
        
#------------------------------------------------------------------------------------
# takes in stim and labels and returns a list of all possible combinations
def makecombos(stims,labels):
    combo=[]
    for s in stims:
        for l in labels:
            combo.append([s,l])
    return combo

#------------------------------------------------------------------------------------
# converts an array into a list
def array2list(data,intconvert):
    result=array(data)
    result[isnan(result)]=-1 #convert nan to -1

    if intconvert: #convert to integer if desired
        result=result.astype(int)
        
    result=result.tolist()
    return result   

#------------------------------------------------------------------------------------
# determines which category a stimulus is in 
def whichcategory(features,validegs):

    # convert to list if necessary
    if 'list' not in str(type(features)):
        features=array2list(features,True)
    
    category=-1
    for i in validegs:
        catnum=validegs.index(i)
        if features in i:
            category=catnum
            
    return category
    
#------------------------------------------------------------------------------------
# find images with a provided set of properties
def findstimulus(stims,comparison):
    comparison=array(comparison)
    comparison[isnan(comparison)]=-1
    for i in stims:
        features=array(i[2])
        features[isnan(features)]=-1
        if array_equal(features,comparison):
            return i

#------------------------------------------------------------------------------------     
# determines which of a set of bins, each of a set of objects is in
def findobjects(objects,bins): 
    result=[]
    for i in objects:
        result.append(-1) #default
        for j in bins:
            if i[0].overlaps(j):
                result[objects.index(i)]=bins.index(j)
    return result
   
#------------------------------------------------------------------------------------
# finds approprtiate inference images
def combinefeatures(original,addition):
    newproperties=array(original)
    currentfeature=0
    for i in newproperties:
        if isnan(i):
            newproperties[currentfeature]=addition[currentfeature]
        currentfeature=currentfeature+1
    return newproperties


#------------------------------------------------------------------------------------   
def buttongui(cursor,timer,buttons,labels):
    #clear events
    timer.reset()
    cursor.clickReset()
    event.clearEvents() 
    
    #iterate until response
    while True:
        
        #quit if desired
        if 'q' in event.getKeys():
            print 'User Terminated'
            core.quit()
            
        #check to see if  any stimulus has been clicked inside of
        for i in buttons:
            if cursor.isPressedIn(i):
                return [labels[buttons.index(i)],timer.getTime()]

#------------------------------------------------------------------------------------
# finds and formats inference images for use as buttons
def getinferencebuttons(stims,missingfeature,buttonsize,win):

##  find the appropriate stimuli
    images=[]
    for i in stims:
        features=i[2]
        nummissingfeatures=sum(isnan(features))
        if (nummissingfeatures==2) and (not isnan(features[missingfeature])):
            images.append(i)
    rnd.shuffle(images) # do a quick shuffle

##  set image position and size
    images[0][0].setPos([-100,-125])
    images[0][0].setSize(buttonsize)
    images[1][0].setPos([ 100,-125])
    images[1][0].setSize(buttonsize)

    buttonimages=[]
    buttonlabels=[]
    buttonborders = []
    
    for i in images:  
    ##  store image stimulus
        buttonimages.append(i[0])
    ##  store value for the provided feature
        features=i[2]
        featurevalue=features[isnan(features) == False].astype(int)
        buttonlabels.append([featurevalue[0],missingfeature])
    
    ##  make border    
    border = visual.Rect(win,width=buttonsize[0]+2,height=buttonsize[1]+2)
    border.setFillColor([1,1,1])
    border.setLineColor([-1,-1,-1])
    border.setPos([-100,-125])
    buttonborders.append(border)  
    border = visual.Rect(win,width=buttonsize[0]+2,height=buttonsize[1]+2)
    border.setFillColor([1,1,1])
    border.setLineColor([-1,-1,-1])
    border.setPos([100,-125])
    buttonborders.append(border)
    
    
    return [buttonimages,buttonlabels,buttonborders]

#------------------------------------------------------------------------------------
# runs switchit tutorial
def classifytutorial(win,instructions,imagestart,buttons,
    buttontext,ffont,fcolor,fsize,cursor,timer,imagesizes):
    
##  init tutorial vars    
    imagedirectories=[os.getcwd() + '\\tutorial\\']
    entertocont = visual.TextStim(win,text='Press the spacebar to continue',
        wrapWidth=1000,color=fcolor,font=ffont,height=fsize,pos=[0,-330])
    x = visual.TextStim(win,text='X',wrapWidth=1000,color=fcolor,
        font=ffont,height=100,pos=imagestart)
    finalinstructs = visual.TextStim(win,text='',wrapWidth=1000,color=fcolor,
        font=ffont,height=fsize,pos=([0,50]))
    
    labellist = ['Unhappy','Happy']
    buttontext[0].setText('Unhappy')
    buttontext[1].setText('Happy')
    
##  grab tutorial stimuli    
    tutstimuli=[]
    tutresponse=[]
    tutrt=[]
    
    for i in imagedirectories:
        temp=[]
        for j in os.listdir(i):
            if j[j.find('.'):] in ['.jpg','.png','.jpeg']:
                tutstimuli.append ([
                    visual.ImageStim(win,image=i+j,name=j,pos=imagestart),j])

##  tutorial screen 1    
    instructions.setText("    At the start of each trial you will see an image in the location above.\n\
    The image will be a member of one of the categories you are learning about.")
    drawall(win,[instructions,x,entertocont])
    core.wait(1)
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()
    
##  tutorial screen 2    
    instructions.setText("    For practice, let's imagine that you are learning to categorize\n\
    examples of unhappy faces and happy faces.")
    tutstimuli[0][0].setPos(array(imagestart) - array([120,0]))
    tutstimuli[2][0].setPos(array(imagestart) + array([120,0]))
    drawall(win,[instructions,tutstimuli[0][0],tutstimuli[2][0],entertocont])
    core.wait(1)
    
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()
    
    tutstimuli[0][0].setPos(imagestart)
    tutstimuli[2][0].setPos(imagestart)

##  tutorial screen 3    
    instructions.setText("    On each trial you will use the mouse to click on the\n\
    category name of the provided example.")
    drawall(win,[instructions,tutstimuli[0][0],buttons,buttontext,entertocont])
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()

##  tutorial screen 4    
    instructions.setText("    You will be provided feedback about your answer.\n\
    Go ahead and click the correct category name.")
    drawall(win,[instructions,tutstimuli[0][0],buttons,buttontext])
    
    while not 'Unhappy' in tutresponse:
        [tutresponse, tutrt] = buttongui(cursor,timer,buttons,labellist)
        
        if 'Unhappy' in tutresponse:
            instructions.setText("Correct! This is a member of the Unhappy category")
        if 'Happy' in tutresponse:
            instructions.setText("Incorrect... This is a member of the Unhappy category")
            break
        
##  tutorial screen 5    
    drawall(win,[instructions,tutstimuli[0][0],entertocont])
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()        

##  tutorial screen 6    
    finalinstructs.setText("Alright! It looks like you've got the hang of it.\n\
\n\
Remember: your goal in the following task is to learn about two new categories by choosing the category name just like you practiced. \n\
\n\
At first you will have to guess the category.  You will receive feedback that will help guide your learning.\n\
\n\
Importantly, you will be tested several times to see how well you are learning the categories.  If you perform well, you will be able to finish the experiment faster.\n\
\n\
Please ask the experimenter if you have any further questions.")
    drawall(win,[finalinstructs,entertocont])
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()     


    buttontext[0].setText('Lape')
    buttontext[1].setText('Tannet')
    
#------------------------------------------------------------------------------------
# finds and formats generate images for use as buttons
def getgeneratebuttons(stimuluslist,missingfeatures,buttonlocations,buttonsize):
    #missingfeatures=array isting the features that are needed for buttons
    #stimuluslist=list of all stimuli
    
##      find the appropriate stimuli
    images=[[],[]]
    for i in list(missingfeatures):
        for j in stimuluslist:
            stim=list(j)
            features=stim[2]
            featurenum=list(missingfeatures).index(i)
            nummissingfeatures=sum(isnan(features))
            if (nummissingfeatures==2) and (not isnan(features[i])):
                stim.append(i)
                images[featurenum].append(stim)

##    do a quick shuffle, then convert button matrix to a vector  
    for i in images:
        rnd.shuffle(i)
    rnd.shuffle(images)
    images[0].extend(images[1])
    images=images[0]

##    set position and size for all images,
##      place images and labels into dedicated lists
    buttonimages=[]
    buttonlabels=[]
    for i in images:
        imagenum=images.index(i)

##        edit image and store it as a button
        i[0].setPos(buttonlocations[imagenum])
        i[0].setSize(buttonsize)
        buttonimages.append(i[0])

##          store value for the provided feature
        features=i[2]
        providedfeature=i[3]
        featurevalue=features[isnan(features) == False].astype(int)
        buttonlabels.append([featurevalue[0],providedfeature])

    return [buttonimages,buttonlabels]

#------------------------------------------------------------------------------------
# waits for responses and completes examples corresponding to user input
def generategui(win,cursor,timer,stimuluslist,trialinfo,
    buttonimages,buttonlabels,clickrectangles,instructions):
    
##        define trial properites
    currentimage=trialinfo[0][0]
    currentproperties=trialinfo[0][2]

##    initalize data to be updated within the loop
    featureorder=[0,0,0]
    nummissingfeatures=sum(isnan(currentproperties))
    numresponses=0

##      draw current stimuli
    drawall(win,[currentimage])
    core.wait(.5)

##    ------ITERATE UNTIL EXAMPLE HAS NO NANs --------------------
    while nummissingfeatures > 0: 

##            draw current image
        drawall(win,[currentimage,instructions,buttonimages])
        core.wait(.5)
        
##            wait for response
        [response,rt]=buttongui(cursor,timer,clickrectangles,buttonlabels)
        responsevalue=response[0]
        responsefeature=response[1]        

##            combine original with response image and find the result stim
        addition=tile(nan,(1,3))[0]
        addition[responsefeature]=responsevalue
        newproperties = combinefeatures(currentproperties,addition)
        newexampleinfo=findstimulus(stimuluslist,newproperties)

##         make sure the subject did not try to generate a provided feature
        if currentimage != newexampleinfo[0]:
            numresponses=numresponses+1
            featureorder[responsefeature]=numresponses

##              update info for the generated image
            currentimage=newexampleinfo[0]
            currentproperties=newexampleinfo[2]
        
##        draw result and determine whether loop should end
        drawall(win,[currentimage])
        core.wait(.5)
        nummissingfeatures=sum(isnan(currentproperties))

    return [newexampleinfo,responsevalue,rt,featureorder]
    
#------------------------------------------------------------------------------------
# takes training stims and feature list and outputs switch matrix
def makeswitchmatrix(trainingblock,stimfeaturelist):
    
##  set up matrix ingredients 
    featindex = stimfeaturelist[1]
    tempfeaturelist = array2list(stimfeaturelist[0][0],True)
    sflist = array2list(stimfeaturelist[0][0],True)

##  zeroed switch matrix    
    switchmatrix=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],
                 [0,0,0],[0,0,0],[0,0,0],[0,0,0]]
                
##  go through each item               
    for item in [0,1,2,3,4,5,6,7]:
    ##  and each feature for that item        
        for j in [0,1,2]:
        ##  check value of feature and switch it
            if sflist[item][j] == 0:
                tempfeaturelist[item][j] = 1
            else:
                tempfeaturelist[item][j] = 0
        ##  find stimulus with features that match the switch       
            for i in sflist:
                if i == tempfeaturelist[item]:
                    switchmatrix[item][j] = featindex[0][sflist.index(i)]
                ##  clear out temp list and end search  
                    tempfeaturelist = array2list(stimfeaturelist[0][0],True)
                    break
    return switchmatrix

#------------------------------------------------------------------------------------
# formats switchit buttons
def getswitchitbuttons(stimuluslist,featurenames,buttonlocations,
            buttonsize,trialproperties,switchbuttonimages,win,
            tutorial,ffont,fcolor,fsize):

##  get correct feature buttons
    if tutorial != True:    
        images = []
        for i in featurenames[0:]:
            for j in switchbuttonimages:
                if i == j[3] and trialproperties[featurenames.index(i)] != j[4]:
                    images.append(j)
                    break
    else:
        images = list(switchbuttonimages)

##  shuffle images
    if tutorial != True:
        rnd.shuffle(images)
    
##  set position and size for all images,
##  place images and labels into dedicated lists
    buttonimages=[]
    buttonlabels=[]
    buttoncovers=[]
    switchlabels = list(featurenames)
    switchlabels.append('Done')
    
    for i in images:
        imagenum=images.index(i)
    ##  make button border    
        border = visual.Rect(win,width=buttonsize[0]+2,height=buttonsize[1]+2)
        border.setFillColor([1,1,1])
        border.setLineColor([-1,-1,-1])
        border.setPos(buttonlocations[imagenum])
        buttonimages.append(border)
    ##  edit image and store it as a button
        i[0].setPos(buttonlocations[imagenum])
        i[0].setSize(buttonsize)
        buttonimages.append(i[0])
    ##  store value for the provided feature
        if tutorial != True:
            features=i[2]
            providedfeature=i[3]
            featurevalue=features[isnan(features) == False].astype(int)
            buttonlabels.append([featurevalue[0],providedfeature])
            switchlabels[images.index(i)] = providedfeature
    ##  init covers
        j = visual.Rect(win,width=buttonsize[0]+10,height=buttonsize[1]+10)
        j.setFillColor([1,1,1])
        j.setLineColor([1,1,1])
        j.setPos(buttonlocations[imagenum])
        buttoncovers.append(j)
##  make done button    
    p = visual.Rect(win,width=150,height=75)
    p.setFillColor([.9,.9,.9])
    p.setLineColor([-1,-1,-1])
    p.setPos(buttonlocations[-1])
    buttonimages.append(p)    
    a = visual.TextStim(win,'Done',font=ffont,color=fcolor,height=fsize,pos=buttonlocations[-1])
    buttonimages.append(a)
## make done cover    
    j = visual.Rect(win,width=155,height=80)
    j.setFillColor([1,1,1])
    j.setLineColor([1,1,1])
    j.setPos(buttonlocations[-1])
    buttoncovers.append(j)    

    return [buttonimages,buttonlabels,buttoncovers,switchlabels]

#------------------------------------------------------------------------------------
# runs switchit tutorial
def switchtutorial(win,instructions,imagestart,buttonlocations,
                ffont,fcolor,fsize,cursor,timer,imagesizes):

##  init tutorial/temp vars    
    imagedirectories=[os.getcwd() + '\\tutorial\\']
    labellist = ['Eyes','Mouth','Done']
    entertocont = visual.TextStim(win,text='Press the spacebar to continue',
        wrapWidth=1000,color=fcolor,font=ffont,height=fsize,pos=[0,-330])
    tutstimlab = visual.TextStim(win,text='Target: Happy Face',wrapWidth=1000,
        color=fcolor,font=ffont,height=fsize,pos=[150,335])
    x = visual.TextStim(win,text='X',wrapWidth=1000,color=fcolor,
        font=ffont,height=100,pos=imagestart)
    tutstimuli=[]
    tutimages = []
    tutlabels = []
    tutcovers = []
    tutresponse = []
    tutend = False
    eyespressed = 0
    mouthpressed = 0

##  make click spots for tutorial buttons
    clickrectanglestut=[]
    for i in [[-100,-125],[100,-125],[0,-225]]:
        clickrectanglestut.append(visual.Rect(win,
            width=imagesizes[1][0],height=imagesizes[1][1],pos=i))

##  adjust for tutorial images
    tutimagestart = list(imagestart)
    
    for i in imagedirectories:
        temp=[]
        for j in os.listdir(i):
            if j[j.find('.'):] in ['.jpg','.png','.jpeg']:
                tutstimuli.append ([
                    visual.ImageStim(win,image=i+j,name=j,pos=tutimagestart),
                    j])

##  get buttons for tutorial
    [buttonimages,buttonlabels,buttoncovers,switchlabels] = getswitchitbuttons(
        tutstimuli[0:4],labellist,buttonlocations,[120,60],[0,0,0],
        tutstimuli[4:6],win,True,ffont,fcolor,fsize)

##  tutorial screen 1    
    instructions.setText("    At the start of each trial you will see an image in the location above.\n\
    The image will be a member of one of the categories you are learning about.")
    drawall(win,[instructions,x,entertocont])
    core.wait(1)
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()

##  tutorial screen 2    
    instructions.setText("    For practice, let's imagine that you are learning to categorize\n\
    examples of unhappy faces and happy faces.")
    tutstimuli[0][0].setPos(array(tutimagestart) - array([120,0]))
    tutstimuli[2][0].setPos(array(tutimagestart) + array([120,0]))
    drawall(win,[instructions,tutstimuli[0][0],tutstimuli[2][0],entertocont])
    core.wait(1)
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()
        
##  reset image locs    
    tutstimuli[0][0].setPos(tutimagestart)
    tutstimuli[2][0].setPos(tutimagestart)

##  tutorial screen 3    
    instructions.setText("    On each trial you will use the provided buttons to change the\n\
    example into a member of the requested category (a happy face).")
    drawall(win,[instructions,tutstimuli[0][0],buttonimages,buttonlabels,entertocont])
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()

##  tutorial screen 4        
    instructions.setText("    A happy face would have different eyes and a different mouth, so practice \n\
    clicking on the buttons to make the image fit the target category.")
    drawall(win,[instructions,tutstimuli[0][0],buttonimages,buttonlabels])
    while not tutend:
        [tutresponse, tutrt] = buttongui(cursor,timer,clickrectanglestut,switchlabels)
        if 'Eyes' in tutresponse:
            if mouthpressed == 0:
                tutstimuli[1][0].setPos([150,175])
                drawall(win,[instructions,tutstimuli[1][0],tutstimlab,
                    buttonimages,buttonlabels,buttoncovers[0]])
                eyespressed = 1        
            if mouthpressed == 1:
                tutend = True
        if 'Mouth' in tutresponse:
            if eyespressed == 0:
                tutstimuli[3][0].setPos([150,175])
                drawall(win,[instructions,tutstimuli[3][0],tutstimlab,
                    buttonimages,buttonlabels,buttoncovers[1]])
                mouthpressed = 1
            if eyespressed == 1:
                tutend = True

##  tutorial screen 6            
    while not 'Done' in tutresponse:
        tutstimuli[2][0].setPos([150,175]) 
        instructions.setText("        When you complete your changes you will click the done button.\n\n\
        You will then be provided feedback about the example you created.")
        entertocont.setText('Click the done button to receive feedback')
        drawall(win,[instructions,tutstimuli[2][0],tutstimlab,
            buttonimages,buttonlabels,buttoncovers[:2],entertocont])
        tutresponse = []
        core.wait(.25)
        [tutresponse, tutrt] = buttongui(cursor,timer,clickrectanglestut,switchlabels)                    

##  tutorial screen 7
    entertocont.setText('Press the spacebar to continue')
    instructions.setText("Correct! You made a member of the Happy Face category")
    tutstimlab.setText("Happy Face")
    drawall(win,[instructions,tutstimuli[2][0],tutstimlab,entertocont])
    if 'q' in event.waitKeys(keyList=['q','space']):
        print 'User Terminated'
        core.quit()

##  tutorial screen 8                
    entertocont.setText('Press the spacebar to begin the experiment')
    tutstimlab.setPos([0,50])
    tutstimlab.setText("Alright! It looks like you've got the hang of it.\n\
\n\
Remember: your goal in the following task is to learn about two new categories by making changes just like you practiced. \n\
\n\
At first you will have to guess what changes to make in order to produce a member of the requested category.  You will receive feedback that will help guide your learning.\n\
\n\
Importantly, you will be tested several times to see how well you are learning the categories.  If you perform well, you will be able to finish the experiment faster.\n\
\n\
Please ask the experimenter if you have any further questions.")
    drawall(win,[tutstimlab,entertocont])
    buttonimages = []
    buttonlabels = []
    buttoncovers = [] 
    switchlabels = []
    if 'q' in event.waitKeys(keyList=['q','space']):
        core.quit()

#------------------------------------------------------------------------------------
# waits for responses and completes examples corresponding to user input
def switchitgui(win,cursor,timer,stimuluslist,trialinfo,switchlabels,
                buttonimages,clickrectangles,featurenames,
                instructions,switchmatrix,buttoncovers,catlabfin,
                targetcategory,phase):

##  define trial properites
    currenttrial = list(trialinfo)
    currentimage = trialinfo[0]
    currentproperties = trialinfo[2]

##  initalize data to be updated in trial loop
    numresponses = 0
    buttonpushed = [0] * len(switchlabels)
    trialcovers = []
    newproperties = list(currentproperties)
    newexampleinfo = []
    endtrial = False
        
##  trial loop starts
    while not endtrial:
    ##  draw trial for all trials > 1
        if numresponses > 0:
            instructions.setText(
            "Here is what you've done so far to make this a " + targetcategory + ". Change another feature OR click done")    
            drawall(win,[currentimage,clickrectangles,buttonimages,instructions,trialcovers,catlabfin])
            core.wait(.5)
    ##  draw first trial
        else:
            drawall(win,[currentimage,clickrectangles,buttonimages,instructions,buttoncovers[-1]])
            core.wait(.5)
    ##  get response 
        [response,rt]=buttongui(cursor,timer,clickrectangles,switchlabels)                
        print response
    ##  continue trial as function of response
        for i in switchlabels:
        ##  populate list with pushed buttons  
            if i in response and buttonpushed[switchlabels.index(i)] != 1:
                buttonpushed[switchlabels.index(i)] = 1
                print buttonpushed
                buttonpushed[-1] = 0
            ##  find out if a feature button is pressed (vs done)    
                if switchlabels.index(i) <= len(switchlabels)-2:
                ##  change target feature and find matching example
                    if currentproperties[featurenames.index(response)] == 0.0:
                        newproperties[featurenames.index(response)] = 1.0
                    else:
                        newproperties[featurenames.index(response)] = 0.0
                    newexampleinfo = findstimulus(stimuluslist,newproperties)
                ##  set new properties
                    currentimage = newexampleinfo[0]
                    currentproperties = list(newproperties)
                    catlabfin.setPos([0,270])
                    if trialinfo[3] == 'Tannet':
                        catlabfin.setText('Target: Lape')
                        if phase == 'switchit':    
                            currentimage.setPos([-150,150])
                            catlabfin.setPos([-150,270])
                    else:
                        catlabfin.setText('Target: Tannet')
                        if phase == 'switchit':    
                            currentimage.setPos([150,150])
                            catlabfin.setPos([150,270])
                            
                    trialcovers.append(buttoncovers[switchlabels.index(i)])
                    numresponses = numresponses + 1
                    
                elif i == switchlabels[-1]:
                    if numresponses > 0:
                        numresponses = numresponses + 1
                        endtrial = True
                    else:
                        numresponses = 0

    return [newexampleinfo,buttonpushed,rt]

#------------------------------------------------------------------------------------
# sets up validation phase
def setvalvars(checkupcounter,valaccuracy,valaccuracylist,fontstuff,win):
##  init instructs n vars
    perf = visual.TextStim(win,text='',wrapWidth=1000,
        color=fontstuff[0],font=fontstuff[1],height=fontstuff[2])
    fb = visual.TextStim(win,text='',wrapWidth=1000,
        color=fontstuff[0],font=fontstuff[1],height=fontstuff[2])
    fb.setPos([0,-100])
    endtraining = False

##  make val accuracy list
    if checkupcounter == 0:
        valaccuracylist.append(valaccuracy)
    ##  set first val feedback
        temp = '%.f' % (valaccuracylist[0] * 100)
        perf.setText('Your accuracy on the first check-up was ' +temp+ '%')
        fb.setText('Press the spacebar to continue.')
    elif checkupcounter == 1:
        valaccuracylist.append(valaccuracy)
    elif checkupcounter > 1:
        valaccuracylist[0] = valaccuracylist[1]
        valaccuracylist[1] = valaccuracy

##  set second thru last val feedback            
    if checkupcounter >= 1:
        twoblockperf = '%.f' % (average(array(valaccuracylist)) * 100)
        perf.setText('Your average accuracy on the last two check-ups was '+twoblockperf+'%')
        if average(array(valaccuracylist)) >= .85:
            fb.setText('You did it! Time to move on, press the spacebar to continue.')     
            endtraining = True
        else:
            fb.setText("Try to score better on the next check-up to move on. Press space to continue")
            
    valinstructs = [[perf],[fb]]
    checkupcounter = checkupcounter + 1
    return [valinstructs, endtraining, checkupcounter]