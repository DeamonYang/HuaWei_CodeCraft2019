#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Car:
    def __init__(self, car_id, car_origin, car_destination, car_speed, car_startTime, car_count,car_dict):
        self.id = car_id
        self.origin = car_origin
        self.destination = car_destination
        self.speed = car_speed
        self.startTime = car_startTime
        self.count = car_count
        self.dict = car_dict

class Cross:
    def __init__(self, cross_id, cross_road1, cross_road2, cross_road3, cross_road4, cross_count,cross_dict):
        self.id = cross_id
        self.road1 = cross_road1
        self.road2 = cross_road2
        self.road3 = cross_road3
        self.road4 = cross_road4
        self.count = cross_count
        self.dict = cross_dict

class Road:
    def __init__(self, road_id, road_length, road_speed, road_channel, road_from, road_to, road_isDuplex, road_count,road_dict):
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
    Cross.road1 = [i[1]for i in read_cross]
    Cross.road2 = [i[2]for i in read_cross]
    Cross.road3 = [i[3]for i in read_cross]
    Cross.road4 = [i[4]for i in read_cross]
    Cross.dict = {}
    for i in range(Cross.count):
        Cross.dict[Cross.id[i]] = i

    Car.count = len(read_car)
    Car.id = [i[0]for i in read_car]
    Car.origin = [i[1]for i in read_car]
    Car.destination = [i[2]for i in read_car]
    Car.speed = [i[3]for i in read_car]
    Car.startTime = [i[4]for i in read_car]
    Car.dict = {}
    for i in range(Car.count):
        Car.dict[Car.id[i]] = i

from reader import read_txt
if __name__ == "__main__":
    #read_road = read_txt('../config/road.txt')
    #read_cross = read_txt('../config/cross.txt')
    #read_car = read_txt('../config/car.txt')
    read_car, read_cross, read_road = read_txt('../config/car.txt', '../config/cross.txt', '../config/road.txt')
    intiData(read_car, read_cross, read_road)
    print(Road.dict)