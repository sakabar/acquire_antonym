#coding: utf-8

def get_pos(mecab_line):
    return mecab_line.split(',')[1]

def get_dic(dic_name, form, mecab_dic_dir='/home/lr/tsakaki/local/src/mecab-ipadic-2.7.0-20070801'):
    verb_dic = {}

    with open(mecab_dic_dir + '/' + dic_name, 'r') as vdic:
        for l in vdic:
            lst = l.split(',')
            surf = lst[0]
            katuyou_type = lst[8]
            katuyou_form = lst[9]
            base = lst[10]


            #未然形はkeyがぶつかる "Error:サ変・−スル 未然ウ接続 ごわする,ごわしょvsごわしょ"
            if katuyou_form == form:
                key_tpl = (katuyou_type, katuyou_form, base)
                if key_tpl in verb_dic:
                    if verb_dic[key_tpl] == surf:
                        pass
                    else:
                        raise Exception('Error:' + " ".join(key_tpl) + "," + surf + "vs" + verb_dic[key_tpl])
                else:
                    verb_dic[key_tpl] = surf

    return verb_dic

def change_form_for_compound(verb_dic, mecab_line):
    lst = mecab_line.split(',')
    pos = lst[1]
    surf = lst[0]
    katuyou_type = lst[5]
    base = lst[7]

    key = ""
    if pos == '動詞':
        key = (katuyou_type, '連用形', base)
    elif pos == "形容詞":
        key = (katuyou_type, 'ガル接続', base)
    elif pos == "名詞":
        return surf
    else:
        raise Exception('Unexpected POS:' + surf + ":" + pos)

    if key in verb_dic:
        #動詞などで、連用形がある場合
        renyou = verb_dic[key]
        return renyou
    else:
        #名詞などの場合
        #形容詞の場合は、「寒暖」などにしなければいけないのでは…
        #FIXME 形容詞の場合: 語幹を返す

        return surf
    

#引数の語を連用形にして結合し、複合語を作る
def get_compound_word(verb_dic, w1, w2):
    r1 = change_form_for_compound(verb_dic, w1)
    r2 = change_form_for_compound(verb_dic, w2)
    return "%s%s" % (r1, r2)

    return
