# ファイル名 : SeCatsSchedule.py.py
# 機能概要 : 定期的にSaitamaSeCats.py.pyを実行する

# ライブラリ、モジュールをインポート
import schedule  # スケジュール
import time  # 時刻
from CreateSentens import CreateSentens
from OperationTweetBot import tweet

def day_task():
    AREA_LIST = ['nw', 'se']
    for area in AREA_LIST:
        tweet(CreateSentens(area).sentens_2())

# 実行時刻
run_time = '09:00'
# スケジュール設定 毎日run_timeになったら
schedule.every().day.at(run_time).do(day_task)
# スケジュールスタート
while True:
    schedule.run_pending()
    time.sleep(30)