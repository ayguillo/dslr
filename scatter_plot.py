#!/usr/bin/python3

from describe import get_dataset
from pair_plot import new_lessons_list, set_color_palette
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import sys
import os

lessons = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
	"Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration",
	"Potions", "Care of Magical Creatures", "Charms", "Flying"]

def least_square(array1, array2):
	t0, t1 = 0, 0
	x, y, x_square, xy, student_nb = 0, 0, 0, 0, len(array1)
	for i in range(0, student_nb):
		x += array1.iloc[i]
		y += array2.iloc[i]
		x_square += array1.iloc[i] ** 2
		xy += array1.iloc[i] * array2.iloc[i]
	if student_nb < 1:
		print("Not enough data")
		sys.exit(-1)
	x /= student_nb
	y /= student_nb
	xy /= student_nb
	x_square /= student_nb

	t1 = abs(xy) - (abs(x) * abs(y))
	if abs(x_square) - (abs(x) ** 2) == 0:
		print("Data error")
		sys.exit(-1)
	t1 /= abs(x_square) - (abs(x) ** 2)
	t0 = abs(y) - t1 * abs(x)
	return (t0, t1)

def one_argument(dict, iteration1):
	len_max = len(dict)
	score, save_iter2, iteration2 = sys.maxsize, 0, 0
	while (iteration2 < len_max):
		if (iteration2 != iteration1):
			tmp0, tmp1 = least_square(dict[lessons[iteration1]], dict[lessons[iteration2]])
			if (abs(tmp0) + abs(tmp1 - 1) < score):
				score = abs(tmp0) + abs(tmp1 - 1)
				save_iter2 = iteration2
		iteration2 += 1
	return(save_iter2)

def no_argument(dict):
	iteration1 = 0
	len_max = len(dict)
	score, save_iter1, save_iter2 = sys.maxsize, 0, 0
	while(iteration1 < len_max):
		iteration2 = iteration1 + 1
		while (iteration2 < len_max):
			tmp0, tmp1 = least_square(dict[lessons[iteration1]], dict[lessons[iteration2]])
			if (abs(tmp0) + abs(tmp1 - 1) < score):
				save_iter1, save_iter2 = iteration1, iteration2
				score = abs(tmp0) + abs(tmp1 - 1)
			iteration2 += 1
		iteration1 +=1
	return(save_iter1, save_iter2)

def found_feature(data, feature1, feature2):
	dict = {}

	for i in lessons :
		dict[i] = data[i].sort_values()
	for i in lessons:
		if (dict[i].min() < 0):
			dict[i] = (-dict[i].min() + dict[i])
			dict[i] /= dict[i].max()
		else :
			dict[i] = dict[i] / dict[i].max()

	iteration1, iteration2, len_max = -1, -1, len(lessons)
	count1, count2 = 0, 0
	if (feature1):
		count1 = 0
		while count1 < len_max:
			if (lessons[count1].lower() == feature1.strip().lower()):
				iteration1 = count1
				break
			count1 += 1
	if (count1 == len_max):
		print("{} not found".format(feature1))
		return(None, None)
	if (feature2):
		count2 = 0
		while count2 < len_max:
			if (lessons[count2].lower() == feature2.strip().lower()):
				iteration2 = count2
				break
			count2 += 1
	if (count2 == len_max):
		print("{} not found".format(feature2))
		return(None, None)
	if (iteration1 == -1 and iteration2 == -1):
		save_iter1, save_iter2 = no_argument(dict)
	elif (iteration1 != -1 and iteration2 == -1):
		save_iter1, save_iter2 = iteration1, one_argument(dict, iteration1)
	elif (iteration1 != -1 and iteration2 != -1):
		save_iter1, save_iter2 = iteration1, iteration2
	else :
		print("Enter a feature 1 please")
		return(None, None)
	return (save_iter1, save_iter2)

def sort_by_houses(color, size, house, data, feature1, feature2, sort):
	data = data.dropna()
	mask = data["Hogwarts House"] == house
	data = data[mask]
	dict = {}
	for i in lessons :
		if (sort):
			dict[i] = data[i].sort_values()
		else :
			dict[i] = data[i]
	plt.scatter(dict[lessons[feature1]], dict[lessons[feature2]], c=color, s=size)

def scatter_plot(args):
	try:
		data = pd.read_csv(args.file)
	except pd.errors.EmptyDataError:
		print("Empty file")
		sys.exit(-1)
	data = data.dropna()
	feature1 = args.feature1
	feature2 = args.feature2
	size = args.size
	sort = args.sort

	save_iter1, save_iter2 = found_feature(data, feature1, feature2)
	if (save_iter1 is None):
		return()
	plt.title('Similar feature')
	plt.xlabel(lessons[save_iter1])
	plt.ylabel(lessons[save_iter2])
	if (args.color):
		sort_by_houses("green", size, "Slytherin", data, save_iter1, save_iter2, sort)
		sort_by_houses("yellow", size, "Hufflepuff", data, save_iter1, save_iter2, sort)
		sort_by_houses("blue", size, "Ravenclaw", data, save_iter1, save_iter2, sort)
		sort_by_houses("red", size, "Gryffindor", data, save_iter1, save_iter2, sort)
		slyth = mpatches.Patch(color='green', label='Slytherin')
		huffle = mpatches.Patch(color='yellow', label='Hufflepuff')
		raven = mpatches.Patch(color='blue', label='Ravenclaw')
		gryff = mpatches.Patch(color='red', label='Gryffindor')
		plt.legend(handles=[slyth, huffle, raven, gryff])
	else :
		dict = {}
		for i in lessons :
			if sort :
				dict[i] = data[i].sort_values()
			else :
				dict[i] = data[i]
		plt.scatter(dict[lessons[save_iter1]], dict[lessons[save_iter2]], c="red", s=size)
	plt.savefig('scatter_plot.png')
	plt.show()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="define your file", type = str)
	parser.add_argument("-f1", "--feature1", help="define feature 1", type = str)
	parser.add_argument("-f2", "--feature2", help="define feature 2", type = str)
	parser.add_argument("-c","--color", help="plot by houses", action="store_true")
	parser.add_argument("-S","--sort", help="ascendant sort", action="store_true")
	parser.add_argument("-s", "--size", help="scatter point size. Default = 0.1", type = float, default=0.1)
	args = parser.parse_args()
	if not os.path.exists(args.file) or not os.path.isfile(args.file):
		print("File error:", args.file)
		sys.exit()
	if (args.size < 0 or args.size > 50):
		print("Invalid size")
		sys.exit()
	scatter_plot(args)
