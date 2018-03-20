from flask import Flask, request, make_response, Response
import os
import json
import pygsheets  # ------------------ the main module Gsheets
from slackclient import SlackClient  # access to slack API
import string  # to get an adc list

f = open("/home/sasha/GoInbound/list_name", "r")
strng = f.read()
f.close()

# -----------wrap this up due to time o time request errors
gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
sh = gc.open('Support hours')
# wks = sh.worksheet(property='index', value='0')
wks = sh.worksheet(property='title', value=strng)
user_confirm = wks.get_values('A100', 'J101', include_empty=1, )
# -debug- print (user_confirm[0])


# Getting a sys var
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# - set thes for security
# SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask webserver for incoming traffic from Slack
app = Flask(__name__)

@app.route("/", methods=["POST"])
def message_actions():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # add comments

    user_who_clicked = form_json['user']['id']
    if user_who_clicked == form_json['callback_id']:
       # new_attach = form_json['original_message']['attachments'][0]['text'] + '\n User has conformed'
        new_attach = '<@' + form_json['callback_id'] + '> has confirmed'
        color = "#008000"
        actions = []
        for row in user_confirm:
            i = 0
            i_list = list(string.ascii_uppercase)
            for cell in row:
                if cell[2:11] == user_who_clicked:
                    cell_to_write = i_list[i] + '101'
                    wks.update_cell(cell_to_write, 'confirmed')
                i += 1
    else:
        new_attach = form_json['original_message']['attachments'][0][
                         'text'] + '\n' + '<@' + user_who_clicked + '> I dont think its good idea.'
        color = "#800000"
        actions = [
            {
                "name": "confirm",
                "text": "Confirm",
                "type": "button",
                "value": "1"
            },
            {
                "name": "confirm",
                "text": "I can't",
                "style": "danger",
                "type": "button",
                "value": "war",
                "confirm": {
                    "title": "Are you sure?",
                    "text": "Would you prefer to notify your manager?",
                    "ok_text": "Yes",
                    "dismiss_text": "No"
                }
            }
        ]
    message_attachments = [
        {
            "text": new_attach,
            "color": color,
            "attachment_type": "default",
            "actions": actions,
            "callback_id": form_json['user']['id']
        }

    ]

    slack_client.api_call(
        "chat.update",
        channel=form_json["channel"]["id"],
        ts=form_json["message_ts"],
        text='',
        attachments=message_attachments
    )

    return make_response("", 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)
