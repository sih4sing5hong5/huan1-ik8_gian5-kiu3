# -*- coding: utf-8 -*-
from 翻譯研究.對摩西翻譯改 import 對摩西翻譯改
import sys

class 對摩西翻譯改通用(對摩西翻譯改):
	埠 = None
	結果檔名 = None
	試驗檔名 = None
	
# mosesserver -f 閩南語斷詞/model/moses.ini --server-port 8201
# mosesserver -f 國語斷詞組/model/moses.ini --server-port 8202
# mosesserver -f 閩南語斷詞組/model/moses.ini --server-port 8203
# mosesserver -f 國語斷詞組閩南語斷詞/model/moses.ini --server-port 8204
# mosesserver -f 國語斷詞閩南語斷詞組/model/moses.ini --server-port 8205
if __name__ == '__main__':
	翻譯研究 = 對摩西翻譯改通用()
	翻譯研究.結果檔名 = sys.argv[1]
	翻譯研究.試驗檔名 = '../基準/試.華臺國語字{}.txt'.format(
			sys.argv[2].replace('華臺',''))
	翻譯研究.埠 = sys.argv[3]
	翻譯研究.載入()
	翻譯研究.試驗()
