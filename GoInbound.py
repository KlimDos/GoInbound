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
current_hour = datetime.datetime.now().strftime('%H')
current_weekday = int(datetime.datetime.now().strftime('%u'))
######################################################################
# current_weekday = 1  # use it for trubleshuting integer
# current_hour = '16' # use it for trubleshuting
######################################################################
# dont know why buy depend of the day we will get specific work hours
current_matrix = 0
if current_weekday == 1:
    current_matrix = wks.get_values('A4', 'H21', include_empty=0, )
elif current_weekday == 2:
    current_matrix = wks.get_values('A24', 'H37', include_empty=0, )
elif current_weekday == 3:
    current_matrix = wks.get_values('A40', 'H53', include_empty=0, )
elif current_weekday == 4:
    current_matrix = wks.get_values('A56', 'H70', include_empty=0, )
elif current_weekday == 5:
    current_matrix = wks.get_values('A74', 'H87', include_empty=0, )
elif current_weekday == 6 or current_weekday == 7:
    exit()

# print(*current_matrix)
current_matrix_without_empty_entries = [elem for elem in current_matrix if len(elem) > 1]
print(*current_matrix_without_empty_entries)

for row in current_matrix_without_empty_entries:
    print(row[0])
    if row[0].split('h')[0] == current_hour:
        i = 0
        for cell in row:
            # print(cell)
            if cell == 'Phones':
                msg = row[0] + ' - ' + current_matrix_without_empty_entries[0][
                    i] + ' thats your hour! Go inbound plse :smile: <@U7G7BTY9L>'
                message_attachments = [
                    {
                        "text": msg,
                        # "fallback": "You are unable to choose a game",
                        "callback_id": "inbound_1488",
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
