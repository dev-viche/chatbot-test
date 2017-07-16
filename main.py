#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 14:31:34 2017

@author: viche
"""

import os
import sys
import json

from flask import Flask, request, Response

import requests
from slackclient import SlackClient

from uiconnector_fbm import UIConnector_FBM
from uiconnector_slack import UIConnector_Slack



"""App Initialization"""
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    #return simple "hello world" for verification
    return 'Hello World!', 200

""" 1. Facebook Messenger Integration"""
# 1. initialize
FBMESSENGER_VERIFY_TOKEN = os.environ["FBMESSENGER_VERIFY_TOKEN"]
FBMESSENGER_PAGEACCESS_TOKEN = os.environ["FBMESSENGER_PAGEACCESS_TOKEN"]
fbm_connector = UIConnector_FBM(FBMESSENGER_VERIFY_TOKEN, FBMESSENGER_PAGEACCESS_TOKEN)

# 2. define the webhook methods
@app.route('/fbmessenger', methods=['GET'])
def fbm_webhook_get():
    return fbm_connector.webhook_verify(request)

@app.route('/fbmessenger', methods=['POST'])
def fbm_webhook_post():
    return fbm_connector.webhook_post(request)
    
"""============================"""    

    
""" 2. Slack Integration """
SLACK_WEBHOOK_TOKEN = os.environ["SLACK_WEBHOOK_TOKEN"]
SLACK_CLIENTACCESS_TOKEN = os.environ["SLACK_CLIENTACCESS_TOKEN"]
slack_connector = UIConnector_Slack(SLACK_WEBHOOK_TOKEN, SLACK_CLIENTACCESS_TOKEN)

@app.route('/slack', methods=['GET'])
def slack_webhook_get():
    return slack_connector.webhook_verify(request)
    
@app.route('/slack', methods=['POST'])
def slack_webhook_post():
    return slack_connector.webhook_post(request)
"""============================"""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
