import pylab as plt
import plotly.plotly as py

fig = plt.figure()

x = 200 + 25*plt.randn(1000)
y = 150 + 25*plt.randn(1000)
n, bins, patches = plt.hist([x, y])

plt.show()