
# KAKEN2Vec-researchers
このリポジトリはKAKEN2Vec-researchersのコードを公開しています。  
KAKEN2Vec-researchers自体は非公開です。  
This repository contains the code to create KAKEN2Vec-researchers.  
KAKEN2Vec-researchers is not open to the public.  

## About
KAKEN2Vec-researchersは科学研究費助成事業データベース[KAKEN](https://kaken.nii.ac.jp/) のデータを使った研究者検索エンジンです。
[ACL2Vec](http://chasen.org/~daiti-m/dist/ACL2Vec/) の [ACL2Vec-authors](http://clml.ism.ac.jp/ACL2Vec-authors/) を参考にしています。  
検索エンジンの基礎は[ACL2Vecと同じアルゴリズム](http://chasen.org/~daiti-m/paper/nlp2021researcher2vec.pdf) です。
KAKENのデータを元に作成したユーザ辞書を形態素解析器に追加していることが特徴です。

KAKEN2Vec-researchers is a Japanese researcher search engine that uses data from Database of Grants-in-Aid for Scientific Research ([KAKEN](https://kaken.nii.ac.jp/)). 
It is based on the [ACL2Vec-authors](http://clml.ism.ac.jp/ACL2Vec-authors/) of [ACL2Vec](http://chasen.org/~daiti-m/dist/ACL2Vec/).
KAKEN2Vec-researchers uses the same algorithm as ACL2Vec ([paper](http://chasen.org/~daiti-m/paper/nlp2021researcher2vec.pdf)), and it is unique in that it adds an user dictionary created from KAKEN data to the morphological analyzer.  


## Disclaimer
本リポジトリ内で公開しているコードを利用する際は，各自の責任でご使用ください。作者は責任を負いかねます。  
When using the code published in this repository, please use it at your own risk. The author is not responsible for any trouble that may occur.

## License
KAKEN2Vec-researchers is distributed under the MIT license.

## Requirements
- Python3 https://www.python.org/
- MeCab https://taku910.github.io/mecab/
- lxml https://lxml.de/
- mecab-python3 https://github.com/samurait/mecab-python3
- unidic https://github.com/polm/unidic-py
- neologdn https://github.com/ikegami-yukino/neologdn (neologdn was used during experimentation, but was not used in the end.)
- numpy https://numpy.org/
- SciPy https://scipy.org/
- scikit-learn https://scikit-learn.org/
- Flask https://palletsprojects.com/p/flask/

リポジトリに含まれていないコードはさらにいくつかのライブラリを必要としますが，それらについては当該コードを参照してください。  
Codes not included in the repository require several more libraries.

## Preparing
以降ではいくつかのディレクトリがあることが前提になっています。下記のように準備しておいてください。  
It is assumed that there are several directories from now on. Please prepare as follows:  

```
mkdir ./kadaidata
mkdir ./rdata
mkdir ./data
mkdir ./data/kwtsvs
mkdir ./data/kadaitsvs
mkdir ./data/textkw
mkdir ./data/soshiki
mkdir ./data/cr
```

### KAKENから研究課題データ（XML）と研究者データ（JSON）を取得する Research Project data (XML) and Researcher data (JSON)
KAKENから研究課題データと研究者データを取得してください。方法は問わないですが，以下が参考になります。  
Please obtain the research project data and researcher data from KAKEN. The method does not matter. The following may be of reference.

- [KAKEN－研究課題をさがす－検索結果画面](https://support.nii.ac.jp/ja/kaken/project_list)
- [KAKEN API ドキュメント](https://support.nii.ac.jp/ja/kaken/api/api_outline)
- [kaken_parse_grants_masterxml](https://github.com/c4ra/kaken_parse_grants_masterxml)

以下では，課題データは `./kadaidata` ，研究者データは `./rdata` に格納されたとして話を進めます。
また課題データの命名規則はkaken_parse_grants_masterxmlと同じとして話を進めます。例： `2020_1-500.xml`　
研究者データは拡張子がjsonとなっていればよいです。

In the following, the author will assume that the research project data is stored in `./kadaidata` and the researcher data is stored in `./rdata`. The author will also assume that the naming convention for the research project data is the same as kaken_parse_grants_masterxml. Example: `2020_1-500.xml`. The researcher data should have a json extension.


### ユーザ辞書作成　User dictionary
KAKENの研究課題に付与されているキーワードと，研究課題ごとに記載された文書から抽出したフレーズをもとに，ユーザ辞書を作成します。  
以下を順に実行してください。  
Create a user dictionary based on the keywords assigned to research projects in KAKEN and the phrases extracted from the texts listed for each proposal. Please do the following in order.

#### keywordsの抽出とDFカウント Keywords and Document Frequency
以降の例では開始年度が2010-2020のデータを扱うことにしている。  
課題データからkeywordsを抽出 `extract_kw_KAKENkadai.py`  
keywordsが入った .tsv を結合 `concatenate_tsv.py`  
キーワードのDF（出現した課題数）をカウントしてソート `count_kw_df.py`  

```
python src/extract_kw_KAKENkadai.py ./kadaidata ./data/kwtsvs -f 2010 -t 2020  
python src/concatenate_tsv.py ./data/kwtsvs/ ./data/kw.tsv  
python src/count_kw_df.py ./data/kw.tsv ./data/kw_df.tsv
```


#### フレーズ抽出 Phrase
続けて「[NPMIによる教師なしフレーズ認識](http://chasen.org/~daiti-m/diary/?0414)」のphraser.pyを使って課題に書かれた文書からもフレーズを取り出します。  

課題XMLから文書を抽出 `extract_text_KAKENkadai.py`  
.tsvを結合 `concatenate_tsv.py`  
タブで区切っていたテキストを結合 `joint_texts.py`  
テキストの加工(nyyとしたことで，neologdnは使わず，数字およびアルファベットの大文字小文字の統一を実施) `normalize_text.py`  

```
python src/extract_text_KAKENkadai.py ./kadaidata ./data/kadaitsvs -f 2010 -t 2020
python src/concatenate_tsv.py ./data/kadaitsvs/ ./data/kadai.tsv
python src/joint_texts.py ./data/kadai.tsv ./data/kadaitext.tsv  
python src/normalize_text.py ./data/kadaitext.tsv nyy ./data/nkadaitext.tsv
```

> 次のwakati.pyはmecabuni.pyを呼び出しているので，先にmecabuni.pyの辞書に関する部分を自身の環境に合わせて書き換える（作者はunidicを使用）

分かち書きを実施 `wakati.py`  
上記の`phraser.py`を使用して，フレーズを特定（上記のアドレスから別途取得してください）    
phraser.pyで特定したフレーズを抽出 `extract_phrase.py`  

```
python src/wakati.py ./data/nkadaitext.tsv ./data/wakati.txt
python src/phraser.py ./data/wakati.txt ./data/phrase.txt 4 0.5 10
python src/extract_phrase.py ./data/phrase.txt ./data/ephrase.txt
```


#### 2つのリストの扱い Keywords lists
これでKAKENから取り出したキーワード（DF付き）`./data/kw_df.tsv`と，文章から取り出したフレーズ`./data/ephrase.txt`の2つのリストができあがる。
ただ，これらの中身を見る限りキーワードの特に低DFのキーワードの中には特定の研究者しか使わないようなキーワードや，フレーズにも正確ではないものもある。
そこで比較的多くの人が使い，正確なフレーズ・キーワードのみをユーザ辞書に入れるという方針をたて，実際には両者のANDをとってどちらにもでてきたものと，キーワードのDFが100以上のものを，ユーザ辞書に入れることにした。`merge_kwphrase.py`

```
python src/merge_kwphrase.py ./data/kw_df.tsv ./data/ephrase.txt ./data/merged.txt
```

#### リストからMeCabのユーザ辞書の作成 MeCab user dictionary
作者によるKAKEN2Vec-researchers構築時は，下記文書のとおりにはできなかったので，コスト推定はせずに決め打ちのコストでCSVを作成し，それをコンパイルした。  
[単語の追加方法](https://taku910.github.io/mecab/dic.html)

作者ができなかったことをうまくやる方法が公開された文書を見つけたので，今ならこちらを参考にするべき。  
[Mecab のコスト推定自動機能を使って UniDic のユーザ辞書をビルドする](https://zenn.dev/zagvym/articles/28056236903369)

作成した辞書 userdic.dic は以降でMeCabを使う際に指定する。


### docvecまでの前処理 Preprocessing to docvec

#### テキストの抽出 Text
KAKENからテキスト（keywords含む）を抽出　`extract_textkw_KAKENkadai.py`  
.tsvを結合 `concatenate_tsv.py`  

```
python src/extract_textkw_KAKENkadai.py ./kadaidata ./data/textkw -f 2010 -t 2020
python src/concatenate_tsv.py ./data/textkw/ ./data/textkw.tsv
```


#### SVMlightに似た形式に変換 SVMlight-like format
課題のID（KID）とその他を分割 `split_KidOther.py`  
その他を結合 `joint_t.py`  

```
python src/split_KidOther.py ./data/textkw.tsv ./data/split
python src/joint_t.py ./data/split_other.tsv ./data/othertext.txt
```

> 次のtantani.pyはmecabuni_addud.pyを呼び出しているので，先にmecabuni_addud.pyの辞書に関する部分を自身の環境に合わせて書き換える（先ほど作成したuserdic.dicをここで指定する）

mecab+unidic+ユーザ辞書によりテキストを分割 `tantani.py`  

```
python src/tantani.py ./data/othertext.txt ./data/bunkatu.txt
```

テキストの加工(数字およびアルファベットの大文字小文字の統一を実施) `normalize_textnonid.py`  
頻度カウントしSVMlight-likeなフォーマット化とDのFカウント `count_tantani.py`   
DFでフィルタリング（今回はDFが1以下または500000以上のものは削除） `filter_df.py`  
単語を単語IDに変換 `word2id.py`   

```
python src/normalize_textnonid.py ./data/bunkatu.txt nyy ./data/nbunkatu.tsv  
python src/count_tantani.py ./data/nbunkatu.tsv ./data/hindo
python src/filter_df.py ./data/hindo_count.txt ./data/hindo_df.txt 1 500000 ./data/hindo_1-500000.txt  
python src/word2id.py ./data/hindo_1-500000.txt ./data/w2id
```


### docvecによるベクトル化（埋め込み）とベクトルの加工 Embedding and vector processing

#### ベクトル化と正規化と事前計算 Embedding, Normalization and Precomputation
PMI-SVDによる埋め込み（ここでは2000次元を指定） `docvec.py`   
文書ベクトルと単語ベクトルをL2正規化 `l2normalization.py`  
事前に単語ベクトルのRの計算 `precalc_R.py`  

```
python src/docvec.py ./data/w2id_idcount.dat ./data/vec2000 -k 2000  
python src/l2normalization.py ./data/vec2000_D.npy ./data/l2vec2000_D.npy  
python src/l2normalization.py ./data/vec2000_W.npy ./data/l2vec2000_W.npy  
python src/precalc_R.py ./data/l2vec2000_W.npy ./data/R_l2vec2000.npy  
```

#### 研究者とベクトルの紐づけ Mapping researchers to vectors

各研究課題から研究組織の情報を抽出 `extract_Soshiki.py`  
.tsvを結合 `concatenate_tsv.py`  
PIの抽出 `filter_soshiki_role.py`  

```
python src/extract_Soshiki.py ./kadaidata ./data/soshiki -f 2010 -t 2020  
python src/concatenate_tsv.py ./data/soshiki/ ./data/soshiki.tsv　 
python src/filter_soshiki_role.py ./data/soshiki.tsv ./data/pi.txt  
```

現役研究者一覧を作成 `extract_currentresearcher.py`  
.tsvを結合 `concatenate_tsv.py`  
PIをさらに現役研究者だけに限定 `limit_kadai_bycurrent.py`  
現役研究者の研究課題リストを作成 `create_kadailist.py`  
処理の都合で課題を行番号に変換 `trans_kid2rown.py`  
研究者ごとのベクトルを作成（平均ベクトル） `calc_researchervec.py`  

```
python src/extract_currentresearcher.py ./rdata ./data/cr/  
python src/concatenate_tsv.py ./data/cr/ ./data/crs.tsv  
python src/limit_kadai_bycurrent.py ./data/pi.txt ./data/crs.tsv ./data/pi_current.txt  
python src/create_kadailist.py ./data/pi_current.txt ./data/kadailist.txt  
python src/trans_kid2rown.py ./data/kadailist.txt ./data/split_kid.tsv ./data/kadairown.txt  
python src/calc_researchervec.py ./data/kadairown.txt ./data/l2vec2000_D.npy ./data/rvec  
```


#### 事前計算 Precalculation
各研究者についてcos類似度が高い研究者50名を事前に計算（注意：実行には時間がかかる）`precalc_cossimRVEC_savememo.py`

```
python src/precalc_cossimRVEC_savememo.py ./data/rvec_meanvec.npy ./data/rvec_erad.txt ./data/cossim_top50.txt
```


## Usage

以降ではFlaskの組み込みサーバで動かします。  
公開する場合は，[公式のドキュメント](https://flask.palletsprojects.com/en/3.0.x/deploying/)を参考に環境を構築してください。

ここまでに作成してきた以下のデータと，HTMLファイルを使います。
- 研究者情報 pi.txt
- 単語とIDの対応 w2id_dic.tsv
- 類似研究者Top50 cossim_top50.txt
- 事前に計算したR R_l2vec2000.npy
- 研究者番号と行番号の対応 rvec_erad.txt
- 研究者ごとのベクトル rvec_meanvec.npy
- 自前で作成したユーザ辞書 userdic.dic
- HTMLファイル index.html

`index.py` の中身を書き換えて，以上のデータを参照するようにしてください。  
`templates/index.html` を使うようにしています。好みでなければ書き換えてください。  
著者はベクトルの次元数をいくつか試したかったため，参照するデータを切り替えられるようにしています。  

`index.py` を実行すると，Flaskの組み込みサーバが起動します。
```
python src/index.py unidic_2000
```
表示されるアドレスにアクセスすると，検索システムが表示されます。

検索欄にキーワードを入れて検索ボタンを押すと下記の過程を経て，検索結果が表示されます。
1. キーワードをMeCab（+ unidic + userdic.dic）で分割
2. 分割した形態素を w2id_dic　でIDに対応付け
3. IDを利用して R から該当のベクトルを抽出
4. 抽出したベクトルの平均を計算
5. 平均ベクトルと rvec_meanvec でcos類似度を計算
6. cos類似度の高い順に研究者を表示

検索結果の研究者番号はクリックできるようになっていますが，
これをクリックすると事前に計算していた類似研究者Top50が表示されます。
検索欄に研究者番号を入れたときも同様に類似研究者が表示されます。


## Author
* mwada(c8)
* Research Management Center, Office of Research Promotion, Tohoku University

## References
- KAKEN：科学研究費助成事業データベース（国立情報学研究所）（ https://kaken.nii.ac.jp/ ）
- 「Researcher2Vec: ニューラル線形モデルによる自然言語処理研究者の可視化と推薦」. 持橋大地, 言語処理学会第27回年次大会 B2-2, 2021.  
- "Researcher2Vec: Neural Linear Model of Scholar Recommendation for Funding Agency". Daichi Mochihashi. International Society for Scientometrics and Informatics (ISSI 2023), Vol. 2, pp.329-335, 2023.  
- ACL2Vec http://chasen.org/~daiti-m/dist/ACL2Vec/

## Acknowledgement
KAKEN2Vec-researchersの作成にあたっては，ACL2Vecの作者である持橋大地先生に教えていただいた内容が各所に活かされています。記して感謝申し上げます。  

