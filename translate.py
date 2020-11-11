# coding=utf-8
# author=zhouxin
# date=2017.7.10
# description
# 调用翻译接口，翻译数据库内词汇

import requests
import json
import re

from models_exp import NewWord

fileName = {
    'n': '名词',
    'u': '不可数名词',
    'c': '可数名词',
    'v': '动词',
    'vi': '不及物动词',
    'vt': '及物动词',
    'auxv': '助动词',
    'conj': '连接词',
    'adj': '形容词',
    'adv': '副词',
    'art': '冠词',
    'prep': '介词',
    'pron': '代名词',
    'num': '数词',
    'int': '感叹词',
}


class Translate:

    def __init__(self):
        # self.util = Utils()
        pass

    # translation api, tranlate a english word to chinese
    # return translation result
    # 百度翻译接口
    def _trans(self, word):
        # res = self.trans.translate('hello', dest='zh-CN')
        url = 'http://fanyi.baidu.com/sug'
        dct = {'kw': word}
        req = requests.post(url, dct)
        print(req)
        req.raise_for_status()
        res = req.json().get('data')
        print(req.json())
        if not res:
            return None
        return res[0].get('v', None)

    def _trans_test(self, word):
        url = 'http://open.iciba.com/huaci_v3/dict.php?word=' + word
        try:
            req = requests.get(url, timeout=10)
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            return None
        script = req.text
        speeches = re.findall(r'<span class=.{0,3}icIBahyI-fl.{0,3}>([a-z]+\.)<', script, re.M | re.I | re.S)
        trans = re.findall(r'<span class=.{0,3}icIBahyI-label_list.{0,3}>(.*?)</span>', script,
                           re.M | re.I |
                           re.S)
        i = 0
        res = {}
        if not speeches:
            return None
        for speech in speeches:
            speech = speech.replace('.', '')
            tran = re.findall(r'<label>(.*?)</label>', trans[i])
            res[speech] = ''.join(tran)
            i += 1
        return ['', json.dumps(res, ensure_ascii=False)]

    # iciba api / 金山词典 api
    # baidu api dont contain Phonogram , so change an api
    def _trans_ici(self, word):

        url = 'http://www.iciba.com/index.php?a=getWordMean&c=search&word=' + word
        print(url)
        try:
            req = requests.get(url)
            req.raise_for_status()
            info = req.json()
            data = info['baesInfo']['symbols'][0]
            assert info['baesInfo']['symbols'][0]
            # 去除没有音标的单词
            assert data['ph_am'] and data['ph_en']
            # 去除没有词性的单词
            assert data['parts'][0]['part']

        except:
            return

        ph_en = '英 [' + data['ph_en'] + ']'
        ph_am = '美 [' + data['ph_am'] + ']'
        ex = ''
        for part in data['parts']:
            ex += part['part'] + ';'.join(part['means']) + ';'

        return ph_en + ph_am, ex

    # 扇贝单词 api
    def _trans_shanbay(self, word):
        url = 'https://api.shanbay.com/bdc/search/?word=' + word
        req = requests.get(url)
        print(req.json())

    # 使用 金山单词 翻译接口
    # 百度接口没有音标
    # 扇贝接口包含的信息不如其他两家
    def trans(self):
        query = NewWord.select().where(NewWord.explanation == '')
        # print(len(query))
        if not query:
            return
        for word in query:
            print(word)
            res = self._trans_test(word.name)
            if res:
                word.phonogram = res[0]
                # word.
                word.explanation = res[1]
            else:
                word.is_valid = False
            word.save()
            # print('suc save word : {}'.format(word.name))
            # time.sleep(1)


if __name__ == '__main__':
    t = Translate()
    # res = t._trans_shanbay('hello')
    # print(res)
    # res = t._trans()
    t.trans()
    # print(t._trans_test('structure'))
