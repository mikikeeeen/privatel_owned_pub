# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# 個人店を探すロジック
# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
# 個人店の探し方
# ①まずは場所検索をする
# ②その中で店名のリストを取得してくる
# ③店名の中で「本店」「池袋店」などを排除する
# ④池袋店などに関しては店の前にきている文字列を取得して日本中の場所を検索するやつで検索をしてみる
# ⑤それでヒットしたら排除をする
# 残った「〇〇屋」とかの「〇〇店」が載っていないやつが個人店である
# ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*

# 前と違ってpipのパスが通ってないので、以下のようにpipをする際は打つように
# python3 -m pip install selenium
from os import waitpid
from typing import Pattern
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_binary             # パスを通すためのコード
from selenium.webdriver.common.by import By
import time
import tkinter
import csv
import re

# ======================================================================
# サンプル用に作成したメソッド(食べログのサイトに言ってソースを抜いてくるメソッド)
def sample_scraping_from_tabelog():
    driver = webdriver.Chrome()
    driver.get("https://tabelog.com/")
    # 実際にソースを抜いてきているところ
    sample_html = driver.page_source
    time.sleep(3)
    driver.quit()


# Flaskで実装する際はここは画面からの入力を受け付ける感じにする
# 今はスタンドアロンでやりたいのでtkinterで実装中(後でちゃんとここはflaskで実装してね!!!)
# 参考サイト：https://www.delftstack.com/ja/howto/python-tkinter/how-to-create-dropdown-menu-in-tkinter/
def get_izakaya_place():
    # Tkクラス生成
    root = tkinter.Tk()
    # 画面サイズ
    root.geometry('400x200')
    # 画面タイトル
    root.title('居酒屋の場所を入力するところ')
    # ラベル
    lbl = tkinter.Label(text='居酒屋の場所を入力(駅名)')
    lbl.place(x=30, y=70)
    # テキストボックス
    input = tkinter.Entry(width=20)
    input.place(x=150, y=70)
    # あんまりいい設計じゃないんだろうけど...致し方ない...これしか思いつかない...
    # 入力された値を取得するメソッド
    def btn_click():
        # input_txtをグローバル変数化(参考サイト：http://www.ops.dti.ne.jp/ironpython.beginner/global.html)
        global input_txt
        input_txt = input.get()
        print(input_txt)

    btn = tkinter.Button(root, text='決定', command=btn_click)
    btn.place(x=170, y=150)
    # 表示
    root.mainloop()

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

# aタグのリストから店名とリンクを抜いてくるメソッド
def get_storename_and_link(a_tag_list, user_input_place):
    # リンクは全て「https://tabelog.com/tokyo/A1304/A130401/13260630」みたいなフォーマットをしている
    storelink_pattern = r'https:\/\/tabelog\.com\/.+\/.+\/.+\/.+\"'
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
    print(storename_and_link_dic)

# 食べログより個人経営の店を取得してくるメソッド
def tabelog_private_store_main(user_input_place):
    # optionはヘッドレス(非表示)でスクレイピングをするためのオプション
    # options = Options()
    # options.add_argument('--headless')
    # ①：まずは入力された値を食べログで検索をする
    # driver = webdriver.Chrome(chrome_options = options)
    driver = webdriver.Chrome()
    driver.get("https://tabelog.com/")
    # 文字列を入力するテキストボックスの場所(idはsaだった)
    textarea_of_station = driver.find_element_by_id("sa")
    textarea_of_station.send_keys(user_input_place)

    # フリーワードのところに「居酒屋」と入力する操作
    textarea_of_station = driver.find_element_by_id("sk")
    textarea_of_station.send_keys('居酒屋')

    # 検索ボタンを押下
    button_search = driver.find_element_by_id("js-global-search-btn")
    button_search.click()

    # ②：次に検索遷移後の画面のソースを取得するメソッド
    source_html = driver.page_source

    # 後で削除してほしいところ==================
    # 取得したソースを別ファイルに出力する
    path = '/Users/mikiken/Desktop/test_scr2.txt'
    f = open(path, 'w')
    # ファイルの中身
    f.write(str(source_html))
    # ====================================


    # ほしいaタグが書いてある箇所
    a_link_pattern = r'<a\sclass=\"list-rst__rst-name-target\scpy-rst-name\"\starget=\"_blank\"\srel=\"noopener\"\sdata-list-dest=\"item_top\"\shref=\"https.+>.+</a>'
    # ちなみにこんな感じの部分を取得したかった
    # ====================================================================================
    # '<a class="list-rst__rst-name-target cpy-rst-name" target="_blank" rel="noopener" da
    # ta-list-dest="item_top" href="https://tabelog.com/tokyo/A1304/A130401/13239063/">肉
    # 寿司&amp;ステーキ食べ放題 肉ギャング 新宿東口店</a>'
    # ====================================================================================
    # 該当する部分のaタグ(店名、リンクが含まれる)を取得
    a_tag_list = re.findall(a_link_pattern, source_html)

    print(a_tag_list)
    
    # 店名とリンクを取得するメソッド
    get_storename_and_link(a_tag_list, user_input_place)
    time.sleep(5)
    driver.quit

if __name__ == '__main__':
    get_izakaya_place()
    user_input_place = input_txt
    # 入力された文字列が駅名かどうかをチェック
    input_check_result = check_if_retry_input(user_input_place)
    print(input_check_result)
    # =====ここまでで入力における作業終わり=======
    # 入力された文字列をもとに検索を開始する
    # 入力された値に問題がなかった時
    if input_check_result == 'OK':
        tabelog_private_store_main(user_input_place)
    # 入力された値に問題があった場合(リトライ処理??)
    else:
        # ここにリトライ処理を書く??
        pass

    # sample_scraping_from_tabelog()


# 焼肉
# "list-rst__rst-photo js-rst-image-wrap

