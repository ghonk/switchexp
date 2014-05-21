print '\n------RUNNING RANKING TEST------'
print '------------------------------------\n'

## define ranking items -- based on all full images
print '-----ITEMS TO RANK:'
rankimages=[]
for i in stimuli:
    features=i[2]
    nummissingfeatures=sum(isnan(features))
    if nummissingfeatures == 0:
        rankimages.append(list(i))
        rankimages[-1].append(len(rankimages)-1)
        print rankimages[-1]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# specify position of each image
x=[-300,-100,100,300]
y=[-150,-300]
positions= makecombos(x,y)
rnd.shuffle(positions)

## set size and position of each image
print '\nstarting locations:'
for i in rankimages:
    num=rankimages.index(i)
    i[0].setPos(positions[num])
    i[0].setSize(imagesizes[1])
    print [i[1:],i[0].pos.tolist()]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# create external stimuli
boxpositions=[[-550,0],[550,0]]
boxsize=[250,700]

textlabels=[] #for each category
for i in categorynames:
    textlabels.append(visual.TextStim(win,text='',
         color=fcolor,font=ffont,height=fsize))
    textlabels[-1].setText('Typical ' + i + ' Leaves')
textlabels[0].setPos([boxpositions[0][0],boxsize[1]/1.9])
textlabels[1].setPos([boxpositions[1][0],boxsize[1]/1.9])

# not typical
textlabels.append(visual.TextStim(win,text='Not At All\nTypical',
         color=fcolor,font=ffont,height=fsize))
textlabels[-1].setPos([boxpositions[0][0],boxsize[1]/-1.8])
textlabels.append(visual.TextStim(win,text='Not At All\nTypical',
         color=fcolor,font=ffont,height=fsize))
textlabels[-1].setPos([boxpositions[1][0],boxsize[1]/-1.8])

boxes=[]
for i in boxpositions:
    boxes.append(visual.Rect(win,width=boxsize[0],height=boxsize[1]))
    boxes[-1].setFillColor([.5,.5,.5])
    boxes[-1].setLineColor([-1,-1,-1])
    boxes[-1].setPos(i)
    
# task text
tasktxt=visual.TextStim(win,text='',wrapWidth=1000,
         color=fcolor,font=ffont,height=fsize)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
## present instructions and wait for response
phase='rankingtest'
presentinstructions(win,instructions,instructiontext,phase)
tasktxt.setText(
'First, use the mouse to drag each example to its correct\n\
category box. Within each category box, carefully arrange the\n\
examples in order of typicality. Be sure to put the best example(s)\n\
of the category toward the top and the least typical example(s)\n\
toward the bottom.\n\
\n\
If you consider some examples to be equally typical, it is ok to put\n\
them side-by-side.\n\
\n\
Press <return> when you are finished.')

tasktxt.setPos([0,125])
##    start trial
starttrial(win,.5, fixcross)

##    draw all stimuli
for i in boxes:
    i.draw(win)
tasktxt.draw(win)
for i in textlabels:
    i.draw()
for i in rankimages:
    i[0].draw()
win.flip()


##determine if images are in the box
insidebox = findobjects(rankimages,boxes)

##    ------ start arranging the examples --------
print '\n------starting gui--------\n'
timer.reset() #start timer
while ('return' not in event.getKeys(keyList='return')) or (-1 in insidebox):
    
    insidebox = findobjects(rankimages,boxes)
    if 'q' in event.getKeys(keyList='q'):
        core.quit()
    
    for i in list(rankimages[::-1]):
        image=i[0]
        if cursor.isPressedIn(image):

            #sort image list so selection is on top
            rankimages.pop(rankimages.index(i))
            rankimages.insert(len(rankimages),i)

            #relocate selection
            while True in cursor.getPressed():
                image.setPos(cursor.getPos())

                # draw objects in depth order
                for j in boxes:
                    j.draw(win)
                tasktxt.draw(win)
                for j in textlabels:
                    j.draw()
                for j in rankimages:
                    j[0].draw()
                win.flip() 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##    ------ analyze and store data --------
ranktime=timer.getTime()
insidebox = findobjects(rankimages,boxes)
print '\nRank Time: ' + str(round(ranktime,3)) + '. Final locations:'
for i in rankimages:

    #define image properties
    features=array2list(i[2],True)
    image=i[0]
    filename=i[1]
    imageid=i[3]
    startlocation=positions[imageid]

    # get category assignment of image
    category=whichcategory(features,validegs)
    category=categorynames[category]
    
    #determine sort status
    finalsort=insidebox[rankimages.index(i)]
    finalsort=categorynames[finalsort]

    if finalsort==category:
        accuracy=1
    else:
        accuracy=0
    
    #get final image location
    endlocation=image.pos.tolist()
    
##        write data to file and print to log
    print [features,filename,category,endlocation,finalsort,accuracy]
    currentdata=[condition,subjectnumber,phase,filename,features,
        category,startlocation,endlocation,finalsort,ranktime,accuracy]
    subjectdata.append(currentdata)
    writefile(subjectfile,subjectdata,',')
