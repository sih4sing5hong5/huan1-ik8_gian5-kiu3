# -*- coding: utf-8 -*-
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
from 臺灣言語工具.字詞組集句章.基本元素.句 import 句
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.斷詞.型音辭典 import 型音辭典
from 臺灣言語工具.斷詞.動態規劃斷詞 import 動態規劃斷詞

class 對摩西翻譯改:
	語料 = None
	對齊語料對應表 = None
	對齊片語表 = None
	辭典對應表 = None
	字典對應表 = None
	連詞 = None
	埠='8080'
	__分析器 = 拆文分析器()
	__粗胚 = 文章粗胚()
	用戶端 = None
	def 載入(self):
		self.語料 = 讀語料()
		self.對齊語料對應表 = self.語料.產生對齊語料對應表(
			來源詞='../語料/訓.國語字_訓.閩南語音.trn.src.vcb',
			目標詞='../語料/訓.國語字_訓.閩南語音.trn.trg.vcb',
			機率表='../語料/訓.國語字_訓.閩南語音.t3.final')

		辭典對應表模型檔名 = '辭典對應表.pickle'
		if os.path.isfile(辭典對應表模型檔名):
			辭典對應表模型檔案 = open(辭典對應表模型檔名, 'rb')
			教育部對應表 = pickle.load(辭典對應表模型檔案)
			辭典對應表模型檔案.close()
		else:
			教育部對應表 = self.語料.產生辭典對應表('../語料/教育部辭典對應詞結果.json')
			辭典對應表模型檔案 = open(辭典對應表模型檔名, 'wb')
			pickle.dump(教育部對應表, 辭典對應表模型檔案, protocol=pickle.HIGHEST_PROTOCOL)
			辭典對應表模型檔案.close()
		self.辭典對應表, self.字典對應表 = 教育部對應表
		語言模型檔名 = '語言模型檔名.pickle'
		if os.path.isfile(語言模型檔名):
			語言模型檔案 = open(語言模型檔名, 'rb')
			self.連詞 = pickle.load(語言模型檔案)
			語言模型檔案.close()
		else:
			self.連詞 = self.語料.讀語言模型檔案('../語料/訓.閩南語音.txt')
			語言模型檔案 = open(語言模型檔名, 'wb')
			pickle.dump(self.連詞, 語言模型檔案, protocol=pickle.HIGHEST_PROTOCOL)
			語言模型檔案.close()
			
		self.用戶端 = 摩西用戶端('localhost',self.埠)
		
		self.辭典 = 型音辭典(4)
		for 型, 音陣列 in self.字典對應表.items():
			for 音 in 音陣列:
				組物件 = self.__分析器.產生對齊組(型, 音)
				for 詞物件 in 組物件.內底詞:
					for 字物件 in 詞物件.內底字:
						暫=字物件.型
						字物件.型=字物件.音
						字物件.音=暫
					self.辭典.加詞(詞物件)
	def 試驗(self):
		斷詞工具 = 動態規劃斷詞()
		標音工具 = 動態規劃標音()
		譀鏡 = 物件譀鏡()
		結果檔案 = open('試驗結果.txt', 'w')
		for 一逝 in self.語料.讀語料檔案('../語料/試.國語字.txt')[:]:
# 			print(一逝)
			翻譯結果 = self.用戶端.翻譯(一逝, 另外參數={'nbest':1})
			全部句 = []
			for 上好句 in 翻譯結果['nbest']:
				句物件 = self.__分析器.建立句物件('')
# 				print(上好句['hyp'])
				編號=0
				for 一个詞 in 上好句['hyp'].split():
# 					print(一个詞)
					集物件 = self.__分析器.建立集物件('')
					if 一个詞.endswith('|UNK|UNK|UNK'):
						國語詞 = 一个詞.replace('|UNK|UNK|UNK', '')
						if 國語詞 in self.對齊語料對應表:
							for 閩南語詞, 機率 in self.對齊語料對應表[國語詞]:
								組物件 = self.__分析器.建立組物件(閩南語詞)
								組物件.屬性 = {'機率':self.連詞.對數(float(機率))}
								集物件.內底組.append(組物件)
							句物件.內底集.append(集物件)
			# 				print('對齊語料對應表',國語詞,對齊語料對應表[國語詞])
			# 				print(集物件)
						elif 國語詞 in self.辭典對應表:
							for 閩南語詞 in self.辭典對應表[國語詞]:
								組物件 = self.__分析器.建立組物件(閩南語詞)
								集物件.內底組.append(組物件)
							句物件.內底集.append(集物件)
			# 				print('辭典對應表',國語詞,辭典對應表[國語詞])
			# 				print(集物件)
						elif 國語詞 in self.字典對應表:
							for 閩南語詞 in self.字典對應表[國語詞]:
								組物件 = self.__分析器.建立組物件(閩南語詞)
								集物件.內底組.append(組物件)
							句物件.內底集.append(集物件)
						else:
							組物件 = self.__分析器.建立組物件(國語詞)
							斷詞了物件 = 斷詞工具.斷詞(self.辭典, 組物件)
							for 集物件 in 斷詞了物件.內底集:
								for 組物件 in 集物件.內底組:
									組物件.屬性={'詞組編號':編號}
							句物件.內底集.extend(斷詞了物件.內底集)
					else:
						組物件 = self.__分析器.建立組物件(一个詞)
						集物件.內底組.append(組物件)
						句物件.內底集.append(集物件)
					編號+=1
				全部句.append(句物件)
			上好分數 = None
			上好物件 = None
			for 句物件 in 全部句:
				結果物件, 結果分數, 詞數 = 標音工具.標音(self.連詞, 句物件)
				if 上好分數 == None or 上好分數 < 結果分數:
					上好分數 = 結果分數
					上好物件 = 結果物件
			結果=[]
			頂一个組物件=None
			for 集物件 in 上好物件.內底集:
				組物件=集物件.內底組[0]
				佮頭前仝款=False
				try:
					if 組物件.屬性['詞組編號']==頂一个組物件.屬性['詞組編號']:
						結果[-1]+='-'
						結果[-1]+=譀鏡.看型(組物件, 物件分字符號='-', 物件分詞符號='-')
						佮頭前仝款=True
				except:
					pass
				if not 佮頭前仝款:
					結果.append(譀鏡.看型(組物件, 物件分字符號='-', 物件分詞符號=' '))
				頂一个組物件=組物件
# 			print(譀鏡.看型(上好物件, 物件分字符號='-', 物件分詞符號=' '))
			結果文句=' '.join(結果)
			print(結果文句)
			print(結果文句, file=結果檔案)

		結果檔案.close()

if __name__ == '__main__':
	翻譯研究 = 對摩西翻譯改()
	翻譯研究.載入()
	翻譯研究.試驗()
