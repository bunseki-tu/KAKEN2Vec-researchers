# mwada(c8)
import argparse
import numpy as np
from collections import defaultdict
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import svds

########################################################################################
# 持橋先生のlda.pyのfmatrix.pyからそのままdocumentクラスと関数を記載
# http://chasen.org/~daiti-m/dist/lda-python/

class document:
    def __init__ (self):
        self.id  = []
        self.cnt = []

def read_svmlight(train):
    print("read data ...")
    data = []
    with open (train, "r") as f:
        for line in f:
            tokens = line.split()
            if len(tokens) > 0:
                doc = document()
                for token in tokens:
                    wid, cnt = token.split(':')
                    doc.id.append(int(wid))
                    doc.cnt.append(int(cnt))
            data.append(doc)
    return data

########################################################################################
# Shifted PPMIの行列を作成 ref:Levy and Goldberg(2014)
# https://papers.nips.cc/paper/2014/file/feab05aa91085b7a8012516bc3533958-Paper.pdf
# SPPMI(d,w) = max(PMI(d,w) - log k,0) 
# k は持橋先生論文を参考に「1」に固定
# http://chasen.org/~daiti-m/paper/nlp2021researcher2vec.pdf
# PMI(d,w) = log(p(d,w) / p(d)p(w)) = log( p(w|d) / p(w))
#               p(w|d):文書内のwの出現数w_d / 文書の総単語数all_d
#               p(w):  文書集合内のwの出現数w_D / 文書集合の総単語数all_D
#          = log( (w_d / all_d) / (w_D / all_D) ) # 除算は遅いはずだが, logのほうがもっと遅いと思うので一部乗算に変形。logのほうが早いなら2つのlogの減算に変形。
#          = log( (w_d * all_D) / (all_d * w_D) )
# coo_matrixを使っていたはずなので，リストを3つ作成

def sppmi_matrix(data):
    print("SPPMI Matrix ...")
    k = 1
    N = len(data) # 文書数
    all_D = 0     # 文書集合の総単語数
    wfreq = defaultdict(int) # 文書集合内のwの出現数
    for doc in data:
        W = len(doc.id) # 文書内の単語の異なり数
        for i in range(W):
            w = doc.id[i]
            c = doc.cnt[i]
            wfreq[w] += c
            all_D    += c

    print("N of Doc:%d" % N)          # 文書数
    print("N of WID:%d" % len(wfreq)) # 文書集合内の単語の異なり数
    sppmi = [] # この3つがcoo_matrix生成用のリスト
    row   = []
    col   = []
    n = 0
    for doc in data:
        W   = len(doc.id)
        all_d = np.sum(doc.cnt)
        for i in range(W):
            wid = doc.id[i]
            w_d = doc.cnt[i]
            w_D = wfreq[wid]
            PMI = np.log( (w_d * all_D) / (all_d * w_D) )
            spmi = PMI - np.log(k)
            if spmi > 0:
                sppmi.append(spmi)
                row.append(n)
                col.append(wid)
        n += 1
    M = coo_matrix((sppmi, (row, col)))
    return M

########################################################################################
# coo_matrixを特異値分解
# 疎行列なのでsvdsでよいはず（これで遅かったらscipy, numpyのライブラリを確認）
# より速くしたいならSVDを行わず，redsvdに実行させる (lightlda.shのイメージ)
# Levy and Goldberg(2014)曰くSymmetric SVDがよいらしいので，これでD, Wを計算
# Symmetric SVD: W = u * sqrt(s), C = v * sqrt(s)

def SymmetricSVD(M, v):
    print("SVD ...")
    u, s, vt = svds(M, k=v)
    D = np.dot(u,    np.diag(np.sqrt(s)))
    W = np.dot(vt.T, np.diag(np.sqrt(s)))
    return D, W

########################################################################################
# save

def save_dw(D, W, out):
    print("save ...")
    np.save(out + "_D.npy", D)
    np.save(out + "_W.npy", W)

########################################################################################

def ap():
    desc_msg = """
    SVMLight類似形式のデータtrainと，次元kを受け取って，
    k次元の文書ベクトルout_D.txtと単語のベクトルout_W.txtを計算し出力する。
    trainの単語IDは「0」はじまりを想定。
    「1」はじまりの場合，単語ベクトルが1行多くなり，
    1行目がどの文書にも出現しなかった単語のベクトルとなる。
    """
    parser = argparse.ArgumentParser(description=desc_msg, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('train', help='読み込むファイル（SVMLight類似形式）')
    parser.add_argument('out', help='出力する2つのファイルのプレフィックス')
    parser.add_argument('-k','--kdim', type=int, default=10, help='次元を指定。デフォルトは10')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    print("start ...")
    data = read_svmlight(args.train)
    M    = sppmi_matrix(data)
    D, W = SymmetricSVD(M, args.kdim)
    save_dw(D, W, args.out)
    print("done.")

if __name__ == "__main__":
    main()

