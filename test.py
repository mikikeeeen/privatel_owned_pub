import re

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

def test_split():
    str = 'test'
    print(len(str.split(' ')))

if __name__ == '__main__':
    # なんか正規表現のチェックをしてたメソッド
    # test_regexp()
    # なんか正規表現がうまくいかないので色々と試行錯誤をしようと思う
    # regexp_test_func()
    test_split()
    


