"""
ファイル名 : CatsSchedule.py
■概要
処理を定期実行するためのモジュールです
"""
# ライブラリ、モジュールをインポート
import schedule  # スケジュール
import time  # 時刻
from CreateSentens import CreateSentens
from OperationTweetBot import tweet

def day_task():
    """
    処理
        譲渡用猫情報の各ページ(北西部、南東部)の情報をまとめたツイートをする
    """
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