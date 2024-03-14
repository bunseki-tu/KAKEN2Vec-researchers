# mwada(c8)
import argparse

def if_NotFound(t, ele):
    if ele != "NotFound":
        tt = t + " " + ele
    else:
        tt = t
    return tt

def jointkw(text):
    ele = text.rstrip("|||").split("||||")
    line = "、".join(ele)
    return line

def process_line(row):
    ele = row.rstrip("\n").split("\t")
    t = ""
    for e in ele[1:-1]:
        t = if_NotFound(t, e)
    if t == "":
        result = "\n"
    else:
        kwtext = jointkw(ele[-1])
        result = ele[0] + "。" + t[1:] + kwtext  + "\n"
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
    parser = argparse.ArgumentParser(description='TSVを読み込んでNotFound以外を結合する。最後のKWは「、」でつなげる。ただし，TSVの最初と最後以外の要素がNotFoundの場合は改行のみ実施 ')
    parser.add_argument('tsv', help='TSV')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    read_write(args.tsv, args.out)

if __name__ == "__main__":
    main()

