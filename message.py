import os  # ------------------ to get sys var
import logging
from slackclient import SlackClient  # ------------------ for slack API
import pygsheets  # ------------------ the main module
import datetime  # ------------------ to operate current time
import random
import time
import json

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

######################################################################
gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
# select the sheet
#  sh = retry(gc.open)('Support hours') - its using retry function
sh = gc.open('Support hours')
# select the worksheet
wks = sh.worksheet(property='title', value=strng)

#cell01 = wks.cell('A2')
# wks = sh.worksheet(property='title', value='April 2 - April 6')
#print(cell01.color)
# cell01.set_text_format('bold', True).value = 'heights'
#cell01.color = (1, 0, 0, 0)

#get_mtrx = wks.get_values('A1', 'A130', include_empty=1)
#print(cell01.color)



WEEKDAY_MATRIX3 = {"WEEKDAY_MATRIX":{
                      "1":{"1":"A2","2":"E15"},
                      "2":{"1":"A29","2":"S50"},
                      "3":{"1":"A54","2":"S75"},
                      "4":{"1":"A79","2":"S103"},
                      "5":{"1":"A107","2":"S128"}},
 "TMP2":{"1":"A141","2":"S141"},
 "TMP3":{"1":"A142","2":"S142"},
 "TMP4":{"1":"A143","2":"T143"}}

######################################################################
#for row in get_mtrx:
#    if row[0] == 'Smolensk time':
#        day_start_flag = True
#        # cell002 =
# if (row[0].split('h')[0] == current_hour):
#     i = 0
#     for cell in row:
#         if cell == 'Phones' and user_confirm[0][i] != 'confirmed':

end_counter = ''
i = 1
d = 1


print(type(WEEKDAY_MATRIX3))

print(WEEKDAY_MATRIX3["WEEKDAY_MATRIX"][str(d)]['1'])

while True:
    n_cell = 'A' + str(i)
    #end_counter = wks.cell(n_cell)
    end_counter = retry(wks.cell)(n_cell)
    print(n_cell)
    if end_counter.value == 'Smolensk time':
        day_start_flag1 = end_counter.label
        day_start_flag = True
        day_end_flag = False
        WEEKDAY_MATRIX3["WEEKDAY_MATRIX"][str(d)]['1'] = end_counter.label
        print('start day %s tracking' % d)
    if end_counter.value == '03h00 - 04h00':
        day_end_flag1 = end_counter.label
        day_end_flag = True
        WEEKDAY_MATRIX3['WEEKDAY_MATRIX'][str(d)]['2'] = end_counter.label
        #print(day_start_flag1)
        print('stop day %s tracking' % d)
        d = d + 1
    if d == 2:
        break
    i = i+1
    time.sleep(1)

js = json.dumps(WEEKDAY_MATRIX3)
f = open("/home/sasha/GoInbound/test", "w")
f.write(js)
f.close()
print("list name overwrote")
