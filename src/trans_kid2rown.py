# mwada(c8)
import argparse

def read_klist(klist):
    dic = {}
    with open(klist, "r") as f:
        i = 0
        for row in f:
            kid = row.rstrip("\n")
            dic[kid] = i
            i += 1
    return dic

def read_ktsv(tsv, dic):
    kdic = {}
    with open(tsv, "r") as f:
        for row in f:
            rid, kids = row.rstrip("\n").split("\t")
            for kid in kids.split("||"):
                if kid not in dic:
                    continue
                if rid in kdic:
                    kdic[rid] = kdic[rid] + "||" + str(dic[kid])
                else:
                    kdic[rid] = str(dic[kid])
    return kdic

def write_dic(dic, out):
    with open(out, "w") as w:
        for k,v in dic.items():
            line = k + "\t" + v + "\n"
            w.write(line)

def ap():
    parser = argparse.ArgumentParser(description='課題を行番号に変換')
    parser.add_argument('tsv', help='研究者ー課題一覧のTSV')
    parser.add_argument('klist', help='ベクトルと対応した課題リスト')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    dic = read_klist(args.klist)
    rdic = read_ktsv(args.tsv, dic)
    write_dic(rdic, args.out)


if __name__ == "__main__":
    main()

