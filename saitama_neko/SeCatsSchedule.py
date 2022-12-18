# ファイル名 : se_cats_schedule.py
# 機能概要 : 定期的にsaitama_se_cats.pyを実行する

# ライブラリ、モジュールをインポート
import schedule  # スケジュール
import time  # 時刻
import saitama_se_cats  # saitama_se_cats

# 実行時刻
run_time = '12:00'
# スケジュール設定 毎日run_timeになったら
schedule.every().day.at(run_time).do(saitama_se_cats.CreateCatlist)
# スケジュールスタート
while True:
    schedule.run_pending()
    time.sleep(30)