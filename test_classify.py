print '\n------RUNNING CLASSIFICATION TESTING------'
print '------------------------------------\n'


if phase == 'validation':
    triallist = '\\valtrials.csv'
else:
    phase = 'classifytest'
    triallist = '\\classifytrials.csv'
    
## ----------------------------------------------------------------
## load valid trials given the shj type
if sys.platform=='darwin':
##    [f1,f2,f3,category,shjtype]
    classifylist= genfromtxt(
        os.getcwd() + '/classifytrials.csv',
        delimiter=',',dtype='int',skip_header=1).astype(float)
else:
    classifylist= genfromtxt(
        os.getcwd() + triallist,
        delimiter=',',dtype='int',skip_header=1).astype(float)

## reduce trial listings
classifylist=classifylist[classifylist[:,-1]==shjcondition]
classifyfeatures=classifylist[:,0:3].tolist()
classifycategory=classifylist[:,3].tolist()

## ----------------------------------------------------------------
## define classify test block -- based on the classifylist
print '-----TEST BLOCK ITEMS:'
classifytestblock=[]
valblockacc=[]

for i in stimuli:
    features=array(i[2])
    features[isnan(features)]=-1.0
    features=features.tolist()
    if features in classifyfeatures:
        category=classifycategory[classifyfeatures.index(features)]
        classifytestblock.append([i,category])
for i in classifytestblock:
    print i

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
##  create a text label
    buttontext.append(visual.TextStim(win,
        text=categorynames[buttonnum],height=fsize,font=ffont,
        color=fcolor,pos=buttons[buttonnum].pos))


## present instructions and wait for response
presentinstructions(win,instructions,instructiontext,phase)

## iterate over blocks and trials
print '------executing trials------\n'

rnd.shuffle(classifytestblock)
trialnum=1

for trial in classifytestblock:        

##        define trial properites
    image=trial[0][0]
    filename=trial[0][1]
    properties=list(trial[0][2])
    category=int(trial[1])
    if category!=-1:
        category=categorynames[category]
    else:
        category='nan'
    
    print category
##        set task text
    tasktext='Click a button to select the correct category.'
    instructions.setText(tasktext)

##    reset image size and position
    image.setSize(imagesizes[0])
    image.setPos(imagestart)
    
##        draw fix cross
    starttrial(win,.5,fixcross)        

##        draw current stimuli
    drawall(win,[image])
    core.wait(.5)
    drawall(win,[image,instructions,buttons,buttontext])
    core.wait(.5)
            
##        wait for response
    [response,rt]=buttongui(cursor,timer,buttons,categorynames)
    drawall(win,[])
    core.wait(.5)

##        check correctness 
    if category=='nan': # if there is no correct answer
        accuracy='nan'
    else:
        if response==category:
            accuracy=1
        else:
            accuracy=0
    valblockacc.append(accuracy)
    
##        print trial info
    print '\nClassify Test Trial '+str(trialnum)+' information:'
    print ['presented image:', properties]
    print ['actual:',category]
    print ['response:', response]
    print ['accuracy:',accuracy]
    
##        click to continue
    if phase != 'validation':
        instructions.setText(continuestring)
        drawall(win,[])
        core.wait(.5)


##        log data
    if phase == 'classifytest':
        currenttrial=[condition,subjectnumber,phase,'',trialnum,filename,
              list(properties),'','','',category,response,rt,accuracy]
    if phase == 'validation':
        currenttrial=[condition,subjectnumber,phase,checkupcounter+1,
            trialnum,filename,list(properties),'','','',category,
            response,rt,accuracy]
    subjectdata.append(currenttrial)
    writefile(subjectfile,subjectdata,',')

    trialnum=trialnum+1

if phase == 'validation':
    valaccuracy = average(array(valblockacc))
