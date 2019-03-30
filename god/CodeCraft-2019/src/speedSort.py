#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from map import *
"""
def speedSort(Car_count):

    car_per_sec = 17 #17-2 702/
    max_speed = 0
    car_divide_speed = []
    car_time_sche = {}

    # split car by speed, car_divide_speed[k] means car speed as k+1
    for i in range(Car_count):
        if Car.speed[i] > max_speed:
            max_speed = Car.speed[i]
    for i in range(max_speed):#按速度对车进行排序
        car_divide_speed.append([])
    for i in range(Car_count):
        car_divide_speed[Car.speed[i] - 1].append(Car.id[i])

    # calculate start time
    time = 0
    for k in range(max_speed):#按速度从大到小发车，同速时切分
        time += 1
        #delta = 1 + (k - 1) * 0.01 #添加一个惩罚系数让数量更平滑
        #time = 1
        # TODO: this can to be changed to better function
        cur_group = car_divide_speed[-k] #速度从大到小
        if not cur_group:
            continue
        cur_amount = len(cur_group)

        for i in range(cur_amount):
            car_time_sche[cur_group[i]] = time
            if (i + 1) % car_per_sec == 0:
            #if (i + 1) % int(car_per_sec * delta * 10) == 0:
                time += 1

    return car_time_sche
"""
def speedSort(Car_count, Car_speed, Car_id):
    max_speed = 0
    car_divide_speed = []

    # split car by speed, car_divide_speed[k] means car speed as k+1
    for i in range(Car_count):
        if Car_speed[i] > max_speed:
            max_speed = Car_speed[i]
    for i in range(max_speed):#按速度建立n个数组
        car_divide_speed.append([])
    for i in range(Car_count):#相同速度放到一个数组中
        car_divide_speed[Car_speed[i] - 1].append(Car_id[i])

    speed_dic = {}
    for i in range(max_speed):#数组变成字典--car.speed：[car.id]
        speed_dic[i+1] = car_divide_speed[i]
    #print(speed_dic)
    return speed_dic

def carPath(map_array, map_road_array, car_inf, car_time_sche):

    car_len = len(car_inf)

    path_road = []
    for i in range(car_len):
        path = Dijkstra(car_inf[i][1] - 1, car_inf[i][2] - 1, map_array)
        path_center = []
        for j in range(len(path) - 1):
            path_center.append(int(map_road_array[path[j]][path[j + 1]]))

        time = car_time_sche[car_inf[i][0]]
        path_road.append(tuple([car_inf[i][0], max(car_inf[i][4], time)] + path_center))

    return path_road

if __name__=="__main__":
    read_road = read_txt('../config/road.txt')
    read_cross = read_txt('../config/cross.txt')
    read_car = read_txt('../config/car.txt')
    intiData(read_car, read_cross, read_road)
    graph = Graph()
    car_time = speedSort(Car.count)
    print(car_time)
