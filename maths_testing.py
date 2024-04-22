import numpy as np
from scipy.stats import binom, bernoulli
import matplotlib.pyplot as plt

ha = 1.1
hd = 1.1
aa = 0.9
ad = 0.9

ph = ha / (ad * 90)
pa = aa / (hd * 90)

fig, ax = plt.subplots(1, 1)

n = 90
x = list(range(101))

pmf_home = binom.pmf(x, n, ph)
cdf_home = binom.cdf(x, n, ph)

pmf_away = binom.pmf(x, n, pa)
cdf_away = binom.cdf(x, n, pa)

draw_prob, home_win_prob = 0, 0
for i in x:
        draw_prob += pmf_home[i] * pmf_away[i]
for i in x[:-1]:
        home_win_prob += pmf_home[i+1] * cdf_away[i]
away_win_prob = 1 - home_win_prob - draw_prob

print(home_win_prob, draw_prob, away_win_prob)





# Plot
n, p = 90, ph
mean, var, skew, kurt = binom.stats(n, p, moments='mvsk')
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
fig, ax = plt.subplots(1, 1)
ax.plot(x, binom.pmf(x, n, ph), 'bo', ms=8, label='home pmf')
ax.plot(x, binom.pmf(x, n, pa), 'ro', ms=8, label='away pmf')
ax.vlines(x, 0, binom.pmf(x, n, ph), colors='b', lw=5, alpha=0.5)
ax.vlines(x, 0, binom.pmf(x, n, pa), colors='r', lw=5, alpha=0.5)
rv = binom(n, ph)
ax.legend(loc='best', frameon=False)
plt.show()

