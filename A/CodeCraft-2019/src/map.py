#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from model import *
def Graph(Cross_count, Road_count, Road_isDuplex, Road_roadFrom, Road_roadTo, Road_length, Road_id):
        plan_roadLength = np.zeros([Cross.count, Cross.count]) + 99999 - 99999 * np.eye(Cross.count)
        plan_road = np.zeros([Cross.count, Cross.count])

        for i in range(Road_count):
            if Road_isDuplex[i] == 1:
                plan_roadLength[Road_roadFrom[i]][Road_roadTo[i]] = plan_roadLength[Road_roadTo[i]][Road_roadFrom[i]] = Road_length[i]
                plan_road[Road_roadFrom[i]][Road_roadTo[i]] = plan_road[Road_roadTo[i]][Road_roadFrom[i]] = Road_id[i]
            else:
                plan_roadLength[Road_roadFrom[i]][Road_roadTo[i]] = Road_length[i]
                plan_road[Road_roadFrom[i]][Road_roadTo[i]] = Road_id[i]
        road_loss = plan_roadLength
        return plan_roadLength, plan_road, road_loss


def Dijkstra(origin, destination, road_road_length):
    #origin = Cross.dict[origin]
    #destination = Cross.dict[destination]
    road_array = []
    temp = []
    road_array.extend(road_road_length[origin])
    temp.extend(road_road_length[origin])
    already_walked = [origin]
    now_path = [origin] * Cross.count #cross*cross
    start = origin
    while (start != destination):
        start = temp.index(min(temp))#最短的一条路的cross_id
        temp[start] = 99999
        path = [start]
        next_start = start
        while (now_path[next_start] != origin):
            path.append(now_path[next_start])
            next_start = now_path[next_start]
        path.append(origin)
        path.reverse()
        already_walked.append(start)
        for j in range(Cross.count):
            if j not in already_walked:
                if (road_array[start] + road_road_length[start][j]) < road_array[j]:
                    road_array[j] = temp[j] = road_array[start] + road_road_length[start][j]
                    now_path[j] = start
    return path