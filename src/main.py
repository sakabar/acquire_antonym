#coding:utf-8
import sys
# import replace_lib #zshrcなどに、PYTHONPATH=$HOME/work/replace_with_antonym/src:$PYTHONPATH などを追加する必要あり。
import lib_acquire_antonym as lib


# def main():
#     for line in sys.stdin:
#         line = line.rstrip()
#         line = line + " " #便宜上、末尾に' 'を足す。後に、' たり 'でsplitするため
#         lst = line.split(' たり ')[0:-1] #リストの末尾は''であるため除く
#         for s in lst:
#             print s

#         sys.exit(1)
#     return 



def tari_tari_pair_func(dic, mecab_lines):
    ans_lst = []
    
    for line in mecab_lines:
        if line.split(',')[0] == "し":
            #スルは無視する
            pass
        elif line.split(',')[1] == "動詞" or line.split(',')[1] == "名詞" or line.split(',')[1] == "形容詞":
            ans_lst.append(line)
        else:
            pass

    if len(ans_lst) != 2:
        #ペアが取れてなかったら次の処理へ
        # sys.stderr.write(",".join(ans_lst) + '\n')
        return 
    
    print lib.get_compound_word(dic, ans_lst[0], ans_lst[1])
    print lib.get_compound_word(dic, ans_lst[1], ans_lst[0])
    print "EOS"

#たり-たりのペアをmecabで解析したものをtrなどでTABを,に置換し、標準入力から受け取り処理する
def main():
    verb_dic = lib.get_dic('Verb.csv','連用形', '/home/lr/tsakaki/work/acquire_antonym')
    adj_dic = lib.get_dic('Adj.csv','ガル接続', '/home/lr/tsakaki/work/acquire_antonym')
    dic = {}
    dic.update(verb_dic)
    dic.update(adj_dic)


    mecab_lines = []

    for line in sys.stdin:
        line = line.rstrip()

        if line == "EOS":
            tari_tari_pair_func(dic, mecab_lines)
            mecab_lines = []
            # sys.exit(1)
        else:
            mecab_lines.append(line)
        

    return 

if __name__ == '__main__':
    main()
