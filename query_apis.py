from __future__ import print_function

import functools
import json
import os

import flask

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth
import google_drive
from google_auth import build_credentials, get_user_info

# /index.py
from flask import Flask, request, jsonify, render_template, url_for
import os
import dialogflow
import requests
import json

import pickle
import os.path

import queryFunctions 


app = flask.Blueprint('query_apis', __name__)


@app.route('/queryApis')
def wee():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        user_name = user_info['given_name']
        return jsonify("hello")
    return 'Please log in before using.<br> <br><a href="http://localhost:8040/google/login">Yeet</a> '


# Sanity check route
@app.route('/WolframAlphaAPIs', methods=['GET'])
def QueryFunction():
    if google_auth.is_logged_in():
        print(request.url)
        query = request.args.get('query') #if key doesn't exist, returns None 

        print("Query: ", query)

# secret keys
        API_KEYS = [] 
        
        queryInstance = queryFunctions.queryFunctions(API_KEYS)
        stored_id, stored_json = queryInstance.wolframAlphaQuery( query )

        print("outside result: ", stored_json)

        # stored_dict = json.loads(stored_json)

        return stored_json
    else:
        return jsonify("log in please")


# Sanity check route
@app.route('/wikipediaQuery', methods=['GET'])
def wikipedia():
    if google_auth.is_logged_in():

        print(request.url)

        query = request.args.get('query') #if key doesn't exist, returns None KA45UE-AX7LU9E53L

        print("Query: ", query)

        API_KEYS = ['']
        
        queryInstance = queryFunctions.queryFunctions(API_KEYS)
        answer = queryInstance.search_wiki(keyword = query)

        print("outside result: ", answer)

        # stored_dict = json.loads(stored_json)

        return answer
    else:
        return jsonify("log in please")


