#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

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