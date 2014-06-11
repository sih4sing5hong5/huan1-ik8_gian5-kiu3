import gzip
import pickle
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
import itertools
import Pyro4

class 語言判斷詞表:
	__物件譀鏡 = 物件譀鏡()
	def 產生(self):
		Pyro4.config.SERIALIZER = 'pickle'
		判斷模型 = Pyro4.Proxy("PYRO:判斷模型@localhost:9091")
		國語孤詞, 閩南語孤詞 = 判斷模型.孤詞表()
		國語孤詞 = self.揣頭前一萬筆(國語孤詞)
		閩南語孤詞 = self.揣頭前一萬筆(閩南語孤詞)
		字串種類={}
		for 資料 in itertools.chain(國語孤詞, 閩南語孤詞):
			詞物件 = 資料[0]
			型=self.__物件譀鏡.看型(詞物件)
			if 型 not in 字串種類:
				字串種類[型]=0
			字串種類[型]+=1
		國語選著詞=[]
		for 資料 in 國語孤詞:
			詞物件 = 資料[0]
			型=self.__物件譀鏡.看型(詞物件)
			if len(國語選著詞)<1000 and 字串種類[型]==1:
				國語選著詞.append(資料)
# 				print(型)
		閩南語選著詞=[]
		for 資料 in 閩南語孤詞:
			詞物件 = 資料[0]
			型=self.__物件譀鏡.看型(詞物件)
			if len(閩南語選著詞)<1000 and 字串種類[型]==1:
				閩南語選著詞.append(資料)
# 				print(型)
			
# 		print(國語孤詞[:10])
# 		print(閩南語孤詞[:10])
# 		print(國語孤詞[5000:5000+10])
# 		print(閩南語孤詞[5000:5000+10])
# 		print(國語孤詞[10000:10000+10])
# 		print(閩南語孤詞[10000:10000+10])
# 		print(len(國語孤詞))
# 		print(len(閩南語孤詞))
		對應編號 = {}
		編號 = 0
		for 資料 in itertools.chain(國語選著詞, 閩南語選著詞):
			詞物件 = 資料[0]
			對應編號[詞物件] = 編號
			編號 += 1
		return 對應編號
	def 揣頭前一萬筆(self, 孤詞表):
		排法 = lambda x:(-x[1], x[2])
		孤詞資料 = []
		for 詞物件, 擺 in 孤詞表:
			if 詞物件 == None:
				continue
			字串 = self.__物件譀鏡.看斷詞(詞物件)
			孤詞資料.append((詞物件, 擺, 字串))
		孤詞資料.sort(key=排法)
		return 孤詞資料[:10000]

if __name__ == '__main__':
	對應編號 = 語言判斷詞表().產生()
	語言判斷詞表檔案 = gzip.open('../語料/分言語/語言判斷詞表.pickle.gz', 'wb')
	pickle.dump(對應編號, 語言判斷詞表檔案,
			protocol = pickle.HIGHEST_PROTOCOL)
	語言判斷詞表檔案.close()
