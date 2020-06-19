#!/usr/bin/python3

import sys
import os
import csv
from src.column_info import column_info
import matplotlib.pyplot as plt
import numpy as np
import argparse

def		multiply_100(tab):
	for i in range (len(tab)):
		tab[i] *= 100
	return tab

def		get_houses_dataset(file):
	f = open(file,"r")
	csv_reader = csv.reader(f, delimiter=',')
	count_line = 0
	dataset = {}
	house_row = -1
	for line in csv_reader:
		if (count_line == 0):
			len_data  = len(line)
			for row_index in range (0, len(line)):
				if (line[row_index] == "Hogwarts House"):
					house_row = row_index
					break
			if (house_row == -1):
				print("Hogwarts House row not found")
				return
		if (len(line) != len_data):
			print("File not well formed")
			return
		
		if line[house_row] not in dataset:
			dataset[line[house_row]] = []
			for j in range (0, len_data):
				dataset[line[house_row]].append([])
		count_row = 0
		for row in line :
			if line[house_row] != "Hogwarts House":
				dataset["Hogwarts House"][count_row] += {row}
			dataset[line[house_row]][count_row] += {row}
			count_row += 1
		count_line += 1
	f.close()
	return (dataset)

def		quart_diff(general_info, house_notes):
	quarts = [0, 0, 0, 0]
	count = len(house_notes)
	for note in house_notes:
		try :
			nb = float(note)
			if nb < general_info[4]:
				quarts[0] += 1
			elif nb < general_info[5]:
				quarts[1] += 1
			elif nb < general_info[6]:
				quarts[2] += 1
			else:
				quarts[3] += 1
		except ValueError :
			count -= 1
	if count < 1:
		print("Not enough data")
		sys.exit(-1)
	quarts[0] /= count
	quarts[1] /= count
	quarts[2] /= count
	quarts[3] /= count
	return quarts

def		difference(datasets, lesson):
	lesson_row = 0
	if "Hogwarts House" not in datasets:
		print("No column 'Hogwarts House'")
		sys.exit(-1)
	for row in datasets["Hogwarts House"]:
		# print(row[0])
		if row[0] == lesson:
			break
		lesson_row += 1
	global_info = column_info(datasets["Hogwarts House"][lesson_row])
	quarts = []
	try:
		quarts.append(quart_diff(global_info, datasets["Gryffindor"][lesson_row]))
		quarts.append(quart_diff(global_info, datasets["Slytherin"][lesson_row]))
		quarts.append(quart_diff(global_info, datasets["Hufflepuff"][lesson_row]))
		quarts.append(quart_diff(global_info, datasets["Ravenclaw"][lesson_row]))
	except KeyError as t:
		print("Missing house:", t)
		sys.exit(-1)
	mean_quart = [(quarts[0][0] + quarts[1][0] + quarts[2][0] + quarts[3][0]) / 4,
				(quarts[0][1] + quarts[1][1] + quarts[2][1] + quarts[3][1]) / 4,
				(quarts[0][2] + quarts[1][2] + quarts[2][2] + quarts[3][2]) / 4,
				(quarts[0][3] + quarts[1][3] + quarts[2][3] + quarts[3][3]) / 4]
	diff =  abs(quarts[0][0] - mean_quart[0]) + abs(quarts[1][0] - mean_quart[0]) + abs(quarts[2][0] - mean_quart[0]) + abs(quarts[3][0] - mean_quart[0])
	diff += abs(quarts[0][1] - mean_quart[1]) + abs(quarts[1][1] - mean_quart[1]) + abs(quarts[2][1] - mean_quart[1]) + abs(quarts[3][1] - mean_quart[1])
	diff += abs(quarts[0][2] - mean_quart[2]) + abs(quarts[1][2] - mean_quart[2]) + abs(quarts[2][2] - mean_quart[2]) + abs(quarts[3][2] - mean_quart[2])
	diff += abs(quarts[0][3] - mean_quart[3]) + abs(quarts[1][3] - mean_quart[3]) + abs(quarts[2][3] - mean_quart[3]) + abs(quarts[3][3] - mean_quart[3])
	return (diff / 16, quarts)

def		lesson_graph(dataset, lesson):
	res, quarts = difference(dataset, lesson)

	n_groups = 4
	means_G = multiply_100(quarts[0])
	means_S = multiply_100(quarts[1])
	means_H = multiply_100(quarts[2])
	means_R = multiply_100(quarts[3])

	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.20
	opacity = 0.8

	rects1 = plt.bar(index - bar_width / 2, means_G, bar_width,
	alpha=opacity,
	color='r',
	label='Gryffyndor')

	rects2 = plt.bar(index + bar_width - bar_width / 2, means_S, bar_width,
	alpha=opacity,
	color='g',
	label='Slytherin')

	rects3 = plt.bar(index + bar_width * 2 - bar_width / 2, means_H, bar_width,
	alpha=opacity,
	color='y',
	label='Hufflepuff')

	rects4 = plt.bar(index + bar_width * 3 - bar_width / 2, means_R, bar_width,
	alpha=opacity,
	color='b',
	label='Ravenclaw')

	plt.xlabel('notes (%)')
	plt.ylabel('student number (%)')
	plt.title(lesson)
	plt.xticks(index + bar_width, ('0-25', '25-50', '50-75', '75-100'))
	plt.legend()

	plt.tight_layout()
	plt.show()

def		histogram_graph(dataset):
	lessons = {"Arithmancy":0, "Astronomy":0, "Herbology":0, "Defense Against the Dark Arts":0,
	"Divination":0, "Muggle Studies":0, "Ancient Runes":0, "History of Magic":0, "Transfiguration":0,
	"Potions":0, "Care of Magical Creatures":0, "Charms":0, "Flying":0}
	for lesson in lessons.keys():
		score, quarts = difference(dataset, lesson)
		lessons[lesson] = score
	lessons_graph, scores_graph = [], []
	for k, v in sorted(lessons.items(), key=lambda x: x[1]):
		lessons_graph += [k.replace(' ', '\n')]
		scores_graph += [v]

	fig = plt.figure(figsize = (13, 7))
	plt.bar(lessons_graph, multiply_100(scores_graph))

	plt.tight_layout()
	plt.show()

def		main():
	lessons = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
	"Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration",
	"Potions", "Care of Magical Creatures", "Charms", "Flying"]
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="define your file", type = str)
	parser.add_argument("-l", "--lesson", help="show the graph for the lesson", type = str)
	args = parser.parse_args()
	if not os.path.exists(args.file) or not os.path.isfile(args.file):
		print("File error:", args.file)
		sys.exit()
	data = get_houses_dataset(args.file)
	if args.lesson:
		for lesson in lessons:
			if args.lesson.lower() == lesson.lower():
				lesson_graph(data, lesson)
				return
		print("Unknow lesson name. try with these:\n\n" + "\n".join(lessons))
	else:
		histogram_graph(data)

if __name__ == "__main__":
	main()