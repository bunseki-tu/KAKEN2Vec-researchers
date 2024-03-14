# mwada(c8)
import argparse
import numpy as np

############################################################################

def read_kiderad(eradkid):
    with open(eradkid, "r") as f:
        edic = {}
        for row in f:
            erad, nrows = row.rstrip("\n").split("\t")
            nrowl = nrows.split("||")
            for nrow in nrowl:
                if erad in edic:
                    edic[erad].append(int(nrow))
                else:
                    edic[erad] = [int(nrow)]
    return edic

def split_vec(D_vec, edic):
    eradvecs = {}
    for k, v in edic.items():
        for i in v:
            if k in eradvecs:
                eradvecs[k] = np.vstack([eradvecs[k], D_vec[i,:]])
            else:
                eradvecs[k] = D_vec[i,:]
    return eradvecs

def calc_meanvec(vecdic):
    mvec = {}
    for k, v in vecdic.items():
#        if k == "NotFound":
#            continue
#        elif v.ndim == 1:
        if v.ndim == 1:
            mvec[k] = v
        else:
            mvec[k] = np.mean(v, axis=0)
    return mvec

def write_pre(mdic, outpre):
    with open(outpre + "_erad.txt", "w") as we:
        vecl = []
        for k, v in sorted(mdic.items()):
            we.write(k + "\n")
            vecl.append(v)
    mvecs = np.vstack(vecl)
    np.save(outpre + "_meanvec.npy", mvecs)

############################################################################
def ap():
    parser = argparse.ArgumentParser(description='eradと行番号（ベクトルに対応）のリストを用いて，eradごとの平均ベクトルを計算。出力は2つで，平均ベクトルと各ベクトルのerad番号リスト。')
    parser.add_argument('eradkid', help='eradkidのリスト')
    parser.add_argument('D', help='D')
    parser.add_argument('outpre', help='出力のプレフィックス')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    D_vec = np.load(args.D)
    eraddic = read_kiderad(args.eradkid)
    vecdic = split_vec(D_vec, eraddic)
    meanvecdic = calc_meanvec(vecdic)
    write_pre(meanvecdic, args.outpre)

if __name__ == "__main__":
    main()

