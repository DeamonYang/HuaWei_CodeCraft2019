#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Alo import *
from map import *
import sys
from reader import read_txt

def main():

    #car_path = sys.argv[1]
    #road_path = sys.argv[2]
    #cross_path = sys.argv[3]
    #answer_path = sys.argv[4]

    read_car, read_cross, read_road = read_txt('../config/car.txt', '../config/cross.txt', '../config/road.txt')#read_txt(car_path, cross_path, road_path)
    intiData(read_car, read_cross, read_road)
    plan_roadLength, plan_road, road_loss = Graph(Cross.count, Road.count, Road.isDuplex, Road.roadFrom, Road.roadTo,
                                                  Road.length, Road.id)
    answer = map1System(plan_road, plan_roadLength)
    #if Car.origin[0] == 18:
    #    answer = map1System(cross_road, road_road_Length)
    #else:
    #    answer = map2System(cross_road, road_road_Length)

    with open(answer_path, 'w') as fp:
        fp.write('\n'.join(str(tuple(x)) for x in answer))

if __name__ == "__main__":
    main()
