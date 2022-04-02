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
    return a_tag_list

# aタグのリストから店名とリンクを抜いてくるメソッド
def get_storename_and_link(a_tag_list, user_input_place):
    # リンクは全て「https://tabelog.com/tokyo/A1304/A130401/13260630」みたいなフォーマットをしている
    storelink_pattern = r'https:\/\/tabelog\.com\/.+\/.+\/.+\/\d{8}'
    # 店名は全て>と<の間にある
    storename_pattern = r'>.+<'
    # 店名とリンクの辞書
    storename_and_link_dic = {}
    storename = ''
    storelink = ''
    for tag in a_tag_list:
        storename = re.findall(storename_pattern, tag)[0]
        storename = storename.replace('>', '').replace('<', '')
        storelink = re.findall(storelink_pattern, tag)[0]
        # 個人店なのかどうかのチェック
        # チェック①：●●店の排除(例：新宿西口店)
        storename = filter_near_station_store(storename, user_input_place)
        # チェックを行い、店名がそのまま返却された場合は個人店であるため辞書に追加をする
        if storename != '':
            # 辞書に「店名：リンク」で追加
            storename_and_link_dic[storename] = storelink
    return storename_and_link_dic

def filter_near_station_store(storename, user_input_place):
    # 店名をスペース区切りで配列化(後で使う)
    storename_splited_by_space = storename.split(' ')
    # 判定用のフラグ
    check_flag = 0
    # ●号店パターン
    multiple_store_pattern = r'.+号店'
    # 単純に「駅名 + 店」パターン
    station_store_pattern = user_input_place + '店'
    # ●●北口パターン
    north_exit_pattern = user_input_place + '北口'
    # ●●南口パターン
    sorth_exit_pattern = user_input_place + '南口'
    # ●●東口パターン
    east_exit_pattern = user_input_place + '東口'
    # ●●西口パターン
    west_exit_pattern = user_input_place + '西口'
    # 「地名 + ●● + 店」パターン(例：新宿NSビル店)
    # この正規表現の参考サイト：https://tech.kx2.site/2021/08/24/python-re-compile%E5%86%85%E3%81%A7%E5%A4%89%E6%95%B0%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%99%E3%82%8B/
    place_char_store_pattern = r'{}.+店'.format(user_input_place)
    # 先頭に何か文字がついてくるパターン(例：西新宿店)
    char_place_store_pattern = r'.+{}店'.format(user_input_place)
    # ●● + 地名 + ●● + 店パターン(例西新宿ラフォーレ店)
    char_place_char_pattern = r'.+{}.+店'.format(user_input_place)

    if station_store_pattern in storename:
        check_flag = 1
    elif north_exit_pattern in storename:
        check_flag = 1
    elif sorth_exit_pattern in storename:
        check_flag = 1
    elif east_exit_pattern in storename:
        check_flag = 1
    elif west_exit_pattern in storename:
        check_flag = 1
    # ●●本店パターン
    elif '本店' in storename:
        check_flag = 1
    #「もし地名 + ●● + 店というフォーマットでfindallをしてみて、見つかった結果が一件でもあれば(配列の要素が１以上なら)」
    elif len(re.findall(place_char_store_pattern, storename)) >= 1:
        check_flag = 1
    #「もし●● + 地名 + 店というフォーマットでfindallをしてみて、見つかった結果が一件でもあれば(配列の要素が１以上なら)」
    elif len(re.findall(char_place_store_pattern, storename)) >= 1:
        check_flag = 1
    #「もし●● + 地名 + ●● + 店というフォーマットでfindallをしてみて、見つかった結果が一件でもあれば(配列の要素が１以上なら)」
    elif len(re.findall(char_place_char_pattern, storename)) >= 1:
        check_flag = 1
    # その駅にある建物店の場合(例：あえん 伊勢丹会館店)
    # このパターンは末尾に●●店と書いてあるため、それで判定する(末尾以外のものを排除するすると例えば●●商店も排除されてしまう)
    # まずはスペースごとに配列にする
    # 「あえん 伊勢丹会館店」のように末尾の単語に店がつき、スペース区切りにした時に要素が2つ以上であるものは系列店の可能性がある
    elif len(storename_splited_by_space) > 1 and '店' in storename_splited_by_space[-1]:
        check_flag = 1
    elif '別館' in storename:
        check_flag = 1
    # ●●号店パターン
    elif len(storename_splited_by_space) > 1 and len(re.findall(multiple_store_pattern, storename_splited_by_space[-1])) >= 1:
        check_flag = 1
    # 返却値の加工
    if check_flag == 0:
        return storename
    elif check_flag == 1:
        return ''

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
        # 個人店のみににフィルターする(個人店リストが辞書型で返される)
        priv_store_dic = get_storename_and_link(izakaya_list, izakaya_place)
        print(priv_store_dic)
        print(len(priv_store_dic))
        # 個人店の件数が5件未満であった場合、２ページまで検索をして足りない件数分を再取得する
        if len(priv_store_dic) < 5:
            # これ以降の続きの処理をかく
            # 59行目のendpointも書き換えないと...




        




# test_scraping_bs4()
