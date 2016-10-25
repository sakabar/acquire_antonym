#!/bin/zsh

set -ue

#Webコーパスから「AたりBたり」のパターンにマッチする文を獲得する
#./tari_tariに保存
if [ `hostname` != "biscuit" ];then
  echo "run at biscuit">&2
  exit 1
fi

corpus_dir=/local/tsakaki/corpus/web-corpus/txt
# output_dir_sentence=~/work/acquire_antonym/tari_tari_sentence
# output_dir_pair=~/work/acquire_antonym/tari_tari_pair
# output_dir_pair_mecab=~/work/acquire_antonym/tari_tari_pair_mecab
# output_dir_compound=~/work/acquire_antonym/tari_tari_pair_compound

output_dir_sentence=/local/tsakaki/output/tari_tari_sentence
output_dir_pair=/local/tsakaki/output/tari_tari_pair
output_dir_pair_mecab=/local/tsakaki/output/tari_tari_pair_mecab
output_dir_compound=/local/tsakaki/output/tari_tari_pair_compound


python_dir=/home/lr/tsakaki/work/acquire_antonym/src

#標準入力から「AたりBたり」を含む文を読み込み、「AたりBたり」の部分のみを出力し、$output_dir_pairに出力する。そしてMecabで解析し、$output_dir_pair_mecabに出力する
function extract_tari_tari_pair(){
  cat - | mecab -O wakati \
    | LC_ALL=C grep -o -- "[^ ]\+ \(し \)\?[ただ]り [^ ]\+ \(し \)\?[ただ]り"
}

#「AたりBたり」をMecabで解析したものを標準入力から受け取り、合成語を出力する
function get_compound_word(){
  cat - | tr '\t' ',' | python src/main.py | mecab -O wakati | LC_ALL=C grep -v "^EOS\t"
}

#途中のgrepでLC_ALL=Cをつけると、[ただ]の部分の分岐ができなくなってミスる…らしい…
for d in $corpus_dir/*; do
  echo "$d" >&2
  f=$d:t:r:r".txt"
  nice -n 15 cat $d/*.txt | LC_ALL=C grep -v "^#" | grep "[ただ]り.\+[ただ]り" |tee $output_dir_sentence/$f \
    | mecab -O wakati | grep -o -- "[^ ]\+ \(し \)\?[ただ]り [^ ]\+ \(し \)\?[ただ]り" | tee $output_dir_pair/$f \
    | tr -d ' ' | mecab |tee $output_dir_pair_mecab/$f \
    | tr '\t' ',' | python $python_dir/main.py | mecab -O wakati | LC_ALL=C grep -v "^EOS\t" > $output_dir_compound/$f:t
done 

