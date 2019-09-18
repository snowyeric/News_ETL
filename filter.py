import csv
import pandas as pd
from hanziconv import HanziConv

c = ["時間", "新聞內容"]
df = pd.DataFrame(columns=c)
# 開啟 CSV 檔案
with open('E:/Python/PyETL/project_eurusd/20190801_111755.csv', newline='',encoding="utf-8")as csvfile:

# 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)

# 以迴圈輸出每一列
  for row in rows:
      if "美元" in row[1] or "欧元" in row[1] and "7" not in row:
        print(row)
        s = pd.Series(row, index=c)
        df = df.append(s, ignore_index=True)
  df.to_csv("news.csv", encoding="utf-8", index=False)
  