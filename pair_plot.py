import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
lessons = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
	"Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration",
	"Potions", "Care of Magical Creatures", "Charms", "Flying"]
sns.set(style="ticks", color_codes=True)
f = open(sys.argv[1], "r")
dataframe = pd.read_csv(f, delimiter=',')
dataframe = dataframe.drop("Index", 1)
dataframe = dataframe.drop("Hogwarts House", 1)
dataframe = dataframe.drop("First Name", 1)
dataframe = dataframe.drop("Last Name", 1)
dataframe = dataframe.drop("Birthday", 1)
dataframe = dataframe.drop("Best Hand", 1)
print(dataframe)
g = sns.pairplot(dataframe, vars=lessons)

plt.tight_layout()
plt.show()