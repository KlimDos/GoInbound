import os  # ------------------ to get sys var
import logging
from slackclient import SlackClient  # ------------------ for slack API
import pygsheets  # ------------------ the main module
import datetime  # ------------------ to operate current time

LOG = logging.getLogger(__name__)


def retry(fn):
    def wrapped(*args, **kwargs):
        while True:
            result, exception = None, None
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                exception = exc
                LOG.exception('Got error - %s', repr(exc))

            if exception is None:
                return result

    return wrapped


#####################################################################
# "G7GMUN1RA" "support_smolensk" - private
# "C7HAE7FEG" "ax-phone_schedule"
# "C9NQKBY8N" "test_aalimov"
#
Chanel_to_post = "C9NQKBY8N"

# User list
# Sveta - <@U7EAWJGBB>
# Victor - <@U7F8LKMK4>
# Alex A. - <@U7FAV8USY>
# Pavel - <@U9N7VNTT4>
# Sasha - <@U7G7BTY9L>
# Alex L. - <@U80KQBF27>
# Artur - <@U94TGT8J3>
# Yette - <@U7ERL2NRJ>
# Marc - <@U7F14B457>
# Matt - <@U7E4QJ8C8>
# Kathlyn - <@U7FLHETDL>
# Jeff - <@U7E5A6BH6>
# Daniel - <@U7E4RCW1E>
# BQ - <@U7E4UNCV6>
# Dave - <@U7E4Q1ZTJ>
# John - <@U7FLGHQKG>
######################################################################
# gathering current data from the instance
current_min = datetime.datetime.now().strftime('%M')
current_hour = datetime.datetime.now().strftime('%H')
current_weekday = int(datetime.datetime.now().strftime('%u'))

# current_weekday = 1  # use it for troubleshooting integer
# current_hour = '14' # use it for troubleshooting
######################################################################

# determining a worksheet name ("month day - month day")
then = datetime.timedelta(days=2)
new_date = datetime.timedelta(days=current_weekday - 1)
current_data_full = datetime.datetime.now() - new_date
end_week = current_data_full + datetime.timedelta(days=4)
strng = current_data_full.strftime("%B %-d") + ' - ' + end_week.strftime("%B %-d")
if (current_weekday == 1 and current_hour == '00') or (os.path.exists('/home/sasha/GoInbound/list_name') is False):
    f = open("/home/sasha/GoInbound/list_name", "w")
    f.write(strng)
    f.close()
    print("list name overwrote")

######################################################################
gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
# select the sheet
#  sh = retry(gc.open)('Support hours') - its using retry function
sh = gc.open('Support hours')
# select the worksheet
# wks = sh.worksheet(property='title', value=strng)
wks = sh.worksheet(property='title', value='April 2 - April 6 global')
######################################################################
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)
######################################################################

#WEEKDAY_MATRIX = {
#    1: ('A4', 'I21'),
#    2: ('A24', 'I37'),
#    3: ('A40', 'I53'),
#    4: ('A56', 'I70'),
#    5: ('A74', 'I87'),
#}

WEEKDAY_MATRIX = {
    1: ('A4', 'R26'),
    2: ('A30', 'R49'),
    3: ('A53', 'R72'),
    4: ('A75', 'R94'),
    5: ('A98', 'R117'),
}

if current_weekday in WEEKDAY_MATRIX:
    current_matrix = wks.get_values(*WEEKDAY_MATRIX.get(current_weekday), include_empty=0)
else:
    exit()
#
# if current_weekday == 1:
#     current_matrix = wks.get_values('A4', 'I21', include_empty=0, )
# elif current_weekday == 2:
#     current_matrix = wks.get_values('A24', 'I37', include_empty=0, )
# elif current_weekday == 3:
#     current_matrix = wks.get_values('A40', 'I53', include_empty=0, )
# elif current_weekday == 4:
#     current_matrix = wks.get_values('A56', 'I70', include_empty=0, )
# elif current_weekday == 5:
#     current_matrix = wks.get_values('A74', 'I87', include_empty=0, )
# elif current_weekday == 6 or current_weekday == 7:
#     exit()

# print(*current_matrix)

current_matrix_without_empty_entries = [elem for elem in current_matrix if len(elem) > 1]
# print(*current_matrix_without_empty_entries)

user_list = wks.get_values('A130', 'R130', include_empty=0, )
user_confirm = wks.get_values('A131', 'S131', include_empty=1, )

print(user_confirm)
######################################################################
# clear the conformations at the beginning of the new hour
if current_min == '00':
    wks.clear('A131', 'R131')
    # - add sleep
######################################################################
for row in current_matrix_without_empty_entries:
    print(row[0])
    if row[0].split('h')[0] == current_hour:
        i = 0
        for cell in row:
            # print(cell)
            if cell == 'Phones' and user_confirm[0][i] != 'confirmed':
                msg = user_list[0][i] + " it's " + row[1] + ' PST.\n' + current_matrix_without_empty_entries[0][
                    i] + ' thats your hour! Go inbound plse :smile:'
                # print(user_list[0][i])
                #  user_id = user_list[0][i][2:10]
                #  print(user_id)
                message_attachments = [
                    {
                        "text": msg,
                        # "fallback": "You are unable to choose a game",
                        "callback_id": user_list[0][i][2:11],
                        "color": "#FF0000",
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
                    channel=Chanel_to_post,
                    text='',
                    attachments=message_attachments
                )
            i += 1
