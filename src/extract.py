#coding:utf-8
#n-gramのスコアを比較して、一番高い順番のものだけを出力する
import sys
def main():
    lines = []

    for line in sys.stdin:
        line = line.rstrip()
        lst = line.split('\t')

        if line == "EOS":
            #スコアが最大のもののみ取ってくる
            key, score = sorted(lines, key=(lambda p: p[1]))[-1]
            score /= len(key.split(' ')) #トークン数で正規化
            print "%s\t%f" % (key, score)
            print "EOS"
            lines = []
        else:
            tpl = (lst[0], float(lst[1]))
            lines.append(tpl)

            
        

if __name__ == '__main__':
    main()
