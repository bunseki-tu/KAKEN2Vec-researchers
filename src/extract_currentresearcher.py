# mwada(c8)
import argparse
import glob
import json

outdir = ""

def list_json(indir):
    path = indir + "*.json"
    jsons = glob.glob(path)
    return jsons

def name_or_notfound(r):
    try:
        familyname = r["name"]["name:familyName"][0]["text"]
        givenname  = r["name"]["name:givenName"][0]["text"]
        fullname = familyname + givenname
    except:
        fullname = "NotFound"
    return fullname

def read_write(df, tsv):
    rs = df["researchers"]
    for researcher in rs:
        erad = researcher["id:person:erad"][0]
        fullname = name_or_notfound(researcher)
        if "affiliations:current" not in researcher:
            continue
        for ac in researcher.get("affiliations:current",[]):
            fyear = ac.get("since",{}).get("commonEra:year","NotFound")
            tyear = ac.get("until",{}).get("commonEra:year","NotFound")
            if "affiliation:institution" in ac:
                instname = ac["affiliation:institution"]["humanReadableValue"][0]["text"]
            else:
                instname = "NotFound"
            niicode  = ac.get("affiliation:institution",{}).get("id:institution:kakenhi","NotFound")
            mextcode = ac.get("affiliation:institution",{}).get("id:institution:mext","NotFound")
            jspscode = ac.get("affiliation:institution",{}).get("id:institution:jsps","NotFound")
            jstcode  = ac.get("affiliation:institution",{}).get("id:institution:jst","NotFound")
            eradcode = ac.get("affiliation:institution",{}).get("id:institution:erad","NotFound")
            if "affiliation:department" in ac:
                dpname = ac["affiliation:department"]["humanReadableValue"][0]["text"]
            else:
                dpname = "NotFound"
            line = ["current",erad,fullname,str(fyear),str(tyear),instname,niicode,mextcode,jspscode,jstcode,eradcode, dpname]
            tsv.write("\t".join(line) + "\n")

def single_process(j):
    global outdir
    print(j + " ...")
    filename = j.rsplit("/", 1)
    name = filename[1].rsplit(".", 1)
    outfile = outdir + name[0] + ".tsv"
    with open(j, "r") as jn:
        df = json.load(jn)
        with open(outfile, "w") as tsv:
            read_write(df, tsv)

def NotMulti_process(jsons):
    for j in jsons:
        single_process(j)

def ap():
    parser = argparse.ArgumentParser(description='KAKENから取得した研究者情報jsonのファイル群を処理して，必要な情報を取得する')
    parser.add_argument('indir', help='jsonが入ったディレクトリ')
    parser.add_argument('outdir', help='出力するディレクトリ')
    args = parser.parse_args()
    return args

def main():
    args = ap()
    jsons = list_json(args.indir)
    global outdir
    outdir = args.outdir
    NotMulti_process(jsons)

if __name__ == "__main__":
    main()

