# mwada(c8)
import argparse
import csv
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
    cw = csv.writer(tsv, delimiter = '\t', lineterminator = '\n')
    writelist = read_xml(xml, year)
    cw.writerows(writelist)

# TSVで出力するので，紛らわしいタブや改行を削除。他も消したかったらここに追加
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

def try_xpathtext(target, tag):
    try:
        result = target.xpath(tag)[0].text
        if result == "":
            result = "NotFound"
    except:
        result = "NotFound"
    return result

def text_from_paraL(paraL):
    text = ""
    for para in paraL.xpath("paragraph"):
        t = para.text
        newt = delete_tabetc(t)
        text = text + newt
    return text

# XMLから取り出したい要素があるならここを修正
def read_xml(xml, year):
    tree = etree.parse(xml)
    nsmap = {"xml": "http://www.w3.org/XML/1998/namespace"}
    kadailist = []
    for gA in tree.xpath('/grantAwards/grantAward'):
        # 必須（のはず）の要素
        awardid = try_att(gA,"id") # 科研費の課題番号ではないが，出現回数1固定なのでこれにした

        # 課題名
        title = try_xpathtext(gA, "summary[@xml:lang='ja']/title")

        # 研究課題ステータスが完了or採択or交付に限定
        st = gA.xpath("summary[@xml:lang='ja']/projectStatus")
        if st == []:
            scode = "NotFound"
        else:
            scode = try_att(st[0], "statusCode")
        if scode != "adopted" and scode != "project_closed" and scode != "granted":
            continue

        # summaryから以下を取得
        #    purpose
        #    abstract
        #    outline of research initial
        #    outline of research performance
        #    outline of research achievement
        purpose = "NotFound"
        abstract = "NotFound"
        initial = "NotFound"
        performance = "NotFound"
        achieve = "NotFound"
        j = 0
        for paraL in gA.xpath("summary[@xml:lang='ja']/paragraphList"):
            paratype = try_att(paraL, "type")
            if paratype == "purpose":
                purpose = text_from_paraL(paraL)
                j = 1
            if paratype == "abstract":
                abstract = text_from_paraL(paraL)
                j = 1
            if paratype == "outline_of_research_initial":
                initial = text_from_paraL(paraL)
                j = 1
            if paratype == "outline_of_research_performance":
                performance = text_from_paraL(paraL)
                j = 1
            if paratype == "outline_of_research_achievement":
                achieve = text_from_paraL(paraL)
                j = 1
        if j == 0:
            continue
        row = [awardid, title, purpose, abstract, initial, performance, achieve]
        kadailist.append(row)
    return kadailist

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
    parser = argparse.ArgumentParser(description='KAKENから課題番号とテキスト（課題名や研究開始時の研究の概要など）を抽出する。開始年度のみ指定可能。')
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

