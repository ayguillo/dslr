import csv
import sys

def get_dataset():
    f = open(sys.argv[1],"r")
    csv_reader = csv.reader(f, delimiter=',')
    count_line = 0
    dataset = []
    for line in csv_reader:
        if (count_line == 0):
            len_data  = len(line)
            for j in range (0, len_data):
                dataset.append([])
        if (len(line) != len_data):
            print("File not well formed")
            return
        count_row = 0
        for row in line :
            dataset[count_row] += {row}
            count_row += 1
        count_line += 1
    f.close()
    return (dataset)

if __name__ == "__main__":
    print(get_dataset())
