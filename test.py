import os                           #------------------ to get sys varybles
from slackclient import SlackClient #------------------ for slack API

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

sc.api_call("channels.list")


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



sc.api_call(
    'chat.postMessage',
     channel='trt',
     as_user=1,
     username='Sashooook',
     text=':smile:',
     attachments=message_attachments,
     reply_broadcast=True
)

#intro_msg  = json.dumps([{"text":"Choose an action","fallback":"You are unable to choose an option","callback_id":"lunch_intro","color":"#3AA3E3","attachment_type":"default","actions":[{"name":"enroll","text":"Enroll","type":"button","value":"enroll"},{"name":"leave","text":"Leave","type":"button","value":"leave"}]}])

#sc.api_call("chat.postMessage", channel=channel, text="What would you like to do?", attachments=intro_msg, as_user=True)