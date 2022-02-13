from bs4 import BeautifulSoup    # importする
import requests
import re
import sys
from tkinter import messagebox
import csv
# URLエンコードをするためのライブラリ(標準)
import urllib.parse
import datetime

# コマンドの引数より検索条件を取得するメソッド
def get_search_condition():
    args = sys.argv
    # 検索条件
    izakaya_place = args[1]
    return izakaya_place

# 入力された文字列がちゃんと場所の名前かどうかを確認するメソッド
def check_if_retry_input(user_input_place):
    checker_result = ''
    # そんな駅名があるのかどうかをチェックするメソッド
    # なんかまた例の如くエンコードに苦しんだんだけどこの参考サイトを見てへ〜ってなった。
    # 参考サイト：https://insilico-notebook.com/python-unicodedecodeerror/
    with open('./csv/tokyo_stations.csv', encoding = 'cp932') as f:
        reader = csv.reader(f)
        for row in reader:
            # csvの４列目に駅名が書いてるので...
            if user_input_place == row[3]:
                checker_result = 'OK'
                break
            else:
                checker_result = 'NG'
    return checker_result

# URL内のクエリパラメータ専用のフォーマットで日付を返却するメソッド(例：svd=20220108)
# 参考サイト：https://note.nkmk.me/python-datetime-now-today/
def creta_date():
    date = ''
    # 2019-02-04 21:04:15.412854みたいな感じで帰ってくる
    dt_now = datetime.datetime.now()
    year = dt_now.year
    month = ''
    day = ''
    # もし月が一桁である場合
    if len(str(dt_now.month)) == 1:
        month = '0' + str(dt_now.month)
    else:
        month = str(dt_now.month)
    if len(str(dt_now.day)) == 1:
        day = '0' + str(dt_now.day)
    else:
        day = str(dt_now.day)
    date = str(year) + str(month) + str(day)
    return date

# 参考サイト：https://note.nkmk.me/python-urllib-parse-quote-unquote/
def create_request_url(izakaya_place):
    request_url = ''
    endpoint = 'https://tabelog.com/tokyo/A1304/A130401/R5172/rstLst/?'
    vs = 'vs=1'
    sa = 'sa='
    sk = 'sk='
    lid = 'lid=top_navi1'
    vac_net = 'vac_net='
    svd = 'svd='
    svt = 'svt=1900'
    svps = 'svps=2'
    hfc = 'hfc=1'
    Cat = 'Cat=RC'
    LstCat = 'LstCat=RC21'
    LstCatD = 'LstCatD=RC2101'
    cat_sk = 'cat_sk='
    # %E9%A7%85は「駅」のデコード
    station_decoded = '%E9%A7%85'
    izakaya_place_encoded = urllib.parse.quote(izakaya_place)
    # svdで渡す値の生成(svd=20220108みたいな感じで渡す)
    svd_value = creta_date()
    # 「居酒屋」という文字(エンコード後)
    izakaya_decode = '%E5%B1%85%E9%85%92%E5%B1%8B'

    # クエリパラメータを少し加工
    sa = sa + izakaya_place_encoded + station_decoded
    svd = svd + svd_value

    # 投げるURLの作成
    request_url = endpoint + vs + '&' + sa + izakaya_place_encoded + station_decoded + '&' + lid + '&' + vac_net + '&' + svd + svd_value + '&' + svt + '&' + svps + '&' + hfc + '&' + Cat + '&' + LstCat + '&' + LstCatD + '&' + cat_sk + izakaya_decode
    # print('====\n' + request_url + '\n======')
    return request_url

def request_and_get_result(request_url):
    # 店名のaタグをリスト化
    a_tag_list = []

    # 投げるための準備
    html = requests.get(request_url)
    soup = BeautifulSoup(html.content, "html.parser")
    return_html = str(soup)

    # # 後で削除しておいて欲しい部分=======================
    # # 取得したソースを別ファイルに出力する
    # path = '/Users/mikiken/Desktop/test_scr4.txt'
    # f = open(path, 'w')
    # # ファイルの中身
    # f.write(return_html)
    # # ================================================

    # なんか帰ってくるaタグの状況が違うのでこちらではscraping_test.pyとは違う正規表現を書いている
    # storelink_pattern = r'<a\sclass=\"list-rst__rst-name-target\scpy-rst-name\"\starget=\"_blank\"\srel=\"noopener\"\sdata-list-dest=\"item_top\"\shref=\"https.+>.+</a>'
    storelink_pattern = r'<a\sclass=\"list-rst__rst-name-target\scpy-rst-name\"\sdata-list-dest=\"item_top\"\shref=\"https.+\"\srel=\"noopener\"\starget=\"_blank\">.+</a>'
    a_tag_list = re.findall(storelink_pattern, return_html)
    print(a_tag_list)
    return a_tag_list

if __name__ == '__main__':
    # まずは検索条件を取得する
    # 今回はローカルで検証をするためにコマンドの引数で渡すが、本来ではあればAPI化するのでクエリパラメータとして渡すようにする
    # (これはLambdaにデプロイするときにそのような設定にする)
    messagebox.showinfo('警告', '引数に駅名(東京限定)を入力して実行をしてください')
    izakaya_place = get_search_condition()
    # 検索条件が何も指定されていないとき
    if izakaya_place == '':
        messagebox.showinfo('エラー', '検索条件が指定されていません。再実行してください')
        sys.exit()
    # 検索条件を検証する
    izakaya_check_result = check_if_retry_input(izakaya_place)
    if izakaya_check_result == 'NG':
        messagebox.showinfo('エラー', '入力された駅名は存在しません。再実行してください')
    # 駅名が存在した場合(有効な駅名である場合)
    elif izakaya_check_result == 'OK':    
        # curlをするためのURLを生成する
        request_url = create_request_url(izakaya_place)
        # その駅周辺の居酒屋のリストを返す(チェーン店含む)
        izakaya_list = request_and_get_result(request_url)

        




# test_scraping_bs4()
