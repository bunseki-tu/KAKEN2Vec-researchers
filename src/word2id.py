# mwada(c8)
import argparse
import re
from collections import defaultdict

wordid = defaultdict(lambda: len(wordid)) # 1+len...と修正すると idは1はじまりとなる

##################################################
def write_iddic(outpre):
    with open(outpre + "_dic.tsv", "w") as f:
        for word, id in sorted(wordid.items(), key=lambda x: x[1], reverse=False):
            f.write("%d\t%s\n" % (id, word))

##################################################
def process(tsv, outpre):
    with open(outpre + "_idcount.dat", "w") as wid:
        with open(tsv, "r") as f:
            for line in f:
                nline = line.rstrip("\n")
                tokens = parse_line(nline)
                if len(tokens) > 0:
                    write_tokens(nline, wid)

def parse_line(line):
    tokens = re.split('[ ]+', line)
    return tokens

def write_tokens(tokens, wid):
    for w, c in wordfreqs(tokens):
        wid.write("%d:%d " % (wordid[w], c))
    wid.write("\n")

def wordfreqs(line):
    if line[-1] == '"':
        line = line[:-1]
    tokens = parse_line(line)
    try:
        for token in tokens:
            pos = token.rfind(':')
            if (pos>0) and (pos < len(token)-1):
                word, count = token[0:pos], int(token[pos+1:])
                yield(word, count)
    except:
        print("\ntoken= |%s|" % token)
        return

##################################################

def ap():
    parser = argparse.ArgumentParser(description='単語頻度をID頻度に変換。変換辞書も同時に作成。idは0はじまり')
    parser.add_argument('tsv', help='TSV')
    parser.add_argument('outpre', help='出力するファイル名のプレフィックス')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    process(args.tsv, args.outpre)
    write_iddic(args.outpre)

if __name__ == "__main__":
    main()

