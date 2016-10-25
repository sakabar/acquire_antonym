#!/bin/zsh

cat ~/work/acquire_antonym/tari_tari_pair_compound/*.txt | grep -v "^EOS" | python ~/work/MyNgram/src/get_ngram.py 2 | grep -v "<S>" | grep -v "</S>" | LC_ALL=C sort | uniq 


