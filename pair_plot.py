import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
# print(dataframe)

def help():
	lessons = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
		"Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration",
		"Potions", "Care of Magical Creatures", "Charms", "Flying"]
	print(sys.argv[0], "file <feature1> <feature2> ... <featureN>")
	print("possible feature names:")
	for lesson in lessons:
		print(lesson)
	sys.exit(0)

def new_lessons_list(args, lessons):
	lessons_new = []
	for lesson in lessons:
		for arg in args:
			if lesson.lower() == arg.lower():
				lessons_new += [lesson]
	return (lessons_new)

if __name__ == "__main__":
	lessons = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
		"Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration",
		"Potions", "Care of Magical Creatures", "Charms", "Flying"]
	if len(sys.argv) < 2:
		print("ERROR: no file")
		help()
	elif (sys.argv[1] == "-h"):
		help()
	sns.set(style="ticks", color_codes=True)
	f = open(sys.argv[1], "r")
	dataframe = pd.read_csv(f, delimiter=',')
	if len(sys.argv) > 2:
		lessons = new_lessons_list(sys.argv[2:], lessons)
	for column_name in dataframe:
		if column_name not in lessons:
			dataframe = dataframe.drop(column_name, 1)
	lines, columns = dataframe.shape
	if columns < 2:
		print("ERROR: pair plot need at least 2 features")
		help()
	sns.pairplot(dataframe, vars=lessons)
	plt.tight_layout()
	plt.show()
	