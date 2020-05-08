from describe import get_dataset
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

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
    x /= student_nb
    y /= student_nb
    xy /= student_nb
    x_square /= student_nb

    t1 = abs(xy) - (abs(x) * abs(y))
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

def scatter_plot(file, feature1, feature2, size):
    data = pd.read_csv(file)
    dict = {}
    data = data.dropna()

    for i in lessons :
        dict[i] = data[i].sort_values()
    for i in lessons:
        if (dict[i].min() < 0):
            dict[i] = (-dict[i].min() + dict[i])
            dict[i] /= dict[i].max()
        else :
            dict[i] = dict[i] / dict[i].max()

    iteration1, iteration2, len_max = -1, -1, len(lessons)
    if (feature1):
        count = 0
        while count < len_max:
            if (lessons[count].lower() == feature1.strip().lower()):
                iteration1 = count
                break
            count += 1
    if (feature2):
        count = 0
        while count < len_max:
            if (lessons[count].lower() == feature2.strip().lower()):
                iteration2 = count
                break
            count += 1
    if (iteration1 == -1 and iteration2 == -1):
        save_iter1, save_iter2 = no_argument(dict)
    elif (iteration1 != -1 and iteration2 == -1):
        save_iter1, save_iter2 = iteration1, one_argument(dict, iteration1)
    elif (iteration1 != -1 and iteration2 != -1):
        save_iter1, save_iter2 = iteration1, iteration2
    else :
        print("Enter a feature 1 please")
        return()

    plt.scatter(dict[lessons[save_iter1]], dict[lessons[save_iter2]], c='red',s=size)
    plt.title('Similar feature')
    plt.xlabel(lessons[save_iter1])
    plt.ylabel(lessons[save_iter2])
    plt.savefig('scatter_plot.png')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="define your file", type = str)
    parser.add_argument("-f1", "--feature1", help="define feature 1", type = str)
    parser.add_argument("-f2", "--feature2", help="define feature 2", type = str)
    parser.add_argument("-s", "--size", help="scatter point size. Default = 0.1", type = float, default=0.1)
    args = parser.parse_args()
    if (args.size < 0 or args.size > 50):
        print("Invalid size")
        sys.exit()
    scatter_plot(args.file, args.feature1, args.feature2, args.size)
