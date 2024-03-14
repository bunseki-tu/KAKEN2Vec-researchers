# mwada(c8)
import argparse

def read_write(tsv, out):
    with open(out, "w") as w:
        with open(tsv, "r") as f:
            for row in f:
                ele = row.split("\t")
                if len(ele) < 3:
                    print(ele)
                    continue
                if ele[2] == "principal_investigator":
                    w.write(row)

def ap():
    parser = argparse.ArgumentParser(description='研究組織のtsvを受け取ったら役割がPIのもののみに限定')
    parser.add_argument('tsv', help='TSV')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    read_write(args.tsv, args.out)

if __name__ == "__main__":
    main()

