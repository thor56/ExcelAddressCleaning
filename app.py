
import csv
import os
import string
from flask import Flask, Response, render_template, request
from flask_bootstrap import Bootstrap
from numpy import NaN
from requests_html import HTMLSession
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

import pandas as pd
from CustomFunctions import *



app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")
    

@app.route('/data', methods=['GET', 'POST'])
def data():
    filename = ""
    if request.method == 'POST':
        f = request.files['csvfile']
        if f.filename == '':
            f = request.files['csvfile1']
        f.save( f.filename)
        filename = f.filename
        df = pd.read_csv(f.filename)
        #(df)
        return process(df, filename)
    return "None"

@app.route('/two', methods=['GET', 'POST'])
def two():
    return render_template("two.html")
    

@app.route('/datatwo', methods=['GET', 'POST'])
def datatwo():
    filename = ""
    if request.method == 'POST':
        f = request.files['csvfile']
        if f.filename == '':
            f = request.files['csvfile1']
        f.save( f.filename)
        filename = f.filename
        df = pd.read_csv(f.filename)
        #(df)
        return processtwo(df, filename)
    return "None"


@app.route('/anchor', methods=['GET', 'POST'])
def anchor():
    return render_template("anchor.html")
     
@app.route('/ScrapAnchor', methods=['GET', 'POST'])
def ScrapAnchor(): 

    url_ = request.form['urlTS'] 
    if url_ == "":
        return "None"
    # url="https://en.wikipedia.org/wiki/McDonald%27s#"

    session = HTMLSession()
    r = session.get(url_)

    b  = requests.get(url_)
    soup = BeautifulSoup(b.text, "lxml")

    dict = {'Anchor':[],
        'Link':[]
       }
  
    df = pd.DataFrame(dict)

    for link in soup.find_all('a'):
        if not link.find('img'):
            link_ = str(link.get('href')).lower()
            if link_ != "" and  "cite" not in link_ and "http" not in link_ and "//" not in link_:
                df.loc[len(df.index)] = [link.text,link.get('href')] 
    
    #(df)


    output = df.to_csv(index=False)
    return Response(
        output ,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename={}".format("Anchor_" + url_[30:] + ".csv")})
            


@app.route('/highlight', methods=['GET', 'POST'])
def Highlight():
    return render_template("highlight.html")
     
@app.route('/ScrapHighlight', methods=['GET', 'POST'])
def ScrapHighlight(): 

    url_ = request.form['urlTS']
    if url_ == "":
        return "None"
    # url="https://en.wikipedia.org/wiki/McDonald%27s#"

    session = HTMLSession()
    r = session.get(url_)

    b  = requests.get(url_)
    soup = BeautifulSoup(b.text, "lxml")

    dict = {'BoldText':[],
        'Link':[]
       }
  
    # df = pd.DataFrame(dict)
    bold_list = soup.find_all('b') + soup.find_all('strong')
    italic_list = soup.find_all('i') + soup.find_all('em')

    

    # output = df.to_csv(index=False)
    return render_template("highlightview.html", lis = bold_list, lis2 = italic_list)
            


if __name__ == "__main__":
    app.run(debug=True)