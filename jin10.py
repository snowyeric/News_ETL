from selenium.webdriver import Chrome
import time
import schedule
from datetime import datetime
import os
import pandas as pd
from hanziconv import HanziConv
from PIL import Image  # pip install image
import matplotlib.pyplot as plt  # pip install matplotlib
from wordcloud import WordCloud  # pip install wordcloud
import jieba  # pip install jieba
import numpy as np
from collections import Counter


def job():
    #先準備好格子df來裝新聞資料data
    c = ["時間", "新聞內容"]
    df = pd.DataFrame(columns = c)
    Now = datetime.now().strftime("%Y%m%d_%H%M%S")

    #連上金時網URL
    driver = Chrome("./chromedriver")
    driver.get("https://www.jin10.com/")
    time.sleep(3)

    #準備兩個變數來裝新聞的發布時間跟發布內容
    news = driver.find_elements_by_class_name("jin-flash_text-box")
    date = driver.find_elements_by_class_name("jin-flash_time")

    #用for迴圈把抓到的元素(逐篇新聞一個一個取出後轉成可讀文字，再放入剛剛準備好的格子df)
    for d, n in zip(date, news ): 
        data = [d.text, n.text]
        # data = HanziConv.toTraditional(data)
        # print(data)
        # if "美" in data[1] or "欧" in data[1]:
             # if "破7" not in data[1]:
        s = pd.Series(data, index=c)
        df = df.append(s, ignore_index=True)
    # df = HanziConv.toTraditional(df)
    #     for n in news:
            # if "美元" in n.text or "欧元" in n.text and "7" not in n.text:
                # s = pd.Series(data, index=c)
                # df = df.append(s, ignore_index=True)
    #最後，把格子裡的內容存入csv檔
    filename = str(Now)+".csv"

    print(str(Now))
    print(filename)
    df.to_csv(filename, encoding="utf-8", index=False)

    #讀csv檔，並透過HanziConv.toTraditional把文字轉換成繁體字元
    simple = open(filename , "r", encoding="utf-8").read()
    text = HanziConv.toTraditional(simple)

    # 設定繁體中文詞庫
    jieba.set_dictionary("jieba_dict/dict.txt.big")
    with open("jieba_dict/stopWord_cloud.txt", "r", encoding="utf-8-sig") as f:  # 設定停用字
        # 讀取停用詞並存於stops串列中

        stops = f.read().split("\n")

    # 儲存字詞
    terms = []

    for t in jieba.cut(text, cut_all=False):
        if t not in stops:
            terms.append(t)
    diction = Counter(terms)

    font = "msyh.ttc"

    # 設定文字雲形狀
    mask = np.array(Image.open("Coins.png"))

    wordcloud = WordCloud(font_path=font)

    # 背景顏色預設黑色, 改為白色
    wordcloud = WordCloud(background_color="white", mask=mask, font_path=font)

    # 產生文字雲
    wordcloud.generate_from_frequencies(frequencies=diction)

    # 產生圖片
    plt.figure(figsize=(6, 6))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    wordcloud.to_file(filename + ".png")



    time.sleep(3)

    #關閉瀏覽器
    driver.close()

    #告訴我的爬蟲，多久要再起來工作一次 
    
    schedule.every(4).hours.do(job)
job()

while True:
    schedule.run_pending()
    time.sleep(1)




