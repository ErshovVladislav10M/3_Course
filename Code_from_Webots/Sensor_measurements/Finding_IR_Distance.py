import numpy
import matplotlib.pyplot as plt


# Преобразование данных дистанционного сенсора в расстояние
def transf_ds(volt):
    volt_val = [0.45, 0.47, 0.5, 0.55, 0.61, 0.69, 0.74,
                0.8, 0.87, 1.04, 1.27, 1.54, 1.99, 2.48, 2.7]
    dist_val = [150, 140, 130, 120, 110, 100, 90,
                80, 70, 60, 50, 40, 30, 20, 15]
    return numpy.interp(volt, volt_val, dist_val)


A = []
B = []
for i in range(10):
    A.append(2.7 - i * 0.25)
    B.append(transf_ds(2.7 - i * 0.25))

volt_val = [0.45, 0.47, 0.5, 0.55, 0.61, 0.69, 0.74, 
                0.8, 0.87, 1.04, 1.27, 1.54, 1.99, 2.48, 2.7]
dist_val = [150, 140, 130, 120, 110, 100, 90, 
            80, 70, 60, 50, 40, 30, 20, 15]
            
plt.plot(A, B, color = 'red', marker = 'o', linestyle = '--')
plt.plot(volt_val, dist_val, color = 'blue', marker = 'o', linestyle = '--')

plt.ylabel('Расстояние', fontsize = 14)
plt.xlabel('Вольтаж', fontsize = 14)
plt.title('Преобразование сигнала DistanceSensor в растояние', fontsize = 15)
plt.show()
