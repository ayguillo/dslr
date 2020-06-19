#!/usr/bin/python3

from pair_plot import new_lessons_list
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import argparse
import sys
import os

def color_tab(column):
	colors = []
	# print(column)
	for house in column:
		if house == "Gryffindor":
			colors += ["rgb(255, 0, 0)"]
		elif house == "Slytherin":
			colors += ["rgb(0, 255, 0)"]
		elif house == "Ravenclaw":
			colors += ["rgb(0, 0, 255)"]
		elif house == "Hufflepuff":
			colors += ["rgb(255, 255, 0)"]
	return colors

def scatter_plot_3d(args):
	try:
		data = pd.read_csv(args.file)
	except pd.errors.EmptyDataError:
		print("Empty file")
		sys.exit(-1)
	lessons = new_lessons_list([args.featureX, args.featureY, args.featureZ],
		["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
		"Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration",
		"Potions", "Care of Magical Creatures", "Charms", "Flying"])
	if (len(lessons) < 3):
		return
	fig = go.Figure(data=[go.Scatter3d(
		   x=data[lessons[0]],
		   y=data[lessons[1]],
		   z=data[lessons[2]],
		   mode='markers',
		   marker=dict(color=color_tab(data["Hogwarts House"]),
					   size=args.size,
					   opacity=args.opacity)
		  )])
	fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
			scene=dict(
					xaxis_title=lessons[0],
					yaxis_title=lessons[1],
					zaxis_title=lessons[2]
			))
	fig.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="define your file", type = str)
	parser.add_argument("featureX", help="define feature for axe X", type = str)
	parser.add_argument("featureY", help="define feature for axe Y", type = str)
	parser.add_argument("featureZ", help="define feature for axe Z", type = str)
	parser.add_argument("-s", "--size", help="scatter point size. Default = 10", type = float, default=10)
	parser.add_argument("-o", "--opacity", help="scatter point opacity. Default = 0.5", type = float, default=0.5)
	args = parser.parse_args()
	if (args.size < 0 or args.size > 500):
		print("Invalid size")
		sys.exit()
	elif (args.opacity < 0 or args.opacity > 1):
		print("Invalid opacity")
		sys.exit()
	elif not os.path.exists(args.file) or not os.path.isfile(args.file):
		print("File error:", args.file)
		sys.exit()
	scatter_plot_3d(args)