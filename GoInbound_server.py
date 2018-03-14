from flask import Flask, request, make_response, Response
import os
import json
from slackclient import SlackClient

import pygsheets  # ------------------ the main module
import datetime  # ------------------ to operate current time

import string


gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
sh = gc.open('1st_sheet')
wks = sh.worksheet(property='index', value='0')
user_confirm = wks.get_values('A100', 'J101', include_empty=1, )
print (user_confirm[0])




# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
#SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask webserver for incoming traffic from Slack
app = Flask(__name__)

# Post a message to a channel, asking users if they want to play a game

attachments_json = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "games_list",
                "text": "Pick a game...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]

message_attachments = [
        {
            "text": "<@U7G7BTY9L> Your time to be online",
            "fallback": "You are unable to choose a game",
            "callback_id": "inbound_1488",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "confirmed",
                    "text": "Confirmed",
                    "type": "button",
                    "value": "1"
                },
                {
                    "name": "confirm",
                    "text": "im not going",
                    "style": "danger",
                    "type": "button",
                    "value": "war",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Wouldn't you prefer a ?",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                }
            ]
        }
    ]


#slack_client.api_call(
#  "chat.postMessage",
#  channel="C9NQKBY8N",
#  text="Shall we play a game?",
#  attachments=message_attachments
#)


@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    menu_options = {
        "options": [
            {
                "text": "Chess",
                "value": "chess"
            },
            {
                "text": "Global Thermonuclear War",
                "value": "war"
            }
        ]
    }

    return Response(json.dumps(menu_options), mimetype='application/json')


@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Check to see what the user's selection was and update the message
    #selection = form_json["actions"][0]["selected_options"][0]["value"]

    #if selection == "war":
    #    message_text = "The only winning move is not to play.\nHow about a nice game of chess?"
    #else:
    #    message_text = ":horse:"

    user_who_clicked = form_json['user']['id']
    if user_who_clicked == form_json['callback_id']:
        new_attach  = form_json['original_message']['attachments'][0]['text'] + '\n User has conformed timestamp'
        for row in user_confirm:
            #print('%s next round' % row)
            i=0
            i_list = list(string.ascii_uppercase)
            for cell in row:
                #print('%s WWW' % cell)
                if cell[2:11]==user_who_clicked:
                    print(user_confirm[1][i])
                    cell_to_write = i_list[i] + '101'
                    print(cell_to_write)
                    wks.update_cell(cell_to_write,'confirmed')
                i += 1
    else:
        new_attach = form_json['original_message']['attachments'][0]['text'] + '\n AnotherUser is clicking wher should have not'

    essage_attachments = [
        {
            "text": new_attach,
            # "fallback": "You are unable to choose a game",
            "color": "#3AA3E3",
            "attachment_type": "default",
        }

    ]

    response = slack_client.api_call(
      "chat.update",
      channel=form_json["channel"]["id"],
      ts=form_json["message_ts"],
      text='',
      attachments=essage_attachments
    )

    return make_response("", 200)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
