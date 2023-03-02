import datetime

import time

from re_data import getdata
from mysqlconfig import InsertData


if __name__ == '__main__':
    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
        if time_now == "00:00:00":  # 此处设置每天定时的时间
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=1)
            all_data = getdata(start_date=start_date, end_date=end_date)
            for d in all_data:
                InsertData("earthquakedata", d)
            time.sleep(2)  # 因为以秒定时，所以暂停2秒，使之不会在1秒内执行多次
