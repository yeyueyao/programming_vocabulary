# coding=utf-8
# author = zhouxin
# date = 2017.7.11
# description
# 该项目启动文件

import os

from settings import DIRS, FILES, DATABASE
from analysis_book import AnlysisBook
from models_exp import new_db, NewWord, NewBook


# 解析所有文件路径
class ParseFile:

    # 解析 settings 中的文件夹地址
    # 程序只会将 txt 文件添加到待获取列表
    def _parse_dirs(self, dirs):

        assert isinstance(dirs, list), 'type(dirs) should be list '
        if not dirs:
            return dirs

        files = []
        for path in dirs:
            if not os.path.isdir(path):
                continue
            for pathname, dirname, filenames in os.walk(path):
                for filename in filenames:
                    # 仅获取 txt　文件
                    if '.txt' in filename:
                        file_path = pathname + os.sep + filename
                        files.append(file_path)

        return files

    # 解析单个文件
    def _parse_files(self, files):

        assert isinstance(files, list), 'type(files) should be list '
        f = []
        for path in files:
            if not os.path.isfile(path) or '.txt' not in path:
                continue
            f.append(path)

        return f

    def parse(self, dirs, files):
        # print(dirs, files)
        f1 = self._parse_dirs(dirs)
        f2 = self._parse_files(files)

        return f1 + f2


# 创建数据库
class Dt:

    def __init__(self):
        self.build()

    def build(self):
        created = os.path.exists(DATABASE)

        if not created:
            new_db.connect()
            new_db.create_tables([NewBook, NewWord])


if __name__ == '__main__':
    # 建表
    dt = Dt()
    # 解析文件路径
    s = ParseFile()
    res = s.parse(DIRS, FILES)
    print(len(res))
    # extract words from books
    ana = AnlysisBook()
    ana.analysis(res)
    print(res)
