# main runner
# Should return arff file

from data_phraser import *
from data_clean import *


def main(base_file):

    print("Starting")

    row_martix = load_data_split_lines(base_file)
    # Write file to csv
    write_file_to_csv(row_martix)

    # Convert file to arff
    print("Starting arff conversion")
    load_data("current_write.csv")



    print("Finished")


if (__name__ == "__main__"):

    main("data/testing.txt")


