
import csv
import os
from flask import Flask, Response, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/data', methods=['GET', 'POST'])
def data():

    if request.method == 'POST':
        f = request.files['csvfile']
        f.save( f.filename)
        df = pd.read_csv(f.filename)
        print(df)
        return process(df)
    return "None"
            
def process(df):

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
    output = df.to_csv(index=False)
    
    return Response(
        output ,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})


def stemmingWords(sentence):
    dict = {'monday': 'Mon' , 'tuesday' : 'Tue', 'wednesday': 'Wed','thursday': 'Thu',  'friday': 'Fri','saturday': 'Sat', 'sunday': 'Sun'  }
    return " ".join([dict.get(w,w) for w in sentence.replace(":"," : ").replace("["," ").replace("]"," ").replace(",","<br>").lower().split()])

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



if __name__ == "__main__":
    app.run(debug=True)