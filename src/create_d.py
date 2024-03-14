# mwada(c8)
import argparse
import re
import numpy as np
import mecabuni_addud as mua
import normalize_textnonid as nm

pat = re.compile("\*+$") # 記号*が1つ以上でその次が文末


# 単語IDと単語の辞書
def read_wdic(wdic):
    dic = {}
    with open(wdic, "r") as f:
        for row in f:
            wid, word = row.rstrip("\n").split("\t")
            dic[word] = int(wid)
    return dic


# 検索キーワードを処理，単語のリストを返す
def process_kwd(kwds):
    list_kwds = kwds.split()
    Lkwd = []
    for kwd in list_kwds:
        asu = pat.search(kwd) # *の個数分増やす処理
        if asu:
            i = len(asu.group()) + 1
            kwd = kwd.rstrip("*")
        else:
            i = 1
        Lkwd = Lkwd + [kwd]*i
    Skwd = "。".join(Lkwd)
    words = mua.morph(Skwd)
    twords = "，".join(words)
    ws = nm.normalizes(twords, "nyy").split("，")
    return ws


# 単語から単語IDへの変換
def match_word(words_list, wdic):
    id_list = []
    for word in words_list:
        if word in wdic:
            id_list.append(wdic[word])
    return id_list

# 単語IDからRの該当箇所を取り出す
def select_vec(R, id_list):
    i = 0
    for id in id_list:
        if i == 0:
            Dvecs = R[:,id]
            i += 1
        else:
            Dvecs = np.vstack([Dvecs, R[:,id]])
    return Dvecs

# ベクトルの平均を計算
def mean_vec(Dvecs):
    if Dvecs.ndim == 1:
        mvec = Dvecs
    else:
        mvec = np.mean(Dvecs, axis=0)
    return mvec


###############################################################
def ap():
    parser = argparse.ArgumentParser(description='キーワード（複数も対応）から検索用ベクトルdを作成')
    parser.add_argument('kwd', help='キーワード（複数の場合は__でくっついている）')
    parser.add_argument('R', help='例のR')
    parser.add_argument('Wdic', help='単語ID辞書')
    parser.add_argument('out', help='出力')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    print("read Widc ...")
    wdic = read_wdic(args.Wdic)
    print("process KWD ...")
    words_list = process_kwd(args.kwd)
    print(words_list)
    print("match word ...")
    id_list = match_word(words_list, wdic)
    print("read R ...")
    R = np.loadtxt(args.R)
    if id_list == []:
        print("not found")
    else:
        print("select vec ...")
        Dvecs = select_vec(R, id_list)
        mD = mean_vec(Dvecs)
        print(mD)
        print(mD.shape)

if __name__ == "__main__":
    main()

