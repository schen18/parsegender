#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 09:36:51 2017

@author: stechen1
"""
import csv
import random
from processtext import *

startyear=1940
endyear=2000

malenames={}
femalenames={}

def countpeople(input):
    malecount=0
    femalecount=0
    seqflag=0
    mprior=0
    fprior=0
    processinput=input.lower()
    processinput=cleanemoji(processinput)
    processinput=cleanstring(processinput)
    wordlist=processinput.split(' ') #[0:-1] skip last word
    for word in wordlist:
        if seqflag==0:
            if namegender(word)=='M':
                seqflag+=1
                mprior=1
                fprior=0
            elif namegender(word)=='F':
                seqflag+=1
                fprior=1
                mprior=0
            else:
                mprior=0
                fprior=0
                
        elif seqflag==1:
            if mprior==1:
                malecount+=1
            elif fprior==1:
                femalecount+=1
                
            seqflag=0
            mprior=0
            fprior=0
            
    return [malecount,femalecount] 

def updatenames(inputname,gender,frequency):
    name=cleanreps(inputname).lower()
    if gender=='M':
        if name in malenames:
            namefrequency=malenames[name]
            malenames[name]=frequency+namefrequency
        else:
            malenames[name]=frequency
        
    elif gender=='F':
        if name in femalenames:
            namefrequency=femalenames[name]
            femalenames[name]=frequency+namefrequency
        else:
            femalenames[name]=frequency
        
def namegender(inputname):
    name=cleanreps(inputname).lower()
    gender=''
    
    malefreq=0    
    if name in malenames:
        malefreq=malenames[name]

    femalefreq=0
    if name in femalenames:
        femalefreq=femalenames[name]
        
    if malefreq+femalefreq==0:
        gender='X'
    else:
        if malefreq==0:
            gender='F'
        elif femalefreq==0:
            gender='M'
        elif malefreq>femalefreq:
            if malefreq/femalefreq>=2:
                gender='M'
            else:
                gender=random.choice('MFM')
        elif femalefreq>malefreq:
            if femalefreq/malefreq>=2:
                gender='F'
            else:
                gender=random.choice('FMF')
        else:
            gender='A'
            
    return gender

def initnames():
    for year in range(startyear,endyear):
        with open('namedata/yob' + str(2000) + '.txt') as yob:
            reader=csv.reader(yob, delimiter=',')
            for row in reader:
                updatenames(row[0],row[1],int(row[2]))


