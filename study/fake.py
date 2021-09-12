# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


a = 957.8
b = 632.1
c = 420.8

# 生成虚假高斯数据
def fake(mu, zeros, sigma=0):
    if sigma == 0:
        sigma = mu / 15
    data = np.random.normal(mu, sigma, 80)
    begin = np.arange(0, 5, 1) * mu / 10
    normal = np.random.normal(np.sqrt(mu) / 4, mu / 30, 5)
    normal[normal <= 0] = 0
    begin += normal
    data[:5] = begin
    data[:zeros] = 0.0
    return data

xs = np.arange(0, 80, 1)
adata = fake(a, 0, a /10)
bdata = fake(b, 0)
cdata = fake(c, 2)

data = adata + bdata + cdata


fig, axs = plt.subplots(1, 1)
axs.set_ylim(0, 2500)
axs.plot(xs, adata, color='r')
axs.plot(xs, bdata, color='g')
axs.plot(xs, cdata, color='b')
axs.plot(xs, data, color='y')
plt.show()

# dfp = np.zeros((80, 4))
# dfp[:, 0] = adata
# dfp[:, 1] = bdata
# dfp[:, 2] = cdata
# dfp[:, 3] = data

# df = pd.DataFrame(dfp, columns=['a', 'b', 'c', 'sum'], dtype=float)

# df.to_excel("./test.xlsx")