import os                           #------------------ to get sys varybles
from slackclient import SlackClient #------------------ for slack API
import pygsheets                    #------------------ the main module
import datetime                     #------------------ to operate current time

######################################################################
#autorizing onto Google sheet API
gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
# select the sheet
sh = gc.open('1st_sheet')
# select the worksheet
wks = sh.worksheet(property='index', value='0')
######################################################################
slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
######################################################################
# gathering current data from the instance
current_hour = datetime.datetime.now().strftime('%H')
current_weekday = int(datetime.datetime.now().strftime('%u'))
######################################################################


######################################################################
# dont know why buy depend of the day we will get specific work hours
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

#print(current_matrix[0][1])
#current_hour = '20' # use it for trubleshuting
for row in current_matrix:
    # print(row[0])
    if row[0].split('h')[0] == current_hour:
        i = 0
        for cell in row:
            #print(cell)
            if cell == 'Phones':
                msg = current_matrix[0][i] + ' thats your hour! Go inbound plse :smile:'
                print(msg)
                sc.api_call("chat.postMessage", channel="trt", username='Go-Inbound Bot', text=msg)
            i += 1
