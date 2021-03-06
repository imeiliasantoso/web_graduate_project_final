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
# from pre3 import convert


def run():
    jvm.start()
    load_csv = Loader("weka.core.converters.CSVLoader")
    data_csv = load_csv.load_file(
        "/Users/imeiliasantoso/web_graduate_project4/predict_page/predict_data.csv")

    saver = Saver("weka.core.converters.ArffSaver")
    saver.save_file(data_csv,
                    "/Users/imeiliasantoso/web_graduate_project4/predict_page/predict_data.arff")

    load_arff = Loader("weka.core.converters.ArffLoader")
    data_arff = load_arff.load_file(
        "/Users/imeiliasantoso/web_graduate_project4/predict_page/predict_data.arff")
    data_arff.class_is_last()

    global j48
    J48_class = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.25", "-M", "2"])
    J48_class.build_classifier(data_arff)
    evaluationj48 = Evaluation(data_arff)
    evaluationj48.crossvalidate_model(J48_class, data_arff , 10, Random(100))
    j48 = str(evaluationj48.percent_correct)
    jvm.stop()
    return j48