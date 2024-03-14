# mwada(c8)
import argparse
from collections import defaultdict

def read_kw(txt):
    d = defaultdict(int)
    with open(txt, "r") as r:
        for line in r:
            kwlist = line.rstrip("\n").split("\t")
            for kw in kwlist:
                d[kw] += 1
    return d

def write_d(out, d):
    with open(out, "w") as w:
        for k, v in sorted(d.items(), key = lambda x:x[1], reverse=True):
            line = k + "\t" + str(v) + "\n"
            w.write(line)

def ap():
    parser = argparse.ArgumentParser(description='タブ区切りのKWファイルを読み込んで，DF（出現した行数）をカウントして，多い順にソートして出力')
    parser.add_argument('txt', help='txt')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    kw_df = read_kw(args.txt)
    write_d(args.out, kw_df)

if __name__ == "__main__":
    main()

