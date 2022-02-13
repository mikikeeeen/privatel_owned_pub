import re
import urllib.parse
from bs4 import BeautifulSoup    # importする
import requests

# <a class="list-rst__rst-name-target cpy-rst-name
def test_regexp():
    pattern = r'<a\sclass=\"list-rst__rst-name-target\scpy-rst-name.+</a>'
    # これが正解の正規表現だ!!!
    pattern_all = r'<a\sclass=\"list-rst__rst-name-target\scpy-rst-name\"\starget=\"_blank\"\srel=\"noopener\"\sdata-list-dest=\"item_top\"\shref=\"https.+>.+</a>'
    str_all = '<a class="list-rst__rst-name-target cpy-rst-name" target="_blank" rel="noopener" data-list-dest="item_top" href="https://tabelog.com/tokyo/A1304/A130401/13239063/">肉寿司&amp;ステーキ食べ放題 肉ギャング 新宿東口店</a>'
    str = '<a class="list-rst__rst-name-target cpy-rst-name>test</a>'
    result = re.match(pattern, str)
    result_all = re.match(pattern_all, str_all)
    print(result)
    print('===========================================')
    print(result_all)

def regexp_test_func():
    path = '/Users/mikiken/Desktop/test_scr.txt'
    f = open(path, 'r')
    # ファイルの中身
    file_contents = f.read()
    # 問題となっている正規表現(なおcotediterだとうまくこの正規表現で検索ができる。けどPythonのコード上だとうまくいかない)
    a_link_pattern = r'<a\sclass=\"list-rst__rst-name-target\scpy-rst-name\"\starget=\"_blank\"\srel=\"noopener\"\sdata-list-dest=\"item_top\"\shref=\"https.+>.+</a>'
    result = re.match(a_link_pattern, file_contents)
    print(result)
    print('===============================')
    # 原因がわかったわ！(参考サイト：https://note.nkmk.me/python-re-match-search-findall-etc/)
    # 以下原因となっていた理由
    # ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    # match()は文字列の先頭がパターンにマッチするとマッチオブジェクトを返す。
    # 上述のように、マッチオブジェクトを使ってマッチした部分文字列を抽出したり、単純にマッチしたかどうかをチェックしたりできる。
    # match()が調べるのはあくまでも先頭のみ。先頭にマッチする文字列がない場合はNoneを返す。
    # ~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
    # →→→→→なのでmatchを使うのはやめよう
    result_new = re.findall(a_link_pattern, file_contents)
    print(result_new)

# <a class="list-rst__rst-name-target cpy-rst-name" data-list-dest="item_top" href="https://tabelog.com/tokyo/A1304/A130403/13194360/" rel="noopener" target="_blank">


def test_split():
    str = 'test'
    print(len(str.split(' ')))


def test_scraping_bs4():
    # 該当するaタグが書いてある箇所を集めたリスト
    a_tag_list = []

    load_url = "https://tabelog.com/tokyo/A1304/A130401/R5172/rstLst/?vs=1&sa=%E6%96%B0%E5%AE%BF%E9%A7%85&sk=%25E5%25B1%2585%25E9%2585%2592%25E5%25B1%258B&lid=top_navi1&vac_net=&svd=20220108&svt=1900&svps=2&hfc=1&Cat=RC&LstCat=RC21&LstCatD=RC2101&cat_sk=%E5%B1%85%E9%85%92%E5%B1%8B"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")

    soup = str(soup)
    # なんか帰ってくるaタグの状況が違うのでこちらではscraping_test.pyとは違う正規表現を書いている
    # storelink_pattern = r'<a\sclass=\"list-rst__rst-name-target\scpy-rst-name\"\starget=\"_blank\"\srel=\"noopener\"\sdata-list-dest=\"item_top\"\shref=\"https.+>.+</a>'
    storelink_pattern = r'<a\sclass=\"list-rst__rst-name-target\scpy-rst-name\"\sdata-list-dest=\"item_top\"\shref=\"https.+\"\srel=\"noopener\"\starget=\"_blank\">.+</a>'
    a_tag_list = re.findall(storelink_pattern, soup)
    print(a_tag_list)

    # 後で削除しておいて欲しい部分=======================
    # 取得したソースを別ファイルに出力する
    path = '/Users/mikiken/Desktop/test_scr3.txt'
    f = open(path, 'w')
    # ファイルの中身
    f.write(str(soup))
    # ================================================

if __name__ == '__main__':
    # なんか正規表現のチェックをしてたメソッド
    # test_regexp()
    # なんか正規表現がうまくいかないので色々と試行錯誤をしようと思う
    # regexp_test_func()
    test_split()
    


