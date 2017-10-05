# このソフトウェアについて

pygameであみだくじゲームを作った。

ゲームといえるか甚だ疑問。pygameを使った最初の試作品。3週間くらいかかった。

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [pyenv](https://github.com/pylangstudy/201705/blob/master/27/Python%E5%AD%A6%E7%BF%92%E7%92%B0%E5%A2%83%E3%82%92%E7%94%A8%E6%84%8F%E3%81%99%E3%82%8B.md) 1.0.10
    * Python 3.6.1
        * [PyGame](http://ytyaru.hatenablog.com/entry/2018/06/11/000000) 1.9.3
        * [PyGame Utilities(pgu)](http://ytyaru.hatenablog.com/entry/2018/06/19/000000) 0.18
        * [PyOpenGL](http://ytyaru.hatenablog.com/entry/2018/06/15/000000) 3.1.0
        * PyOpenGL_accelerate 3.1.0
        * PyOpenGL_Demo 3.0.0
        * [Pillow](https://pillow.readthedocs.io/en/4.2.x/) 4.2.1
        * [NumPy](http://www.numpy.org/) 1.13.1

## ライブラリ

```sh
$ pip freeze > requirements.txt
```
requirements.txt
```
numpy==1.13.1
olefile==0.44
pgu==0.18
Pillow==4.2.1
pygame==1.9.3
PyOpenGL==3.1.0
PyOpenGL-accelerate==3.1.0
PyOpenGL-Demo==3.0.0
```

## ライブラリの一括インストール

```sh
$ pip install -r requirements.txt
```

（このアプリで使っているのは`pygame`だけのはずなので他は不要かもしれない）

https://docs.python.jp/3/tutorial/venv.html#managing-packages-with-pip

# 実行

```sh
$ cd src
$ python Main.py
```

操作キー|説明
--------|----
ESC|終了する。
←,A|カーソルを左に移す
→,D|カーソルを右に移す
Z,Space,Enter|決定する（カーソル決定、アニメーション省略、あみだくじ再開）

# 概要

あみだくじゲーム。

http://ytyaru.hatenablog.com/entry/2018/06/27/000000

## pygame

* メインループ
* イベント処理（キーボード入力）
* 描画
    * 線
        * pygame.draw.line(...)
        * pygame.draw.lines(...)
    * 文字列
        * screen.blit(font.render(...))

## ゲームとしての最低限要素

* 結果の分岐（ランダム）
* インタラクティブ性（ユーザとシステムの対話）
* 演出（選択から結果までのアニメーション）

# 課題

* コードを綺麗にしたい
    * `Initialize`, `Finalize`フレームワークが使われていない
    * CalcSizeでCursor文字を参照できないからハードコーディングしている
    * GameCommand内にStateに参照させる必要のない描画メソッドがある(`DrawGhostleg`, `DrawCursor`)
* アニメーション強制終了するとき瞬時に完了しない
* 結果表示時、何らかの演出が欲しい（効果音等）

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

以下、利用させていただいたもの。感謝。

## ライブラリ

Library|License|Copyright
-------|-------|---------
[pygame](http://www.pygame.org/)|[LGPL](https://www.pygame.org/docs/)|[pygame](http://www.pygame.org/)

## フォント

Font|License|Copyright
----|-------|---------
[M+](http://mplus-fonts.osdn.jp/about.html)|[Free](http://mplus-fonts.osdn.jp/about.html)|[M+](http://mplus-fonts.osdn.jp/about.html)
[美咲フォント](http://www.geocities.jp/littlimi/misaki.htm#download)|[Free](http://www.geocities.jp/littlimi/font.htm)|[美咲フォント](http://www.geocities.jp/littlimi/font.htm)

