import csv
from tabnanny import check
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_binary             # パスを通すためのコード
from selenium.webdriver.common.by import By
import pdb
import time
import json
import sys
from tkinter import messagebox


# カウントをリセットするかどうかを聞くメソッド(リセット処理も)
def check_reset():
    # リセットをしたかどうかを確認するフラグ
    resetflag = 0
    check = messagebox.askyesno('リセット確認', 'カウントのリセットを行いますか?')
    if check == True:
        check2 = messagebox.askyesno('最終確認', '本当の本当にカウントのリセットを行いますか?')
        if check2 == True:
            # リセット処理
            f = open('ManageCount/ManageCount.txt', 'w')
            f.write("0")
            resetflag = 1
    # リセットが行われていない場合
    if resetflag == 0:
        return "notreseted"
    # リセットが行われた場合
    elif resetflag == 1:
        return "reseted"
    
        
def endpoint_finder(lapcount):
    # なんか文字列型になっているので変換
    lapcount = int(lapcount)
    # 駅名(CSVに書いてあるやつ)
    station_name = ''
    driver = webdriver.Chrome()
    # 駅名とURLの関係を表す辞書
    dict_station_url = {}
    loop_count = 0
    # CSVを何行目から読めば良いか
    startlinenum = 0
    # 今何行目を読んでいるか
    readingrownum = 0
    # CSVの読み込み
    with open('./csv/tokyo_stations.csv', encoding = 'cp932') as f:
        startlinenum =  10 * lapcount
        reader = csv.reader(f)
        for row in reader:
            # 今読んでいる行数をカウント
            readingrownum = readingrownum + 1
            
            # 今読み込んでいる行が開始すべき行、またはそれ以降の行か
            if readingrownum >= startlinenum:
                # 今何行分読んでいるかをカウント
                loop_count = loop_count + 1
                # csvの４列目に駅名が書いてるので...
                station_name = row[3]
                # DDos攻撃を避けるために実施
                time.sleep(2)
                
                # ヘッダーでないかを確認
                if station_name != 'station_name':
                    driver.get("https://tabelog.com/")
                    # 文字列を入力するテキストボックスの場所(idはsaだった)
                    textarea_of_station = driver.find_element_by_id("sa")
                    textarea_of_station.send_keys(station_name)

                    # フリーワードのところに「居酒屋」と入力する操作
                    textarea_of_station = driver.find_element_by_id("sk")
                    textarea_of_station.send_keys('居酒屋')
                    # 検索ボタンを押下
                    button_search = driver.find_element_by_id("js-global-search-btn")
                    button_search.click()

                    # ②：今表示されているURLを取得
                    cur_url = driver.current_url
                    dict_station_url[station_name] = cur_url
                    # 10回ループしたらやめる(DDos攻撃の防止)
                    if loop_count == 2:
                        break
    return dict_station_url

# カウントを一つ増やすメソッド
def incre_count(lapcount):
    newcount = int(lapcount) + 1
    f = open('ManageCount/ManageCount.txt', 'w')
    f.write(str(newcount))

if __name__ == '__main__':
    # 何周目の処理なのかを管理する
    lapcount = 0
    # カウントをリセットするためのメソッド
    resetresult=  check_reset()

    # 今何周目なのかを認識(別テキストファイルにて管理しているため、それを読み込む)
    # リセットされた場合は当然ラップカウントは0なのでpassをする
    if resetresult == "reseted":
        pass
    # 今何周目なのかを把握するためにテキストファイルを読み込む
    elif resetresult == "notreseted":
        f = open('ManageCount/ManageCount.txt', 'r')
        lapcount = f.read()
        f.close

    # 駅名とURLが対応している辞書型の変数
    dic_sta_and_url = endpoint_finder(lapcount)
    # このタイミングでカウントを一つ増やす(処理が完了したので)
    incre_count(lapcount)
    # レポート作成する


 

    

