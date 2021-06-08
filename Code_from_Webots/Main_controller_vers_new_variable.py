from controller import Robot
import math
import struct
import numpy
import random


# Преобразование данных ls в соответствии с реальным датчиком
def transform_light(light):
    if light > 1000: light = 1000
    angle = 180 * (math.pi / 2 - math.asin(light / 1000)) / math.pi
    light_val = [0, 23, 45, 66, 85, 115, 117, 115,
                 85, 66, 45, 23, 0]
    angle_val = [-90, -80, -67.5, -60, -45, -22.5, 0,
                 22.5, 45, 60, 67.5, 80, 90]
    return numpy.interp(angle, angle_val, light_val) * 1000 / 117


# Нахождение угла по датчикам ls
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


# Внесение погрешности в показания ls
def inaccuracy_ls(light):
    percent_val = [0.7951, 0.7985, 0.8152, 0.8489, 0.8723, 0.9046]
    error_comp_val = [0.4706, 0.198, 0.0796, 0.0175, 0.0067, 0.0059]
    light_val = [51, 101, 201, 399, 600, 799]

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


# Внесение погрешности в показания ds
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


# create the Robot instance
robot = Robot()


# get the time step of the current world
timestep = int(robot.getBasicTimeStep())


# initialize motors
wheels = []
for i in range(2):
    wheels.append(robot.getMotor('wheel' + str(i + 1)))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)


# initialize emmiters
emit_main = robot.getEmitter('emit_main')


# Вводим количество членов группы не включая самого робота (т.е. n-1)
num_of_robots = 2


# Список для приема сообщений
bearing_comrades = [[0] * num_of_robots, [0] * num_of_robots]


# initialize receiver
rec_main = robot.getReceiver('rec_main')
rec_main.enable(timestep)


# initialize distance sensor
ds = robot.getDistanceSensor('ds')
ds.enable(timestep)
    

# initialize light sensor
ls = []
for i in range(4):
    ls.append(robot.getLightSensor('ls' + str(i + 1)))
    ls[i].enable(timestep)


# initialize compass
com = robot.getCompass('com')
com.enable(timestep)


# Начальное значение на двигатели
leftSpeed = 0
rightSpeed = 0


# Переменные для задания обхода препятствия
avoidObstacleCounter = 0
detourObstacleCounter = 0
j = 0
p = 0


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    # Расчитываем азимут
    north = com.getValues()
    rad = math.atan2(north[0], north[2])
    bearing = (rad - 1.5708) / math.pi * 180.0;
    if bearing < 0.0:
        bearing += 360
    cos_com = north[0]
    sin_com = north[2]
    #print(cos_com, sin_com)
    
    # Ищем максимум из датчиков
    light = []
    for i in range(4):
        light.append(inaccuracy_ls(transform_light(ls[i].getValue())))
    #print(light[0])
    #print(comp_angle(light)[0])
    
    
    # Расчет азимута движения на источник по четырем сенсорам света.
    dbearing = comp_angle(light)
 
    # Вводим уверенность в курсем по датчикам света q_az b
    # и q_dis - уверенность по датчику направления. a_q - коэфициент
    # d - показаия датчика дистанции.
    q = 0.3
    a_q = 0.5
    d = inaccuracy_ds(ds.getValue())
    #print(round(d))
    #print(ds.getValue())
    
    if comp_angle(light) > 90 and comp_angle(light) < 180:
        q = 0
    else:
        q = (1 - a_q) * (1 - abs((light[0] - light[3]) / (light[0] + light[3]))) + a_q * (d / 1000)
    
    # Передаем сообщение на микрочип для связи
    #print(bearing)
    message = struct.pack("dd", bearing, q)
    emit_main.send(message)
    
    # Принимаем сообщение от микрочипа связи
    for i in range(num_of_robots):
        if rec_main.getQueueLength() > 0:
            message = rec_main.getData()
            dataList = struct.unpack("dd", message)
            bearing_comrades[i][0] = dataList[0]
            bearing_comrades[i][1] = dataList[1]
            rec_main.nextPacket()
    #print("Robot", *bearingn)
    
    # Считаем среднюю уверенность соседей q_sr
    q_sum = 0
    k_i = num_of_robots
    q_sr = q
    for i in range(num_of_robots):
        if bearing_comrades[i][1] != 0:
            q_sum += bearing_comrades[i][1]
        else:
            k_i -= 1
    if k_i > 0:
        q_sr = q_sum / k_i
    else:
        q_sr = 1
    #print ("q_sr", q_sr)
    
    # Считаем средневзвешенный курс соседей dbearingn_sr_w
    dbearingn_sr_w = 0
    cos_sum_sr_w = 0
    sin_sum_sr_w = 0
    sin_sum_w = 0
    cos_sum_w = 0
    k_i_w = 0
    for i in range(num_of_robots):
        cos_sum = 0
        sin_sum = 0
        if bearing_comrades[i][1] > 0:
            cos_sum_w += math.cos(math.radians(bearing_comrades[i][0])) * bearing_comrades[i][1]
            sin_sum_w += math.sin(math.radians(bearing_comrades[i][0])) * bearing_comrades[i][1]
            k_i_w += 1
    if k_i_w != 0:
        cos_sum_sr_w = cos_sum_w / k_i_w
        sin_sum_sr_w = sin_sum_w / k_i_w
    
    # Расчитываем курс в группе dbearingG исходя из данных группы
    # alpha - коэфициент, p - уверенность к курсу при пересчете от группы
    alpha = 0.5
    dbearingG = 0
    
    if k_i_w == 0:
        dbearingG = dbearing
    else:
        cos_dbearing = math.cos(math.radians(dbearing))
        sin_dbearing = math.sin(math.radians(dbearing))
        cos_db_G = ((1 - alpha) * cos_dbearing * q + alpha * cos_sum_sr_w) / ((1 - alpha) * q + alpha * q_sr)
        sin_db_G = ((1 - alpha) * sin_dbearing * q + alpha * sin_sum_sr_w) / ((1 - alpha) * q + alpha * q_sr)
        if cos_db_G > 0 and sin_db_G > 0:
            dbearingG = math.degrees(math.acos(cos_db_G))
        elif cos_db_G > 0 and sin_db_G < 0:
            dbearingG = 360 - math.degrees(math.acos(cos_db_G))
        elif cos_db_G < 0 and sin_db_G > 0:
            dbearingG = 180 - math.degrees(math.acos(cos_db_G))
        elif cos_db_G < 0 and sin_db_G < 0:
            dbearingG = 180 + math.degrees(math.acos(cos_db_G))
        
    if d < 50 and d > 30:
        if comp_angle(light) < 90 or comp_angle(light) > 270:
            if comp_angle(light) < 180:
                j = 1 # право
            else:
                j = 2 # лево
        else:
            j = 0
       
        if j == 2:
            dbearingG += 10
        elif j == 1:
            dbearingG -= 10
    # print(j)
    
    if dbearingG > 360:
        dbearingG -= 360

    # Задаем движение
    if bearing == dbearingG and sum(light) > 0:
        leftSpeed = 3.14
        rightSpeed = 3.14
    elif dbearingG > bearing and dbearingG < bearing + 180:
        leftSpeed = 3.14
        rightSpeed = 2
    elif dbearingG > bearing and dbearingG > bearing + 180:
        leftSpeed = 2
        rightSpeed = 3.14
    elif bearing > dbearingG and bearing < dbearingG + 180:
        leftSpeed = 2
        rightSpeed = 3.14
    elif bearing > dbearingG and bearing > dbearingG + 180:
        leftSpeed = 3.14
        rightSpeed = 2
    else:
        leftSpeed = 0
        rightSpeed = 0
    
    # Обход препятствий
    #print(p, d)
    if d <= 30 and avoidObstacleCounter == 0 and detourObstacleCounter == 0:
        avoidObstacleCounter = 30
        detourObstacleCounter = 150
        if comp_angle(light) < 90 or comp_angle(light) > 270:
            if comp_angle(light) < 180:
                p = 0 # право
            else:
                p = 1 # лево
   
    if avoidObstacleCounter != 0 or detourObstacleCounter != 0:
        if avoidObstacleCounter != 0:
            avoidObstacleCounter -= 1

            if p == 1:
                leftSpeed = -2
                rightSpeed = 2
            elif p == 0:
                leftSpeed = 2
                rightSpeed = -2

        elif detourObstacleCounter != 0:
            detourObstacleCounter -= 1

            leftSpeed = 2
            rightSpeed = 2
            
    #print(avoidObstacleCounter)
    #print(detourObstacleCounter)
            
    # Отправляем значение на моторы
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
