import matplotlib.pyplot as plt
import random
import os


def create_X_Y(Y2):
    X1 = []
    for i in Y2:
        if i not in X1:
           X1.append(i)

    X1.sort()
    Y1 = [0 for i in range(len(X1))]
    for i in Y2:
        if i in X1:
           Y1[X1.index(i)] += 1

    return X1, Y1

d_test = '25'
file_name = os.getcwd()

file_real = open(file_name + r'\test_error_sensor\ds_real\ds_mov_' + d_test + '.txt', 'r')
Y2 = [float(line) for line in file_real]

X1, Y1 = create_X_Y(Y2)

plt.bar(X1, Y1, color='blue', label='На реальном роботе')


file_simulation = open(file_name + r'\test_error_sensor\ds_simulation\ds_' + d_test + '.txt', 'r')
Y2 = [float(line) for line in file_simulation]

X1, Y1 = create_X_Y(Y2)

plt.plot(X1, Y1, color = 'red', marker = '', linestyle = '-', markerfacecolor = 'red', label = 'В симуляции c погрешностью 9.23%')
plt.xticks(X1, X1)


def inaccuracy_ds(d, error_comp=0.0923):
    p = random.uniform(0, 1)
    if p <= 0.03827:
        q = random.uniform(0, error_comp)
        return round(d * (1 - q))
    elif p >= 0.96173:
        q = random.uniform(0, error_comp)
        return round(d * (1 + q))
    else:
        return round(d)


Y2 = [inaccuracy_ds(float(d_test)) for i in range(3100)]

X1, Y1 = create_X_Y(Y2)

plt.plot(X1, Y1, color = 'purple', marker = '', linestyle = '-', markerfacecolor = 'purple', label = 'Заданным распределением c погрешностью 9.23%')


plt.title('Распределение значений на расстоянии ' + d_test + ' см', fontsize = 15)
plt.xlabel('Значение в см', fontsize = 14)
plt.ylabel('Количество значений', fontsize = 14)
plt.legend(loc='best')
