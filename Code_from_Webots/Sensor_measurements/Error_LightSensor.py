import matplotlib.pyplot as plt
import numpy
import random
import os


ls_test = '600'
file_name = os.getcwd()

file_real = open(file_name + '\test_error_sensor\ls_real\ls_mov' + ls_test + '.txt', 'r')

Y2 = [float(line) for line in file_real]

max_val_r = max(Y2)
min_val_r = min(Y2)

error_comp_r = (max_val_r - min_val_r) / (min_val_r + max_val_r) * 100
medium_val_r = (min_val_r + max_val_r) / 2

X1 = []
for i in Y2:
    if i not in X1:
       X1.append(round(i))

X1.sort()
Y1 = [0 for i in range(len(X1))]
for i in Y2:
    if i in X1:
       Y1[X1.index(i)] += 1

#plt.plot(X1, Y1, color = 'green', marker = '', linestyle = '-', markerfacecolor = 'green', label = 'На реальном роботе')
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


X1 = []
a = min_val_r
while a <= max_val_r:
    X1.append(a)
    a += 1

Y1 = [0 for i in range(len(X1))]
for i in range(len(Y2)):
    p = int(inaccuracy_ls(float(ls_test)) - min_val_r)
    Y1[p] += 1

plt.plot(X1, Y1, color = 'purple', marker = '', linestyle = '-', markerfacecolor = 'purple',
         label = 'Заданным распределением с погрешностью 0.67%')


plt.title('Распределение значений при значении ' + ls_test, fontsize = 15)
plt.xlabel('Значение в условных единицах', fontsize = 14)
plt.ylabel('Количество значений', fontsize = 14)
plt.legend(loc='best')
plt.show()
