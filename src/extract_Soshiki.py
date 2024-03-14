# mwada(c8)
import argparse
import csv
import glob
import os
from lxml import etree
from multiprocessing import Pool

outdir = ""

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

def read_write(xml, tsv):
    cw = csv.writer(tsv, delimiter = '\t', lineterminator = '\n')
    writelist = read_xml(xml)
    cw.writerows(writelist)

# TSVで出力するので，紛らわしいタブや改行を削除。他も消したかったらここに追加。
def delete_tabetc(text):
    new_text = text.replace('\t',' ').replace('\n',' ')
    return new_text

def check_len(x):
    if len(x) == 0:
        return "NA"
    else:
        return x[0].text


def try_att(target, att):
    try:
        result = target.attrib[att]
        if result == "":
            result = "NotFound"
    except:
        result = "NotFound"
    return result


# XMLから取り出したい要素があるならここを修正してください。
def read_xml(xml):
    tree = etree.parse(xml)
    nsmap = {"xml": "http://www.w3.org/XML/1998/namespace"}
    kadailist = []
    for gA in tree.xpath('/grantAwards/grantAward'):
        # 必須（のはず）の要素
        # awardnumber = gA.attrib["awardNumber"] # 20190722 頻度が1..1から0..1になったらしい。ないのもある？
        awardid = try_att(gA,"id") # 単純な科研費の課題番号ではないが，出現回数1固定なのでコレにした

        # この先が研究組織。一人一行なので行数は課題数の数倍になる
        # 研究者番号がない場合，その後扱えないのでなかったら飛ばす

        members = gA.xpath("./summary[@xml:lang='ja']/member")
        for m in members:
            try:
                erad = m.attrib["eradCode"]
            except:
                continue
                #erad = "NA"
            try:
                role = m.attrib["role"]
            except:
                role = "NA"
            institution = check_len(m.xpath("./institution"))
            department  = check_len(m.xpath("./department"))
            jobtitle    = check_len(m.xpath("./jobTitle"))
            fullname    = check_len(m.xpath("./personalName/fullName"))
            row = [awardid,
                    erad,
                    role,
                    institution,
                    department,
                    jobtitle,
                    fullname
                ]
            kadailist.append(row) # research_collaborator（研究協力者は消すか迷ったが，今回はまだ入れておく）
    return kadailist


def single_process(xmlfile):
    global outdir
    print(xmlfile + " ...")
    filename = xmlfile.rsplit("/", 1)
    name = filename[1].rsplit(".", 1)
    outfile = outdir + name[0] + ".tsv"
    with open(xmlfile, "r") as xml:
        with open(outfile, "w") as tsv:
            read_write(xml, tsv)

# 並列処理。スレッド数-1で実行するようになっている。
# =>訂正，今は４スレッドに決め打ち（LDAが動いているため）
def multi_process(xmlfiles):
    numfile = len(xmlfiles)
    print('NumFile: %d' % numfile)
    #core = os.cpu_count() - 1
    core = 4
    print('Using thred: %d' % core)
    p = Pool(core)
    p.map(single_process, xmlfiles)
    p.terminate()
    p.join()

def ap():
    parser = argparse.ArgumentParser(description='KAKENのXMLをばらして研究組織をTSVで取り出す。範囲指定の年をいれない場合，2015-2020のXMLが対象になる。')
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

if __name__ == '__main__':
    main()

