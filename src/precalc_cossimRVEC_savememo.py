# mwada(c8)
import argparse
import numpy as np
from numpy.core.fromnumeric import sort
from sklearn.metrics.pairwise import cosine_similarity

###############################################################
def read_list(file):
    list = []
    with open(file, "r") as f:
        for row in f:
            e = row.rstrip("\n")
            list.append(e)
    return list


###############################################################
def calc_and_save_rvecs(rvec, elist, w):
    loop = 0
    rnum = 50
    #indexdic = {}
    #valuedic = {}
    N, V = rvec.shape
    for i in range(N):
        loop += 1
        if (loop % 100) == 0:
            print(loop)
        evec = rvec[i,:]
        cossim = cosine_similarity(evec.reshape(1, -1), rvec)[0]
        top_indices = np.argsort(cossim)[::-1][:rnum]
        top_value = np.sort(cossim)[::-1][:rnum]
        # mapping
        erad, erads = mapping_erads(i, elist, top_indices)
        # write
        line = erad + "\t" + "||".join(erads) + "\t" + "||".join([str(n) for n in top_value]) + "\n"
        w.write(line)

def mapping_erads(i, elist, tindex):
    erad = elist[i]
    erads = []
    values = []
    for rindex in tindex:
        erads.append(elist[rindex])
    return erad, erads

#def save_dics(eraddic, valuedic, out):
#    with open(out, "w") as w:
#        for k, v in eraddic.items():
#            line = k + "\t" + "||".join(v) + "\t" + "||".join([str(n) for n in valuedic[k]]) + "\n"
#            w.write(line)

###############################################################
def ap():
    parser = argparse.ArgumentParser(description='研究者ベクトルの類似上位50人を事前計算')
    parser.add_argument('rvec', help='研究者ベクトル')
    parser.add_argument('eradlist', help='ベクトルに対応するeradリスト')
    parser.add_argument('out', help='出力')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    print("read rvec ...")
    rvec = np.load(args.rvec)
    print("read elist ...")
    elist = read_list(args.eradlist)
    print("calc rvec ...")
    with open(args.out, "w") as w:
        calc_and_save_rvecs(rvec, elist, w)
    #eraddic, newvaluedic = mapping_erad(elist, indexdic, valuedic)
    #save_dics(eraddic, newvaluedic, args.out)
    print("end ...")


if __name__ == "__main__":
    main()

