print '\n------RUNNING CLASSIFICATION------'
print '------------------------------------\n'

## define classify block -- based on all full images
print '-----TRAINING ITEMS:'
trainingblock=[]
checkupcounter = 0
endtraining = False

for i in stimuli:
    features=i[2]
    nummissingfeatures=sum(isnan(features))
    if nummissingfeatures == 0:
        print i
        trainingblock.append(i)

##make classification buttons
buttons=[]
buttontext=[]
for i in categorynames:
    buttonnum=categorynames.index(i)
    
    buttons.append(visual.Rect(win, width=150, height=75))
    buttons[buttonnum].setFillColor([.8,.8,.8])
    buttons[buttonnum].setLineColor([-1,-1,-1])
    
    buttons[buttonnum].setPos([-100,-100])
    if buttonnum==1:
        buttons[buttonnum].setPos([100,-100])
        
    #create a text label
    buttontext.append(visual.TextStim(win,
        text=categorynames[buttonnum],height=fsize,font=ffont,
        color=fcolor,pos=buttons[buttonnum].pos))

## present instructions and wait for response
phase='classify'
presentinstructions(win,instructions,instructiontext,phase)

## __________________________________________________________
## TUTORIAL HERE                                             |

tutorialskip = False
if not tutorialskip:
    classifytutorial(win,instructions,imagestart,
        buttons,buttontext,ffont,fcolor,fsize,
        cursor,timer,imagesizes)

## __________________________________________________________|
##


## iterate over blocks and trials
print '------executing trials------\n'
for blocknum in range(1, numtrainingblocks+1):
    if endtraining == True:
        phase = ''
        break
    rnd.shuffle(trainingblock)
    trialnum=1
    
    for trial in trainingblock:
##        define trial properites
        image=trial[0]
        filename=trial[1]
        properties=list(trial[2].astype(int))
        
##        determine category membership
        for i in validegs:
            if list(properties) in i:
                category=categorynames[validegs.index(i)]
        
##        set task text
        tasktext='Click a button to select the correct category.'
        instructions.setText(tasktext)

##        draw fix cross
        starttrial(win,.5,fixcross)        

##        draw current stimuli
        drawall(win,[image])
        core.wait(.5)
        drawall(win,[image,instructions,buttons,buttontext])
        core.wait(.5)
                
##        wait for response
        [response,rt]=buttongui(cursor,timer,buttons,categorynames)
        drawall(win,[image])
        core.wait(.5)

##        check correctness and return feedback
        if response==category:
            feedback='Correct! this is a member of the ' + category + ' category.'
            accuracy=1
        else:
            feedback='Incorrect... this is a member of the ' + category + ' category.'
            accuracy=0

##        print trial info
        print '\nBlock '+str(blocknum)+', Trial '+str(trialnum)+' information:'
        print ['presented image:', properties]
        print ['actual:',category]
        print ['response:', response]
        print ['accuracy:',accuracy]
        
        instructions.setText(feedback)
        drawall(win,[instructions,image])
        core.wait(.5)

##        click to continue
        instructions.setText(feedback+continuestring)
        drawall(win,[image,instructions])
        core.wait(.5)        
        clicktocontinue(cursor)

##        log data
        currenttrial=[condition,subjectnumber,phase,blocknum,trialnum,filename,
              list(properties),'','','',category,response,rt,accuracy]
        subjectdata.append(currenttrial)
        writefile(subjectfile,subjectdata,',')

        trialnum=trialnum+1

##  initiate validation
    if blocknum == 1 or (blocknum + 1) % 2 == 0: 
        phase = 'validation'
        if checkupcounter == 0:
            valaccuracylist = []
        if checkupcounter > 6:
            phase = 'classify'
            endtraining = True
        else:
            print '\n|----------executing validation-----------|\n'
            print ['check-up number',checkupcounter + 1]
            execfile('test_classify.py')
        ##  get val vars
            [valinstructs, endtraining, checkupcounter] = setvalvars(checkupcounter,
                valaccuracy,valaccuracylist,
                [fcolor,ffont,fsize],win)
        ##  give feedback    
            phase = 'classify'
            drawall(win,[valinstructs[0],valinstructs[1]])
            if 'q' in event.waitKeys(keyList=['q','space']):
                print 'User Terminated'
                core.quit()

    