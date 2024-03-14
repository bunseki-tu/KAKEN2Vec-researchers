# mwada(c8)
import argparse

def read_current(current):
    cset = set()
    with open(current, "r") as f:
        for row in f:
            cu, rid, other = row.split("\t", 2)
            cset.add(rid)
    return cset

def process_kadai(soshiki, cset, out):
    with open(out, "w") as w:
        with open(soshiki, "r") as f:
            for row in f:
                process_line(row, cset, w)

def process_line(row, cset, w):
    kid, rid, other = row.split("\t",2)
    if rid in cset:
        w.write(row)

def ap():
    parser = argparse.ArgumentParser(description='研究組織を抽出した課題を，カレントありの研究者一覧で絞り込む')
    parser.add_argument('soshiki', help='組織TSV')
    parser.add_argument('current', help='currentのリスト')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    cset = read_current(args.current)
    process_kadai(args.soshiki, cset, args.out)



if __name__ == "__main__":
    main()

