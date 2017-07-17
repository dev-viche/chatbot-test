#!/usr/bin/env python27
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 10:23:52 2017

@author: viche
"""

import json
import requests
import sys
from flask import request

class UIConnector_FBM():
    
    def __init__(self, webhook_token, client_token):
        self.FBMESSENGER_VERIFY_TOKEN = webhook_token
        self.FBMESSENGER_PAGETACCESS_TOKEN = client_token

    def webhook_verify(self, request):
        
        # if a webhook endpoint, it must echo back the 'hub.challenge' value
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if request.args.get("hub.verify_token") == self.FBMESSENGER_VERIFY_TOKEN:
                return request.args["hub.challenge"], 200
            return "FB Messenger webhook verification token mismatch", 403
        
        # else, return simple "hello world" for verification
        return 'Hello World!', 200
    
    def webhook_post(self, request):
        data = request.get_json()
        self.log(data)
        
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
    
                    if messaging_event.get("message"):  # someone sent us a message
    
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = "any thing" # messaging_event["message"]["text"]  # the message's text
    
                        self.webhook_respond(sender_id, "Vic loves Julia!")
    
                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass
    
                    if messaging_event.get("optin"):  # optin confirmation
                        pass
    
                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass
        
        return "ok", 200
    
        
    def webhook_respond(self, recipient_id, message_text):
        
        self.log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    
        params = {
            "access_token": self.FBMESSENGER_PAGETACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text": message_text,
                        "buttons":[
                            {
                                "type":"web_url",
                                "url":"https://petersapparel.parseapp.com",
                                "title":"Show Website"
                            },
                            {
                                "type":"postback",
                                "title":"Start Chatting",
                                "payload":"USER_DEFINED_PAYLOAD"
                            }
                        ]
                    }
                }    
                #"text": message_text
            }
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)
    
    def log(self, message):
        print(str(message))
        sys.stdout.flush()