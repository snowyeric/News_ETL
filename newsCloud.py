from PIL import Image  # pip install image
import matplotlib.pyplot as plt  # pip install matplotlib
from wordcloud import WordCloud  # pip install wordcloud
import jieba  # pip install jieba
import numpy as np
from collections import Counter

text = open('20190910_101329.csv', "r", encoding="utf-8").read()  # 讀文字資料

jieba.set_dictionary("jieba_dict/dict.txt.big")  # 設定繁體中文詞庫
with open("jieba_dict/stopWord_cloud.txt", "r", encoding="utf-8-sig") as f:  # 設定停用字
    stops = f.read().split("\n")  # 讀取停用詞並存於stops串列中

terms = []  # 儲存字詞
for t in jieba.cut(text, cut_all=False):
    if t not in stops:
        terms.append(t)
diction = Counter(terms)

font = "msyh.ttc"
mask = np.array(Image.open("Coins.png"))  # 設定文字雲形狀
wordcloud = WordCloud(font_path=font)
wordcloud = WordCloud(background_color="white", mask = mask, font_path=font)  # 背景顏色預設黑色, 改為白色
wordcloud.generate_from_frequencies(frequencies=diction)  # 產生文字雲

# 產生圖片
plt.figure(figsize=(6, 6))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

wordcloud.to_file("news_Wordcloud.png")
