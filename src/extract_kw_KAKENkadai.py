# mwada(c8)

import argparse
import glob
import os
from lxml import etree
from multiprocessing import Pool

outdir = ""

##########################################
# 出力先の確認と，抽出対象のXMLのリストを作成
def check_outdir(outpath):
    path = check_slash(outpath)
    global outdir
    outdir = path

def check_slash(text):
    c = text[-1]
    if c != "/":
        text = text + "/"
    return text

def list_xmlfile(path, fy, ty):
    path = check_slash(path)
    xmlfiles = []
    for i in range(fy, ty + 1):
        fullpath = path + str(i) + "_*.xml"
        files = glob.glob(fullpath)
        xmlfiles.extend(files)
    return xmlfiles

##########################################
def read_write(xml, tsv, year):
    read_xml(xml, year, tsv)

# タブ区切りで出力するので，紛らわしいタブや改行を削除。他も消したかったらここに追加
def delete_tabetc(text):
    new_text = text.replace('\t',' ').replace('\n',' ')
    return new_text

# 見つからない場合，NAを返すため
def try_att(target, att):
    try:
        result = target.attrib[att]
        if result == "":
            result = "NotFound"
    except:
        result = "NotFound"
    return result

# XMLから取り出したい要素があるならここを修正
def read_xml(xml, year, w):
    tree = etree.parse(xml)
    nsmap = {"xml": "http://www.w3.org/XML/1998/namespace"}
    kadailist = []
    for gA in tree.xpath('/grantAwards/grantAward'):
        # 必須（のはず）の要素
        awardid = try_att(gA,"id") # 科研費の課題番号ではないが，出現回数1固定なのでコレにした
        kwL = gA.xpath("summary[@xml:lang='ja']/keywordList/keyword") # keywordを取り出す
        if kwL == []:
            continue
        else:
            text = ""
            for kw in kwL:
                t = kw.text
                newt = delete_tabetc(t)
                text = text + newt + "\t"
        text = text[:-1] + "\n"
        #row = [awardid, text]
        #kadailist.append(row)
        w.write(text)

#######################################################
##   処理を並列でやるか否か

# 個々のプロセス
def single_process(xmlfile):
    global outdir
    print(xmlfile + " ...")
    filename = xmlfile.rsplit("/", 1)
    name = filename[1].rsplit(".", 1)
    outfile = outdir + name[0] + ".tsv"
    syear = name[0].split("_")[0]
    with open(xmlfile, "r") as xml:
        with open(outfile, "w") as tsv:
            read_write(xml, tsv, syear)

# 並列処理。スレッド数-1,もしくは固定で実行するようになっている。
def multi_process(xmlfiles):
    numfile = len(xmlfiles)
    print('NumFile: %d' % numfile)
    core = os.cpu_count() - 1
    #core = 4
    print('Using thred: %d' % core)
    p = Pool(core)
    p.map(single_process, xmlfiles)
    p.terminate()
    p.join()

# 検証用。並列処理だとエラー特定が面倒になるので，シングルで動かす。
def Not_multi_process(xmlfiles):
    for xml in xmlfiles:
        single_process(xml)

#######################################################

def ap():
    parser = argparse.ArgumentParser(description='KAKENの課題データxmlからKeywordを抽出する。開始年度のみ指定可能。並列で動く。')
    parser.add_argument('xmldir', help='XMLの入ったディレクトリ')
    parser.add_argument('outdir', help='tsvを出力するディレクトリ')
    parser.add_argument('-f', '--fromYear', type=int, default=2015, help='開始年度の範囲指定：ここから')
    parser.add_argument('-t', '--toYear', type=int, default=2020, help='開始年度の範囲指定：ここまで')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    xmllist = list_xmlfile(args.xmldir, args.fromYear, args.toYear)
    check_outdir(args.outdir)

    multi_process(xmllist)
    #Not_multi_process(xmllist) # 検証用

if __name__ == '__main__':
    main()

