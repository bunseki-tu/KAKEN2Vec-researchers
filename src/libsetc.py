# mwada(c8)
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 事前に計算した類似研究者ファイルの読み込み
def read_precalc(pre):
    eraddic = {}
    valuedic = {}
    with open(pre, "r") as f:
        for row in f:
            eraddic, valuedic = process_line(row, eraddic, valuedic)
    return eraddic, valuedic

# 上記読み込み時の各行の処理
def process_line(row, edic, vdic):
    erad, result, vs = row.rstrip("\n").split("\t")
    r = result.split("||")
    v = vs.split("||")
    edic[erad] = r
    vdic[erad] = v
    return edic, vdic

# 研究者情報の読み込み
def read_researcher(file):
    dic = {}
    with open(file, "r") as f:
        for row in f:
            ele = row.split("\t")
            dic[ele[1]] = [ele[2], ele[5]]
    return dic

# 研究者番号検索がきた場合の処理
def search_erad(erad, edic, vdic):
    if erad in edic:
        result = edic[erad]
        vresult = vdic[erad]
    else:
        result = ""
        vresult = ""
    return erad, result, vresult

# 検索結果のHTMLを作成
def create_htmlresult(erad, result, vresult, rinfo):
    htmlc = []
    for i in range(len(result)):
        RI = rinfo[result[i]]
        kaken = "https://nrid.nii.ac.jp/ja/nrid/10000" + result[i] # KAKENのリンク
        row = [str(i), vresult[i][:5], result[i], RI[0], RI[1], kaken]
        htmlc.append(row)
    return htmlc

# キーワード検索時，キーワードのベクトルdと研究者ベクトルRvecのコサイン類似度計算して上位を返す
def calc_d_Rvec(d, Rvec):
    rnum = 50
    cossim = cosine_similarity(d.reshape(1, -1), Rvec)[0]
    top_indices = np.argsort(cossim)[::-1][:rnum]
    top_value = np.sort(cossim)[::-1][:rnum]
    values = [str(n) for n in top_value]
    return top_indices, values

# 研究者番号と行番号の対応
def mapping_erad(elist, indices):
    erads = []
    for rindex in indices:
        erads.append(elist[rindex])
    return erads

# リストの読み込み
def read_list(file):
    list = []
    with open(file, "r") as f:
        for row in f:
            e = row.rstrip("\n")
            list.append(e)
    return list


###############################################################

def main():
    print("検索サイト用のメソッドをまとめている")
    print("これだけではうごかない")

if __name__ == "__main__":
    main()

