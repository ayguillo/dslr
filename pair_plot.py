import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def set_color_palette(column):
	g, s, r, h = 0, 0, 0, 0
	colors = []
	for house in column:
		if house == "Gryffindor" and not g:
			g = 1
			colors += ["#FF0000"]
		elif house == "Slytherin" and not s:
			s = 1
			colors += ["#00FF00"]
		elif house == "Ravenclaw" and not r:
			r = 1
			colors += ["#0000FF"]
		elif house == "Hufflepuff" and not h:
			h = 1
			colors += ["#FFFF00"]
		if g and s and r and h:
			break
	sns.set_palette(colors)


def help():
	lessons = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
		"Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration",
		"Potions", "Care of Magical Creatures", "Charms", "Flying"]
	print(sys.argv[0], "file [-c] <feature1> <feature2> ... <featureN>")
	print("possible feature names:")
	for lesson in lessons:
		print(lesson)
	sys.exit(0)

def new_lessons_list(args, lessons):
	lessons_new = []
	for arg in args:
		found = False
		for lesson in lessons:
			if lesson.lower() == arg.lower():
				lessons_new += [lesson]
				found = True
				break
		if not found:
			print("Warning: unknow lesson \"" + arg + "\"")
	return (lessons_new)

if __name__ == "__main__":
	lessons = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
		"Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration",
		"Potions", "Care of Magical Creatures", "Charms", "Flying"]
	color = 0
	if len(sys.argv) < 2:
		print("ERROR: no file")
		help()
	elif (sys.argv[1] == "-h"):
		help()
	sns.set(style="ticks", color_codes=True)
	f = open(sys.argv[1], "r")
	dataframe = pd.read_csv(f, delimiter=',')
	if len(sys.argv) > 2:
		if sys.argv[2] == "-c":
			color = 1
		if len(sys.argv) > 2 + color:
			lessons = new_lessons_list(sys.argv[2 + color:], lessons)
	for column_name in dataframe:
		if column_name not in lessons and column_name != "Hogwarts House":
			dataframe = dataframe.drop(column_name, 1)
	lines, columns = dataframe.shape
	if columns < 2:
		print("ERROR: pair plot need at least 2 features")
		help()
	if color:
		set_color_palette(dataframe["Hogwarts House"])
		g = sns.pairplot(dataframe, hue="Hogwarts House", vars=lessons, plot_kws={'alpha':0.3})
		g._legend.remove()
	else:
		sns.pairplot(dataframe, vars=lessons)
	plt.tight_layout()
	plt.show()
	