# Author Conor O'Kelly
import os
import csv

def main():

    print("Starting main")



def load_data_split_lines(file_name):

    raw_file = open(file_name, encoding='ISO-8859-1')

    read_file = raw_file.read()

    lines = read_file.splitlines()

    # print(lines[0])
    # Split line based on \t

    formated_lines =[]

    for li in lines:
        # print("one line")
        split_line = li.split("\t")
        cleaned_line = []

        for item in split_line:
            if item[0:3] == "nan":
                item = ""
            cleaned_line.append(item.strip())
        formated_lines.append(cleaned_line)

    return formated_lines


def write_file_to_csv(row_matrix):
    with open("current_write.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(row_matrix)

    return 0

if (__name__ == "__main__"):

    print(os.getcwd())

    data_rows = load_data_split_lines("data/training.txt")
    # print(data_rows)
    write_file_to_csv(data_rows)
