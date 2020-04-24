# import get_dataset from describe.py

import sys
import csv
from column_info import column_info
import matplotlib.pyplot as plt

def get_houses_dataset(file):
	f = open(file,"r")
	csv_reader = csv.reader(f, delimiter=',')
	count_line = 0
	dataset = {}
	house_row = -1
	for line in csv_reader:
		if (count_line == 0):
			len_data  = len(line)
			for row_index in range (0, len(line)):
				# print(line[row_index])
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
	quarts[0] /= count
	quarts[1] /= count
	quarts[2] /= count
	quarts[3] /= count
	return quarts

def		homogene(datasets, lesson):
	lesson_row = 0
	for row in datasets["Hogwarts House"]:
		# print(row[0])
		if row[0] == lesson:
			break
		lesson_row += 1
	global_info = column_info(datasets["Hogwarts House"][lesson_row])
	quarts = []
	quarts.append(quart_diff(global_info, datasets["Gryffindor"][lesson_row]))
	# print(G_quart)
	quarts.append(quart_diff(global_info, datasets["Slytherin"][lesson_row]))
	quarts.append(quart_diff(global_info, datasets["Hufflepuff"][lesson_row]))
	quarts.append(quart_diff(global_info, datasets["Ravenclaw"][lesson_row]))
	mean_quart = [(quarts[0][0] + quarts[1][0] + quarts[2][0] + quarts[3][0]) / 4,
				(quarts[0][1] + quarts[1][1] + quarts[2][1] + quarts[3][1]) / 4,
				(quarts[0][2] + quarts[1][2] + quarts[2][2] + quarts[3][2]) / 4,
				(quarts[0][3] + quarts[1][3] + quarts[2][3] + quarts[3][3]) / 4]
	diff =  abs(quarts[0][0] - mean_quart[0]) + abs(quarts[1][0] - mean_quart[0]) + abs(quarts[2][0] - mean_quart[0]) + abs(quarts[3][0] - mean_quart[0])
	diff += abs(quarts[0][1] - mean_quart[1]) + abs(quarts[1][1] - mean_quart[1]) + abs(quarts[2][1] - mean_quart[1]) + abs(quarts[3][1] - mean_quart[1])
	diff += abs(quarts[0][2] - mean_quart[2]) + abs(quarts[1][2] - mean_quart[2]) + abs(quarts[2][2] - mean_quart[2]) + abs(quarts[3][2] - mean_quart[2])
	diff += abs(quarts[0][3] - mean_quart[3]) + abs(quarts[1][3] - mean_quart[3]) + abs(quarts[2][3] - mean_quart[3]) + abs(quarts[3][3] - mean_quart[3])
	return (diff / 16, quarts)

data = get_houses_dataset(sys.argv[1])
# print("Arithmancy                   :", homogene(data, "Arithmancy"))
# print("Astronomy                    :", homogene(data, "Astronomy"))
# print("Herbology                    :", homogene(data, "Herbology"))
# print("Defense Against the Dark Arts:", homogene(data, "Defense Against the Dark Arts"))
# print("Divination                   :", homogene(data, "Divination"))
# print("Muggle Studies               :", homogene(data, "Muggle Studies"))
# print("Ancient Runes                :", homogene(data, "Ancient Runes"))
# print("History of Magic             :", homogene(data, "History of Magic"))
# print("Transfiguration              :", homogene(data, "Transfiguration"))
# print("Potions                      :", homogene(data, "Potions"))
# print("Care of Magical Creatures    :", homogene(data, "Care of Magical Creatures"))
# print("Charms                       :", homogene(data, "Charms"))
# print("Flying                       :", homogene(data, "Flying"))



res, quarts = homogene(data, "Arithmancy")
# n_bins = 4
import numpy as np
x = [[1, 4, 5, 2], [2, 8, 7, 3], [1, 4, 2, 6], [6, 1, 7, 3]]

# fig, ax0 = plt.subplots(nrows=1, ncols=1)
# ax0, ax1, ax2, ax3 = axes.flatten()

# colors = ['red', 'green', 'yellow', 'blue']
# houses = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
# data to plot


n_groups = 4
means_G = quarts[0]
means_S = quarts[1]
means_H = quarts[2]
means_R = quarts[3]

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
label='Larves')

rects4 = plt.bar(index + bar_width * 3 - bar_width / 2, means_R, bar_width,
alpha=opacity,
color='b',
label='Ravenclaw')

plt.xlabel('notes (%)')
plt.ylabel('student number (%)')
plt.title('poudlard')
plt.xticks(index + bar_width, ('0-25', '25-50', '50-75', '75-100'))
plt.legend()

plt.tight_layout()
plt.show()


# n, bins, patches = plt.hist([1, 2, 3, 4], [7, 8, 9], facecolor='red', alpha=0.5)
# plt.show()
# print(data["Hogwarts House"])

# histogram(data)
