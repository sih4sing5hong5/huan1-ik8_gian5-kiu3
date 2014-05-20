import json
from 處理TGB.提掉網頁標仔工具 import 提掉網頁標仔工具
from 處理TGB.提掉文章標仔工具 import 提掉文章標仔工具
import gzip
from 分言語.語言判斷用戶端 import 判斷
import os
from 臺灣言語工具.斷詞.中研院工具.官方斷詞剖析工具 import 官方斷詞剖析工具
from 臺灣言語工具.斷詞.中研院工具.斷詞結構化工具 import 斷詞結構化工具
from 臺灣言語工具.字詞組集句章.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.字詞組集句章.音標系統.閩南語.教會羅馬字音標 import 教會羅馬字音標
from 臺灣言語工具.字詞組集句章.解析整理.文章粗胚 import 文章粗胚

class 解析TGB:
	def 看國閩分數(self, 分數檔名 ):
		分數檔案 = gzip.open(分數檔名, 'rt')
		問題, 答案 = json.load(分數檔案,)
		分數檔案.close()
		訓練問題=[]
		from sklearn import svm
		for 問 in 問題:
			訓練問題.append([問[0]])
		clf = svm.SVC()
		clf.fit(訓練問題, 答案)
# 		clf.fit(問題, 答案)  
		結果=clf.predict(訓練問題)
		毋著=0
		for 結,答 in zip(結果,答案):
			print(結,答)
			if 結!=答:
				毋著+=1
		print(毋著,len(答案))
# 		for 問, 答 in zip(問題, 答案):
# 		分數檔案 = gzip.open(分數檔名, 'wt')
# 		json.dump((), 分數檔案)
# 		分數檔案.close()

if __name__ == '__main__':
	TGB = 解析TGB()
	TGB.看國閩分數('../語料/TGB/逐句訓練分數.json.gz')
