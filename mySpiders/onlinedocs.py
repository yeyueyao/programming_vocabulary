# coding=utf-8
# author = zhouxin
# date = 2017.7.13
# description
# download online books,
# 资源来自与 readthedocs.io
# 下载某个在线的文档所有的文字

import bs4
import queue

from mySpiders.utils import Utils

PATH_DIR = 'docs/'


class _Down:

    def __init__(self):
        self.util = Utils()

    def _save(self, title, words):

        self.util.checkpath(PATH_DIR)
        if not words:
            return
        with open(PATH_DIR + title, 'a+')as f:
            f.write(words)

    # 递归抓取某文档所有链接
    def _download(self, qu, domain, title, switch=True):
        # print(title)
        if qu.empty():
            return

        url = qu.get()
        text = self.util.req(url)

        if not text:
            # qu.put(url)
            return self._download(qu, domain, title, False)

        if switch:
            res = self._download_links(domain, text)
            for i in res:
                qu.put(i)

        words = self._download_docs(text)
        self._save(title, words)

        return self._download(qu, domain, title, switch=False)

    def _download_docs(self, page):

        soup = bs4.BeautifulSoup(page, 'lxml')
        soup_body = soup.find('body')
        words = ''
        if soup_body:
            words += soup_body.get_text(' ')

        return words

    def _download_links(self, domain, page):

        lst = []
        soup = bs4.BeautifulSoup(page, 'lxml')
        soup_link = soup.find_all('a')
        for link in soup_link:
            lst.append(domain + link['href'])

        return lst

    def download(self, url, domain, title):
        # title = 'Problem Solving with Algorithms and Data Structures using Python.pdf'
        qu = queue.Queue()
        qu.put(url)

        return self._download(qu, domain, title)


class Pat1(_Down):

    def __init__(self):
        # super(_Down, self).__init__()
        self.util = Utils()
        # 某文档信息
        # self.url = 'https://interactivepython.org/courselib/static/pythonds/index.html'
        # self.domain = 'https://interactivepython.org/courselib/static/pythonds/'
        # self.title = 'Problem Solving with Algorithms and Data Structures using Python.txt'
        # self.url = 'http://chimera.labs.oreilly.com/books/1230000000393/index.html'
        # self.domain = 'http://chimera.labs.oreilly.com/books/1230000000393/'
        # self.title = 'Python Cookbook.txt'
        self.url = 'http://docs.peewee-orm.com/en/stable/'
        self.domain = self.url
        self.title = 'peewee.txt'

    def _download_links(self, domain, page):
        lst = []
        soup = bs4.BeautifulSoup(page, 'lxml')
        soup_li = soup.find_all('li', class_="toctree-l1")
        for li in soup_li:
            lst.append(domain + li.a['href'])
        res = list(set(lst))
        # print(len(res))
        return res

    def get(self):
        return self.download(self.url, self.domain, self.title)


if __name__ == '__main__':
    p1 = Pat1()
    p1.get()
