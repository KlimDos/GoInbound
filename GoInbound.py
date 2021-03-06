import os
import logging
from slackclient import SlackClient
import pygsheets
import datetime
import random
import json

"""-------------Constants--------------"""
shName = 'Support hours'
cFile = 'creds.json'
configJson = '/home/sasha/GoInbound/config.json'
logFileName = '/home/sasha/GoInbound/mylog.log'
###################################################


emoji = (
    'davidh', 'joshua', 'revolution_parrot', 'trump', 'scat_sleepy', 'glitch_crab', 'adam', 'scarederic', 'mike',
    'happy',
    'sadmike', 'lightsaber', 'krishna', 'mitch', 'swiper', 'minion', 'unamused_face', 'piggy', 'mirror_parrot',
    'coolio',
    'python', 'bugs', 'cloudfinder', 'pikachu2', 'captain_obvious', 'hero', 'rock', 'huh', 'weasel', 'coffee_',
    'tardis',
    'szechuan', 'cry_laughing', 'grumpycat', 'troll', 'francisco', 'nod', 'jonk', 'scat_conspirator', 'shaka',
    'godmode',
    'noice', 'itwasntme', 'cry_', 'coololi', 'yellow_duck', 'bryan', 'debian', 'porg', 'bowtie', 'celebrate', 'whew',
    'black_square', 'axcient', 'penguin_', 'dead_girl', 'bruno', 'discodancer', 'adi', 'ninjaphone', 'barf', 'ibelieve',
    'krishnaboom', 'blush_', 'sadpanda', 'hendance', 'godfather', 'rage4', 'superwoman', 'unix', 'smileycute',
    'call_me',
    'slap', 'dusty_stick', 'portal_parrot', 'captain', 'madunikitty', 'andy', 'grinning_face', 'angrytrump',
    'science_parrot', 'coolkim', 'cube', 'brb', 'homer', 'kevin', 'scat_concern', 'goberserk', 'bryanboom', 'finnadie',
    'pirate_parrot', 'hairybruno', 'rick', 'poof', 'facepalm', 'madandy', 'bowlingpin', 'sad_parrot', 'birdp', 'nico',
    'trogdor', 'police', 'neckbeard', 'ussr', 'white_square', 'madsteve', 'goodnews', 'cubimal_chick', 'shipit',
    'hulkfist',
    'steveboom', 'philosoraptor', 'picklerick', 'shocked', 'tami', 'madadam', 'slack_call', 'linux', 'stable_parrot',
    'sovjet_parrot', 'face_with_tears_of_joy', 'toe', 'trap', 'hi5', 'hug', 'rotating_parrot', 'monkey_dance', 'atleti',
    'madmike', 'hairnetkevin', 'dab_', 'unikitty', 'notsure', 'zoidberg', 'derek', 'defcon25', 'giggle', 'why',
    'donttalktome', 'triplets_parrot', 'bearsteve', 'montz', 'okay', 'scat_think', 'ren', 'peep', 'doh', 'barca',
    'blush_normal', 'pjsalt', 'ultra_parrot', 'summer', 'guillermo', 'ssearch_cat', 'superman', 'coolbruno', 'bbill',
    'beafraid', 'clapping', 'dull', 'beryl', 'cheddar', 'mway', 'towelie', 'toucansam', 'duck_yellow', 'phoneninja',
    'disappearing_ninja', 'tongue_out', '5floppy', 'r2d2', 'pikachu', 'deadpoollove', 'doge', 'snoopy', 'simple_smile',
    'angel_parrot', 'surprised', 'coffeebean', 'fast_parrot', 'sombrero_parrot', 'sadpicard', 'hairnetmike',
    'shipit_parrot', 'madkevin', 'morty', 'fry', 'rube', 'slack', 'squirrel', 'banghead', 'fingerscrossed',
    'with_rolling_eyes', 'moonwalk_parrot', 'yaomingmeme', 'rofl', 'kris', 'davidn', 'nooice', 'deal_with_it_parrot',
    'octocat', 'rage1', 'ippon_seoi_nage', 'rebel', 'handsinair', 'this', 'skinnyjoshua', 'troll_parrot', 'scat_work',
    'lipssealed', 'real', 'grumpy', 'murphys', 'rage2', 'kappa', 'hurtrealbad', 'eye_wink', 'efolder', 'trollface',
    'high_fives', 'thumbsup_parrot', 'steve', 'peace_out', 'peace', 'sweating', 'sbug', 'coreyb', 'winkinghamster',
    'shame', 'acorn', 'bender', 'palm_face', 'kim', 'thumbsup_all', 'knoif', 'pride', 'parrot_poop', 'metal', 'vzhuh',
    'angrydink', 'partyparrot', 'rage3', 'cmd', 'headbang', 'smirk1', 'skype_face_palm', 'highflyer', 'smile-coffee',
    'cruella', 'fifo_parrot_r', 'sun', 'axcientx', 'pumpkin', 'fu', 'kumomon', 'jaws', 'fifo_parrot', 'feelsgood',
    'oli',
    'feelsbadman', 'poopy', 'vovka', 'mustache_parrot', 'hairoli', 'hammer_time', 'ooee', 'bowing', 'headdesk',
    'fidget_spinner', 'turkey_', 'like_it', 'crying_face', 'chicknugg', 'penarol', 'portalcake', 'coolsteve', 'suspect',
    'fist_pump', 'sdelight_cat', 'yoda', 'ninja')

LOG = logging.getLogger(__name__)

#####################################################################
# "G7GMUN1RA" "support_smolensk" - private
# "C7HAE7FEG" "ax-phone_schedule"
# "C9NQKBY8N" "test_aalimov"
# "U7G7BTY9L

Chanel_to_post = "C7HAE7FEG"

#####################################################################
# gathering current data from the instance
current_min = datetime.datetime.now().strftime('%M')
current_hour = datetime.datetime.now().strftime('%H')
current_weekday = int(datetime.datetime.now().strftime('%u'))

# current_weekday = 1  # use it for troubleshooting integer
# current_hour = '10' # use it for troubleshooting
######################################################################

# determining a worksheet name ("month day - month day")
then = datetime.timedelta(days=2)
new_date = datetime.timedelta(days=current_weekday - 1)
current_data_full = datetime.datetime.now() - new_date
end_week = current_data_full + datetime.timedelta(days=4)
strng = current_data_full.strftime("%B %-d") + ' - ' + end_week.strftime("%B %-d")


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


def get_matrix():
    '''
    
    :return: 
    '''
    # with open('data.json') as f:
    data = json.load(open(configJson))
    return data


if (current_weekday == 1 and current_hour == '02') or (os.path.exists('/home/sasha/GoInbound/list_name') is False):
    f = open("/home/sasha/GoInbound/list_name", "w")
    f.write(strng)
    f.close()
    print("list name overwrote")

if int(current_hour) < 4:
    current_weekday = current_weekday - 1

######################################################################
gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
# select the sheet
#  sh = retry(gc.open)('Support hours') - its using retry function
sh = gc.open('Support hours')
# select the worksheet
wks = sh.worksheet(property='title', value=strng)
# wks = sh.worksheet(property='title', value='April 2 - April 6')
######################################################################
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

we = get_matrix()
WEEKDAY_MATRIX = get_matrix()['WEEKDAY_MATRIX']
new_dic = we['WEEKDAY_MATRIX']
new_dic2 = {}

for k, v in new_dic.items():
    new_dic2[int(k)] = v
    # print(k,v)

vr1 = get_matrix()['VR']['1']
vr2 = get_matrix()['VR']['2']
vr3 = get_matrix()['VR']['3']
vr4 = get_matrix()['VR']['4']
vr5 = get_matrix()['VR']['5']
vr6 = get_matrix()['VR']['6']

WEEKDAY_MATRIX = new_dic2

if current_weekday in WEEKDAY_MATRIX:
    current_matrix = wks.get_values(*WEEKDAY_MATRIX.get(current_weekday), include_empty=0)
else:
    exit()

current_matrix_without_empty_entries = [elem for elem in current_matrix if len(elem) > 1]
# print(*current_matrix_without_empty_entries)

######################################################################
# clear the conformations at the beginning of the new hour

if current_min == '00':
    wks.clear(chr(ord(vr1[0]) + 2) + vr1[1:], vr4)  # vr1 vr2
    # - add sleep

user_list = wks.get_values(vr2, vr5, include_empty=0, )
user_confirm = wks.get_values(vr1, vr6, include_empty=1)
user_confirm_lunch = wks.get_values(vr3, vr4, include_empty=1, )

print(user_confirm)

######################################################################
for row in current_matrix_without_empty_entries:
    print(row[0])
    if (row[0].split('h')[0] == current_hour):
        i = 0
        for cell in row:
            if cell == 'Phones' and user_confirm[0][i] != 'confirmed':
                emoji_final = ':' + emoji[random.randint(0, 280)] + ':'
                msg = user_list[0][i] + " it's " + row[1] + ' PST.\n' + current_matrix_without_empty_entries[0][
                    i] + ' thats your hour! Go inbound plse ' + emoji_final
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
                if int(current_min) > 0:
                    Chanel_to_post = user_list[0][i][2:11]
                slack_client.api_call(
                    "chat.postMessage",
                    channel=Chanel_to_post,
                    text='',
                    attachments=message_attachments
                )
            if cell == 'Lunch' and user_confirm_lunch[0][i] != 'confirmed':
                msg = user_list[0][i] + " Lunch time!!!"
                callback_id_lunch = user_list[0][i][2:11] + 'lunch'
                message_attachments = [
                    {
                        "text": msg,
                        "callback_id": callback_id_lunch,
                        "color": "#D358F7",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "Dismiss",
                                "text": "Dismiss",
                                "type": "button",
                                "value": "1",
                                "style": "primary"
                            }, ]
                    }
                ]

                slack_client.api_call(
                    "chat.postMessage",
                    channel=user_list[0][i][2:11],
                    text='',
                    attachments=message_attachments
                )
            i += 1
