import json
import urllib.request
from 臺灣言語工具.字詞組集句章.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.標音.語句連詞 import 語句連詞
from 翻譯研究.讀語料 import 讀語料
from 臺灣言語工具.字詞組集句章.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.字詞組集句章.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
import pickle
import os
from 臺灣言語工具.標音.動態規劃標音 import 動態規劃標音
from 臺灣言語工具.字詞組集句章.解析整理.物件譀鏡 import 物件譀鏡

		
if __name__ == '__main__':
	語料 = 讀語料()
	對齊語料對應表=語料.產生對齊語料對應表(
		來源詞='../語料/訓.國語字_訓.閩南語音.trn.src.vcb',
		目標詞='../語料/訓.國語字_訓.閩南語音.trn.trg.vcb',
		機率表='../語料/訓.國語字_訓.閩南語音.t3.final')
	辭典對應表模型檔名='辭典對應表.pickle'
	if os.path.isfile(辭典對應表模型檔名):
		辭典對應表模型檔案=open(辭典對應表模型檔名,'rb')
		教育部對應表 = pickle.load(辭典對應表模型檔案)
		辭典對應表模型檔案.close()
	else:
		教育部對應表=語料.產生辭典對應表('/home/chhsueh/git/temp/test/test3/結果.json')
		辭典對應表模型檔案=open(辭典對應表模型檔名,'wb')
		pickle.dump(教育部對應表, 辭典對應表模型檔案, protocol=pickle.HIGHEST_PROTOCOL)
		辭典對應表模型檔案.close()
	辭典對應表,字典對應表=教育部對應表
	分析器=拆文分析器()
	粗胚=文章粗胚()
	語言模型檔名='語言模型檔名.pickle'
	if os.path.isfile(語言模型檔名):
		語言模型檔案=open(語言模型檔名,'rb')
		連詞 = pickle.load(語言模型檔案)
		語言模型檔案.close()
	else:
		連詞=語料.讀語言模型檔案('../語料/訓.閩南語音.txt')
		語言模型檔案=open(語言模型檔名,'wb')
		pickle.dump(連詞, 語言模型檔案, protocol=pickle.HIGHEST_PROTOCOL)
		語言模型檔案.close()
	標音工具=動態規劃標音()
	譀鏡=物件譀鏡()
	結果檔案=open('翻譯結果.txt','w')
	for 一逝 in 語料.讀語料檔案('../語料/試.國語字.txt'):
		句物件=分析器.建立句物件('')
		for 國語詞 in 一逝.split():
			集物件=分析器.建立集物件('')
			if 國語詞 in 對齊語料對應表:
				for 閩南語詞,機率 in 對齊語料對應表[國語詞]:
					組物件=分析器.建立組物件(閩南語詞)
					組物件.屬性={'機率':連詞.對數(float(機率))}
					集物件.內底組.append(組物件)
# 				print('對齊語料對應表',國語詞,對齊語料對應表[國語詞])
# 				print(集物件)
			elif 國語詞 in 辭典對應表:
				for 閩南語詞 in 辭典對應表[國語詞]:
					組物件=分析器.建立組物件(閩南語詞)
					集物件.內底組.append(組物件)
# 				print('辭典對應表',國語詞,辭典對應表[國語詞])
# 				print(集物件)
			elif 國語詞 in 字典對應表:
				for 閩南語詞 in 字典對應表[國語詞]:
					組物件=分析器.建立組物件(閩南語詞)
					集物件.內底組.append(組物件)
			else:
				組物件=分析器.建立組物件(國語詞)
				集物件.內底組.append(組物件)
			句物件.內底集.append(集物件)
		結果物件,上好分數, 詞數=標音工具.標音(連詞, 句物件)
# 		print(結果物件)
		print(譀鏡.看型(結果物件, 物件分字符號='-', 物件分詞符號=' '))
		print(譀鏡.看型(結果物件, 物件分字符號='-', 物件分詞符號=' '),file=結果檔案)
	結果檔案.close()
