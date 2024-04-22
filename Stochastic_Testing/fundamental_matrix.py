import numpy as np

# TODO: Go to page 418 of prob

P = np.array([
    [0.5, 0.25, 0.25],
    [0.5, 0, 0.5],
    [0.25, 0.25, 0.5]
])

Pn = P
u = np.array([1, 0, 0])
ui = u

#print(np.dot(u, P))

expected_visits = np.array([0, 0, 0])

# Probability matrix after i transitions (Pi), probability of being in each state at time i (ui)
#for i in range(10):
#    expected_visits = expected_visits + ui
#    print(f'P{i}\n{Pn}')
#    print(f'\nu{i} : {ui}')
#    Pi = np.dot(P, Pn)
#    Pn = Pi
#    ui = np.dot(u, Pi)

#print(f'\n Expected visits after 1 transition: {expected_visits}')
#print(sum(expected_visits))


# Match Matrix Version

P = np.array([
    [0.1, 0, 0.1, 0.5, 0.2, 0, 0, 0.1, 0], # HC
    [0, 0, 1, 0, 0, 0, 0, 0, 0], # HK
    [0.15, 0, 0.5, 0.2, 0.1, 0, 0, 0.05, 0], # HP
    [0, 0, 0.4, 0.2, 0.4, 0, 0, 0, 0], # C
    [0, 0, 0.1, 0.2, 0.5, 0, 0.15, 0, 0.05], # AP
    [0, 0, 0, 0, 1, 0, 0, 0, 0], # AK
    [0, 0, 0.2, 0.5, 0.1, 0, 0.1, 0, 0.1], # AC
    [0, 0, 0, 0, 0, 1, 0, 0, 0], # HG
    [0, 1, 0, 0, 0, 0, 0, 0, 0] # AG
])

print(np.sum(P))

Pn = P

u = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0])
ui = u

expected_visits = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

for i in range(46):
    expected_visits = expected_visits + ui
    #print(f'P{i}\n{Pn}')
    #print(f'\nu{i} : {ui}, sum ui = {sum(ui)}')
    Pi = np.dot(P, Pn)
    Pn = Pi
    ui = np.dot(u, Pi)

print(f'\n Expected visits after first_half: {expected_visits}')
print(sum(expected_visits))

u = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0])
ui = u
Pn = P

for i in range(46):
    expected_visits = expected_visits + ui
    Pi = np.dot(P, Pn)
    Pn = Pi
    ui = np.dot(u, Pi)

print(f'\n Expected visits total: {expected_visits}')
print(sum(expected_visits))

## Now calculating expected transitions for heatmap
y = expected_visits
y[1] -= 1
y[5] -= 1
y *= (44/45)
y[1] += 1
y[5] += 1
print('\n', y, "sum", sum(y))

expected_transitions = P * y[:, np.newaxis]
print('\n', expected_transitions)
print(np.sum(expected_transitions))