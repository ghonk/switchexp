print '\n------RUNNING INFERENCE TESTING------'
print '----------------------------------------\n'

## ----------------------------------------------------------------
## load valid trials given the shj type
if sys.platform=='darwin':
##    [F1,F2,F3,CATEGORY,RESPONSEFEATURE,CORRECT,SHJ]
    inferencelist= genfromtxt(
        os.getcwd() + '/inferencetrials.csv',
        delimiter=',',dtype='int',skip_header=1).astype(float)
else:
    inferencelist= genfromtxt(
        os.getcwd() + '\\inferencetrials.csv',
        delimiter=',',dtype='int',skip_header=1).astype(float)

## reduce trial listings
inferencelist=inferencelist[inferencelist[:,-1]==shjcondition]
inferencelist=inferencelist[:,0:-1]


## ----------------------------------------------------------------
## define block -- based on trials listed in inferencetrials
print '-----INFERENCE TEST BLOCK:'
inferenceblock=[]
for i in stimuli:
    stimfeatures=array(i[2])
    stimfeatures[isnan(stimfeatures)]=-1.0
    for j in inferencelist:
        trialfeatures=array(j[0:3])
        if array_equal(stimfeatures,trialfeatures):
            print j
            responsefeature=int(j[4])-1
            category=categorynames[int(j[3])]
            correct=int(j[5])
            inferenceblock.append([i,category,responsefeature,correct])


## ----------------------------------------------------------------
## LOAD BUTTONS, TEXT, ETC
    
##create rectangles that subsitute for actual image buttons
clickrectangles=[]
clickrectangles.append(visual.Rect(win,
    width=imagesizes[1][0],height=imagesizes[1][1],pos=[-100,-125]))
clickrectangles.append(visual.Rect(win,
    width=imagesizes[1][0],height=imagesizes[1][1],pos=[100,-125]))

## ----------------------------------------------------------------
## present instructions and wait for response
phase='inferencetest'
presentinstructions(win,instructions,instructiontext,phase)


## ----------------------------------------------------------------
## iterate over trials
print '\n------executing trials------\n'
rnd.shuffle(inferenceblock)

trialnum=1
for trial in inferenceblock:

##        define trial properites
    startcategory=trial[1]
    startimage=trial[0][0]
    filename=trial[0][1]
    startproperties=trial[0][2]
    responsefeature=trial[2]
    correctresponse=trial[3]
    
##        set task text and set image params
    startimage.setSize(imagesizes[0])
    startimage.setPos(imagestart)
    tasktext='Which of these would you expect for a member of the ' +startcategory+ ' category?'
    instructions.setText(tasktext)    

##        get current buttons
    [buttonimages, buttonlabels, buttonborders] = getinferencebuttons(
        stimuli,responsefeature,imagesizes[1],win)

##        draw fix cross
    starttrial(win,.5,fixcross)

##      draw current stimuli
    drawall(win,[startimage])
    core.wait(.5)
    drawall(win,[startimage,instructions,buttonborders,buttonimages])
    core.wait(.5)

##            wait for response
    [response,rt]=buttongui(cursor,timer,clickrectangles,buttonlabels)
    response=response[0] # ([1] is the feature #, is equal to responsefeature)

##            combine original with response image and find the result stim
    addition=tile(nan,(1,3))[0]
    addition[responsefeature]=response
    newproperties = combinefeatures(startproperties,addition)
    newexampleinfo=findstimulus(stimuli,newproperties)

##          update info for the generated image
    completedimage=newexampleinfo[0]
    completedproperties=newexampleinfo[2]
    
##        draw result
    drawall(win,[completedimage])
    core.wait(.5)

##        determine correctness
    if response==correctresponse:
        accuracy=1
    else:
        accuracy=0

##    update order of feature presentation
    featureorder=[0,0,0]
    featureorder[responsefeature]=1
    
##        print trial info
    print '\nInference Test Trial '+str(trialnum)+' information:'
    print ['finalimage:', list(completedproperties)]
    print ['feature order:',featureorder]
    print ['queued category:',startcategory]
    print ['response:', response]
    print ['correct response:',correctresponse]    

##        click to continue
    instructions.setText(continuestring)
    drawall(win,[completedimage,instructions])
    core.wait(.5)        
    clicktocontinue(cursor)

##        log data
    currenttrial=[condition,subjectnumber,phase,'',trialnum,filename,
        list(completedproperties),featureorder,startcategory,response,
        correctresponse,rt,accuracy]
    subjectdata.append(currenttrial)
    writefile(subjectfile,subjectdata,',')

    trialnum=trialnum+1
            
