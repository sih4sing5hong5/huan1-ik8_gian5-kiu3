# -*- coding: utf-8 -*-
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
from 翻譯研究.讀語料 import 讀語料
from 臺灣言語工具.斷詞.辭典揣詞 import 辭典揣詞
from 臺灣言語工具.斷詞.連詞揀集內組 import 連詞揀集內組
from 臺灣言語工具.表單.語句連詞 import 語句連詞
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.解析整理.字物件篩仔 import 字物件篩仔
from 臺灣言語工具.基本元素.公用變數 import 無音
from 臺灣言語工具.表單.型音辭典 import 型音辭典
from 校對.公家辭典連詞 import 公家辭典連詞

class 數位標字:
	__語料 = 讀語料()
	def 標字(self, 辭典, 連詞, 閩南語一對一檔名, 結果檔名 = None):
		__分析器 = 拆文分析器()
		__粗胚 = 文章粗胚()
		__家私 = 轉物件音家私()
		__譀鏡 = 物件譀鏡()
		動態斷詞 = 辭典揣詞()
		動態標音 = 連詞揀集內組()
		篩仔 = 字物件篩仔()
		結果 = []
		for 閩南語一對一 in self.__語料.讀語料檔案(閩南語一對一檔名):
			原來組物件 = __分析器.轉做組物件(閩南語一對一)
			# 處理型佮音仝款，愛共音提掉
			字陣列 = 篩仔.篩出字物件(原來組物件)
			for 字物件 in 字陣列:
				if 字物件.音 == 字物件.型:
					字物件.音 = 無音
			斷詞句物件, 分數, 詞數 = 動態斷詞.斷詞(辭典, 原來組物件)
			標音句物件, 分數, 詞數 = 動態標音.標音(連詞, 斷詞句物件)
			字陣列 = 篩仔.篩出字物件(標音句物件)
			for 字物件 in 字陣列:
				if 字物件.音 == 無音:
					字物件.音 = 字物件.型
# 			print(__譀鏡.看斷詞(標準句物件))
# 			print(斷詞句物件)
			所在 = 0
			還原斷詞組物件 = __分析器.建立組物件('')
			for 原來詞物件 in 原來組物件.內底詞:
				詞物件 = __分析器.建立詞物件('')
				詞物件.內底字 = 字陣列[所在:所在 + len(原來詞物件.內底字)]
				還原斷詞組物件.內底詞 .append(詞物件)
				所在 += len(原來詞物件.內底字)
			if 結果檔名 == None:
				print(__譀鏡.看斷詞(還原斷詞組物件))
			else:
				結果.append(__譀鏡.看斷詞(還原斷詞組物件))
# 			print(__譀鏡.看音(標音句物件), file=斷詞檔案)
		if 結果檔名 != None:
			self.__語料.寫語料檔案(結果檔名, '\n'.join(結果))

if __name__ == '__main__':
	辭典連詞 = 公家辭典連詞()
	辭典, 連詞 = 辭典連詞.產生而且加一个檔案('../語料/訓.華臺一對一斷詞.txt.gz')

	標字 = 數位標字()
	標字.標字(辭典, 連詞, '../語料/臺語文數位典藏一對一.txt.gz')

