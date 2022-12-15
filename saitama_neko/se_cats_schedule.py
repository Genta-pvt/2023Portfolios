import schedule
import time
import saitama_se_cats

run_time = '12:00'
schedule.every().day.at(run_time).do(saitama_se_cats.CreateCatlist)

while True :
    schedule.run_pending()
    time.sleep(30)