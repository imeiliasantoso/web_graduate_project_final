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
from pre2_predict import run


cgitb.enable()
form = cgi.FieldStorage()

age = eval(form.getvalue('age'))
balance = eval(form.getvalue('balance'))
radio1_job = eval(form.getvalue('radio1_job'))
radio2_job = eval(form.getvalue('radio2_job'))
radio3_job = eval(form.getvalue('radio3_job'))
radio1_status = eval(form.getvalue('radio1_status'))
radio2_status = eval(form.getvalue('radio2_status'))
radio3_status = eval(form.getvalue('radio3_status'))
radio1_edu = eval(form.getvalue('radio1_edu'))
radio2_edu = eval(form.getvalue('radio2_edu'))
radio3_edu = eval(form.getvalue('radio3_edu'))
radio4_edu = eval(form.getvalue('radio4_edu'))
radio1_contact = eval(form.getvalue('radio1_contact'))
radio2_contact = eval(form.getvalue('radio2_contact'))
radio3_contact = eval(form.getvalue('radio3_contact'))
radio1_hs = eval(form.getvalue('radio1_hs'))
radio2_hs = eval(form.getvalue('radio2_hs'))
radio1_loan = eval(form.getvalue('radio1_loan'))
radio2_loan = eval(form.getvalue('radio2_loan'))


data3 = pd.read_csv('/Users/imeiliasantoso/web_graduate_project4/predict_page/predict_header.csv')

age = str(age)
balance = str(balance)
job = ""
marital = ""
education = ""
housing = ""
contact=""
loan = ""


#job
if (radio1_job == 'Emplyoed'):
	job = "1"

if (radio2_job == 'Unemplyoed'):
	job = "-1"

if (radio2_job == 'Unknown'):
	job = "0"

#status
if (radio1_status == 'Married'):
	marital = "1"

if (radio2_status== 'Unmarried'):
	marital = "-1"

if (radio3_status == 'Unknown'):
	marital = "0"


#edu
if (radio1_edu == 'Primary'):
	education = "1"

if (radio2_edu == 'Secondary'):
	education = "2"

if (radio3_edu == 'Teritory'):
	education = "3"

if (radio4_edu == 'Unknown'):
	education = "0"


# #Contact
if (radio1_contact == 'Telephone'):
	contact = "1"

if (radio2_contact == 'Cellular'):
	contact = "2"

if (radio3_contact == 'Unknown'):
	contact = "0"


# #Housing
if (radio1_hs == 'Yes'):
	housing = "1"

if (radio2_hs == 'No'):
	housing = "0"

#Loan
if (radio1_loan == 'Yes'):
	loan = "1"

if (radio2_loan == 'No'):
	loan = "0"






df = pd.DataFrame(data3)

df1 = pd.DataFrame({'age':[age],'job':[job],'marital':[marital],'education':[education],'contact':[contact],
	'balance':[balance],'housing':[housing],'loan':[loan]})

#df2 = df.append(df1)
df1.to_csv('/Users/imeiliasantoso/web_graduate_project4/predict_page/predict_header.csv', index = False)

data1 = '/Users/imeiliasantoso/web_graduate_project4/predict_page/predict_full.csv'
data2 = '/Users/imeiliasantoso/web_graduate_project4/predict_page/predict_result.csv'
data4 = '/Users/imeiliasantoso/web_graduate_project4/predict_page/predict_header.csv'


Result_Age = ""


clf = tree.DecisionTreeClassifier()
with open(data1) as csvDataFile1:
    csvReader = csv.reader(csvDataFile1)
    Z = list(csvReader)

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







