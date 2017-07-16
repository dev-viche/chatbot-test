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

import UIConnector_FBM, UIConnector_Slack



"""App Initialization"""
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    #return simple "hello world" for verification
    return 'Hello World!', 200

""" 1. Facebook Messenger Integration"""
# 1. initialize
FBM_WEBHOOK_TOKEN = os.environ["FBM_WEBHOOK_TOKEN"]
FBM_CLIENTACCESS_TOKEN = os.environ["FBM_CLIENTACCESS_TOKEN"]
uiconnector_fbm = UIConnector_FBM(FBM_WEBHOOK_TOKEN, FBM_CLIENTACCESS_TOKEN)

# 2. define the webhook methods
@app.route('/fbmessenger', methods=['GET'])
def fbm_webhook_get():
    uiconnector_fbm.webhook_verify(request)

@app.route('/fbmessenger', methods=['POST'])
def fbm_webhook_post():
    uiconnector_fbm.webhook_post(request)
    return "ok", 200
"""============================"""    

    
""" 2. Slack Integration """
SLACK_WEBHOOK_TOKEN = os.environ["SLACK_WEBHOOK_TOKEN"]
SLACK_CLIENTACCESS_TOKEN = os.environ["SLACK_CLIENTACCESS_TOKEN"]
uiconnector_slack = UIConnector_Slack(SLACK_WEBHOOK_TOKEN, SLACK_CLIENTACCESS_TOKEN)

@app.route('/slack', methods=['GET'])
def slack_webhook_get():
    uiconnector_slack.webhook_verify(request)
    
@app.route('/slack', methods=['POST'])
def slack_webhook_post():
    uiconnector_slack.webhook_post(request)
"""============================"""


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
