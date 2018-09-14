#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:49:00 2017

@author: stechen1
"""
from textblob import TextBlob
from processnames import *
from processtext import *

filename='samplecomments.txt'

malecount=0
femalecount=0
commentcount=0
avgcount=0

initnames()

with open(filename) as old:
    
    text=old.read()
    text=cleanstring(cleanemoji(text))
    blob = TextBlob(text)
    ngram_var = blob.ngrams(n=3)

    for line in old:
        commentcount+=1
        counted=countpeople(line)
        avgcount=(avgcount+counted[0]+counted[1])/2
        malecount=malecount+counted[0]
        femalecount=femalecount+counted[1]

    print (str(malecount) + ' males & ' + str(femalecount) + ' females tagged in ' + str(commentcount) + ' comments. Average of ' + str(avgcount) + ' tagged per comment')
    print(ngram_var)