import subtitle_visualization
import count_list_creator
import subtitles_parser
from os import listdir
from os.path import isfile, join
import csv


def parse_subs(directory_path, new_directory_path):
    """
    Parses all files in the given directory, and creates for every file a new csv file
    with the percent of every subtitle and its VADER rank.
    :param directory_path: input directory name
    :param new_directory_path: output directory name
    """
    all_files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]

    for file_name in all_files:
        new_file_name = directory_path + "/" + file_name
        try:
            percent_lst, rank_lst = subtitles_parser.parse_sub_file(new_file_name)
            if percent_lst == -1:
                print(file_name + " --- File opening failed")
                continue
            else:
                # create a csv file that contains the percents and ranks for a single
                # subtitles file:
                with open(new_directory_path + "/" + file_name[:len(file_name) - 4] +
                          " Ranks.csv", 'w', newline='') as rank_file:
                    csv_writer = csv.writer(rank_file)
                    csv_writer.writerow(percent_lst)
                    csv_writer.writerow(rank_lst)
                    print(file_name + " file was created successfully")
        except Exception:
            print(new_file_name + " has made an error")


def sum_peaks(mypath):
    """
    After creating files with percents and ranks, this function iterates over all the
    files and for each movie it counts how many emotional peaks there are in each
    percentage of the movie. The results are saved in a new csv file.
    :param mypath: path to the directory that contains the files to iterate over
    """
    subs_files_lst = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    res = []
    for file_name in subs_files_lst:
        with open(file=mypath+"/"+file_name, mode="r", encoding="utf8") as subtitle_file:
            try:
                # read the file:
                csv_reader = list(csv.reader(subtitle_file))
                percent_lst = csv_reader[0]
                rank_lst = csv_reader[1]
                count_lst = count_list_creator.count_emotional_peaks(percent_lst, rank_lst)
                if count_lst == -1:
                    print(file_name + " was not included")
                    continue
                res.append(count_lst)
            except Exception:
                print(file_name + " was not included")
                continue

    # write the results to a csv file:
    with open(mypath + "All Peaks.csv", "w", newline="") as outfile:
        writer = csv.writer(outfile)
        for line in res:
            writer.writerow(line)


if __name__ == "__main__":

    # call this function with ("HollywoodSubs", "HollywoodRanks") or ("BollywoodSubs",
    # "BollywoodRanks") to parse all subtitle files and create a file of ranks for each
    # one:
    parse_subs("BollywoodSubs", "BollywoodRanks")

    # after creating rank files, call this function with "HollywoodRanks" or
    # "BollywoodRanks" to sum the peaks of every movie:
    sum_peaks("HollywoodRanks")

