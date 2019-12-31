from dictionary import news_retrieval, Normalizing, Tokenization, Stemming, add_word
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# xx = []
# yy = []

# dfs = pd.read_excel('IR-F19-Project01-Input-2k.xlsx')
# contents = dfs['content']

# for j in range(30):

#     doc_number = [i for i in range(j*30 + 20)]
#     dic = {}
#     for doc_id in doc_number:
#         x = contents[doc_id]
#         x = news_retrieval(x) # واکشی
#         x = Normalizing(x)
#         x = Tokenization(x) # استخراج توکن
#         # x = remove_frequents(x)
#         x = Stemming(x) ## ریشه یابی
#         dic = add_word(doc_id, x, dic) # ایجاد شاخص معکوس مکانی

#     cnt = 0
#     for ii in dic.items():
#         for a in ii[1]:
#             cnt += len(a[1])

#     xx.append(len(dic))
#     yy.append(cnt)

# print(xx)
# print(yy)


## _____________________________________________###

x = np.array(
    [2260, 4025, 5198, 6004, 6784, 7307, 7872, 8507, 9398, 10304, 10936, 11339, 11927, 12324, 12946, 13265, 13725,
     14155, 14393, 14732, 15055, 15606, 15962, 16343, 16613, 17025, 17322, 17601, 18000, 18335])
y = np.array(
    [8984, 19929, 32477, 42801, 55525, 63187, 71541, 82448, 98520, 116481, 129003, 138050, 149173, 158302, 170897,
     181512, 195722, 205707, 212584, 222028, 231984, 243753, 256174, 269007, 277874, 292062, 302539, 311886, 328802,
     340391])
x = np.log10(x)
y = np.log10(y)
k = 0.4
yy = np.log10(k) + 1.4 * x

plt.plot(x, y, label='real')
plt.plot(x, yy, label='predicted')
plt.legend(loc=1)
plt.show()