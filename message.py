import os
from flask import Flask, request, make_response, Response
from slackclient import SlackClient
import json

# Your app's Slack bot user token
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient(SLACK_API_TOKEN)

# Flask webserver for incoming traffic from Slack
app = Flask(__name__)


