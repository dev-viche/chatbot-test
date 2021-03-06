#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 15:44:33 2017

@author: viche
"""

import json
import requests
import sys
from flask import request
from slackclient import SlackClient

class UIConnector_Slack():
    
    def __init__(self, webhook_token, client_token):
        self.SLACK_WEBHOOK_TOKEN = webhook_token
        self.SLACK_CLIENTACCESS_TOKEN = client_token
        
        # initialize the Slack Client
        self.slack_client = SlackClient(self.SLACK_CLIENTACCESS_TOKEN)

    def webhook_verify(self, request):

        return 'It Works!', 200
    
    def webhook_post(self, request):
        
        if request.form.get('token') == self.SLACK_WEBHOOK_TOKEN:
            channel = request.form.get('channel_name')
            username = request.form.get('user_name')
            text = request.form.get('text')
            inbound_message = 'slack:' + username + " in " + channel + " says: " + text
            
            self.log(inbound_message)
        
            self.webhook_respond("Vic loves Julia!", channel)
        
        return 'ok', 200
    
        
    def webhook_respond(self, message, channel):
        self.slack_client.api_call('chat.postMessage', channel=channel, text=message)
    
    def log(self, message):
        print(str(message))
        sys.stdout.flush()