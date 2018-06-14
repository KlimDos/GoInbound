from flask import Flask, request, make_response, Response
import os
import json
import pygsheets  # ------------------ the main module Gsheets
from slackclient import SlackClient  # access to slack API
import string  # to get an adc list
import re
import logging

# logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='mylog.log')

LOG = logging.getLogger(__name__)

LOG.info("===================================STARTING GOINBOUND SERVER=======================================")

try:
    f = open("/home/sasha/GoInbound/list_name", "r")
    strng = f.read()
    f.close()
except Exception as exc:
    exception = exc
    LOG.exception('Got error - %s', repr(exc))

# -----------wrap this up due to time o time request errors
gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
sh = gc.open('Support hours')
# wks = sh.worksheet(property='index', value='0')
wks = sh.worksheet(property='title', value=strng)
# wks = sh.worksheet(property='title', value='April 2 - April 6')
user_confirm = wks.get_values('A141', 'T142', include_empty=1, )
user_confirm_lunch = wks.get_values('A141', 'T141', include_empty=1, )
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

    # ======== whay is doing this function ========== #
    ptrn = re.compile(r'.*(\:(.*)\:).*')
    rplc = re.compile(r'\s+')
    orig_msg = form_json["original_message"]["attachments"][0]["text"]
    match = ptrn.match(rplc.sub(' ', orig_msg))
    if match: match = match.groups()[0]
    # print(match)
    # ======== whay is doing this function ========== #

    if user_who_clicked == form_json['callback_id']:
        # new_attach = form_json['original_message']['attachments'][0]['text'] + '\n User has conformed'
        new_attach = '<@' + form_json['callback_id'] + '> has confirmed ' + match
        color = "#008000"
        actions = []
        for row in user_confirm:
            i = 0
            i_list = list(string.ascii_uppercase)
            for cell in row:
                if cell[2:11] == user_who_clicked:
                    cell_to_write = i_list[i] + '142'  # =====!!!!!!!!!!!!!!!!!!!!!!!!!+++++++++
                    wks.update_cell(cell_to_write, 'confirmed')
                i += 1



    elif form_json['callback_id'] == user_who_clicked + 'lunch':
        new_attach = '<@' + user_who_clicked + '> enjoy your meal '
        color = "#D358F7"
        actions = []
        for row in user_confirm_lunch:
            i = 0
            i_list = list(string.ascii_uppercase)
            for cell in row:
                LOG.warning('*** lunch wrapper')
                if cell[2:11] == user_who_clicked:
                    cell_to_write = i_list[i] + '143'  # =====!!!!!!!!!!!!!!!!!!!!!!!!!+++++++++
                    wks.update_cell(cell_to_write, 'confirmed')
                i += 1


    else:
        new_attach = form_json['original_message']['attachments'][0][
                         'text'] + '\n' + '<@' + user_who_clicked + '> Will cover this hour.'
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


    LOG.info('Message: %s' % form_json)

    return make_response("", 200)

### curl -i -X POST -H "Content-Type: application/json" -d '{"action":"renew","password":"123"}' 'http://localhost:8091/refreshing'
@app.route('/refreshing', methods=['POST'])
def fo():
    content = request.get_json(silent=True)
    LOG.info('refreshing list_name')
    if content['password'] == "123":
        if content['action'] == "renew":
            try:
                f = open("/home/sasha/GoInbound/list_name", "r")
                strng = f.read()
                f.close()
                LOG.info('New List Name - %s', strng)
            except Exception as exc:
                exception = exc
                LOG.exception('Got error - %s', repr(exc))
        else:
            LOG.warning('Wrong Action')
    else:
        LOG.warning('Wrong Password')
    return 'OK'

 # ====================== #

@app.route('/shift', methods=['POST'])
def fo2():
    #content = request.get_json(silent=True)
    #content2 = json.loads(request.form["payload"])
    LOG.info('shift request')
    #LOG.warning(type(content2))

    #LOG.warning('Message', content)
    #return 'OK', type(content)
    return request.get_data()



##################################
@app.route('/post_strng', methods=['POST'])
def foo():
    if not request.json:
        dic = request.json
    print(request.json)
    print(type(dic))
    for key, key2 in dic.items():
        print(key, key2)

    # form_json2 = json.loads(request.form["payload2"])

    try:
        f = open("/home/sasha/GoInbound/list_name", "r")
        strng = f.read()
        f.close()
        LOG.info('List Name - %s', strng)
    except Exception as exc:
        exception = exc
        LOG.exception('Got error - %s', repr(exc))

    return json.dumps(request.json)

##################################






if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8091, debug=True)
    app.run(host='0.0.0.0', port=8090, debug=True)
