# -*- coding: utf-8 -*-

from textblob import TextBlob
from processnames import *
from processtext import *

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def find_nth_overlapping(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start

# inputfile can take an array of csv files
inputfile=['samplefacebook_comments']
# Exclude the page / author own comments and replies
excludeauthor=['Philadelphia Cream Cheese']
# statuscheck takes an array of status(i.e. post) ids of interest
statuscheck=['40367782924_10156527050277925','40367782924_10156523849842925']

maleauthor={'Main':0,'Sub':0}
maletag={'Male':0,'Female':0}
femaleauthor={'Main':0,'Sub':0}
femaletag={'Male':0,'Female':0}
commentcount=0
sentiment={'Male Positive':0,'Female Positive':0,'Male Negative':0,'Female Negative':0}

initnames()
            
def authorcount(subauthor,male,female,tagged,polarity):
    global maleauthor
    global maletag
    global femaleauthor
    global femaletag
    global sentiment
    if male>female:
        maletag['Male']=maletag['Male']+tagged[0]
        maletag['Female']=maletag['Female']+tagged[1]
        if subauthor>0:
            maleauthor['Main']+=1
        else:
            maleauthor['Sub']+=1
        
        if polarity>0:
            sentiment['Male Positive']+=1
        elif polarity<-0:
            sentiment['Male Negative']+=1
            
    elif female>male:
        femaletag['Male']=femaletag['Male']+tagged[0]
        femaletag['Female']=femaletag['Female']+tagged[1]
        if subauthor>0:
            femaleauthor['Main']+=1
        else:
            femaleauthor['Sub']+=1
            
        if polarity>0:
            sentiment['Female Positive']+=1
        elif polarity<-0:
            sentiment['Female Negative']+=1


with open('_'.join(statuscheck)+'.txt', 'w') as new:    
    for input in inputfile:
        with open(input + '.csv') as old:
            for line in old:
                if "comment_id" not in line:
                    line=line.replace(',"',',')
                    line=line.replace('",',',')
                    # Extract status, comment and author
                    status=line[find_nth(line,',',1)+1:find_nth(line,',',2)]
                    extract=line[find_nth(line,',',3)+1:find_nth(line,',2017',1)]
                    author=extract[extract.rfind(',')+1:]
                    subauthor=len(line[find_nth(line,',',2)+1:find_nth(line,',',3)])
                    if author not in excludeauthor:
                        comment=extract[:extract.rfind(',')]
                        # all only works if 1 element, any only works if multiple
                        if len(statuscheck)>1 and any([result in status for result in statuscheck]):
                            new.write(comment + '\n')
                            commentcount+=1
                            gender=countpeople(author)
                            cleanline=cleanstring(cleanemoji(comment))
                            opinion=TextBlob(cleanline)
                            tagged=countpeople(cleanline)
                            authorcount(subauthor,gender[0],gender[1],tagged,opinion.sentiment.polarity)
                        elif len(statuscheck)==1 and all([result in status for result in statuscheck]):
                            new.write(comment + '\n')
                            commentcount+=1
                            gender=countpeople(author)
                            cleanline=cleanstring(cleanemoji(comment))
                            opinion=TextBlob(cleanline)
                            tagged=countpeople(cleanline)
                            authorcount(subauthor,gender[0],gender[1],tagged,opinion.sentiment.polarity)

print (str(commentcount) + ' comments')
print (str(maleauthor['Main']) + ' + ' + str(maleauthor['Sub']) + ' male authors (' + str(sentiment['Male Positive']) + ' positive, ' + str(sentiment['Male Negative']) + ' negative) tagged ' + str(maletag['Male']) + ' males & ' + str(maletag['Female']) + ' females')
print (str(femaleauthor['Main']) + ' + ' + str(femaleauthor['Sub']) + ' female authors (' + str(sentiment['Female Positive']) + ' positive, ' + str(sentiment['Female Negative']) + ' negative) tagged ' + str(femaletag['Male']) + ' males & ' + str(femaletag['Female']) + ' females')


