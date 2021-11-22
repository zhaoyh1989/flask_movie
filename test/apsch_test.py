from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

def aps_test():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

scheduler = BlockingScheduler(timezone="Asia/Shanghai")
scheduler.add_job(func=aps_test, trigger="cron", second="*/2")
scheduler.start()


