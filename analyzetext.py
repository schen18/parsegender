#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:58:02 2017

@author: stechen1
"""
import spacy
nlp = spacy.load('en')
from processtext import *
from emoji_parse import EmojiDict

verbs={}
adverbs={}
adjectives={}
emoji_counter = EmojiDict()

listverbs=[]
listadverbs=[]
listadjectives=[]

filename='samplecomments'

def updatedict(word,dictionary):
    if word in dictionary:
        dictionary[word]+=1
    else:
        dictionary[word]=1
        
with open(filename + '_nlpoutput.txt', 'w') as new:
    with open(filename + '.txt', encoding='utf-8') as old:
        for line in old:
            emoji_counter.add_emoji_count(line)       
            line=cleanstring(cleanemoji(line))
            cleanline=nlp(line)
            for word in cleanline:
                if word.pos_=='VERB' and len(word.lemma_)>2:
                    listverbs.append(word.lemma_)
                    updatedict(word.lemma_,verbs)
                elif word.pos_=='ADV' and len(word.lemma_)>2:
                    listadverbs.append(word.lemma_)
                    updatedict(word.lemma_,adverbs)
                elif word.pos_=='ADJ' and word.lemma_!='-PRON-':
                    listadjectives.append(word.lemma_)
                    updatedict(word.lemma_,adjectives)
            
            if len(listverbs)+len(listadverbs)+len(listadjectives)>0:
                new.write(' '.join(listadjectives) + ',' + ' '.join(listadverbs) + ',' + ' '.join(listverbs) + '\n')
                listverbs.clear()
                listadverbs.clear()
                listadjectives.clear()

        
## show results
print (str(emoji_counter.total_emoji) + ' comments used ' + str(emoji_counter.total_indiv_emoji) + ' emojis')

for emoji in emoji_counter.dict:
    if emoji_counter.dict[emoji]>0:
        print(emoji + str(emoji_counter.dict[emoji]))
        
    
        