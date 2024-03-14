# mwada(c8)
import argparse

def read_kadaitsv(tsv):
    dic = {}
    with open(tsv, "r") as f:
        for row in f:
            kid, rid, other = row.split("\t", 2)
            if rid in dic:
                dic[rid] = dic[rid] + "||" +kid
            else:
                dic[rid] = kid
    return dic

def write_dic(dic, out):
    with open(out, "w") as w:
        for k,v in dic.items():
            line = k + "\t" + v + "\n"
            w.write(line)

def ap():
    parser = argparse.ArgumentParser(description='研究者ごとの課題一覧を作成')
    parser.add_argument('tsv', help='課題研究者のTSV')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    dic = read_kadaitsv(args.tsv)
    write_dic(dic, args.out)


if __name__ == "__main__":
    main()

