print '\n--------RUNNING SWITCHIT TEST------'

## define testing block -- based on all 3f images
print '-----TEST ITEMS:'
switchtestingblock=[]

## init trial vars
switchbuttonimages=[]
stimfeaturelist=[]
itemindex=[]
catlabfin = visual.TextStim(win,'',font=ffont,
    color=fcolor,height=fsize,pos=[0, 0])
           
## grab appropriate stimuli
for i in stimuli:
    features=i[2]
    nummissingfeatures=sum(isnan(features))
    if nummissingfeatures==0:
        switchtestingblock.append(i)
    if nummissingfeatures==2:
        switchbuttonimages.append(i)

## setup button image list
for i in switchbuttonimages:
##  get feature label    
    featureloc = where(isnan(i[2]) == False)
    featureloc = featureloc[0]
    i.append(featurenames[featureloc])
## get feature value
    i.append(i[2][featureloc])

## combine image list with category names and index
for i in switchtestingblock:
    if condition < 4:
        i.append(categorynames[whichcategory(i[-1],validegs)])
        i.append(switchtestingblock.index(i)+1)
    print i
    stimfeaturelist.append(i[2])
    itemindex.append(switchtestingblock.index(i)+1)\

## make reference list for the switch matrix
stimfeaturelist = [[stimfeaturelist],[itemindex]]

## create switch matrix
#print '-----------Switch Matrix------------'
switchmatrix = makeswitchmatrix(switchtestingblock,stimfeaturelist)

## present instructions and wait for response
phase='switchtest'
presentinstructions(win,instructions,instructiontext,phase)
 
##  Set the location of each button
buttonlocations=[[-200,-125],
                 [0,-125],
                 [200,-125],
                 [0,-275]]

## init click areas
clickrectangles=[]
for i in buttonlocations:
    clickrectangles.append(visual.Rect(win,
        width=imagesizes[1][0],height=imagesizes[1][1],pos=i))
## special props for done button (not an image)
clickrectangles[-1] = visual.Rect(win,width=150,height=75,pos=[0,-275])

## iterate over blocks and trials
print '\n------executing trials------\n'
print switchtestingblock
rnd.shuffle(switchtestingblock)
trialnum = 1
  
for trial in switchtestingblock:
##  define trial properites
    startimage=trial[0]
    filename=trial[1]
    startproperties=trial[2]
    startcategory=trial[3]
    if startcategory == 'Lape':
        targetcategory = 'Tannet'
    else:
        targetcategory = 'Lape' 
    startimage.setSize(imagesizes[0])
    startimage.setPos(imagestart)

##  set task text
    tasktext='Use the buttons below to change this leaf into a '+targetcategory+' leaf.'
    instructions.setText(tasktext)

##  grab buttons
    [buttonimages,buttonlabels,buttoncovers,switchlabels] = getswitchitbuttons(
        stimuli,featurenames,buttonlocations,imagesizes[1],
        startproperties,switchbuttonimages,win,False,
        ffont,fcolor,fsize)

##  draw fix cross
    starttrial(win,.5,fixcross) 

##  run gui interface
    [completedstimulusinfo,buttonpushed,rt]=switchitgui(
        win,cursor,timer,stimuli,trial,switchlabels,
        buttonimages,clickrectangles,featurenames,
        instructions,switchmatrix,buttoncovers,catlabfin,
        targetcategory,phase)

##  get info about final example
    completedimage=completedstimulusinfo[0]
    completedproperties=completedstimulusinfo[2]

##  determine correctness, block accuracy and return feedback
    completedproperties = list(completedproperties.astype(int))
    for i in validegs:
        if completedproperties in i:
            currentcategory=validegs.index(i)
            currentcategory=categorynames[currentcategory]

    if currentcategory == startcategory:
        accuracy=0    
    else:
        accuracy=1
        
##  click to continue
    instructions.setText(continuestring)
    drawall(win,[completedimage,instructions])
    
##  log data
    currenttrial=[condition,subjectnumber,phase,blocknum,trialnum,filename,
        list(completedproperties),list(startproperties),startcategory,
        currentcategory,rt,accuracy,sum(buttonpushed)]
    subjectdata.append(currenttrial)
    writefile(subjectfile,subjectdata,',')

##  print trial info
    print '\nBlock '+str(blocknum)+', Trial '+str(trialnum)+' information:'
    print ['finalimage:',list(completedproperties)]
    print ['buttons pushed:',buttonpushed]
    print ['original cat:',startcategory]
    print ['switched cat:',currentcategory]
    print ['accuracy:',accuracy]

##  end trial
    core.wait(.5)        
    clicktocontinue(cursor)
    trialnum = trialnum + 1
