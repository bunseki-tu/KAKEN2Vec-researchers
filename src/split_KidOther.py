# mwada(c8)
import argparse

##################################################

def read_split_write(tsv, pre):
    with open(pre + "_kid.tsv", "w") as wkid:
        with open(pre + "_other.tsv", "w") as wcount:
            with open(tsv, "r") as f:
                for line in f:
                    ele = line.split("\t", 1)
                    wkid.write(ele[0] + "\n")
                    wcount.write(ele[1])

##################################################

def ap():
    parser = argparse.ArgumentParser(description='KIDとそれ以外を分離する')
    parser.add_argument('tsv', help='TSV')
    parser.add_argument('outpre', help='出力するファイル名のプレフィックス')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    read_split_write(args.tsv, args.outpre)

if __name__ == "__main__":
    main()

