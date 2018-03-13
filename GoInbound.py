import os  # ------------------ to get sys var
from slackclient import SlackClient  # ------------------ for slack API
import pygsheets  # ------------------ the main module
import datetime  # ------------------ to operate current time

######################################################################
# autorizing onto Google sheet API
gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
# select the sheet
sh = gc.open('1st_sheet')
# select the worksheet
wks = sh.worksheet(property='index', value='0')
######################################################################
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)
######################################################################
# gathering current data from the instance
current_min = datetime.datetime.now().strftime('%M')
current_hour = datetime.datetime.now().strftime('%H')
current_weekday = int(datetime.datetime.now().strftime('%u'))
######################################################################
# current_weekday = 1  # use it for trubleshuting integer
current_hour = '14' # use it for trubleshuting
######################################################################
# dont know why buy depend of the day we will get specific work hours
current_matrix = 0
if current_weekday == 1:
    current_matrix = wks.get_values('A4', 'I21', include_empty=0, )
elif current_weekday == 2:
    current_matrix = wks.get_values('A24', 'I37', include_empty=0, )
elif current_weekday == 3:
    current_matrix = wks.get_values('A40', 'I53', include_empty=0, )
elif current_weekday == 4:
    current_matrix = wks.get_values('A56', 'I70', include_empty=0, )
elif current_weekday == 5:
    current_matrix = wks.get_values('A74', 'I87', include_empty=0, )
elif current_weekday == 6 or current_weekday == 7:
    exit()

# print(*current_matrix)
current_matrix_without_empty_entries = [elem for elem in current_matrix if len(elem) > 1]
print(*current_matrix_without_empty_entries)

user_list = wks.get_values('A100', 'I100', include_empty=0, )

user_confirm = wks.get_values('A101', 'J101', include_empty=1, )
print (user_confirm)
if current_min == '00':
    wks.clear('A101', 'I101')

for row in current_matrix_without_empty_entries:
    print(row[0])
    if row[0].split('h')[0] == current_hour:
        i = 0
        for cell in row:
            # print(cell)
            if cell == 'Phones' and user_confirm[0][i]!='confirmed':
                msg = user_list[0][i] +" it's "+ row[0] + '.\n' + current_matrix_without_empty_entries[0][i] + ' thats your hour! Go inbound plse :smile:'
          #      print(user_list[0][i])
              #  user_id = user_list[0][i][2:10]
              #  print(user_id)
                message_attachments = [
                    {
                        "text": msg,
                        # "fallback": "You are unable to choose a game",
                        "callback_id": user_list[0][i][2:11],
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
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
                    }
                ]
                print(msg)
                slack_client.api_call(
                    "chat.postMessage",
                    channel="C9NQKBY8N",
                    text='',
                    attachments=message_attachments
                )
            i += 1
