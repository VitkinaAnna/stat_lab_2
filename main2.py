import random
import matplotlib.pyplot as plt
import math
import statistics

# Кількість реалізацій та кількість членів у кожній реалізації
count_realizations = 1000
num_adds = 1000

# Інтервал та кількість кроків для створення часового ряду
time_delta = 0.01
time = 1

# Створення матриці гаусівських випадкових чисел для кожної реалізації
gauss_matrix = [[random.gauss(0, 1) for _ in range(num_adds + 1)] for _ in range(count_realizations)]

# Створення порожнього списку для збереження значень кожної реалізації в кожний момент часу
list_realizations = [[] for _ in range(count_realizations)]

# Функція для обчислення значень кожної реалізації в заданий момент часу
def calculate_values(i, term_count, time):
    return time * gauss_matrix[i][0] + math.sqrt(2) * sum(
        gauss_matrix[i][term] * math.sin(term * math.pi * time) / math.pi / term
        for term in range(1, term_count + 1)
    )

# Заповнення списку realizations значеннями для кожної реалізації в кожний момент часу
for i in range(count_realizations):
    current_time = 0
    while current_time < time:
        list_realizations[i].append(calculate_values(i, num_adds, current_time))
        current_time += time_delta

# Вивід графіків для перших двох реалізацій
for i in range(len(list_realizations[:2])):
    y = list_realizations[i]
    x = [time_delta*i for i in range(int(1/time_delta))]
    plt.plot(x, y)
    plt.title(f'Реалізація {i}')
    plt.show()

# Обчислення  середнього значення для кожного моменту часу
realization = [val for row in list_realizations for val in row]
terms = [sum(row) / len(row) for row in list_realizations]

# Вивід гістограми для середніх значень
plt.hist(terms)
plt.xlabel('Cереднє значення')
plt.ylabel('Частота')
plt.show()

print(f"Середнє значення: {sum(realization) / len(realization)}")

# Обчислення дисперсії для кожного моменту часу
variances = [statistics.variance(row) for row in list_realizations]

# Вивід гістограми для дисперсій
plt.hist(variances)
plt.xlabel('Дисперсія')
plt.ylabel('Частота')
plt.show()

print(f"Дисперсія: {statistics.variance(realization)}")

# Рівні для обчислення часу перетину кожною реалізацією
reach_level = [0.5, -0.5]

# Створення списку для збереження часу перетину кожною реалізацією для кожного рівня
values = [[] for _ in range(len(reach_level))]
for i in range(len(reach_level)):
    for row in list_realizations:
        for j in range(len(row)):
            if reach_level[i] > 0:
                if row[j] > reach_level[i]:
                    values[i].append(j *  time_delta)
                    break
            else:
                if row[j] < reach_level[i]:
                    values[i].append(j * time_delta)
                    break

# Вивід гістограм для часу перетину кожною реалізацією для кожного рівня
for value in values:
    plt.hist(value)
    plt.show()
