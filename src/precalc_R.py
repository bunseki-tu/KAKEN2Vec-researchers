# mwada(c8)
import argparse
import numpy as np

def calc_R(W):
    print(W.shape)
    return np.linalg.solve (np.dot(W.T,W), W.T)

###############################################################
def ap():
    parser = argparse.ArgumentParser(description='持橋先生資料のRを事前計算')
    parser.add_argument('wvec', help='単語ベクトル, npy')
    parser.add_argument('out', help='出力, npy')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    print("read rvec ...")
    W = np.load(args.wvec)
    print("calc R ...")
    R = calc_R(W)
    print("save ...")
    print(R.shape)
    np.save(args.out, R)

if __name__ == "__main__":
    main()

