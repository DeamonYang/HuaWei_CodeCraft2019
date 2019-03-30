#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from sNumCarSort import all_car_path
#from speedSort import *
from  speedTimeSort5_1 import *
from map import *
import sys
from reader import read_txt

def main():

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    #road_path = '../config/road.txt'
    #cross_path = '../config/cross.txt'
    #car_path = '../config/car.txt'
    #answer_path = '../config/answer.txt'

    read_car, read_cross, read_road = read_txt(car_path, cross_path, road_path)

    intiData(read_car, read_cross, read_road)
    planRoadLength, planRoad, roadLoss = Graph(Cross.count, Road.count, Road.isDuplex, Road.roadFrom, Road.roadTo, Road.length, Road.id)
    #answer = all_car_path(graph.plan_roadLength, graph.plan_road) #numCarWays
    #car_time = speedSort(Car.count)#speedsort
    #cross_loss = cal_cross_loss(read_cross, read_road)
    #answer = carPath(graph.plan_roadLength, graph.plan_road, read_car, car_time)#speedsort
    #if Car.origin[0] == 18:
    #    answer = call(planRoadLength, planRoad, roadLoss)
    #else:
    answer = cal(planRoadLength, planRoad, roadLoss)

    with open(answer_path, 'w') as fp:
        fp.write('\n'.join(str(tuple(x)) for x in answer))

if __name__ == "__main__":
    main()
