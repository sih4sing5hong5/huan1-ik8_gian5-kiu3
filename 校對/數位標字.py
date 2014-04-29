# -*- coding: utf-8 -*-
from 臺灣言語工具.斷詞.中研院工具.官方斷詞剖析工具 import 官方斷詞剖析工具
from 臺灣言語工具.斷詞.中研院工具.斷詞結構化工具 import 斷詞結構化工具
from 臺灣言語工具.字詞組集句章.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.字詞組集句章.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.字詞組集句章.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.字詞組集句章.解析整理.轉物件音家私 import 轉物件音家私
from 翻譯研究.讀語料 import 讀語料
from 臺灣言語工具.斷詞.動態規劃斷詞 import 動態規劃斷詞
from 臺灣言語工具.標音.動態規劃標音 import 動態規劃標音
from 臺灣言語工具.標音.語句連詞 import 語句連詞
from 臺灣言語工具.字詞組集句章.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.字詞組集句章.解析整理.字物件篩仔 import 字物件篩仔
from 臺灣言語工具.字詞組集句章.基本元素.公用變數 import 無音
from 臺灣言語工具.斷詞.型音辭典 import 型音辭典

class 數位標字:
	__語料 = 讀語料()
	def 標字(self, 辭典, 連詞, 閩南語一對一檔名, 結果檔名=None):
		__分析器 = 拆文分析器()
		__粗胚 = 文章粗胚()
		__家私 = 轉物件音家私()
		__譀鏡 = 物件譀鏡()
		動態斷詞 = 動態規劃斷詞()
		動態標音 = 動態規劃標音()
		篩仔 = 字物件篩仔()
		結果 = []
		for 閩南語一對一 in self.__語料.讀語料檔案(閩南語一對一檔名):
			句物件 = __分析器.轉做句物件(閩南語一對一)
# 			標準句物件 = __家私.轉做標準音標(臺灣閩南語羅馬字拼音, 句物件)
			標準句物件 = 句物件
			# 處理型佮音仝款，愛共音提掉
			字陣列 = 篩仔.篩出字物件(標準句物件)
			for 字物件 in 字陣列:
				if 字物件.音 == 字物件.型:
					字物件.音 = 無音					
			斷詞句物件, 分數, 詞數 = 動態斷詞.斷詞(辭典, 標準句物件)
			標音句物件, 分數, 詞數 = 動態標音.標音(連詞, 斷詞句物件)
			字陣列 = 篩仔.篩出字物件(標音句物件)
			for 字物件 in 字陣列:
				if 字物件.音 == 無音:
					字物件.音 = 字物件.型
# 			print(__譀鏡.看斷詞(標準句物件))
# 			print(斷詞句物件)
			if 結果檔名 == None:
				print(__譀鏡.看斷詞(標音句物件))
			else:
				結果.append(__譀鏡.看斷詞(標音句物件))
# 			print(__譀鏡.看音(標音句物件), file=斷詞檔案)
		self.__語料.寫語料檔案(結果檔名, 結果)
# 			print(斷字)
	
	
if __name__ == '__main__':
	語料 = 讀語料()	
	辭典 = 型音辭典(4)
	語料.產生辭典(辭典, '../語料/辭典一對一.txt.gz')
	語料.產生辭典(辭典, '../語料/附錄句一對一斷詞.txt.gz')
	語料.產生辭典(辭典, '../語料/訓.例句一對一斷詞.txt.gz')
	語料.產生辭典(辭典, '../語料/訓.華臺一對一斷詞.txt.gz')
	連詞 = 語句連詞(3)
	語料.產生連詞(連詞, '../語料/附錄句一對一斷詞.txt.gz')
	語料.產生連詞(連詞, '../語料/訓.例句一對一斷詞.txt.gz')
	語料.產生連詞(連詞, '../語料/訓.華臺一對一斷詞.txt.gz')
	
	標字 = 數位標字()
	標字.標字(辭典, 連詞, '../語料/臺語文數位典藏一對一.txt.gz')
	
