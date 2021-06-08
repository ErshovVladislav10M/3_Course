import matplotlib.pyplot as plt
import math
import os


Y = [[], [], [], []]

file_name = os.getcwd()

file = open(file_name + '\test_light_angle\four_value_light.txt', 'r')
i = 0
for line in file:
    Y[i].append(float(line))
    i += 1
    i %= 4


def comp_angle(light):
    if max(light) == sum(light):
        return light.index(max(light)) * 90 + 45

    if light[0] + light[1] == 0:
        real_l1 = light[2]
        real_l2 = light[3]
        angle_sector = 225
    if light[1] + light[2] == 0:
        real_l1 = light[3]
        real_l2 = light[0]
        angle_sector = 315
    if light[2] + light[3] == 0:
        real_l1 = light[0]
        real_l2 = light[1]
        angle_sector = 45
    if light[3] + light[0] == 0:
        real_l1 = light[1]
        real_l2 = light[2]
        angle_sector = 135

    return (math.atan(real_l2 / real_l1) * 180 / math.pi + angle_sector) % 360


X = [180 - 180 * i / len(Y[0]) for i in range(len(Y[0]))]
A = [90 - 180 * i / len(Y[0]) for i in range(len(Y[0]))]
B = []

for i in range(len(Y[0])):
    light = []
    for j in range(4):
        light.append(Y[j][i])

    if comp_angle(light) > 180:
        B.append(comp_angle(light) - 360)
    else:
        B.append(comp_angle(light))

plt.plot(X, A, color = 'r', marker = '', linestyle = '-', markerfacecolor = 'r', label = 'Реальный угол')
plt.plot(X, B, color = 'b', marker = '', linestyle = '--', markerfacecolor = 'b', label = 'Высчитанный угол по формуле')
plt.xlabel('Время', fontsize = 14)
plt.ylabel('Угол направления на свет', fontsize = 14)
plt.title('Сравнение реального и вычисленного угла', fontsize = 15)
plt.legend(loc = 'best')
plt.show()

print(max([abs(A[i] - B[i]) for i in range(len(A))]))
