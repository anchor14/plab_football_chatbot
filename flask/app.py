from flask import Flask, request, Response, make_response, jsonify
# from flask import Flask, request, jsonify, render_template
import requests
import os
import dialogflow
import json
import csv
# from post import Post
import sqlite3

class Post:
    def __init__(self,data):
        self.location=data[0]
        self.sessions=data[1]


data=[]

def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}


def ReadCSV(file):
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            data.append(row)
        return data

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    return "Hello World!"

@app.route("/postJson", methods=['GET','POST'])
def postJson():
    # Save JSON data  as 2D list and give it to db module to handle

    return Response("We received something.")

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("webhook fxn touched")
    # return response
    return Response("something has come.")
# run Flask app

if __name__ == "__main__":
    app.run()
