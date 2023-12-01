import random
import matplotlib.pyplot as plt
import math

# Задана інтенсивність Пуассонівського потоку
intens = 0.1  # Інтенсивність Пуассонівського потоку
time = 500    # Кількість часових міток
num_realizations = 1000  # Кількість реалізацій


# Ініціалізація списку значень та реалізацій
val = [0.0 for _ in range(num_realizations)]
realizations = [[] for _ in range(num_realizations)]

# Моделювання Пуассонівського потоку
for _ in range(time):
    for i in range(num_realizations):
        realizations[i].append(val[i])
        val[i] += -1 / intens * math.log(1 - random.random())

# Візуалізація перших 6 реалізацій
for i in range(len(realizations[:6])):
    y = realizations[i]
    x = [i for i in range(time)]
    plt.plot(x, y)
    plt.xlabel('Часовий індекс')
    plt.ylabel('Значення')
    plt.title(f'Реалізація {i}')
    plt.show()

# Побудова гістограм для подій в різний момент часу
event_indices = [1, 2, 3, 4, 5, 6]  # Вказати індекси подій для аналізу
events = [[row[idx] for row in realizations] for idx in event_indices]

for i, event in enumerate(events):
    plt.hist(event)
    plt.xlabel('Час появи події')
    plt.ylabel('Кількість подій')
    plt.title(f'Гістограма часу появи {event_indices[i]}-ої події')
    plt.show()

# Побудова гістограм для інтервалів між подіями
intervals = [[] for i in range(num_realizations)]
for i in range(num_realizations):
    for j in range(time - 1):
        intervals[i].append(realizations[i][j + 1] - realizations[i][j])

for i in range(len(intervals[:6])):
    plt.hist(intervals[i])
    plt.xlabel('Інтервал між подіями')
    plt.ylabel('Кількість подій')
    plt.title(f'Гістограма інтервалів між подіями (реалізація {i})')
    plt.show()

# Побудова гістограми появи рівно n подій
n_events = 200  # Вказати кількість подій для аналізу
selected_events = [row[n_events - 1] for row in realizations]

plt.hist(selected_events)
plt.xlabel(f'Час появи {n_events} подій')
plt.ylabel('Кількість подій')
plt.title(f'Гістограма часу появи {n_events} подій')
plt.show()
