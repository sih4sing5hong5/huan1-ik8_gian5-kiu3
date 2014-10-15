# -*- coding: utf-8 -*-
from 臺灣言語工具.斷詞.中研院工具.官方斷詞剖析工具 import 官方斷詞剖析工具
from 臺灣言語工具.斷詞.中研院工具.斷詞結構化工具 import 斷詞結構化工具
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
from 翻譯研究.讀語料 import 讀語料
from 臺灣言語工具.斷詞.連詞揀集內組 import 連詞揀集內組
from 臺灣言語工具.表單.實際語句連詞 import 實際語句連詞
from 臺灣言語工具.解析整理.字物件篩仔 import 字物件篩仔
from 臺灣言語工具.基本元素.公用變數 import 無音
from 校對.公家辭典連詞 import 公家辭典連詞
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
class 華臺斷詞:
	__語料 = 讀語料()
	def 處理音標(self, 辭典, 閩南語一對一檔名, 結果檔名=None,
			辭典揣詞類=拄好長度辭典揣詞):
# 		斷字檔案 = open(檔案名.replace('.txt', '斷字.txt'), 'w')
# 		斷詞檔案 = open(檔案名.replace('.txt', '斷詞.txt'), 'w')
# 		斷詞剖析工具=官方斷詞剖析工具()
# 		結構化工具=斷詞結構化工具()
# 		譀鏡=物件譀鏡()
		__分析器 = 拆文分析器()
		__粗胚 = 文章粗胚()
		__家私 = 轉物件音家私()
		__譀鏡 = 物件譀鏡()
		連詞 = 實際語句連詞(1)
		動態斷詞 = 辭典揣詞類()
		動態標音 = 連詞揀集內組()
		篩仔 = 字物件篩仔()
		結果 = []
		for 一逝 in self.__語料.讀語料檔案(閩南語一對一檔名):
			句物件 = __分析器.轉做句物件(一逝)
# 			標準句物件 = __家私.轉音(臺灣閩南語羅馬字拼音, 句物件)
			標準句物件 = 句物件
			斷詞句物件, 分數, 詞數 = 動態斷詞.揣詞(辭典, 標準句物件)
			標音句物件, 分數, 詞數 = 動態標音.揀(連詞, 斷詞句物件)
# 			字陣列 = 篩仔.篩出字物件(標音句物件)
# 			for 字物件 in 字陣列:
# 				if 字物件.音 == 無音:
# 					字物件.音 = 字物件.型
			if 結果檔名 == None:
				print(__譀鏡.看分詞(標音句物件))
			else:
				結果.append(__譀鏡.看分詞(標音句物件))
# 			print(__譀鏡.看音(標音句物件), file=斷詞檔案)
			
		if 結果檔名 != None:
			self.__語料.寫語料檔案(結果檔名, '\n'.join(結果))
	
if __name__ == '__main__':
	辭典連詞 = 公家辭典連詞()
	辭典, 連詞 = 辭典連詞.產生而且加一个檔案('../語料/臺語文數位典藏一對一.txt.gz')
	
	斷字詞 = 華臺斷詞()
	斷字詞.處理音標(辭典, '../語料/訓.華臺一對一斷詞.txt.gz')
	
