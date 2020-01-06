from __future__ import print_function

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth
import google_drive
from google_auth import build_credentials, get_user_info

# /index.py

import flask
from flask import Flask, request, jsonify, render_template, url_for
import os
import json

import pickle
import os.path

from flask import Flask, jsonify, render_template, request
from io import StringIO
import pandas as pd
import requests


import sheetsFunctions



app = flask.Blueprint('graphScrape', __name__)



def convertFormat(dfs):
    payload = []
    for df in dfs:
        each_df_payload = []
        columns = df.columns

        for i in range(len(df)):
            dictVal = {}
            for j in range(len(columns)):
                try: 
                    dictVal[str(columns[j])] = int(df[columns[j]][i])
                except:
                    dictVal[str(columns[j])] = str(df[columns[j]][i])
            each_df_payload.append(dictVal)
        payload.append({"columns" : list(columns), "data": each_df_payload})

    return payload


def scraper(link):
    print("scraping...", link)

    try:
        source = requests.get(link).text
        TESTDATA =  StringIO(source)
        df = pd.read_csv(TESTDATA, sep=",")

        if(len(df.columns) > 0 and len(df) > 0):
            print("VALID CSV FORMAT")
            return convertFormat([df])
        
    except:
        print("NOT CSV FORMAT")


    try:
        dfs = pd.read_html(link)
        return convertFormat(dfs)
    except:
        return "No Tables Found"




@app.route('/graphScrape')
def graphScrape():
    return render_template('graphScrape.html', someVal = "Hello World")


@app.route('/ScrapeData', methods=['GET'])
def ScrapeData():
    link = request.args.get("submitted_link")
    data = scraper(link)
    return jsonify(data)





# Sanity check route
@app.route('/readSheetPd', methods=['GET'])
def readSheetPandas():
    if google_auth.is_logged_in():
        print(request.url)
        value1 = request.args.get('sheet_id') #if key doesn't exist, returns None
        print("Value1: ", value1)
      
        functionName = "readSheet"

        credentials = build_credentials()

        googleInstance = sheetsFunctions.sheetsFunctions(credentials)
        items = googleInstance.readSheet(value1)
        # items = getattr(googleInstance, functionName)(*listVals)

        df = pd.DataFrame(items[1:], columns = items[0]) 

        payload = convertFormat([df])
        return jsonify(payload)
        # print(items)
        # return jsonify(items)
    else:
        return jsonify("log in please")

