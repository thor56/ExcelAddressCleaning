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

def processtwo(df, filename1):

    # df = pd.read_csv('Before.csv')
    # df['Opening hours'] = df['Opening hours'].map(stemmingWords)
    # df['Pin'] = df['State'].map(separatelocality2)
    # df['State'] = df['State'].map(separatelocality1)
    
    df['Phone'] = df['Phone'].map(phonenum)
    df['Review URL'] = df['Review URL'].map(reviews)    
    df['Google Maps URL'] = df['Google Maps URL'].map(googleMapsUrl)    
    df['Monday'] = df['Opening hours'].map(mondayCol)
    df['Tuesday'] = df['Opening hours'].map(tuesdayCol)
    df['Wednesday'] = df['Opening hours'].map(wednesdayCol)
    df['Thursday'] = df['Opening hours'].map(thursdayCol)
    df['Friday'] = df['Opening hours'].map(fridayCol)
    df['Saturday'] = df['Opening hours'].map(saturdayCol)
    df['Sunday'] = df['Opening hours'].map(sundayCol)
    df['iFrame'] = "<iframe src=\"https://maps.google.com/maps?q=" + df['Name'] + df['Fulladdress'].map(addrForIframe) + "&output=embed\" width=\"100%\" height=\"450\" frameborder=\"0\" style=\"border:0\" allowfullscreen></iframe>"
    df['Status'] = "draft"
    df['Interlink2'] = ""
    df['Interlink1'] = ""
    df['Category'] = ""
    df['Tag1'] = ""
    df['Tag2'] = ""
    df['None'] = "None"
    df['Block'] = "<!-- wp:block {\"ref\":2442} /-->"
    



    
    print(df)
    # df = df.sort_values('Pin')

    df2 = pd.DataFrame()
    df2.insert(0,"None",df['None'],True)
    df2.insert(1,"Name",df['Name'],True)
    df2.insert(2,"Full Address",df['Fulladdress'],True)
    df2.insert(3,"Street",df['Street'],True)
    df2.insert(4,"Categories",df['Categories'],True)
    df2.insert(5,"Phone",df['Phone'],True)
    df2.insert(6,"Average Rating",df['Average Rating'],True)
    df2.insert(7,"Review URL",df['Review URL'],True)
    df2.insert(8,"Google Maps URL",df['Google Maps URL'],True)
    df2.insert(9,"Latitude",df['Latitude'],True)
    df2.insert(10,"Longitude",df['Longitude'],True)
    df2.insert(11,"Monday",df['Monday'],True)
    df2.insert(12,"Tuesday",df['Tuesday'],True)
    df2.insert(13,"Wednesday",df['Wednesday'],True)
    df2.insert(14,"Thursday",df['Thursday'],True)
    df2.insert(15,"Friday",df['Friday'],True)
    df2.insert(16,"Saturday",df['Saturday'],True)
    df2.insert(17,"Sunday",df['Sunday'],True)
    df2.insert(18,"iFrame",df['iFrame'],True)
    df2.insert(19,"Status",df['Status'],True)
    df2.insert(20,"Interlink1",df['Interlink1'],True)
    df2.insert(21,"Interlink2",df['Interlink2'],True)
    df2.insert(22,"Category",df['Category'],True)
    df2.insert(23,"Tag1",df['Tag1'],True)
    df2.insert(24,"Tag2",df['Tag2'],True)
    df2.insert(25,"Block",df['Block'],True)
    if 'Review Count' in df.columns:
        df2.insert(26,"Review Count",df['Review Count'],True)


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

def mondayCol(sentence ):
    

    dict_ = {'monday': 'Monday' , 'tuesday' : 'Tuesday', 'wednesday': 'Wednesday','thursday': 'Thursday',  'friday': 'Friday','saturday': 'Saturday', 'sunday': 'Sunday'  }
    if sentence == NaN or str(sentence) == "nan" or str(sentence) == "":
        return ""
    
    str3 = str(sentence) 


    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    print(lst2)
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x
    
    print(dict2['Mon'])
    # Monday : 6 : 30am-10pm
    if (dict2['Mon'].count(":") > 1):
        return dict2['Mon'].split(":",1)[1]

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)
            

    return dict2["Mon"]

def mondayCol(sentence ):
    
    dict_ = {'monday': 'Monday' , 'tuesday' : 'Tuesday', 'wednesday': 'Wednesday','thursday': 'Thursday',  'friday': 'Friday','saturday': 'Saturday', 'sunday': 'Sunday'  }
    if sentence == NaN or str(sentence) == "nan" or str(sentence) == "":
        return ""
    
    str3 = str(sentence)
   
   

    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    print(lst2)
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x
    
    print(dict2['Mon'])

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)
            
    if str3.count(":") > 7:
        return dict2["Mon"].split(":",1)[1].replace(" : ",":")


    return dict2["Mon"].split(":")[1]

def tuesdayCol(sentence ):
    
    dict_ = {'monday': 'Monday' , 'tuesday' : 'Tuesday', 'wednesday': 'Wednesday','thursday': 'Thursday',  'friday': 'Friday','saturday': 'Saturday', 'sunday': 'Sunday'  }
    if sentence == NaN or str(sentence) == "nan" or str(sentence) == "":
        return ""
    
    str3 = str(sentence)
    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    print(lst2)
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x
    
    print(dict2['Mon'])

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)

    if str3.count(":") > 7:
            return dict2["Tue"].split(":",1)[1].replace(" : ",":")


    return dict2["Tue"].split(":")[1]

def wednesdayCol(sentence ):
    
    dict_ = {'monday': 'Monday' , 'tuesday' : 'Tuesday', 'wednesday': 'Wednesday','thursday': 'Thursday',  'friday': 'Friday','saturday': 'Saturday', 'sunday': 'Sunday'  }
    if sentence == NaN or str(sentence) == "nan" or str(sentence) == "":
        return ""
    
    str3 = str(sentence)
    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    print(lst2)
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x
    
    print(dict2['Mon'])

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)
            
    if str3.count(":") > 7:
        return dict2["Wed"].split(":",1)[1].replace(" : ",":")

    return dict2["Wed"].split(":")[1]

def thursdayCol(sentence ):
    
    dict_ = {'monday': 'Monday' , 'tuesday' : 'Tuesday', 'wednesday': 'Wednesday','thursday': 'Thursday',  'friday': 'Friday','saturday': 'Saturday', 'sunday': 'Sunday'  }
    if sentence == NaN or str(sentence) == "nan" or str(sentence) == "":
        return ""
    
    str3 = str(sentence)
    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    print(lst2)
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x
    
    print(dict2['Mon'])

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)
            
    if str3.count(":") > 7:
        return dict2["Thu"].split(":",1)[1].replace(" : ",":")

    return dict2["Thu"].split(":")[1]

def fridayCol(sentence ):
    
    dict_ = {'monday': 'Monday' , 'tuesday' : 'Tuesday', 'wednesday': 'Wednesday','thursday': 'Thursday',  'friday': 'Friday','saturday': 'Saturday', 'sunday': 'Sunday'  }
    if sentence == NaN or str(sentence) == "nan" or str(sentence) == "":
        return ""
    
    str3 = str(sentence)
    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    print(lst2)
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x
    
    print(dict2['Mon'])

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)
            
    if str3.count(":") > 7:
        return dict2["Fri"].split(":",1)[1].replace(" : ",":")

    return dict2["Fri"].split(":")[1]

def saturdayCol(sentence ):
    
    dict_ = {'monday': 'Monday' , 'tuesday' : 'Tuesday', 'wednesday': 'Wednesday','thursday': 'Thursday',  'friday': 'Friday','saturday': 'Saturday', 'sunday': 'Sunday'  }
    if sentence == NaN or str(sentence) == "nan" or str(sentence) == "":
        return ""
    
    str3 = str(sentence)
    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    print(lst2)
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x
    
    print(dict2['Mon'])

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)
            
    if str3.count(":") > 7:
        return dict2["Sat"].split(":",1)[1].replace(" : ",":")

    return dict2["Sat"].split(":")[1]

def sundayCol(sentence ):
    
    dict_ = {'monday': 'Monday' , 'tuesday' : 'Tuesday', 'wednesday': 'Wednesday','thursday': 'Thursday',  'friday': 'Friday','saturday': 'Saturday', 'sunday': 'Sunday'  }
    if sentence == NaN or str(sentence) == "nan" or str(sentence) == "":
        return ""
    
    str3 = str(sentence)
    str2 =  " ".join([dict_.get(w,w) for w in str3.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])
    lst2 = str2.split(" <br> ")
    print(lst2)
    dict2 = dict()
    for x in lst2:
        dict2[x[:3]] = x
    
    print(dict2['Mon'])

    l = [] 
    for x in dict_: 
        try:
            l.append(dict2[dict_[x]])
        except:
            print(dict2)
            
    if str3.count(":") > 7:
        return dict2["Sun"].split(":",1)[1].replace(" : ",":")

    return dict2["Sun"].split(":")[1]

def separatelocality1(sentence):
    return str(sentence).replace(", ",",").split(",")[0]

def separatelocality2(sentence):
    
    lst = str(sentence).replace(", ",",").split(",")
    
    if len(lst) > 1:
        return str(sentence).replace(", ",",").split(",")[1]
    return ""

# (432) 758-2992
# <a href="tel:+1 432-758-2992" rel="nofollow">+1 432-758-2992</a>
def phonenum(sentence):
    sentences = str(sentence)
    num = sentences.replace("(","").replace(")","-").replace(" ","")
#     return "<a href=\"tel:+1 " + sentence.replace("(","").replace(")","-").replace(" ","") + "\" rel=\"nofollow\">+1 432-758-2992</a>"
    return "<a href=\"tel:+1 " + num + "\" rel=\"nofollow\">+1 " + num + "</a>"

def addrForIframe(sentence):
    sentences = str(sentence)
    return "+" + sentences.replace(" ","+")

# <a href="https://www.google.com/maps?cid=3184598461857161322" target="_blank" rel="nofollow">Get Directions</a>
def location(sentence):
    sentences = str(sentence)
    return "<a href=\"" + sentences + "\" target=\"_blank\" rel=\"nofollow\">Get Directions</a>"

def reviews(sentence):
    sentences = str(sentence)
    return "<a href=\"" + sentences + "\" target=\"_blank\" rel=\"nofollow\">Reviews on Google</a>"

def googleMapsUrl(sentence):
    sentences = str(sentence)
    return "<a href=\"" + sentences + "\" target=\"_blank\" rel=\"nofollow\">Get Directions</a>"

