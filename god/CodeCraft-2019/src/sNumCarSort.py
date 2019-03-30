#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from map import *

def all_car_path(map_array, map_road_array):
    path_road = []
    for i in range(Car.count):
        car_id = Car.dict[i]
        path = Dijkstra(Car.origin[car_id], Car.destination[car_id], map_array)
        path_center = []
        for j in range(len(path)-1):
            path_center.append(int(map_road_array[path[j]][path[j + 1]]))#把路口点cross转化成road id
        time = car_id // 15 #每个时间出发数量限制11-2 1006 /12-2 928/15-2 758 /25-2 溢出 纯粹寻找边际
        path_road.append(tuple([Car.id[car_id], max(Car.startTime[car_id], time)] + path_center))
        print(path_road)
    return path_road

if __name__ == "__main__":
    read_car, read_cross, read_road = read_txt('../config/car.txt', '../config/cross.txt', '../config/road.txt')
    intiData(read_car, read_cross, read_road)
    planRoadLength, planRoad, roadLoss = Graph(Cross.count, Road.count, Road.isDuplex, Road.roadFrom, Road.roadTo,
                                               Road.length, Road.id)
    test = all_car_path(planRoadLength, planRoad)