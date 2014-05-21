print '\n------RUNNING SINGLE ITEM TYPICALITY TESTING------'
print '----------------------------------------------------\n'
numscalepositions=9
scaleposition=[0,-100]
scalesize=.8 


#------------------------------------------------------------------------------------
## LOAD STIMULI
## define block -- based on all 3f images
print '-----SINGLE ITEM TYPICALITY TEST BLOCK:'
stypicalityblock=[]
for i in stimuli:
    features=i[2]
    nummissingfeatures=sum(isnan(features))
    if nummissingfeatures==0:
        stypicalityblock.append(list(i))

## combine image list with category names
for i in stypicalityblock:
    category=whichcategory(i[2],validegs)
    i.append(categorynames[category])

for i in stypicalityblock:
    print i


# create rating scale
leftoption='\n  Not at\n\
all typical'
rightoption='\nHighly\n\
typical'

ratingscale=visual.RatingScale(win,high=numscalepositions,
        highAnchorText=rightoption,lowAnchorText=leftoption,
        textColor=fcolor,textFont=ffont,textSizeFactor=.7,
        escapeKeys=['q'],showScale=False,lineColor=[0,0,0],
        acceptText ='Accept',acceptPreText='',minTime = .5,
        showValue = False,pos=scaleposition,displaySizeFactor=scalesize) 
        
#this is a rectanlge that makes the scale look like it has a box
scalewindow=visual.Rect(win,width=500,height=150)
scalewindow.setFillColor([.9,.9,.9])
scalewindow.setLineColor([0,0,0])
scalewindow.setPos(scaleposition)

#------------------------------------------------------------------------------------
## BEGIN TRIALS
## present instructions and wait for response
phase='stypicality'
presentinstructions(win,instructions,instructiontext,phase)

## iterate over blocks and trials
print '\n------executing trials------\n'
rnd.shuffle(stypicalityblock)
trialnum=1
for trial in stypicalityblock:
    
##        define trial properites
    category=trial[3]
    image=trial[0]
    filename=trial[1]
    properties=array2list(trial[2],True)

    image.setSize(imagesizes[0])
    image.setPos(imagestart)

##        set task text
    tasktext='How typical is this leaf of the '+category+' category?'
    instructions.setText(tasktext)

##        draw fix cross
    starttrial(win,.5,fixcross)

    drawall(win,[image])
    core.wait(.5)

    ratingscale.reset()
    while ratingscale.noResponse:
        drawall(win,[image,scalewindow,instructions,ratingscale])
        
    typicalityrating = ratingscale.getRating()
    reactiontime = ratingscale.getRT()

                         
##        print trial info
    print '\nSingle Item Typicality Trial '+str(trialnum)+' information:'
    print ['Start Image:', properties]
    print ['Category:',category]
    print ['Rating:',typicalityrating]    

    win.flip()
    core.wait(.5)        

##        log data
    currenttrial=[condition,subjectnumber,phase,'',trialnum,filename,
        properties,category,reactiontime,typicalityrating]
    subjectdata.append(currenttrial)
    writefile(subjectfile,subjectdata,',')

    trialnum=trialnum+1
            
