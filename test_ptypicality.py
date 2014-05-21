print '\n------RUNNING PAIRWISE TYPICALITY------'
print '---------------------------------------\n'

imagepositions=[[-175,150],[175,150]]
buttonpositions=[[-175,-100],[0,-100],[175,-100]]
buttontext=['Left','Tie','Right']

##------------------------------------------------------------------------------------
##  LOAD STIMULI
## define training block -- based on all 3f images
print '-----PAIRWISE TYPICALITY TEST BLOCK:'
ptypicalityblock=[]
for i in stimuli:
    features=i[2]
    nummissingfeatures=sum(isnan(features))
    if nummissingfeatures==0:
        ptypicalityblock.append(list(i))

##make pairs of images        
ptypicalityblock=list2pairs(ptypicalityblock)

## refine block -- delete between-category pairs
for i in ptypicalityblock:
    pairnumber=ptypicalityblock.index(i)
    c1=whichcategory(i[0][2],validegs)
    c2=whichcategory(i[1][2],validegs)
    if c1==c2:
        i.append(categorynames[c1])
    else:
        ptypicalityblock=ptypicalityblock[:pairnumber]+ptypicalityblock[pairnumber+1:]

for i in ptypicalityblock:
    print i[0]
    print i[1]
    print i[2]
    print ''


##create button stimuli
buttons=[]
buttonlabels=[]
for i in range(3):    
    buttons.append(visual.Rect(win, width=150, height=75))
    buttons[i].setFillColor([.8,.8,.8])
    buttons[i].setLineColor([-1,-1,-1])
    buttons[i].setPos(buttonpositions[i])
        
    #create a text label
    buttonlabels.append(visual.TextStim(win,
        text=buttontext[i],height=fsize,font=ffont,
        color=fcolor,pos=buttonpositions[i]))


##------------------------------------------------------------------------------------
##  START RUNNING
## present instructions and wait for response
phase='ptypicality'
presentinstructions(win,instructions,instructiontext,phase)

## iterate over blocks and trials
print '\n------executing trials------\n'
rnd.shuffle(ptypicalityblock)
trialnum=1
for trial in ptypicalityblock:

##        define trial properites
    images=[trial[0][0],trial[1][0]]
    filenames=[trial[0][1],trial[1][1]]
    properties=[array2list(trial[0][2],True),
                array2list(trial[1][2],True)]
    category=trial[2]

##    set image position and size
    for i in images:
        i.setPos(imagepositions[images.index(i)])
        i.setSize(imagesizes[0])

##        set task text
    tasktext='Which leaf is more typical of the '+category+' category?'
    instructions.setText(tasktext)
    
##        draw fix cross
    starttrial(win,.5,fixcross)

##    draw current stimuli
    drawall(win,[images])
    core.wait(.5)
    drawall(win,[images,instructions,buttons,buttonlabels])

##        wait for response
    [response,rt]=buttongui(cursor,timer,buttons,buttontext)
    drawall(win,[images])
    core.wait(.5)

##        print trial info
    print '\nPairwise Typicality Trial '+str(trialnum)+' information:'
    print ['Left Image:', properties[0]]
    print ['Right Image:', properties[1]]
    print ['Category:',category]
    print ['Response:',response]    

    win.flip()
    core.wait(.5)

##        log data
    currenttrial=[condition,subjectnumber,phase,'',trialnum,filenames,
        properties[0],properties[1],category,rt,response]
    subjectdata.append(currenttrial)
    writefile(subjectfile,subjectdata,',')

    trialnum=trialnum+1
            
