import logging
import pygsheets
import datetime
import time
import json
import string

"""-------------Constants--------------"""
WEEKDAY_MATRIX3 = {"WEEKDAY_MATRIX": {
    "1": {"1": "x", "2": "y"},
    "2": {"1": "x", "2": "y"},
    "3": {"1": "x", "2": "y"},
    "4": {"1": "x", "2": "y"},
    "5": {"1": "x", "2": "y"}},
    "VR": {
        "1": "z",
        "2": "z",
        "3": "z",
        "4": "z",
        "5": "z",
        "6": "z"},
}

shName = 'Support hours'
cFile = 'creds.json'
configJson = '/home/sasha/GoInbound/config.json'
logFileName = '/home/sasha/GoInbound/mylog.log'
###################################################

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=logFileName)
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


def def_WName():
    """
    # determining a worksheet name ("month day - month day")
    #then = datetime.timedelta(days=2)
    # gathering current data from the instance
    # current_weekday = 1  # use it for troubleshooting integer
    """

    current_weekday = int(datetime.datetime.now().strftime('%u'))
    current_data_full = datetime.datetime.now() - datetime.timedelta(days=current_weekday - 1)
    end_week = current_data_full + datetime.timedelta(days=4)
    wName = current_data_full.strftime("%B %-d") + ' - ' + end_week.strftime("%B %-d")
    return wName


def open_sheet(shName, wName, cFile):
    """Open Google Spreadsheet.

    Keyword arguments:
    shName -- the name of the Spread Sheet
    wName  -- the name of the Work Sheet
    cFile  -- Path to credentials file

    Returns an object 'WorkSheet'
    #gc = pygsheets.authorize(outh_file='creds.json', outh_nonlocal=True)
    # select the sheet
    #  sh = retry(gc.open)('Support hours') - its using retry function
    #sh = gc.open('Support hours')
    # select the worksheet
    """
    workSheet = pygsheets.authorize(outh_file=cFile, outh_nonlocal=True).open(shName).worksheet(property='title',
                                                                                                value=wName)
    return workSheet


def create_WorkWeekMatrix():
    i = 1
    d = 1

    ABC = string.ascii_uppercase
    wks = open_sheet(shName, def_WName(), cFile)
    LOG.info("-----< Start config creating >-----")
    while True:
        end_counter = retry(wks.cell)('A' + str(i))
        if end_counter.value == 'Smolensk time':
            WEEKDAY_MATRIX3["WEEKDAY_MATRIX"][str(d)]['1'] = end_counter.label
            print('start day %s tracking' % d)
            LOG.info('start day %s tracking'), d
        if end_counter.value == '03h00 - 04h00':
            WEEKDAY_MATRIX3['WEEKDAY_MATRIX'][str(d)]['2'] = str(ABC[(end_counter.col - 1) + 1]) + str(end_counter.row)
            print('stop day %s tracking' % d)
            LOG.info('stop day %s tracking'), d
            d = d + 1
        if end_counter.value == 'TMP1':
            WEEKDAY_MATRIX3["TMP1"]['1'] = end_counter.label

        if end_counter.value == 'end' or end_counter.label == 'A200':
            break
        i = i + 1
        time.sleep(1)
    LOG.info("-----< Stop config creating >-----")
    return WEEKDAY_MATRIX3


def create_WorkWeekMatrix_new():

    wks = open_sheet(shName, def_WName(), cFile)
    cell_list_y = wks.range('A1:A200', returnas='cells')


    LOG.info("-----< Start config creating >-----")

    LOG.info("-----< Finding X >-----")
    cell_list_x = wks.range('A1:Z1', returnas='cells')
    i = 0
    for item_x in cell_list_x[0]:
        #print(item_x.value)
        if item_x.value == 'end':
            LOG.info("column index  = %s"), (item_x.label[0])
            print("column index  = %s" % item_x.label[0])
            break

    LOG.info("-----< Finding Y >-----")
    d = 1
    for item_y in cell_list_y:
        #print(item[0].label)
        if item_y[0].value == 'Smolensk time':
            WEEKDAY_MATRIX3["WEEKDAY_MATRIX"][str(d)]['1'] = item_y[0].label
            print('start day %s tracking on %s' % (d, item_y[0].label))
            LOG.info('start day %s tracking'), d
        if item_y[0].value == '03h00 - 04h00':
            WEEKDAY_MATRIX3['WEEKDAY_MATRIX'][str(d)]['2'] = item_x.label[0] + str(item_y[0].row)
            print('stop day %s tracking on %s' % (d, item_x.label[0] + str(item_y[0].row)))
            LOG.info('stop day %s tracking'), d, (item_x.label[0] + str(item_y[0].row))
            d = d + 1
        if item_y[0].value == 'VR': # - для очистки
            WEEKDAY_MATRIX3["VR"]['1'] = 'A' + str(item_y[0].row + 2)
            WEEKDAY_MATRIX3["VR"]['2'] = 'A' + str(item_y[0].row + 1)
            WEEKDAY_MATRIX3["VR"]['3'] = 'A' + str(item_y[0].row + 3)
            WEEKDAY_MATRIX3["VR"]['4'] = item_x.label[0] + str(item_y[0].row + 3)
            WEEKDAY_MATRIX3["VR"]['5'] = chr(ord(item_x.label[0])-1) + str(item_y[0].row + 1)
            WEEKDAY_MATRIX3["VR"]['6'] = item_x.label[0] + str(item_y[0].row + 2)

    LOG.info("-----< Stop config creating >-----")
    return WEEKDAY_MATRIX3


f = open(configJson, "w")
f.write(json.dumps(create_WorkWeekMatrix_new()))
f.close()
print("the Work Week Matrix has been overwritten")
LOG.info("the Work Week Matrix has been overwritten")

"""
#==================================
#cell01 = wks.cell('A2')
# wks = sh.worksheet(property='title', value='April 2 - April 6')
#print(cell01.color)
# cell01.set_text_format('bold', True).value = 'heights'
#cell01.color = (1, 0, 0, 0)

#get_mtrx = wks.get_values('A1', 'A130', include_empty=1)
#print(cell01.color)
"""
