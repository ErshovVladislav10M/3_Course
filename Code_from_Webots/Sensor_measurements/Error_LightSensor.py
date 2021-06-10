import matplotlib.pyplot as plt
import numpy
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


ls_test = '600'
file_name = os.getcwd()

file_real = open(file_name + r'\test_error_sensor\ls_real\ls_mov_' + ls_test + '.txt', 'r')
Y2 = [float(line) for line in file_real]

X1, Y1 = create_X_Y(Y2)

plt.bar(X1, Y1, color = 'blue', label = 'На реальном роботе')
plt.xticks(X1, X1)


def inaccuracy_ls(light):
    percent_val = [0.7985, 0.8152, 0.8489, 0.8723]
    error_comp_val = [0.198, 0.0796, 0.0175, 0.0067]
    light_val = [101, 201, 399, 600]

    error_comp = numpy.interp(light, light_val, error_comp_val)
    percent = numpy.interp(light, light_val, percent_val)

    p = random.uniform(0, 1)
    if p <= (1 - percent) / 2:
        q = random.uniform(0, error_comp)
        return round(light * (1 - q))
    elif p >= percent / 2 + 0.5:
        q = random.uniform(0, error_comp)
        return round(light * (1 + q))
    else:
        return round(light)


size = len(Y2)
Y2 = [inaccuracy_ls() for i in range(size)]

X1, Y1 = create_X_Y(Y2)

plt.plot(X1, Y1, color = 'purple', marker = '', linestyle = '-', markerfacecolor = 'purple',
         label = 'Заданным распределением с погрешностью 0.67%')


plt.title('Распределение значений при значении ' + ls_test, fontsize = 15)
plt.xlabel('Значение в условных единицах', fontsize = 14)
plt.ylabel('Количество значений', fontsize = 14)
plt.legend(loc='best')
plt.show()
