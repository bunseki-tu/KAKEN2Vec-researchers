# mwada(c8)
import argparse

##################################################

def ex_phrase(file, out):
    phrases = set()
    with open(file, "r") as f:
        for line in f:
            words = line.rstrip("\n").split()
            phrases = addp(words, phrases)
    with open(out, "w") as w:
        for phrase in phrases:
            w.write(phrase.replace("_", "") + "\n")

def addp(words, phrases):
    for w in words:
        if '_' in w:
            phrases.add(w)
    return phrases

##################################################

def ap():
    parser = argparse.ArgumentParser(description='phraser.pyで作ったファイルからフレーズを抽出する')
    parser.add_argument('file', help='input file')
    parser.add_argument('out', help='output file')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    ex_phrase(args.file, args.out)
    print("end ...")

if __name__ == "__main__":
    main()

