# mwada(c8)
import argparse
import re

pat = re.compile(r"^[a-zA-Z0-9_\-]+$")

def eisu_or_one(text):
    i = 0
    if len(text) == 1:
        i = 1
    if pat.search(text):
        i = 1
    if " " in text:
        i = 1
    return i


def read_kw(tsv):
    dic = {}
    with open(tsv, "r") as f:
        i = 0
        j = 0
        for line in f:
            i += 1
            row = line.rstrip("\n").split("\t")
            if eisu_or_one(row[0]) == 0:
                dic[row[0]] = int(row[1])
                j += 1
    print("kw:", i)
    print("kw_z:", j)
    return dic

def read_ph(txt):
    s = set()
    with open(txt, "r") as f:
        i = 0
        j = 0
        for line in f:
            i += 1
            row = line.rstrip("\n")
            if eisu_or_one(row) == 0:
                s.add(row)
                j += 1
    print("ph:", i)
    print("ph:", j)
    return s

def and_or_many(kwdic, phset):
    newset = set()
    for k, v in kwdic.items():
        if v > 99:
            newset.add(k)
        elif k in phset:
            newset.add(k)
    return newset

def write_set(out, nset):
    with open(out, "w") as w:
        for t in nset:
            tl = t + "\n"
            w.write(tl)

def ap():
    parser = argparse.ArgumentParser(description='KAKENのキーワードを抽出したリストと，KAKENのテキストから抽出したフレーズのANDをとって，ANDでのこるorキーワードの出現件数が100以上のキーワードを出力する(1文字のもの，英数字だけのものは除く) ')
    parser.add_argument('kw', help='TSV')
    parser.add_argument('ph', help='phrase')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    kw_dic = read_kw(args.kw)
    ph_set = read_ph(args.ph)
    new_set = and_or_many(kw_dic, ph_set)
    write_set(args.out, new_set)

if __name__ == "__main__":
    main()

