# 参考サイト
## 1. 無料のクラウドサーバー上でpython(selenium+cromedriver)を定期実行する方法
https://kurouto.xyz/?p=52

<br>

## 2. Heroku経由のGit pushに失敗する件について
### 2.1 状況
[こちら](https://kurouto.xyz/?p=52)のサイトを参考にして最後のGit pushをしようとしたところ、以下のような状況になって非常に困った。

```
mikiken@miki-no-MacBook-Air-357 privatel_owned_pub % git push heroku main
Enumerating objects: 41, done.
Counting objects: 100% (41/41), done.
Delta compression using up to 8 threads
Compressing objects: 100% (39/39), done.
Writing objects: 100% (41/41), 12.59 MiB | 395.00 KiB/s, done.
Total 41 (delta 15), reused 0 (delta 0), pack-reused 0
remote: Compressing source files... done.
remote: Building source:
remote: 
remote: -----> Building on the Heroku-20 stack
remote: -----> Using buildpacks:
remote:        1. heroku/python
remote:        2. https://github.com/heroku/heroku-buildpack-google-chrome.git
remote:        3. https://github.com/heroku/heroku-buildpack-chromedriver.git
remote: -----> Python app detected
remote: -----> Using Python version specified in runtime.txt
remote:  !     Requested runtime (python==3.8.8) is not available for this stack (heroku-20).
remote:  !     Aborting.  More info: https://devcenter.heroku.com/articles/python-support
remote:  !     Push rejected, failed to compile Python app.
remote: 
remote:  !     Push failed
remote:  !
remote:  ! ## Warning - The same version of this code has already been built: e6c177e375f7d22259d62ef510f270d2201e63e7
remote:  !
remote:  ! We have detected that you have triggered a build from source code with version e6c177e375f7d22259d62ef510f270d2201e63e7
remote:  ! at least twice. One common cause of this behavior is attempting to deploy code from a different branch.
remote:  !
remote:  ! If you are developing on a branch and deploying via git you must run:
remote:  !
remote:  !     git push heroku <branchname>:main
remote:  !
remote:  ! This article goes into details on the behavior:
remote:  !   https://devcenter.heroku.com/articles/duplicate-build-version
remote: 
remote: Verifying deploy...
remote: 
remote: !       Push rejected to privately-owned-pub.
remote: 
To https://git.heroku.com/privately-owned-pub.git
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to 'https://git.heroku.com/privately-owned-pub.git'
```

そこで以下のサイトを参考にしてみた

参考サイト：https://qiita.com/flour/items/985b4628672a85b8e4f3

## ちょっとブラウザが重すぎるからめっちゃここに参考サイトを貼り付けるわ
 - https://kurouto.xyz/?p=52
 - https://deepblue-ts.co.jp/git/git-push-error/
 - https://qiita.com/yuch_i/items/b9898ce482f30ab7ca87
 - https://mebee.info/2020/08/19/post-16968/
 - https://dev.classmethod.jp/articles/protect-branch/


<br>

<br>

# 食べログのURLの構成について
priv_store_search.pyにおいて売っているこのURL

```
https://tabelog.com/tokyo/A1304/A130401/R5172/rstLst/?vs=1&sa=%E6%96%B0%E5%AE%BF%E9%A7%85&sk=%25E5%25B1%2585%25E9%2585%2592%25E5%25B1%258B&lid=top_navi1&vac_net=&svd=20220108&svt=1900&svps=2&hfc=1&Cat=RC&LstCat=RC21&LstCatD=RC2101&cat_sk=%E5%B1%85%E9%85%92%E5%B1%8B
```

これのクエリパラメータのところを変えると検索条件を変えることができるのではないか説が浮上しているので、これを検証する

## 1. まずはこれをデコードしてみた

```
https://tabelog.com/tokyo/A1304/A130401/R5172/rstLst/?vs=1&sa=新宿駅&sk=%E5%B1%85%E9%85%92%E5%B1%8B&lid=top_navi1&vac_net=&svd=20220108&svt=1900&svps=2&hfc=1&Cat=RC&LstCat=RC21&LstCatD=RC2101&cat_sk=居酒屋
```

<br>

## 2. なんかいまいちデコードしきれていないので完全にデコードをした

```
https://tabelog.com/tokyo/A1304/A130401/R5172/rstLst/?vs=1&sa=新宿駅&sk=居酒屋&lid=top_navi1&vac_net=&svd=20220108&svt=1900&svps=2&hfc=1&Cat=RC&LstCat=RC21&LstCatD=RC2101&cat_sk=居酒屋
```

これでわかるのはクエリパラメータとして使っているのは以下のものたち

 - vs=1
 - sa=新宿駅
 - sk=居酒屋
 - lid=top_navi1
 - vac_net=
 - svd=20220108
 - svt=1900
 - svps=2
 - hfc=1
 - Cat=RC
 - LstCat=RC21
 - LstCatD=RC2101
 - cat_sk=居酒屋


## 3.1 新宿駅の部分を渋谷に変えてみた(sa=渋谷駅でやってみた)

ちゃんと渋谷の検索結果が出てきた。scraping_test.pyを動かして抽出できた結果と変わらない。

## 3.2 


<br>

<br>

