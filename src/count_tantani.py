# mwada(c8)
import argparse
from collections import defaultdict

def hindo(text):
    d = defaultdict(int)
    tlist = text.split(" ")
    for t in tlist:
        d[t] += 1
    return d

def dic2line(d):
    line = ""
    for k, v in sorted(d.items(), key= lambda x:x[1], reverse=True ):
        line = line + k + ":" + str(v) + " "
    return line[:-1]

def dfcount(df, hindo):
    for k, v in hindo.items():
        df[k] += 1
    return df


########################################################
def read_out(file, out):
    with open(out + "_count.txt", "w") as wc:
        with open(file, "r") as f:
            i = 0
            df = defaultdict(int)
            for row in f:
                if (i % 100000) == 0:
                    print(i)
                i+=1
                text = row.rstrip("\n")
                hindodic = hindo(text)
                line = dic2line(hindodic)
                df = dfcount(df, hindodic)
                wc.write(line + "\n")
    with open(out + "_df.txt", "w") as wd:
        for k, v in sorted(df.items(), key= lambda x:x[1], reverse=True ):
            line = k + ":" + str(v)
            wd.write(line + "\n")
    print(i)

########################################################

def ap():
    parser = argparse.ArgumentParser(description='空白区切りの短単位を受け取って，頻度をカウントしlibsvm likeなフォーマットで出力し，DFカウントした辞書もだす')
    parser.add_argument('tsv', help='tsv')
    parser.add_argument('out', help='out, pre')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    read_out(args.tsv, args.out)

if __name__ == '__main__':
    main()

