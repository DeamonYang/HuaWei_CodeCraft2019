#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 978
from map import *
import sys

def speedSort(Car_count, Car_speed, Car_id):
    max_speed = 0
    car_divide_speed = []
    car_divide_time = []
    car_divide_merge = []
    car_length = []
    max_time = 0

    for i in range(Car_count):
        if Car_speed[i] > max_speed:
            max_speed = Car_speed[i]
    for i in range(max_speed):#按速度建立n个数组
        car_divide_speed.append([])
    for i in range(Car_count):#相同速度放到一个数组中
        car_divide_speed[Car_speed[i] - 1].append(Car_id[i])

    for i in range(Car_count):
        if Car.startTime[i] > max_time:
            max_time = Car.startTime[i]
    for i in range(max_time*max_speed):
        car_divide_time.append([])
    for i in range(Car_count):
        car_divide_time[Car_speed[i]*max_time-Car.startTime[i]].append(Car_id[i])

    n = 0
    m = 0
    for i in range(max_speed):
        car_divide_merge.append([])
    for i in car_divide_time:
        car_divide_merge[m].extend(i)
        n+=1
        if(n%max_time == 0):
            m+=1
    speed_dic = {}
    for i in range(max_speed):#数组变成字典--car.speed：[car.id]
        speed_dic[i+1] = car_divide_merge[i]
    return speed_dic

def record_road(batch, road_use_list, road_percent_list):
    for i in batch:
        for j in i[2:]:
            road_id_bias = Road.dict[j]
            road_use_list[road_id_bias] += 1

    sum_use = sum(road_use_list)
    for i in range(Road.count):
        road_percent_list[i] = road_use_list[i] / sum_use

    return road_use_list, road_percent_list

def time_split(group, car_per_sec):

    group_divide_time = []
    car_num = len(group)
    batch_num = int(car_num / car_per_sec ) + 1 #一个速度分成的组数

    for i in range(batch_num):
        cur_batch = []
        for j in range(car_per_sec ):#相乘不是一组的车辆数，且>=车数
            try:
                cur_batch.append(group.pop())
            except:
                break
        group_divide_time.append(cur_batch)
    #print(group_divide_time)
    return group_divide_time

def update_loss(array_loss, array_dis, Road_count, Road_length, Road_channel, Road_speed, Road_isDuplex,
                Road_roadFrom, Road_roadTo, road_percent_list,speed):#, cross_loss

    for i in range(Road_count):

        use_rate = road_percent_list[i]
        loss = Road_length[i] * (1 / min(Road_speed[i], speed) + 30 * use_rate / Road.channel[i])#+ 0.3 * max(cross_loss[Road_roadFrom[i]+1], cross_loss[Road_roadTo[i]+1])
        loss = loss *(1+2*road_percent_list[i])
        if Road_isDuplex[i] == 1:
            array_loss[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = array_loss[Cross.dict[Road_roadTo[i]]][Cross.dict[Road_roadFrom[i]]] = loss
        else:
            array_loss[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = loss
    return array_loss

def cal_car_path(map_loss_array, map_road_array, batch, time):
    path_road_time = []

    for i in batch:
        car_id = Car.dict[i]
        path = Dijkstra(Car.origin[car_id], Car.destination[car_id], map_loss_array)
        path_center = []
        a = len(path)

        path_center.append(Car.id[car_id])
        path_center.append(max(Car.startTime[car_id], time))
        for j in range(a - 1):
            path_center.append(int(map_road_array[path[j]][path[j + 1]]))
        path_road_time.append(path_center)
    #print(path_road_time)
    return path_road_time

def cal(plan_roadLength, plan_road, road_loss):
    time = 1
    answer = []
    speed_list = []
    road_use_list = [0*x for x in range(Road.count)]
    road_percent_list = [0*x for x in range(Road.count)]

    car_divide_speed = speedSort(Car.count, Car.speed, Car.id)
    #取出速度数组
    for speed in car_divide_speed:
        speed_list.append(speed)
    speed_list.reverse()
    for speed in speed_list:
        cur_group = car_divide_speed[speed] #一个速度的数组
        if not cur_group:#空组
            continue
        car_per_sec = 500#280 60/1在图一表现更好，280/7图二，综合更好
        group_divide_time = time_split(cur_group, car_per_sec)
        interval_time = 20#7
        for batch in group_divide_time:
            #road_loss = update_loss(road_loss, plan_roadLength, Road.count, Road.length, Road.channel, Road.speed,
            #                                              Road.isDuplex, Road.roadFrom, Road.roadTo, road_percent_list,speed)
            #batch_path_time = cal_car_path(road_loss, plan_road, batch, time)
            batch_path_time = cal_car_path(plan_roadLength, plan_road, batch, time)
            #road_use_list, road_percent_list = record_road(batch_path_time, road_use_list, road_percent_list)
            time += interval_time
            answer += batch_path_time
            #print(answer)
    return answer

if __name__=="__main__":
    read_car, read_cross, read_road = read_txt('../config/car.txt', '../config/cross.txt', '../config/road.txt')
    intiData(read_car, read_cross, read_road)
    planRoadLength, planRoad, roadLoss = Graph(Cross.count, Road.count, Road.isDuplex, Road.roadFrom, Road.roadTo,
                                               Road.length, Road.id)
    test = cal(planRoadLength, planRoad, roadLoss)
