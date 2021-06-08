import matplotlib.pyplot as plt
import random
import os

d_test = '25'
file_name = os.getcwd()

file_real = open(file_name + '\test_error_sensor\ds_real\ds_mov' + d_test + '.txt', 'r')
Y2 = [float(line) for line in file_real]

min_val_r = round(min(Y2))
max_val_r = round(max(Y2))
medium_val_r = round(sum(Y2) / len(Y2))
error_comp_r = (max(Y2) - medium_val_r) / medium_val_r * 100

X1 = []
for i in range(len(Y2)):
    if Y2[i] not in X1:
       X1.append(Y2[i])

X1.sort()
Y1 = [0 for i in range(len(X1))]
for i in range(len(Y2)):
    if Y2[i] in X1:
       Y1[X1.index(Y2[i])] += 1

X2 = []
for i in range(len(X1)):
    X2.append((X1[i] - medium_val_r) / medium_val_r * 100)

max_number_r = max(Y1)

#print(Y1)
#print((min(X1) - medium_val_r) / medium_val_r * 100)
#print((max(X1) - medium_val_r) / medium_val_r * 100)

plt.bar(X1, Y1, color='blue', label='На реальном роботе')
#plt.plot(X1, Y1, color = 'blue', linestyle = '-', label = 'На реальном роботе')
#for i in range(len(X1)):
#    txt = str(round(X1[i]))
#    plt.text(X2[i] - 0.5, max_number_r * (0.1 + (i % 2) * 0.03), txt)


file_simulation = open(file_name + '\test_sensor\ds_simulation\ds_' + d_test + '.txt', 'r')
Y2 = [float(line) for line in file_simulation]

X1 = []
for i in range(len(Y2)):
    if Y2[i] not in X1:
       X1.append(int(Y2[i]))

X1.sort()
Y1 = [0 for i in range(len(X1))]
for i in range(len(Y2)):
    if Y2[i] in X1:
       Y1[X1.index(Y2[i])] += 1

#plt.plot(X1, Y1, color = 'red', marker = '', linestyle = '-', markerfacecolor = 'red', label = 'В симуляции c погрешностью 9.23%')
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


X1 = []
a = min_val_r
while a <= max_val_r:
    X1.append(a)
    a += 1

Y1 = [0 for i in range(len(X1))]
for i in range(len(Y2)):
    p = inaccuracy_ds(float(d_test)) - min_val_r
    Y1[inaccuracy_ds(float(d_test)) - min_val_r] += 1

plt.plot(X1, Y1, color = 'purple', marker = '', linestyle = '-', markerfacecolor = 'purple', label = 'Заданным распределением c погрешностью 9.23%')


plt.title('Распределение значений на расстоянии ' + d_test + ' см', fontsize = 15)
plt.xlabel('Значение в см', fontsize = 14)
plt.ylabel('Количество значений', fontsize = 14)
plt.legend(loc='best')
plt.show()
