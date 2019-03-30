#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from reader import read_txt
import numpy as np
import pandas as pd
from model import *
def Graph(Cross_count, Road_count, Road_isDuplex, Road_roadFrom, Road_roadTo, Road_length, Road_id):
        #对角矩阵，对角取0，设置每两个点间的距离，等于路径上的权值
        plan_roadLength = np.zeros([Cross_count, Cross_count]) + 10000 - 10000 * np.eye(Cross_count)
        plan_road = np.zeros([Cross_count, Cross_count])#36*36的每个起点到终点的路号，等于路径图

        for i in range(Road_count):
            if Road_isDuplex[i] == 1:
                plan_roadLength[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = plan_roadLength[Cross.dict[Road_roadTo[i]]][Cross.dict[Road_roadFrom[i]]] = Road_length[i]
                plan_road[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = plan_road[Cross.dict[Road_roadTo[i]]][Cross.dict[Road_roadFrom[i]]] = Road_id[i]
            else:
                plan_roadLength[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = Road_length[i]
                plan_road[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = Road_id[i]
        road_loss = plan_roadLength
        return plan_roadLength, plan_road, road_loss


def Dijkstra(origin, destination, planRoadLength):
    #inf = 10000 #死路
    origin = Cross.dict[origin]
    destination = Cross.dict[destination]
    path_array = []
    temp_array = []
    path_array.extend(planRoadLength[origin])
    temp_array.extend(planRoadLength[origin])
    #print(path_array)
    #temp_array[origin] = inf
    already_traversal = [origin]
    path_parent = [origin] * Cross.count #cross*cross

    i = origin
    while (i != destination):
        i = temp_array.index(min(temp_array))#最短的一条路的cross_id
        temp_array[i] = 10000
        path = [i]
        #path.append(i)#记录走过的路
        k = i
        while (path_parent[k] != origin):
            path.append(path_parent[k])
            k = path_parent[k]
        path.append(origin)
        path.reverse()
        already_traversal.append(i)
        for j in range(Cross.count):
            if j not in already_traversal:
                if (path_array[i] + planRoadLength[i][j]) < path_array[j]:
                    path_array[j] = temp_array[j] = path_array[i] + planRoadLength[i][j]
                    path_parent[j] = i
    #print(path)
    return path



if __name__ == "__main__":
    read_car, read_cross, read_road = read_txt('../config/car.txt', '../config/cross.txt', '../config/road.txt')
    intiData(read_car, read_cross, read_road)
    plan_roadLength, plan_road, road_loss = Graph(Cross.count, Road.count, Road.isDuplex, Road.roadFrom, Road.roadTo, Road.length, Road.id)
    print(plan_roadLength)
    #print(graph.plan_roadLength)
    #print(graph.plan_road)
    #test = [3]
    #print([3] * 4)