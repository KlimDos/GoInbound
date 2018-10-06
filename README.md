# GoInbound

the app for notifying users that they need go inbound

#### The time table in Gsheets 
#### Notifying in Slack

libs - 
### sensitive required
* sheets.googleapis.com-python.json - auth file fog GSheet
* creds.json - - auth file fog GSheet

### parts
wrapper_json.sh - starts create_json.py
config.json - result of running create_json.py
mylog.log - server logs
log.txt - checker logs
list_name - the name of the list in GSheet