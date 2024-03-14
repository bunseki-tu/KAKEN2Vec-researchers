# mwada(c8)
import argparse
import sys
import glob

def tsv_list(path):
    path = path + "*.tsv"
    files = glob.glob(path)
    return files

def read_write_one(tsvs, out):
    with open(out, "w") as of:
        for tsv in tsvs:
            with open(tsv, "r") as f:
                rw_one(f, of)

def rw_one(f, of):
    for line in f:
        if line != "":
            of.write(line)

# catでもよい
def ap():
    parser = argparse.ArgumentParser(description='TSVをひとつのファイルに結合する。空の行は削除')
    parser.add_argument('tsvdir', help='TSVの入ったディレクトリ')
    parser.add_argument('out', help='出力するファイル名')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    tsvs = tsv_list(args.tsvdir)
    out = args.out
    read_write_one(tsvs, out)

if __name__ == "__main__":
    main()

