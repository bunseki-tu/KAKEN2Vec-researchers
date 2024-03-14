# mwada(c8)
import argparse
import mecabuni as mu

########################################################
def wakati_write(file, out):
    with open(out, "w") as mw:
        with open(file, "r") as f:
            i = 0
            for row in f:
                if (i % 100000) == 0:
                    print(i)
                i+=1
                kid, text = row.rstrip("\n").split("\t")
                wakati = mu.morph_split(text)
                write_middle(wakati, mw)
            print(i)

def write_middle(wakati, mw):
    line = " ".join(wakati) + "\n"
    mw.write(line)

########################################################

def ap():
    parser = argparse.ArgumentParser(description='IDとテキストが入っているTSVを取り込んで，テキストをMeCabで分かち書きして出力。IDは消える')
    parser.add_argument('tsv', help='tsv')
    parser.add_argument('out', help='分かち書きした結果を書き込むファイル')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    wakati_write(args.tsv, args.out)
    print("end ...")

if __name__ == '__main__':
    main()

