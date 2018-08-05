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
from flask import Flask, request
from pre2_register import run


cgitb.enable()
form = cgi.FieldStorage()

name = eval(form.getvalue('name'))
age = eval(form.getvalue('age'))
duration = eval(form.getvalue('duration'))
day = eval(form.getvalue('day'))
month = eval(form.getvalue('month'))
balance = eval(form.getvalue('balance'))
campaign = eval(form.getvalue('campaign'))
pdays = eval(form.getvalue('pdays'))
previous = eval(form.getvalue('previous'))


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

# radio1_balance = eval(form.getvalue('radio1_balance'))
# radio2_balance = eval(form.getvalue('radio2_balance'))
# radio3_balance = eval(form.getvalue('radio3_balance'))
# radio4_balance= eval(form.getvalue('radio4_balance'))


radio1_hs = eval(form.getvalue('radio1_hs'))
radio2_hs = eval(form.getvalue('radio2_hs'))

radio1_loan = eval(form.getvalue('radio1_loan'))
radio2_loan = eval(form.getvalue('radio2_loan'))

radio1_def = eval(form.getvalue('radio1_def'))
radio2_def = eval(form.getvalue('radio2_def'))


# radio1_day = eval(form.getvalue('radio1_day'))
# radio2_day = eval(form.getvalue('radio2_day'))
# radio3_day = eval(form.getvalue('radio3_day'))
# radio4_day = eval(form.getvalue('radio4_day'))

# radio1_pdays = eval(form.getvalue('radio1_pdays'))
# radio2_pdays = eval(form.getvalue('radio2_pdays'))
# radio3_pdays = eval(form.getvalue('radio3_pdays'))
# radio4_pdays = eval(form.getvalue('radio4_pdays'))
# radio5_pdays = eval(form.getvalue('radio5_pdays'))

# radio1_previous = eval(form.getvalue('radio1_previous'))
# radio2_previous = eval(form.getvalue('radio2_previous'))
# radio3_previous = eval(form.getvalue('radio3_previous'))
# radio4_previous = eval(form.getvalue('radio4_previous'))

radio1_pout = eval(form.getvalue('radio1_pout'))
radio2_pout = eval(form.getvalue('radio2_pout'))
radio3_pout = eval(form.getvalue('radio3_pout'))
radio4_pout = eval(form.getvalue('radio4_pout'))

radio1_y = eval(form.getvalue('radio1_y'))
radio2_y = eval(form.getvalue('radio2_y'))
radio3_y = eval(form.getvalue('radio3_y'))


data = pd.read_csv('/Users/imeiliasantoso/web_graduate_project5/register_page/bank-full_input.csv')
l = len(data) + 1

#default


age = str(age)
duration = str(duration)
month = str(month)
campaign = str(campaign)
balance = str(balance)
day = str(day)
pdays = str(pdays)
previous = str(previous)

job = ""
marital = ""
education = ""
default = ""

housing = ""
loan = ""

poutcome =""
y =""

#job
if (radio1_job == 'Emplyoed'):
	job = "emplyoed"

if (radio2_job == 'Unemplyoed'):
	job = "unemplyoed"

if (radio2_job == 'Unknown'):
	job = "unknown"

#status
if (radio1_status == 'Married'):
	marital = "married"

if (radio2_status== 'Unmarried'):
	marital = "unmarried"

if (radio3_status == 'Unknown'):
	marital = "unknown"


#edu
if (radio1_edu == 'Primary'):
	education = "primary"

if (radio2_edu == 'Secondary'):
	education = "secondary"

if (radio3_edu == 'Teritory'):
	education = "teritory"

if (radio4_edu == 'Unknown'):
	education = "unknown"


# #Contact
if (radio1_contact == 'Telephone'):
	contact = "telephone"

if (radio2_contact == 'Cellular'):
	contact = "cellular"

if (radio3_contact == 'Unknown'):
	contact = "unknown"

# #balance
# if (radio1_balance == 'Low'):
# 	balance = "low"

# if (radio2_balance == 'Average'):
# 	balance = "average"

# if (radio3_balance == 'High'):
# 	balance = "high"

# if (radio4_balance == 'Very High'):
# 	balance = "veryhigh"

# #Housing
if (radio1_hs == 'Yes'):
	housing = "yes"

if (radio2_hs == 'No'):
	housing = "no"

#Loan
if (radio1_loan == 'Yes'):
	loan = "yes"

if (radio2_loan == 'No'):
	loan = "no"


#deafult
if (radio1_def == 'Yes'):
	default = "yes"

if (radio2_def == 'No'):
	default = "no"



# #Day
# if (radio1_day == '1st Week'):
# 	day = "1stweek"

# if (radio2_day == '2nd Week'):
# 	day = "2ndweek"

# if (radio3_day == '3rd Week'):
# 	day = "3rdweek"

# if (radio4_day == '4th Week'):
# 	day = "4thweek"



# #Previous day
# if (radio1_pdays == '1 month'):
# 	pdays = "1month"

# if (radio2_pdays == '1 month to 6 months'):
# 	pdays = "1monthto6months"

# if (radio3_pdays == '1 year to 2 years'):
# 	pdays = "1yearto2years"

# if (radio4_pdays == 'More than 2 years'):
# 	pdays = "morethan2years"

# if (radio5_pdays == 'Never'):
# 	pdays = "never"



#Previous hr
# if (radio1_previous == 'Low'):
# 	previous = "low"

# if (radio2_previous == 'Medium'):
# 	previous = "medium"

# if (radio3_previous == 'High'):
# 	previous = "high"

# if (radio4_previous == 'Never'):
# 	previous = "never"

#poutcome
if (radio1_pout == 'Success'):
	poutcome = "success"

if (radio2_pout == 'Failure'):
	poutcome = "failure"

if (radio3_pout == 'Other'):
	poutcome = "other"

if (radio4_pout == 'Unknown'):
	poutcome = "unknown"

#result
if (radio1_y == 'Yes'):
	y = "yes"

if (radio2_y == 'No'):
	y = "no"



df = pd.DataFrame(data)
#full
df1 = pd.DataFrame({'age':[age],'job':[job],'marital':[marital],'education':[education],'contact':[contact],
	'balance':[balance],'housing':[housing],'loan':[loan],'default':[default],'duration':[duration],'day':[day],
	'month':[month],'campaign':[campaign],'pdays':[pdays],'previous':[previous],'poutcome':[poutcome],'y':[y]})
# some
#df1 = pd.DataFrame({'duration':[duration],'poutcome':[poutcome], 'month':[month], 'age':[age],'previous':[previous],'y':[y]})
df2 = df.append(df1)
df2.to_csv('/Users/imeiliasantoso/web_graduate_project5/register_page/bank-full_input.csv', index = False)

accuracy = run()


Result_Accuracy = accuracy
Result_Accuracy_Original = "90.31811%"

print "Content-type:application/json\r\n\r\n"
print json.dumps({'status':'yes',
	'Result_Accuracy':json.dumps(Result_Accuracy),
	'Result_Accuracy_Original':json.dumps(Result_Accuracy_Original)
	})
print ""
#convert()
