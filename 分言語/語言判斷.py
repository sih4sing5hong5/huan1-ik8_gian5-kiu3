import gzip
import pickle
import os
import unicodedata
from 臺灣言語工具.字詞組集句章.基本元素.公用變數 import 統一碼漢字佮組字式類
from 臺灣言語工具.字詞組集句章.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.字詞組集句章.解析整理.字物件篩仔 import 字物件篩仔
from 臺灣言語工具.字詞組集句章.音標系統.閩南語.教會羅馬字音標 import 教會羅馬字音標
from 臺灣言語工具.字詞組集句章.音標系統.閩南語.通用拼音音標 import 通用拼音音標
from 臺灣言語工具.斷詞.中研院工具.官方斷詞剖析工具 import 官方斷詞剖析工具
from 臺灣言語工具.斷詞.中研院工具.斷詞結構化工具 import 斷詞結構化工具
from 臺灣言語工具.標音.動態規劃標音 import 動態規劃標音
from 臺灣言語工具.斷詞.動態規劃斷詞 import 動態規劃斷詞
import Pyro4
from 臺灣言語工具.字詞組集句章.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.字詞組集句章.解析整理.轉物件音家私 import 轉物件音家私
from 分言語.語言判斷模型 import 語言判斷模型

class 語言判斷:
	國語連詞 = None
	閩南語辭典 = None
	閩南語連詞 = None
	__粗胚 = 文章粗胚()
	__分析器 = 拆文分析器()
	__篩仔 = 字物件篩仔()
	__家私 = 轉物件音家私()
	__斷詞剖析工具 = 官方斷詞剖析工具()
	__斷詞結構化工具 = 斷詞結構化工具()
	__標音 = 動態規劃標音()
	__斷詞 = 動態規劃斷詞()
	判斷模型 = 語言判斷模型()
	def 分數(self, 語句):
		處理減號 = self.__粗胚.建立物件語句前處理減號(教會羅馬字音標, 語句)
		教羅, 通用 = self.有偌濟音標(處理減號)
		return self.國語分數(處理減號), self.閩南語分數(處理減號), \
			self.有偌濟漢字(處理減號), 教羅, 通用
	def 有偌濟漢字(self, 語句):
		漢字 = 0
		for 字 in 語句:
			if unicodedata.category(字) in 統一碼漢字佮組字式類:
				漢字 += 1
		return 漢字 / len(語句)
	def 有偌濟音標(self, 處理減號):
		教羅 = 0
		通用 = 0
		組物件 = self.__分析器.建立組物件(處理減號)
		字陣列 = self.__篩仔.篩出字物件(組物件)
		for 字物件 in 字陣列:
			if 教會羅馬字音標(字物件.型).音標 != None:
				教羅 += 1
			if 通用拼音音標(字物件.型).音標 != None:
				通用 += 1
		return 教羅 / len(字陣列), 通用 / len(字陣列),
	def 國語分數(self, 處理減號):
		斷詞結果 = self.__斷詞剖析工具.斷詞(處理減號, 一定愛成功=True)
		章物件 = self.__斷詞結構化工具.斷詞轉章物件(斷詞結果)
		標好, 分數, 詞數 = self.判斷模型.國語分數(章物件)
		return 分數, 詞數
	def 閩南語分數(self, 處理減號):
		教羅, 通用 = self.有偌濟音標(處理減號)
		組物件 = self.__分析器.建立句物件(處理減號)
		if 教羅 >= 通用:
			標準組物件 = self.__家私.轉做標準音標(教會羅馬字音標, 組物件)
		else:
			標準組物件 = self.__家私.轉做標準音標(通用拼音音標, 組物件)
		標好, 分數, 詞數 = self.判斷模型.閩南語分數(標準組物件)
		return 分數, 詞數

判斷 = 語言判斷()
Pyro4.config.SERIALIZER = 'pickle'
判斷.判斷模型 = Pyro4.Proxy("PYRO:判斷模型@localhost:9091")

def __試驗():
	print(判斷.分數('tsiong1-hua3-kuan7 ting2-jim7 gi7-tiunn2 peh8-hong5-sim1 e5 hau7-senn1 peh8-bin2-kiat8 '))
	print(判斷.分數('彰化縣 前任 議長 白鴻森 的 兒子 白閔傑'))
	print(判斷.分數('彰化縣 前任 議長 白鴻森 的 後生 白閔傑'))
	print(判斷.分數('Piān-nā到「決戰ê關鍵」, ta̍k-ê to lóng ē顧慮「事後算siàu」(無論是內場iah外場), m̄-chiah ē jú來jú無人beh開路, 衝頭1 ê. Chit-má內場做頭ê壓力已經大kah接受採訪ê時, 講tio̍h學生安全tō目屎liàn--落-來.'))
	print(判斷.分數('每到「決戰關頭」，大家都會顧慮「秋後算帳」（不管是場內、場外），所以越來越沒有人要當頭開第一槍。現在場內當頭的已經壓力大到受訪時，談到學生安全時都落下眼淚了。 '))

if __name__ == '__main__':
	import cProfile
	cProfile.run('__試驗()')
	