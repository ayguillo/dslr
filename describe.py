import csv
import sys
from column_info import column_info
import os
import pandas as pd

def is_number(str):
    try:
        float(str)
    except ValueError:
        return False
    else:
        return isinstance(float(str), (int,float))

def describe(data):
    rows, columns = os.popen('stty size', 'r').read().split()
    tab_feature, tab_res, count_line, n_feature = [], [], 0, 0
    index = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    len_i = len(index)
    for line in data :
        if (is_number(line[1])):
            tab_res.append(column_info(data[count_line][1:]))
            tab_feature.append(line[0])
            n_feature += 1
        count_line += 1
    df = pd.DataFrame(tab_res, columns = index, index = tab_feature)
    print(df)
    # print(tab_count)
    print(len(tab_res), len(tab_feature))
    # print(tab_res)
    # print(tab_feature)
    


def get_dataset(file):
    f = open(file,"r")
    csv_reader = csv.reader(f, delimiter=',')
    count_line = 0
    dataset = []
    for line in csv_reader:
        if (count_line == 0):
            len_data  = len(line)
            for j in range (0, len_data):
                dataset.append([])
        if (len(line) != len_data):
            f.close()
            print("File not well formed")
            return
        count_row = 0
        for row in line :
            dataset[count_row] += {row}
            count_row += 1
        count_line += 1
    f.close()
    return (dataset)

def main():
    data = get_dataset(sys.argv[1])
    describe(data)

if __name__ == "__main__":
    main()
