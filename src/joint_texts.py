# mwada(c8)
import argparse

def if_NotFound(t, ele):
    if ele != "NotFound":
        tt = t + " " + ele
    else:
        tt = t
    return tt

def process_line(row):
    ele = row.rstrip("\n").split("\t")
    t = ""
    for e in ele[1:]:
        t = if_NotFound(t, e)
    if t == "":
        result = "\n"
    else:
        result = ele[0] + "\t" + t[1:] + "\n"
    return result

def read_write(file, out):
    with open(out, "w") as w:
        with open(file, "r") as f:
            i = 0
            for row in f:
                i += 1
                if (i % 100000) == 0:
                    print(i)
                text = process_line(row)
                w.write(text)

def ap():
    parser = argparse.ArgumentParser(description='TSVを読み込んでNotFound以外を空白挟んで結合する。ただしTSVの要素のうち最初の要素以外がNotFoundの場合は改行のみ書き込む ')
    parser.add_argument('tsv', help='TSV')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    read_write(args.tsv, args.out)

if __name__ == "__main__":
    main()

