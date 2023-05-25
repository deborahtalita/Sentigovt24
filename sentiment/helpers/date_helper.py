from datetime import datetime, timedelta
import pytz

timezone = pytz.timezone('Asia/Jakarta')

def convertDate(date):
    date = datetime.strptime((datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')),('%Y-%m-%d'))
    date = date.replace(tzinfo=pytz.utc).astimezone(timezone)
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return date

def getDates(start, end):
    dates = []
    i = 0

    cur_date = start
    while cur_date <= end:
        date = cur_date.strftime('%Y-%m-%d')
        # print(date) 
        dates.append(date)
        cur_date += timedelta(days=1)

    return dates