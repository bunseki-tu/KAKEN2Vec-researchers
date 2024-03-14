# mwada(c8)
import argparse
import neologdn
import re

pat = re.compile(r'[0-9０-９]')
pat_maru = re.compile(r'[①-⑨]')

def read_write(file, out, nop):
    with open(out, "w") as w:
        with open(file, "r") as f:
            i = 0
            for row in f:
                if (i % 10000) == 0:
                    print(i)
                i += 1
                ele = row.rstrip("\n").split("\t")
                tt = normalizes(ele[1], nop)
                line = ele[0] + "\t" + tt + "\n"
                w.write(line)
    print(i)

def normalizes(t, nop):
    if nop[0] == "y":
        t1 = neologdn.normalize(t)
    else:
        t1 = t
    if nop[1] == "y":
        t2 = n_normalize(t1)
    else:
        t2 = t1
    if nop[2] == "y":
        t3 = upper2lower(t2)
    else:
        t3 = t2
    return t3

def n_normalize(t):
    t1 = re.sub(pat, '0', t)
    t2 = re.sub(pat_maru, '(0)', t1)
    return t2

def upper2lower(t):
    tl = t.lower()
    return tl

def ap():
    parser = argparse.ArgumentParser(description='1列目ID，2列目日本語文書のTSVを受け取り，文書を正規化（neologdn，数字の統一，アルファベットの大文字小文字）')
    parser.add_argument('tsv', help='TSV')
    parser.add_argument('nop', help='正規化のオプション。3文字でnynというように実施する字はyしない字はn，1文字目：neologdnの統一，2文字目：数字の統一，3文字目：アルファベットの大文字小文字')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    if len(args.nop) == 3:
        read_write(args.tsv, args.out, args.nop)
    else:
        print("normalize option error")

if __name__ == "__main__":
    main()

