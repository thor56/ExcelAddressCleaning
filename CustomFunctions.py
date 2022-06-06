import csv
import os
import string
from flask import Flask, Response, render_template, request
from flask_bootstrap import Bootstrap
from numpy import NaN

import pandas as pd




def process(df, filename1):

    # df = pd.read_csv('Before.csv')
    # df['Opening hours'] = df['Opening hours'].map(stemmingWords)
    # df['Pin'] = df['State'].map(separatelocality2)
    # df['State'] = df['State'].map(separatelocality1)
    df['Opening hours'] = df['Opening hours'].map(stemmingWords)
    df['Pin'] = df['State'].map(separatelocality2)
    df['State'] = df['State'].map(separatelocality1)
    df['Phone Number'] = df['Phone Number'].map(phonenum)
    df['Name, State,Pin'] = df['Name'] + ", " + df['State'] + ", " +  df['Pin'] 
    df['Location'] = df['Location'].map(location)
    print(df)
    df = df.sort_values('Pin')
    df2 = pd.DataFrame()
    df2.insert(0,"Name, State,Pin",df['Name, State,Pin'],True)
    df2.insert(1,"Phone Number",df['Phone Number'],True)
    df2.insert(2,"Location",df['Location'],True)
    df2.insert(3,"Full Address",df['Full Address'],True)
    df2.insert(4,"Opening hours",df['Opening hours'],True)
    print(df2)
   

    output = df2.to_csv(index=False)
    os.remove(filename1)
    return Response(
        output ,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename={}".format("after_" + filename1)})


def stemmingWords(sentence ):
    dict_ = {'monday': 'Mon' , 'tuesday' : 'Tue', 'wednesday': 'Wed','thursday': 'Thu',  'friday': 'Fri','saturday': 'Sat', 'sunday': 'Sun'  }
    if sentence == NaN or str(sentence) == "nan":
        return ""
    
    str3 = str(sentence)
    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)

    return " <br> ".join(l)


def separatelocality1(sentence):
    return sentence.replace(", ",",").split(",")[0]

def separatelocality2(sentence):
    
    lst = sentence.replace(", ",",").split(",")
    
    if len(lst) > 1:
        return sentence.replace(", ",",").split(",")[1]
    return ""

# (432) 758-2992
# <a href="tel:+1 432-758-2992" rel="nofollow">+1 432-758-2992</a>
def phonenum(sentence):
    sentences = str(sentence)
    num = sentences.replace("(","").replace(")","-").replace(" ","")
#     return "<a href=\"tel:+1 " + sentence.replace("(","").replace(")","-").replace(" ","") + "\" rel=\"nofollow\">+1 432-758-2992</a>"
    return "<a href=\"tel:+1 " + num + "\" rel=\"nofollow\">+1 " + num + "</a>"

# <a href="https://www.google.com/maps?cid=3184598461857161322" target="_blank" rel="nofollow">Get Directions</a>
def location(sentence):
    sentences = str(sentence)
    return "<a href=\"" + sentences + "\" target=\"_blank\" rel=\"nofollow\">Get Directions</a>"

