# coding=utf-8
# author = zhouxin
# date = 2017.7.17
# description
# extract all valid words to a csv file
# 提取所有有效单词到 file 文件


from models_exp import NewWord
import json

result = {}
fileName = {
    'n': '名词_n',
    'u': '不可数名词_u',
    'c': '可数名词_c',
    'v': '动词_v',
    'vi': '不及物动词_vi',
    'vt': '及物动词_vt',
    'auxv': '助动词_auxv',
    'conj': '连接词_conj',
    'adj': '形容词_adj',
    'adv': '副词_adv',
    'art': '冠词_art',
    'prep': '介词_prep',
    'pron': '代名词_pron',
    'num': '数词_num',
    'int': '感叹词_int',
    'abbr': '缩写词_abbr',
}

fileHandel = {}
for key in fileName:
    fileHandel[key] = open('/Users/shuizhou/PycharmProjects/test/programming_vocabulary/result/' + fileName[key] +
                           '.txt',
                           "a+",
                           encoding='utf-8')


def extract():
    query = NewWord.select()
    print(query)
    for word in query:
        res = []
        for i in [word.name, word.explanation]:
            res.append(i)

        yield res


def save(res):
    word = res[0]
    explanation = json.loads(res[1])
    for k in explanation:
        fileHandel[k].write(word + "\r\n")
        break


def main():
    row = extract()
    count = 1
    while True:
        try:
            row_data = next(row)
        except:
            break
        save(row_data)
        count += 1


if __name__ == '__main__':
    main()
    # res = extract()
    # print(next(res))
    # print(next(res))
    # print(next(res))
