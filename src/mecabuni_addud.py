# mwada(c8)
import argparse
import MeCab
from collections import defaultdict

tagger = MeCab.Tagger('-d unidicのある場所を指定 -u 作成したユーザ辞書dicを指定')

########################################################
def text2libsvmstr(text):
    words = morph(text)
    freq = defaultdict(int)
    wordcount = ''
    for word in words:
        freq[word] += 1
    for w, c in sorted(freq.items(), key=lambda x: -x[1]):
        wordcount = wordcount + w + ':' + str(c) + ' '
    return wordcount[:-1]

########################################################

def morph_split(text):
    tagger.parse('')
    pr = tagger.parse(text)
    words = []

    for node in pr.split("\n"):
        if node == "":
            break
        an = node.split("\t")
        if an[0] == 'EOS':
            break

        features = an[1].split(',')

        if (features[0] == "BOS/EOS"):
            pass
        else:
            words.append(an[0])
    return words




def morph(text):
    tagger.parse('')
    pr = tagger.parse(text)
    words = []
    for node in pr.split("\n"):
        if node == "":
            break
        an = node.split("\t")
        word = ''
        if an[0] == 'EOS':
            break

        features = an[1].split(',')
        surface = an[0]
        if len(features) > 8:
            base = features[7] # lemma https://pypi.org/project/unidic/
        else:
            base = "*"

        if base == "*" or base == "":
            word = surface
        else:
            word = base

        if (features[0] == "BOS/EOS"):
            pass
        elif (features[1] == "空白"):
            pass
        elif (features[1] == "読点"):
            pass
        elif (features[1] == "句点"):
            pass
        elif (features[1] == "括弧開"):
            pass
        elif (features[1] == "括弧閉"):
            pass
        elif (word == ","):
            pass
        else:
            if ' ' in word:
                word = word.replace(' ', '_')
            words.append(word)
    return words


########################################################

def ap():
    parser = argparse.ArgumentParser(description='mecabuniに対してユーザ辞書を追加したver。ライブラリ。テキストを入れると形態素(mecab+unidic)に分割してリストを返すmorphと，morphを使ってテキストを入れるとlibsvm likeな形式のストリングを返すtext2libsbmstrの，2つが入っている.追加：単純に分割するだけのmorph_splitを追加')
    args = parser.parse_args()
    return args

def main():
    args = ap()

if __name__ == '__main__':
    main()

