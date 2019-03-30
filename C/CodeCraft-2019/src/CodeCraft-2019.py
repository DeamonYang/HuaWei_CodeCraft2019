#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import numpy as np

def read_txt(carPath, crossPath, roadPath):
	carData = []
	crossData = []
	roadData = []
	with open(carPath, 'r') as lines:
		for line in lines:
			line = line.split(',')
			if re.findall("\d+", line[0]) != []:
				line[0] = re.findall("\d+", line[0])[0]
			if re.findall("\d+", line[-1]) != []:
				line[-1] = re.findall("\d+", line[-1])[0]
			carData.append(line)
	with open(roadPath, 'r') as lines:
		for line in lines:
			line = line.split(',')
			if re.findall("\d+", line[0]) != []:
				line[0] = re.findall("\d+", line[0])[0]
			if re.findall("\d+", line[-1]) != []:
				line[-1] = re.findall("\d+", line[-1])[0]
			roadData.append(line)
	with open(crossPath, 'r') as lines:
		for line in lines:
			line = line.split(',')
			if re.findall("\d+", line[0]) != []:
				line[0] = re.findall("\d+", line[0])[0]
			if re.findall("\d+", line[-1]) != []:
				line[-1] = re.findall("\d+", line[-1])[0]
			crossData.append(line)

	carData = carData[1:]
	for i in range(len(carData)):
		for j in range(len(carData[i])):
			carData[i][j] = int(carData[i][j].strip())
	roadData = roadData[1:]
	for i in range(len(roadData)):
		for j in range(len(roadData[i])):
			roadData[i][j] = int(roadData[i][j].strip())
	crossData = crossData[1:]
	for i in range(len(crossData)):
		for j in range(len(crossData[i])):
			crossData[i][j] = int(crossData[i][j].strip())
			if j>0 and crossData[i][j] == 1:
				crossData[i][j] = -1
	return carData, crossData, roadData

class Car:
    def __init__(self, car_id, car_origin, car_destination, car_speed, car_startTime, car_count, car_dict):
        self.id = car_id
        self.origin = car_origin
        self.destination = car_destination
        self.speed = car_speed
        self.startTime = car_startTime
        self.count = car_count
        self.dict = car_dict

class Cross:
    def __init__(self, cross_id, cross_road1, cross_road2, cross_road3, cross_road4, cross_count, cross_dict):
        self.id = cross_id
        self.road1 = cross_road1
        self.road2 = cross_road2
        self.road3 = cross_road3
        self.road4 = cross_road4
        self.count = cross_count
        self.dict = cross_dict

class Road:
    def __init__(self, road_id, road_length, road_speed, road_channel, road_from, road_to, road_isDuplex, road_count, road_dict):
        self.id = road_id
        self.length = road_length
        self.speed = road_speed
        self.channel = road_channel
        self.roadFrom = road_from
        self.roadTo = road_to
        self.isDuplex = road_isDuplex
        self.count = road_count
        self.dict = road_dict

def intiData(read_car, read_cross, read_road):
    Road.count = len(read_road)
    Road.id = [i[0]for i in read_road]
    Road.length =[i[1]for i in read_road]
    Road.speed = [i[2]for i in read_road]
    Road.channel = [i[3]for i in read_road]
    Road.roadFrom = [i[4]for i in read_road]
    Road.roadTo = [i[5]for i in read_road]
    Road.isDuplex = [i[6]for i in read_road]
    Road.dict = {}
    for i in range(Road.count):
        Road.dict[Road.id[i]] = i

    Cross.count = len(read_cross)
    Cross.id = [i[0]for i in read_cross]
    Cross.dict = {}
    for i in range(Cross.count):
        Cross.dict[Cross.id[i]] = i
    Cross.road1 = [i[1]for i in read_cross]
    Cross.road2 = [i[2]for i in read_cross]
    Cross.road3 = [i[3]for i in read_cross]
    Cross.road4 = [i[4]for i in read_cross]

    Car.count = len(read_car)
    Car.id = [i[0]for i in read_car]
    Car.origin = [i[1]for i in read_car]
    Car.destination = [i[2]for i in read_car]
    Car.speed = [i[3]for i in read_car]
    Car.startTime = [i[4]for i in read_car]
    Car.dict = {}
    for i in range(Car.count):
        Car.dict[Car.id[i]] = i

def Graph(Cross_count, Road_count, Road_isDuplex, Road_roadFrom, Road_roadTo, Road_length, Road_id):
        # 对角矩阵，对角取0，设置每两个点间的距离，等于路径上的权值
    plan_roadLength = np.zeros([Cross_count, Cross_count]) + 10000 - 10000 * np.eye(Cross_count)
    plan_road = np.zeros([Cross_count, Cross_count])  # 36*36的每个起点到终点的路号，等于路径图

    for i in range(Road_count):
        if Road_isDuplex[i] == 1:
            plan_roadLength[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = \
            plan_roadLength[Cross.dict[Road_roadTo[i]]][Cross.dict[Road_roadFrom[i]]] = Road_length[i]
            plan_road[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = \
            plan_road[Cross.dict[Road_roadTo[i]]][Cross.dict[Road_roadFrom[i]]] = Road_id[i]
        else:
            plan_roadLength[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = Road_length[i]
            plan_road[Cross.dict[Road_roadFrom[i]]][Cross.dict[Road_roadTo[i]]] = Road_id[i]
    road_loss = plan_roadLength
    return plan_roadLength, plan_road, road_loss


def Dijkstra(origin, destination, planRoadLength):
    origin = Cross.dict[origin]
    destination = Cross.dict[destination]
    path_array = []
    temp_array = []
    path_array.extend(planRoadLength[origin])
    temp_array.extend(planRoadLength[origin])
    already_traversal = [origin]
    path_parent = [origin] * Cross.count
    i = origin
    while (i != destination):
        i = temp_array.index(min(temp_array))
        temp_array[i] = 10000
        path = [i]
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
    return path

def speedSort(Car_count, Car_speed, Car_id):
    max_speed = 0
    car_divide_speed = []
    car_divide_time = []
    car_divide_merge = []
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
    return group_divide_time

def update_loss(array_loss, array_dis, Road_count, Road_length, Road_channel, Road_speed, Road_isDuplex,
                Road_roadFrom, Road_roadTo, road_percent_list,speed):
    for i in range(Road_count):

        use_rate = road_percent_list[i]
        loss = Road_length[i] * (1 / min(Road_speed[i], speed) + 30 * use_rate / Road.channel[i])
        loss = loss *(1+2*road_percent_list[i])#3就不行了

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
    j = 0
    for speed in speed_list:
        cur_group = car_divide_speed[speed] #一个速度的数组
        if not cur_group:#空组
            continue
        car_per_sec = 5000
        group_divide_time = time_split(cur_group, car_per_sec)
        interval_time = 5#7
        for batch in group_divide_time:

            road_loss = update_loss(road_loss, plan_roadLength, Road.count, Road.length, Road.channel, Road.speed,
                                                          Road.isDuplex, Road.roadFrom, Road.roadTo, road_percent_list,speed)
            batch_path_time = cal_car_path(road_loss, plan_road, batch, time)
            road_use_list, road_percent_list = record_road(batch_path_time, road_use_list, road_percent_list)
            time += interval_time
            answer += batch_path_time
            print(answer)
    return answer

def main():

    #car_path = sys.argv[1]
    #road_path = sys.argv[2]
    #cross_path = sys.argv[3]
    #answer_path = sys.argv[4]
    answer_path = '../config/answer.txt'
    read_car, read_cross, read_road = read_txt('../config/car.txt', '../config/cross.txt', '../config/road.txt')
    #read_car, read_cross, read_road = read_txt(car_path, cross_path, road_path)
    intiData(read_car, read_cross, read_road)
    planRoadLength, planRoad, roadLoss = Graph(Cross.count, Road.count, Road.isDuplex, Road.roadFrom, Road.roadTo,
                                               Road.length, Road.id)
    answer = cal(planRoadLength, planRoad, roadLoss)

    with open(answer_path, 'w') as fp:
        fp.write('\n'.join(str(tuple(x)) for x in answer))

if __name__ == "__main__":
    main()
