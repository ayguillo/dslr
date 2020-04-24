# import get_dataset from describe.py

import sys
import csv
from column_info import column_info

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
	G_quart = quart_diff(global_info, datasets["Gryffindor"][lesson_row])
	# print(G_quart)
	S_quart = quart_diff(global_info, datasets["Slytherin"][lesson_row])
	H_quart = quart_diff(global_info, datasets["Hufflepuff"][lesson_row])
	R_quart = quart_diff(global_info, datasets["Ravenclaw"][lesson_row])
	mean_quart = [(G_quart[0] + S_quart[0] + H_quart[0] + R_quart[0]) / 4,
				(G_quart[1] + S_quart[1] + H_quart[1] + R_quart[1]) / 4,
				(G_quart[2] + S_quart[2] + H_quart[2] + R_quart[2]) / 4,
				(G_quart[3] + S_quart[3] + H_quart[3] + R_quart[3]) / 4]
	diff =  abs(G_quart[0] - mean_quart[0]) + abs(S_quart[0] - mean_quart[0]) + abs(H_quart[0] - mean_quart[0]) + abs(R_quart[0] - mean_quart[0])
	diff += abs(G_quart[1] - mean_quart[1]) + abs(S_quart[1] - mean_quart[1]) + abs(H_quart[1] - mean_quart[1]) + abs(R_quart[1] - mean_quart[1])
	diff += abs(G_quart[2] - mean_quart[2]) + abs(S_quart[2] - mean_quart[2]) + abs(H_quart[2] - mean_quart[2]) + abs(R_quart[2] - mean_quart[2])
	diff += abs(G_quart[3] - mean_quart[3]) + abs(S_quart[3] - mean_quart[3]) + abs(H_quart[3] - mean_quart[3]) + abs(R_quart[3] - mean_quart[3])
	return (diff / 16)

data = get_houses_dataset(sys.argv[1])
print("Arithmancy                   :", homogene(data, "Arithmancy"))
print("Astronomy                    :", homogene(data, "Astronomy"))
print("Herbology                    :", homogene(data, "Herbology"))
print("Defense Against the Dark Arts:", homogene(data, "Defense Against the Dark Arts"))
print("Divination                   :", homogene(data, "Divination"))
print("Muggle Studies               :", homogene(data, "Muggle Studies"))
print("Ancient Runes                :", homogene(data, "Ancient Runes"))
print("History of Magic             :", homogene(data, "History of Magic"))
print("Transfiguration              :", homogene(data, "Transfiguration"))
print("Potions                      :", homogene(data, "Potions"))
print("Care of Magical Creatures    :", homogene(data, "Care of Magical Creatures"))
print("Charms                       :", homogene(data, "Charms"))
print("Flying                       :", homogene(data, "Flying"))
# print(data["Hogwarts House"])

# histogram(data)
