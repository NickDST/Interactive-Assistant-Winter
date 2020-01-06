import functools
import json
import os

import flask

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth
import google_drive
import external_apis
import query_apis
import graphScrape

# /index.py
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json



app = flask.Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(google_auth.app)
app.register_blueprint(google_drive.app)
app.register_blueprint(external_apis.app)
app.register_blueprint(query_apis.app)
app.register_blueprint(graphScrape.app)



@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        user_name = user_info['given_name']
        return render_template('index.html', user_info = user_info)
        # return render_template('list.html', user_info = user_info)
        # return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return 'Please log in before using.<br> <br><a href="http://localhost:8040/google/login">Yeet</a> '


@app.route('/speech')
def reee():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        user_name = user_info['given_name']
        return render_template('speechTest.html', user_info = user_info)
    return 'Please log in before using.<br> <br><a href="http://localhost:8040/google/login">Yeet</a> '
    

@app.route('/bluebird')
def bluebird():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        user_name = user_info['given_name']
        return render_template('bluebird.html', user_info = user_info)
    return 'Please log in before using.<br> <br><a href="http://localhost:8040/google/login">Yeet</a> '


@app.route('/firestore')
def firestore():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        user_name = user_info['given_name']
        return render_template('firebase.html', user_info = user_info)
    return 'Please log in before using.<br> <br><a href="http://localhost:8040/google/login">Yeet</a> '

@app.route('/firebaseAuth')
def firebaseAuth():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        user_name = user_info['given_name']
        return render_template('firebaseAuth.html', user_info = user_info)
    return 'Please log in before using.<br> <br><a href="http://localhost:8040/google/login">Yeet</a> '



@app.route('/testVue')
def testVue():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        user_name = user_info['given_name']
        return render_template('testVue.html', user_info = user_info)
        # return render_template('list.html', user_info = user_info)
        # return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return 'Please log in before using.<br> <br><a href="http://localhost:8040/google/login">Yeet</a> '



# Sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
        return jsonify("yeet")













# run Flask app
if __name__ == "__main__":
    app.run()