#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from map import *

def speedSort(Car_count, Car_speed, Car_id, Car_start_time):
    max_speed = 0
    max_time = 0
    car_divide_speed = []
    car_divide_time = []
    car_divide_merge = []
    car_divide_merge2 = []
    car_length = []
    #速度排序
    for i in range(Car_count):
        if Car_speed[i] > max_speed:
            max_speed = Car_speed[i]
    for i in range(max_speed):#按速度建立n个数组
        car_divide_speed.append([])
    for i in range(Car_count):#相同速度放到一个数组中
        car_divide_speed[Car_speed[i] - 1].append(Car_id[i])
    #开始时间排序
    for i in range(Car_count):
        if Car_start_time[i] > max_time:
            max_time = Car_start_time[i]
    for i in range(max_time*max_speed):
        car_divide_time.append([])
    for i in range(Car_count):
        car_divide_time[Car_speed[i]*max_time-Car_start_time[i]].append(Car_id[i])
    #时间合并
    n = 0
    m = 0
    for i in range(max_speed):
        car_divide_merge.append([])
    for i in car_divide_time:
        car_divide_merge[m].extend(i)
        n+=1
        if(n%max_time == 0):
            m+=1
    #坐标排序
    for i in range(max_speed):
        car_divide_merge2.append([])
    y=0
    for car_divide_merge_speed in car_divide_merge:
        x=-1
        for t in range(len(car_divide_merge_speed)):
            car_length.append([])
        for i in car_divide_merge_speed:
            x += 1
            x1, x2 = 0, 0
            y1, y2 = 1, 1
            for j in range(Car.destination[i-Car.id[0]]):
                x1 += 1
                if(x1 > 8):
                    x1=1
                    y1 +=1

            for j in range(Car.origin[i-Car.id[0]]):
                x2 += 1
                if(x2 > 8):
                    x2=1
                    y2 +=1
            tmp = (x1-x2)*(x1-x2)+((y1-y2)*(y1-y2))#惩罚了多转弯

            car_length[x] = [Car_id[i-Car.id[0]], tmp]
        car_length = sorted(car_length, key=lambda x:x[1], reverse=True)

        for i in car_length:
            car_divide_merge2[y].append(i[0])
        y+=1
        car_length = []

    #存入字典
    speed_dic = {}
    for i in range(max_speed):#数组变成字典--car.speed：[car.id]
        speed_dic[i+1] = car_divide_merge[i]
    return speed_dic

def divideCar(same_speed_group, car_div_time):
    group_divide_car = []
    car_num = len(same_speed_group)
    same_num = int(car_num / car_div_time )  #一个速度分成的组数

    for i in range(same_num+1):
        tmp = []
        for j in range(car_div_time ):
            try:
                tmp.append(same_speed_group.pop())
            except:
                break
        group_divide_car.append(tmp)

    return group_divide_car

def findRoadTime(road_road_length_loss, cross_road, car_array, time):
    road_time = []
    for i in car_array:
        car_id = i - Car.id[0]
        road = Dijkstra(Car.origin[car_id]-1, Car.destination[car_id]-1, road_road_length_loss)
        road_list = []
        road_list.append(Car.id[car_id])
        road_list.append(max(Car.startTime[car_id], time))
        for j in range(len(road) - 1):
            road_list.append(int(cross_road[road[j]][road[j + 1]]))
        road_time.append(road_list)
    return road_time

def roadInCar(road_time, in_car_list, in_car_per):
    road_id_bias = Road.id[0]
    for i in road_time:
        for j in i[2:]:
            #road_id_bias = Road.dict[j]
            in_car_list[j-road_id_bias] += 1

    for i in range(Road.count):
        in_car_per[i] = in_car_list[i] / sum(in_car_list)

    return in_car_list, in_car_per

def loss(road_road_length_loss, Road_count, Road_length, Road_channel, Road_speed, Road_isDuplex,
          Road_roadFrom, Road_roadTo, road_percent_list, speed):

    for i in range(Road_count):
        loss = Road_length[i] * (1 / min(Road_speed[i], speed) + 30 * road_percent_list[i] / Road_channel[i])
        loss = loss *(1+2*road_percent_list[i])
        if Road_isDuplex[i] == 1:
            array_loss[Road_roadFrom[i]][Road_roadTo[i]] = array_loss[Road_roadTo[i]][Road_roadFrom[i]] = loss
        else:
            array_loss[Road_roadFrom[i]][Road_roadTo[i]] = loss
    return road_road_length_loss

def map1System(cross_road, road_loss):
    time = 1
    answer = []
    speed_list = []
    in_car_list = [0*x for x in range(Road.count)]
    in_car_per = [0*x for x in range(Road.count)]

    car_divide_speed = speedSort(Car.count, Car.speed, Car.id, Car.startTime)

    #取出速度数组
    for speed in car_divide_speed:
        speed_list.append(speed)
    speed_list.reverse()
    j = 0
    for speed in speed_list:
        same_speed_group = car_divide_speed[speed] #一个速度的数组
        if not same_speed_group:#空组
            continue
        car_div_time = 500
        group_divide_time = divideCar(same_speed_group, car_div_time)
        wait_time = 8
        for car_array in group_divide_time:
            road_loss = loss(road_loss, Road.count, Road.length, Road.channel, Road.speed,
                                                          Road.isDuplex, Road.roadFrom, Road.roadTo, in_car_per,speed)
            road_time = findRoadTime(road_loss, cross_road, car_array, time)
            in_car_list, in_car_per = roadInCar(road_time, in_car_list, in_car_per)
            time += wait_time
            answer += road_time
        print(answer)
    return answer

def map2System(cross_road, road_loss):
    time = 1
    answer = []
    speed_list = []
    in_car_list = [0*x for x in range(Road.count)]
    in_car_per = [0*x for x in range(Road.count)]

    car_divide_speed = speedSort(Car.count, Car.speed, Car.id, Car.startTime)
    #取出速度数组
    for speed in car_divide_speed:
        speed_list.append(speed)
    speed_list.reverse()
    j = 0
    for speed in speed_list:
        same_speed_group = car_divide_speed[speed] #一个速度的数组
        if not same_speed_group:#空组
            continue
        car_div_time = 280
        group_divide_time = divideCar(same_speed_group, car_div_time)
        if j <= 10 :
            wait_time = 7#7
        else:
            wait_time = 8
        j+= 1
        n = 0
        for car_array in group_divide_time:
            road_loss = loss(road_loss, Road.count, Road.length, Road.channel, Road.speed,
                                                          Road.isDuplex, Road.roadFrom, Road.roadTo, in_car_per,speed)
            road_time = findRoadTime(road_loss, cross_road, car_array, time)
            in_car_list, in_car_per = roadInCar(road_time, in_car_list, in_car_per)
            if n<3 :
                time += wait_time
            else:
                time += wait_time+1
            n += 1
            answer += road_time
    return answer