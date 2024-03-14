# mwada(c8)
import argparse
import numpy as np
from sklearn.preprocessing import normalize

def l2n(vec):
    nvec = normalize(vec, norm='l2', axis=1)
    return nvec

def read_vec(vec):
    npvec = np.load(vec)
    print(npvec.shape)
    return npvec

def ap():
    parser = argparse.ArgumentParser(description='ベクトルのファイルを読み込んでL2正規化を行う，要は超球の表面上に位置づける')
    parser.add_argument('vec', help='vec, npy')
    parser.add_argument('out', help='出力するファイル名, npy')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    vec = read_vec(args.vec)
    nvec = l2n(vec)
    np.save(args.out, nvec)
    

if __name__ == "__main__":
    main()

