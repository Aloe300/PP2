import datetime

now = datetime.datetime.now()
five_days_ago = now - datetime.timedelta(days=5)

print("Now:", now)
print("5 days ago:", five_days_ago)

#######################################################

import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#######################################################

import datetime

today = datetime.datetime.now()
today_no_micro = today.replace(microsecond=0)

print("With microseconds:", today)
print("Without microseconds:", today_no_micro)