from create_endpoint import create_endpoint
import schedule
from time import sleep

# スケジュール実行したいやつを定義している
def task():
    create_endpoint('Yes')

# schedule.every(2).minutes.do(task)
schedule.every(2).seconds.do(task)

while True:
    print('tyou')
    schedule.run_pending()
    sleep(1)


