# -*- coding: utf-8 -*-
"""
Created on Thu May  5 19:48:17 2022

@author: jonrb
"""

import nltk
from nltk.stem.wordnet import WordNetLemmatizer as WNL
from nltk.corpus import wordnet as wn
import pandas as pd
from wordsegment import load, segment

"""
This function imports the csv and identifies the column titles. It takes the values from the summary column and turns it into a string
then it generates a word, casual, and sentence token from this string
"""


class Category:
    def __init__(self, category):
        self.category = category
        self.tasks = []

    def __str__(self): # prints the number and suit of the card when called
        return f"{self.category}"

class Task:
    def __init__(self, task):
        self.task = task
        self.inputs = []
        self.outputs = []
        self.in_count = 0
        self.out_count = 0

    def __str__(self): # prints the number and suit of the card when called
        return f"{self.task}"

class Word:
    def __init__(self,word):
        self.word = word
        self.synonyms = []

class Process:
    def __init__(self,process):
        self.process = process
        self.inputs = []
        self.outputs = []
        self.categories = []
        self.tasks = []
        self.input_percentage = []
        self.output_percentage = []
        
    def __str__(self): # prints the number and suit of the card when called
        return f"{self.process}"


def open_file(file):
    line_list = []
    with open(file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            else:
                line = line.strip("\n")
                line_list.append(line.split(','))
    # print(line_list)
    return line_list
  
def process(lines):
    processes = []
    process_list = []
    for i in lines:
        processes.append(i[2])
    
    processes = list(set(processes))
    
    for i in processes:
        P = Process(i)
        process_list.append(P)
    return process_list
 
def category(lines):
    categories = []
    category_list = []
    for i in lines:
        categories.append(i[1])
 
    categories = list(set(categories))
    for i in categories:
        C = Category(i)
        category_list.append(C)
    return category_list

def tasks(lines):
    tasks = []
    task_list = []
    for i in lines:
        tasks.append(i[0])
    for i in tasks:
        T = Task(i)
        task_list.append(T)
    task_list = list(set(task_list))
    return task_list

def inputs(lines):
    inputs = []
    for i in lines:
        inputs.append([i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
    for i in inputs:
        for j in range(len(i)-1,0,-1):
            if i[j] == '':
                i.pop(j)
            else:
                continue
    return inputs

def outputs(lines):
    outputs = []
    for i in lines:
        outputs.append([i[20],i[21],i[22],i[23],i[24],i[25],i[26],i[27],i[28],i[29]])
    for i in outputs:
        for j in range(len(i)-1,0,-1):
            if i[j] == '':
                i.pop(j)
            else:
                continue
    return outputs

def lemmize(words):
    word_list = 0
    lemmize = []
    for i in range(len(words)):
        if word_list == 0:
            word_list = words[i]
        else:
            word_list = word_list + ' ' + words[i]
    wtoken = nltk.word_tokenize(word_list)
    for f in wtoken:
        lemmize.append(WNL().lemmatize(f, 'v'))
    return lemmize

def synonyms(word):
    # print(word)
    synonyms = wn.synsets(word)
    return synonyms

 

if __name__ == '__main__':
    
    file = 'Project Management Inputs Outputs and Tasks.csv'
    train = 'file_names.csv'
    opened = open_file(file)
    open_train = open_file(train)
    training = []
    for i in open_train:
        for j in i:
            x = j.split('_',5)
            x = x[-1]
            x = x.split('.')
            x = x[0]
            training.append(x)
    training = sorted(training)
    # print(training)
    lines = []
    for i in opened:
        line = []
        for j in i:
            if j =='\n':
                continue
            else:
                line.append(j)
        lines.append(line)
    processes = process(lines)
    categories = category(lines)
    tasks = tasks(lines)
    inputs = inputs(lines)
    outputs = outputs(lines)
   
    for b,i in enumerate(lines):
        for j in categories:
            if i[1] == j.category:
                j.tasks.append(i[0])
        for a,j in enumerate(tasks):
            if i[0] == j.task:
                j.inputs = lemmize(inputs[a])
                j.outputs = lemmize(outputs[a])
        for j in processes:
            if i[2] == j.process:
                for k in categories:
                    if i[1] == k.category:
                        j.categories.append(k)
                j.tasks.append(i[0])
                j.inputs.append(lemmize(inputs[b]))
                j.outputs.append(lemmize(outputs[b]))
            
    synonym = []

    for line in inputs:    
        for word in line:
            synonym.append(synonyms(word))
            
    for line in outputs:
        for word in line:
            synonym.append(synonyms(word))
    
    train_syn = []
    for line in training:
        for word in line:
            train_syn.append(synonyms(word))
    
    similarities = []    
    s_one = []
    s_two = []
    for syn in synonym:
        for s in syn:
            s_one.append(s)
            print(s_one)
    print(s_one)
    for train in train_syn:
        for t in train:
            s_two.append(t)
    
    for s in s_one:
        for t in s_two:
            similarities.append(s.wup_similarity(t))
    print(similarities)                   
                