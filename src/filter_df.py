# mwada(c8)
import argparse
import re

##############################################################
def parse_line(line):
    tokens = re.split('[ ]+', line)
    return tokens

def readdf(tsv):
    df = {}
    with open(tsv, "r") as r:
        for line in r:
            nline = line.rstrip("\n").rsplit(":",1)
            df[nline[0]] = int(nline[1])
    return df

def split_wordcount(token):
    pos = token.rfind(':')
    try:
        if (pos>0) and (pos < len(token)-1):
            word, count = token[0:pos], int(token[pos+1:])
            return word, count
        else:
            print("pos error...")
    except:
        print(token)

def read_write(txt, out, delset):
    with open(out, "w") as wf:
        with open(txt, "r") as r:
            for line in r:
                newwc = []
                nline = line.rstrip("\n")
                wordcounts = parse_line(nline)
                for wc in wordcounts:
                    w, c = split_wordcount(wc)
                    if not w in delset:
                        newwc.append(wc)
                if len(newwc) > 0:
                    newline = " ".join(newwc) + "\n"
                else:
                    newline = "\n"
                wf.write(newline)

def hindocheck(dfdic, mindf, maxdf):
    delset = set()
    for k, v in dfdic.items():
        if v >= maxdf or mindf >= v:
            delset.add(k)
    return delset


##############################################################
def ap():
    parser = argparse.ArgumentParser(description='2つのファイルを受け取って，指定したDF以上以下の単語は取り除く')
    parser.add_argument('txt', help='txt')
    parser.add_argument('df', help='df')
    parser.add_argument('mindf',type=int, default=1, help='数字，これ以下のDFの単語は削除する。デフォルトは1')
    parser.add_argument('maxdf',type=int, default=10000000, help='数字，これ以上のDFの単語は削除する。デフォルトは10000000')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    dfdic = readdf(args.df)
    delset = hindocheck(dfdic, args.mindf, args.maxdf)
    read_write(args.txt, args.out, delset)

if __name__ == "__main__":
    main()

