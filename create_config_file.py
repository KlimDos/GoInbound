import logging
import pygsheets
import os
import json

LOG = logging.getLogger(__name__)

from pprint import pprint

with open('/home/sasha/GoInbound/config.json') as f:
    data = json.load(f)
pprint(data)

#f = open("/home/sasha/GoInbound/config.conf", "a")
#f.write("line 1 \n")
#f.close()
#print("config file has been overwritten")

#//examples
print('===========================================')
print(data['TMP2']['1'])
print(data['WEEKDAY_MATRIX']['1']['2'])


WEEKDAY_MATRIX2 = {
    1: ('A4', 'S25'),
    2: ('A29', 'S50'),
    3: ('A54', 'S75'),
    4: ('A79', 'S103'),
    5: ('A107', 'S128')
}


WEEKDAY_MATRIX3 = {
                   "WEEKDAY_MATRIX":{
                      "1":
                          {
                            "1":"A4",
                            "2":"S25"
                          },
                      "2":
                          {
                            "1":"A29",
                            "2":"S50"
                          },
                      "3":
                          {
                            "1":"A54",
                            "2":"S75"
                          },
                      "4":
                          {
                            "1":"A79",
                            "2":"S103"
                          },
                      "5":
                          {
                            "1":"A107",
                            "2":"S128"
                          }
    },
 "TMP2":
       {
           "1":"A141",
           "2":"S141"
       },

 "TMP3":
       {
           "1":"A142",
           "2":"S142"
       },
 "TMP4":
       {
           "1":"A143",
           "2":"T143"
       }
}


end_counter = ''
i = 1
d = 1
while True:
    n_cell = 'A' + str(i)
    #end_counter = wks.cell(n_cell)
    end_counter = retry(wks.cell)(n_cell)
    print(n_cell)
    if end_counter.value == 'Smolensk time':
        day_start_flag1 = end_counter.label
        day_start_flag = True
        day_end_flag = False
        WEEKDAY_MATRIX[d][0] = end_counter.label
        print('start day %s tracking' % d)
    if end_counter.value == '03h00 - 04h00':
        day_end_flag1 = end_counter.label
        day_end_flag = True
        WEEKDAY_MATRIX[d][1] = end_counter.label
        #print(day_start_flag1)
        print('stop day %s tracking' % d)
        d = d + 1
    if d == 6:
        break
    i = i+1
    time.sleep(1)
pass




js = json.dumps(WEEKDAY_MATRIX3)

f = open("/home/sasha/GoInbound/test", "w")
f.write(js)
f.close()
print("list name overwrote")