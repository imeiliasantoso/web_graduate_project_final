#! /usr/bin/env python2

import weka.core.jvm as jvm
from weka.core.converters import Loader, Saver
from weka.classifiers import Classifier
from weka.classifiers import Evaluation
from weka.core.classes import Random
import weka.plot.graph as plot_graph

import re
import numpy as np
import string
import HTMLParser
import nltk
from nltk.stem.porter import PorterStemmer
import cgi, cgitb
import json
import sys, os
import pandas as pd
import csv as csv
# import openpyxl as xls
# import csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import tree
from flask import Flask, request
from pre2_predict2 import run
from pre3_predict2 import convert

cgitb.enable()
form = cgi.FieldStorage()



month = eval(form.getvalue('month'))
duration = eval(form.getvalue('duration'))
pdays = eval(form.getvalue('pdays'))
previous = eval(form.getvalue('previous'))
radio1_pout = eval(form.getvalue('radio1_pout'))
radio2_pout = eval(form.getvalue('radio2_pout'))
radio3_pout = eval(form.getvalue('radio3_pout'))
radio4_pout = eval(form.getvalue('radio4_pout'))

data3 = pd.read_csv('/Users/imeiliasantoso/web_graduate_project4/predict_page/predict2_header.csv')

month = str(month)
duration = str(duration)
pdays = str(pdays)
previous = str(previous)
poutcome = ""
#poutcome
if (radio1_pout == 'Success'):
	poutcome = "2"

if (radio2_pout == 'Failure'):
	poutcome = "-1"

if (radio3_pout == 'Other'):
	poutcome = "1"

if (radio4_pout == 'Unknown'):
	poutcome = "0"

#additional month
if (month == 'jan'):
	month = "1"

if (month == 'feb'):
	month = "2"

if (month == 'mar'):
	month = "3"

if (month == 'apr'):
	month = "4"




df = pd.DataFrame(data3)

df1 = pd.DataFrame({'month':[month],'duration':[duration],'pdays':[pdays],'previous':[previous],'poutcome':[poutcome]})

#df2 = df.append(df1)
df1.to_csv('/Users/imeiliasantoso/web_graduate_project4/predict_page/predict2_header.csv', index = False)

data1 = '/Users/imeiliasantoso/web_graduate_project4/predict_page/predict2_full.csv'
data2 = '/Users/imeiliasantoso/web_graduate_project4/predict_page/predict2_result.csv'
data4 = '/Users/imeiliasantoso/web_graduate_project4/predict_page/predict2_header.csv'


Result_Age = "test"



clf = tree.DecisionTreeClassifier()
with open(data1) as csvDataFile1:
    csvReader1 = csv.reader(csvDataFile1)
    Z = list(csvReader1)

with open(data2) as csvDataFile2:
    csvReader2 = csv.reader(csvDataFile2)
    ZZ= list(csvReader2)

clf = clf.fit(Z, ZZ)

with open(data4) as csvDataFile3:
 	csvDataFile3.next()
 	csvReader3 = csv.reader(csvDataFile3)
 	N = list(csvReader3)

prediction2= clf.predict(N)
prediction = str(prediction2).strip('[]')

if prediction == "'yes'":
	prediction = "subcribe"

if prediction == "'no'":
	prediction = "not subcribe"

Result_Name = prediction
Result_Accuracy = run()

print "Content-type:application/json\r\n\r\n"
print json.dumps({'status':'yes',
	'Result_Name':json.dumps(Result_Name),
	'Result_Accuracy':json.dumps(Result_Accuracy)
	})
print ""

#convert()




