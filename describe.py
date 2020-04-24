import csv
import sys

def main():
    f = open(sys.argv[1],"r")
    csv_reader = csv.reader(f, delimiter=',')
    count_line = 0
    dataset = []
    for line in csv_reader:
        if (count_line == 0):
            len_data  = len(line)
        if (len(line) != len_data):
            print("File not well formed")
            return
        count_row = 0
        for row in line :
            count_row += 1
        count_line += 1
    print(dataset)
    f.close()

if __name__ == "__main__":
    main()
