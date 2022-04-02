import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_binary             # パスを通すためのコード
from selenium.webdriver.common.by import By
import pdb
import time
import json

def endpoint_finder():
    # 駅名(CSVに書いてあるやつ)
    station_name = ''
    driver = webdriver.Chrome()
    # 駅名とURLの関係を表す辞書
    dict_station_url = {}
    loop_count = 0
    # CSVの読み込み
    with open('./csv/tokyo_stations.csv', encoding = 'cp932') as f:
        reader = csv.reader(f)
        for row in reader:
            loop_count = loop_count + 1
        # for i in range(10):
            # csvの４列目に駅名が書いてるので...
            station_name = row[3]
            # DDos攻撃を避けるために実施
            time.sleep(2)
            
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
                if loop_count == 3:
                    break
    return dict_station_url


if __name__ == '__main__':
    # 今何周目なのかを認識(別テキストファイルにて管理しているため、それを読み込む)
    # ***********************************
    # ***********************************


    dic_sta_and_url = endpoint_finder()

    print("変換前の結果を表示")
    print(dic_sta_and_url)

    # 返却値をjson型に変換
    # dic_sta_and_url_json = json.dumps(dic_sta_and_url)

    print("変換後の結果を表示")
    print(dic_sta_and_url)

    # jsonファイルでレポートを作成
    # ちなみにこれで書き込みされた駅名は文字こーどが変になっているが、json形式の文字列になっているだけなので後でjson.json.loadをするとちゃんと治る
    # 参考サイト：https://mayumega.site/prog/py_json_wra/
    # ちなみに感じはこの文字コードになる：https://glyphwiki.org/wiki/Group:JIS%E7%AC%AC1%E6%B0%B4%E6%BA%96
    j_w=open("report/test.json","w", encoding="utf-8")
    json.dump(dic_sta_and_url,j_w,indent=2)
    j_w.close()

    

