import csv
from posixpath import split
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

                    # 確認用print
                    print('駅名：' + station_name + '\nURL：' + cur_url)
                    # 10回ループしたらやめる(DDos攻撃の防止)
                    if loop_count == 10:
                        break
    return dict_station_url

# カウントを一つ増やすメソッド
def incre_count(lapcount):
    newcount = int(lapcount) + 1
    f = open('ManageCount/ManageCount.txt', 'w')
    f.write(str(newcount))

def create_report(dic_sta_and_url):
    # 全てのリストを表示
    # print(dic_sta_and_url)
    urlsplited = []

    # csvを読み込み
    with open('report/report.csv', 'a', encoding = 'cp932') as reportcsv:
        writer = csv.writer(reportcsv)
        # 参考として帰ってくるURLを貼り付ける：赤土小学校前': 'https://tabelog.com/tokyo/A1324/A132401/R11091/rstLst/?vs=1&sa=%E8%B5%A4%E5%9C%9F%E5%B0%8F%E5%AD%A6%E6%A0%A1%E5%89%8D&sk=%25E5%25B1%2585%25E9%2585%2592%25E5%25B1%258B&lid=top_navi1&vac_net=&svd=20220402&svt=1900&svps=2&hfc=1&Cat=RC&LstCat=RC21&LstCatD=RC2101&cat_sk=%E5%B1%85%E9%85%92%E5%B1%8B'
        for station in dic_sta_and_url:
            # URLを/で分割
            urlsplited =  dic_sta_and_url[station].split("/")
            # 各項目を変数化(詳細はCSVのヘッダーを参照)
            # ちなみに以下のif文はこーゆーエラーを避けるため→    fifth  = urlsplited[7]   IndexError: list index out of range
            url = dic_sta_and_url[station]
            if len(urlsplited) >= 4:
                first  = urlsplited[3]
            if len(urlsplited) >= 5:
                second = urlsplited[4]
            if len(urlsplited) >= 6:
                third  = urlsplited[5]
            if len(urlsplited) >= 7:
                forth  = urlsplited[6]
            if len(urlsplited) >= 8:
                fifth  = urlsplited[7]

            # 以下はクエリパラメータに関する変数化
            queryparamsloca = len(urlsplited) - 1
            queryparamsplit = urlsplited[queryparamsloca].split("&")
            if len(queryparamsplit) >= 1:
                vs      = queryparamsplit[0].replace("?vs=", "")
            if len(queryparamsplit) >= 2:
                sa      = queryparamsplit[1].replace("sa=", "")
            if len(queryparamsplit) >= 3:
                sk      = queryparamsplit[2].replace("sk=", "")
            if len(queryparamsplit) >= 4:
                lid     = queryparamsplit[3].replace("lid=", "")
            if len(queryparamsplit) >= 5:
                vac_net = queryparamsplit[4].replace("vac_net", "")
            if len(queryparamsplit) >= 6:
                svd     = queryparamsplit[5].replace("svd=", "")
            if len(queryparamsplit) >= 7:
                svt     = queryparamsplit[6].replace("svt=", "")
            if len(queryparamsplit) >= 8:
                svps    = queryparamsplit[7].replace("svps=", "")
            if len(queryparamsplit) >= 9:
                hfc     = queryparamsplit[8].replace("hfc=", "")
            if len(queryparamsplit) >= 10:
                Cat     = queryparamsplit[9].replace("Cat=", "")
            if len(queryparamsplit) >= 11:
                LstCat  = queryparamsplit[10].replace("LstCat=", "")
            if len(queryparamsplit) >= 12:
                LstCatD = queryparamsplit[11].replace("LstCatD=", "")
            if len(queryparamsplit) >= 13:
                cat_sk  = queryparamsplit[12].replace("cat_sk=", "")

            # CSVへの書き込み(１行ずつ)
            writer.writerow(
                [
                    '\n' + station,
                    url,
                    first,
                    second,
                    third,
                    forth,
                    fifth,
                    vs,
                    sa,
                    sk,
                    lid,
                    vac_net,
                    svd,
                    svt,
                    svps,
                    hfc,
                    Cat,
                    LstCat,
                    LstCatD,
                    cat_sk
                ]
                
            )

# if __name__ == '__main__':
# checkskipはカウントリセットをスキップするかどうかを確認するためのもの(Yesならカウントリセットしないで進む)
def create_endpoint(checkskip):
    print('実行はされてる')


    # 何周目の処理なのかを管理する
    lapcount = 0
    # カウントリセット処理自体を飛ばさないとき
    if checkskip == 'No':
        # カウントをリセットするためのメソッド
        resetresult =  check_reset()
    # カウントリセット処理自体を飛ばすとき
    elif checkskip == 'Yes':
        resetresult = "notreseted"

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
    create_report(dic_sta_and_url)

    # Dos攻撃を避けるために5分ほどスリープを入れる
    time.sleep(300)

