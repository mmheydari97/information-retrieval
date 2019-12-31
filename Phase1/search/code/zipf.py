import numpy as np
import matplotlib.pyplot as plt

dic = {}  ## dictionary (do not remove frequents words)
ss = []
for ii in dic.items():
    cnt = 0
    for a in ii[1]:
        cnt += len(a[1])
    ss.append(cnt)

ss.sort()
num = 20
ss = [390, 391, 392, 394, 394, 397, 399, 405, 420, 421, 424, 425, 427, 434, 435, 436, 440, 451, 452, 458, 461, 464, 471,
      473, 474, 475, 482, 486, 488, 489, 499, 504, 507, 513, 514, 514, 526, 528, 530, 539, 539, 550, 553, 554, 566, 572,
      590, 596, 600, 603, 603, 611, 641, 648, 650, 690, 702, 719, 723, 760, 818, 965, 985, 995, 1009, 1047, 1108, 1108,
      1140, 1147, 1219, 1229, 1253, 1290, 1306, 1311, 1345, 1366, 1367, 1481, 1526, 1533, 1762, 2440, 2589, 3904, 4481,
      5032, 5137, 5403, 5580, 6123, 6292, 8254, 10195, 10278, 10719, 12915, 16706]
ss = ss[-num:]  ## most 100 frequents

# y = np.array(ss)
y = np.array(ss)
y = np.log10(y)
y = y[::-1]

x = np.array([i + 1 for i in range(num)])
x = np.log10(x)

k = 30000
yy = np.log10(k) - x
# x = x[::-1]
# print(x)

# print(y[0:10])
# print(x[0:10])

plt.plot(x, y, label='real')
plt.plot(x, yy, label='predicted')
plt.legend(loc=1)
plt.show()