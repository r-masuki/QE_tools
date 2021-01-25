# README

## 概要
Quantum Espressoの出力からデータを読み込むスクリプトの集合。

## 全エネルギー
### read_energy_log.py
#### 概要
scf計算の全エネルギーの変化を調べるスクリプト。scf計算の出力ファイルからiterationごとの全エネルギーの計算結果を読み出し、ファイルに
```
$ (iteration数) (全エネルギー)
```
の形で書き出す。

#### 実行方法
scf計算のアウトプット(pw.material.scf.outとする)と読み出した結果を出力したいファイル名(energy_log.txtとする)をコマンドライン引数で与えて
```
$ python3 read_energy_log.py pw.material.scf.out energy_log.txt
```
で実行する。

## band計算

### make_band_xtics.py
#### 概要
band計算の結果とインプットファイルから、high symmetry pointsの名前と出力データにおけるx座標を読み出し、gnuplotのxticsの行を作る。

#### 実行方法
band計算のインプット(pw.material.band.inとする)と、bands.xのアウトプット(bands.material.outとする)と、xticsを出力したいファイル名(xtics.txtとする)を
コマンドライン引数で与えて、
```
$ python3 make_band_xtics.py pw.material.band.in bands.material.out xtics.txt
```
として実行する。
出力ファイルは、以下のようにgnuplotのx軸の目盛りを指定するコマンド行が出力される。
```
set xtics ("" G" 0.0000, " Y" 0.2049, ...)
```

#### 仮定
pw.material.band.inでは、K_POINTS(必ず大文字)の行の次にk点の数、続けてk点の情報が書いてあることを仮定している。
!を区切り文字としてk点の名前を読んでいるので、行の最後の!の後にスペースを入れずにK点の名前を書き込んでおく必要がある。
(スペースを入れても問題なく動くが、k点の名前の先頭にスペースが入る)
また、このk点のリストがファイルの末尾に書いてある必要がある。
```
K_POINTS {crystal_b}
14
   0.0000000000     0.0000000000     0.0000000000   7  !{/Symbol G}
   0.0000000000     0.0000000000     0.5000000000   10  !Y
   ...
```

## Phonon
### make_ph_kpath.py

#### 概要
PHononのmatdyn.xでphonon bandを計算する際のkpathを生成するプログラム。

#### 実行方法
kpathを生成する以下のようなinput fileを作成する。
```
   0.0000000000     0.0000000000     0.0000000000   20  {/Symbol_G}
   0.5000000000     0.0000000000     0.0000000000   20  X
   0.5000000000    -0.5000000000     0.0000000000   20  M
   0.0000000000     0.0000000000     0.0000000000   20  {/Symbol_G}
   0.5000000000    -0.5000000000     0.5000000000   20  R
   0.5000000000    -0.5000000000     0.0000000000   20  M
```
このinput fileの名前をkpath.txtとすると、
```
$ python3 make_ph_kpath.py kpath.txt
```
でプログラムを実行できる。プログラムを実行すると、matdyn.xのインプットファイル用のkpathがph_kpath.txtに書き出される。また、plotでxticsを指定するコマンドがxtics.txtに書き出される。

#### 注意事項
input fileを作成するときは以下の点に注意が必要である。
1. 最終行のあとは改行などが入っていはいけない。
2. 行を読み込んでスペースで分割するので、kpathの名前はスペースを含んではいけない。スペースを含む場合は、_を入れておけば自動的にスペースで置換される。(_は使えないので、後で仕様を変えるかもしれない。)