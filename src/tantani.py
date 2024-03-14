# mwada(c8)
import argparse
import mecabuni_addud as muud
from collections import defaultdict

outdir = ""

########################################################
def read_out(file, out):
    with open(out, "w") as w:
        with open(file, "r") as f:
            i = 0
            for row in f:
                if (i % 10000) == 0:
                    print(i)
                i+=1
                text = row.rstrip("\n")
                risuto = muud.morph(text)
                line = " ".join(risuto) + "\n"
                w.write(line)
    print(i)

########################################################

def ap():
    parser = argparse.ArgumentParser(description='テキストを分割。空白で区切った状態にする。分割は MeCab + unidic + ユーザ辞書。')
    parser.add_argument('txt', help='txt')
    parser.add_argument('out', help='頻度を追加したtsvを出力')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    read_out(args.txt, args.out)

if __name__ == '__main__':
    main()

