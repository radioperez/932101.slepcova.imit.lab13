from numpy.random import default_rng
import numpy as np
import matplotlib.pyplot as plt
currency1 = [1]
currency2 = [1]
t = [0]
w1 = [0]
w2 = [0]

delta = 1/100
nrm = default_rng().normal

mu = 1 # drift
sigma = 0.6 # volatility -- standart deviation

while len(t) < 100:
    t.append(t[-1] + delta)
    w1.append(w1[-1] + nrm()*np.sqrt(t[-1] - t[-2]))
    w2.append(w2[-1] + nrm()*np.sqrt(t[-1] - t[-2]))
    coin1 = currency1[-1] * np.exp((mu - sigma**2 / 2)*(t[-1] - t[-2])+ sigma * w1[-1])
    currency1.append(coin1)
    coin2 = currency2[-1] * np.exp((mu - sigma**2 / 2)*(t[-1] - t[-2])+ sigma * w2[-1])
    currency2.append(coin2)

plt.plot(t, currency1, label='Currency 1')
plt.plot(t, currency2, label='Currency 2')
plt.legend()
plt.show()