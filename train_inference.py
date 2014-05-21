print '\n------RUNNING INFERENCE TRAINING------'
print '----------------------------------------\n'

## define training block -- based on all 2f images
print '-----TRAINING ITEMS:'
trainingblock=[]
for i in stimuli:
    features=i[2]
    nummissingfeatures=sum(isnan(features))
    remainingfeatures=features[isnan(features) ==  False]
    if (nummissingfeatures==1) and (sum(remainingfeatures)==1):
        trainingblock.append(i)

## combine image list with category names
trainingblock = makecombos(trainingblock,categorynames)
for i in trainingblock:
    print i

##create rectangles that subsitute for actual image buttons
clickrectangles=[]
clickrectangles.append(visual.Rect(win,
    width=imagesizes[1][0],height=imagesizes[1][1],pos=[-100,-125]))
clickrectangles.append(visual.Rect(win,
    width=imagesizes[1][0],height=imagesizes[1][1],pos=[100,-125]))

## present instructions and wait for response
phase='inference'
presentinstructions(win,instructions,instructiontext,phase)

## iterate over blocks and trials
print '\n------executing trials------\n'
for blocknum in range(1, numtrainingblocks+1):
    rnd.shuffle(trainingblock)
    trialnum=1
    for trial in trainingblock:

##        define trial properites
        startcategory=trial[1]
        startimage=trial[0][0]
        filename=trial[0][1]
        startproperties=trial[0][2]

##        set task text
        tasktext='task instructions-- ' + startcategory
        instructions.setText(tasktext)    

##        determine missing feature and get current buttons
        missingfeature=nonzero(isnan(startproperties))
        missingfeature=int(missingfeature[0])
        [buttonimages, buttonlabels] = getinferencebuttons(
            stimuli,missingfeature,imagesizes[1])

##        draw fix cross
        starttrial(win,.5,fixcross) 

##        run inference gui interface
        [completedstimulusinfo,response,rt,featureorder]=generategui(
            win,cursor,timer,stimuli,trial,
            buttonimages,buttonlabels,clickrectangles,instructions)

##        get info about final example
        completedimage=completedstimulusinfo[0]
        completedproperties=completedstimulusinfo[2]

##        determine correctness and return feedback
        completedproperties = list(completedproperties.astype(int))
        for i in validegs:
            if completedproperties in i:
                currentcategory=validegs.index(i)
                currentcategory=categorynames[currentcategory]

        if currentcategory == startcategory:
            feedback='Correct! this is a member of the ' + currentcategory + ' category.'
            accuracy=1
        else:
            feedback='Incorrect... this is a member of the ' + currentcategory + ' category.'
            accuracy=0
        instructions.setText(feedback)
        drawall(win,[instructions,completedimage])
        core.wait(.5)

##        print trial info
        print '\nBlock '+str(blocknum)+', Trial '+str(trialnum)+' information:'
        print ['finalimage:', list(completedproperties)]
        print ['feature order:',featureorder]
        print ['queued:',startcategory]
        print ['actual:', currentcategory]
        print ['accuracy:',accuracy]    

##        click to continue
        instructions.setText(feedback+continuestring)
        drawall(win,[completedimage,instructions])
        core.wait(.5)        
        clicktocontinue(cursor)

##        log data
        currenttrial=[condition,subjectnumber,phase,blocknum,trialnum,filename,
            list(completedproperties),featureorder,startcategory,currentcategory,accuracy]
        subjectdata.append(currenttrial)
        writefile(subjectfile,subjectdata,',')

        trialnum=trialnum+1
            
