from controller import Robot
import struct
import random


# create the Robot instance
robot = Robot()


# get the time step of the current world
timestep = int(robot.getBasicTimeStep())


# initialize emmiters
emit = robot.getEmitter('emit')

emit_main = robot.getEmitter('emit_main')


# Вводим количество членов группы не включая самого робота (т.е. n-1)
num_of_robots = 2


# initialize receiver
rec = []
for i in range(num_of_robots):
    rec.append(robot.getReceiver('rec' + str(i + 1)))
    rec[i].enable(timestep)

rec_main = robot.getReceiver('rec_main')
rec_main.enable(timestep)


# Курс и уверенность в курсе
bearing = 0
confidence_bearing = 0


# Список для приема сообщений
bearing_comrades = [[0] * num_of_robots, [0] * num_of_robots]


# Время переключения между роботами для приема сообщений
time_wait_switch = 0


# Номер робота, от которого принимаем сообщение
index_robot_rec = 0


# Main loop:
while robot.step(timestep) != -1:

    # Принимаем сообщение от основного микрочипа
    if rec_main.getQueueLength() > 0:
        message = rec_main.getData()
        dataList = struct.unpack("dd", message)
        bearing = dataList[0]
        confidence_bearing = dataList[1]
        rec_main.nextPacket()
    #print(bearing)

    # Передаем сообщение соседям
    p = random.uniform(0, 1)
    if p > 0.04:
        message = struct.pack("dd", bearing, confidence_bearing)
        emit.send(message)

    # Принимаем сообщение от соседей
    if time_wait_switch != 0:
        time_wait_switch -= 1
    elif rec[index_robot_rec].getQueueLength() > 0:
        message = rec[index_robot_rec].getData()
        dataList = struct.unpack("dd", message)
        bearing_comrades[index_robot_rec][0] = dataList[0]
        bearing_comrades[index_robot_rec][1] = dataList[1]
        rec[index_robot_rec].nextPacket()

        index_robot_rec += 1
        index_robot_rec %= num_of_robots
        time_wait_switch = 2
    #print("Robot", *bearing_comrades)

    # Перадаем сообщение на основной микрочип
    for i in range(num_of_robots):
        message = struct.pack("dd", bearing_comrades[i][0], bearing_comrades[i][1])
        emit_main.send(message)