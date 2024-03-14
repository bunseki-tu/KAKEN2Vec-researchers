# mwada(c8)
import argparse
import re
import sys
import numpy as np

import libsetc
import create_d as c_d

from flask import Flask, render_template, request
app = Flask(__name__)

################################################################
def ap():
    parser = argparse.ArgumentParser(description='検索サイト用サーバ起動')
    parser.add_argument('ver', help='どのバージョンのサイトを起動するか選択(unidic_2000)')
    args = parser.parse_args()
    return args

################################################################
# 準備

# 各種ファイルの読み込み，一部はmmapで読み込みメモリを節約
args = ap()
if args.ver == "unidic_2000":
    print("unidic_2000")
    rinfo = libsetc.read_researcher("./data/pi.txt")
    wdic = c_d.read_wdic("./data/w2id_dic.tsv")
    edic, vdic = libsetc.read_precalc("./data/cossim_top50.txt")
    R = np.load("./data/R_l2vec2000.npy", mmap_mode="r")
    elist = libsetc.read_list("./data/rvec_erad.txt")
    Rvecs = np.load("./data/rvec_meanvec.npy", mmap_mode="r")
# 別のバージョンを選択できるようにするならここも編集
# elif args.ver == "":
#     print("")
#     rinfo = libsetc.read_researcher("")
#     wdic = c_d.read_wdic("")
#     edic, vdic = libsetc.read_precalc("")
#     R = np.load("", mmap_mode="r")
#     elist = libsetc.read_list("")
#     Rvecs = np.load("", mmap_mode="r")
else:
    print("select other option")
    sys.exit()


################################################################
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET': # GETされたとき
        searchE = ["", "", ""]
        htmlc = ["", "", "","", "", ""]
        return render_template('index.html', result_list = htmlc, search = searchE)
    elif request.method == 'POST': # POSTされたとき
        poststr = request.form["sterm"]

        if re.match(r"\d{8}", poststr):# 数字8桁なら研究者番号検索
            erad, result, vresult = libsetc.search_erad(poststr, edic, vdic)
            if result == "":
                searchE = [erad, "この研究者番号の研究者は存在しないか検索対象外です", ""]
                htmlc = ["", "", "","", "", ""]
            else:
                htmlc = libsetc.create_htmlresult(erad, result, vresult, rinfo)
                searchE = [erad, rinfo[erad][0], rinfo[erad][1]]

        else:# キーワード検索
            words_list = c_d.process_kwd(poststr)
            id_list = c_d.match_word(words_list, wdic)
            if id_list == []:
                htmlc = ["", "", "","", "", ""]
                searchE = ["（キーワード検索）", poststr, "見つかりませんでした"]
            else:
                Dvecs = c_d.select_vec(R, id_list)
                mD = c_d.mean_vec(Dvecs)
                top_indices, vresult = libsetc.calc_d_Rvec(mD, Rvecs)
                erad = "00000000"
                result = libsetc.mapping_erad(elist, top_indices)
                htmlc = libsetc.create_htmlresult(erad, result, vresult, rinfo)
                searchE = ["（キーワード検索）", poststr, words_list]
        return render_template('index.html', result_list = htmlc, search = searchE)

################################################################

# host, portは下の文書を見ながら決め打ちに
# https://flask.palletsprojects.com/en/3.0.x/quickstart/
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


