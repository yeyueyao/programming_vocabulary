# -*- coding: utf-8 -*-
import sys

"""
Created on Sun Mar  3 12:22:49 2019

@author: Ben
"""

import importlib

importlib.reload(sys)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# from PyPDF2.pdf import PdfFileReader, PdfFileWriter, ContentStream

sys.setrecursionlimit(1000000)  # 例如这里设置为一百万


## 处理PDF
## 读取PDF的内容 filename是待处理的PDF的名字

###使用PDFminer读取
def getDataUsingPyPDF(pdffile, savefile):
    parser = PDFParser(open('/Users/shuizhou/PycharmProjects/test/programming_vocabulary/download/' + pdffile,
                            'rb'))  # 以二进制打开文件 ,并创建一个pdf文档分析器
    doc = PDFDocument()  ##创建一个pdf文档
    # 将文档对象和连接分析器连接起来
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()

    # 判断该pdf是否支持txt转换

    if doc.is_extractable:
        # 创建一个PDF设备对象
        rsrcmgr = PDFResourceManager()
        # 创建一个pdf设备对象
        laparamas = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparamas)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        contents = ""  # 保存读取的text
        savefile = '/Users/shuizhou/PycharmProjects/test/programming_vocabulary/files/' + savefile
        f = open(savefile, "a+",
                 encoding='utf-8')
        # 依次读取每个page的内容

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()  # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            # 在windows下，新文件的默认编码是gbk编码，所以我们在写入文件的时候需要设置一个编码格式，如下：
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    results = results.replace("\n", " ")  # 去掉换行符 因为排版问题 有的换行导致句子中断
                    f.write(results + "\n")


## 将读取的content以txt格式存放到本地
def saveText(content, Textfile):
    with open(Textfile, "w", encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    # getDataUsingPyPDF('Accelerated C++ Practical Programming by Example.pdf', '2222.txt')
    # getDataUsingPyPDF('C++ Multithreading Cookbook.pdf', '3333.txt')
    # getDataUsingPyPDF('Learn Swift On The Mac.pdf', '5555.txt')
    # getDataUsingPyPDF('Objective-C for Absolute Beginners, 4th Edition.pdf', '6666.txt')
    # getDataUsingPyPDF('Swift Pocket Reference.pdf', '7777.txt')
    # getDataUsingPyPDF('Swift Development with Cocoa.pdf', '8888.txt')
    # getDataUsingPyPDF('Csharp.in.Depth.4th.Edition.pdf', '9999.txt')
    # getDataUsingPyPDF('Learning Cocoa with Objective-C, 4th Edition.pdf', 'cccc.txt')
    # getDataUsingPyPDF('Programming Entity Framework DbContext.pdf', 'dddd.txt')
    # getDataUsingPyPDF('Beginning C 2008 Objects.pdf', 'eeee.txt')
    # getDataUsingPyPDF('The C- Programmer s Study Guide (MCSD).pdf', 'ffff.txt')
    # getDataUsingPyPDF('Xamarin Studio for Android Programming.pdf', 'gggg.txt')
    # getDataUsingPyPDF('Building Maintainable Software, C- Edition.pdf', 'hhhh.txt')
    # getDataUsingPyPDF('Illustrated C- 7, 5th Edition.pdf', 'iiii.txt')
    # getDataUsingPyPDF('Visual C- 2005 Demystified.pdf', 'jjjj.txt')

    # getDataUsingPyPDF('C++CLI in Action.pdf', 'kkkk.txt')
    # getDataUsingPyPDF('Illustrated WPF.pdf', 'llll.txt')
    # getDataUsingPyPDF('Pro Silverlight 3 in C-.pdf', 'mmmm.txt')
    # getDataUsingPyPDF('Professional C- 2012 and .NET 4.5.pdf', 'nnnn.txt')
    # getDataUsingPyPDF('Programming C- 5.0.pdf', 'oooo.txt')
    getDataUsingPyPDF('Unit Testing Principles, Practices, and Patterns.pdf', 'pppp.txt')
