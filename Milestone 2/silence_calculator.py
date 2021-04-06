from os import listdir
from os.path import isfile, join
import subtitles_parser
import csv
import count_list_creator


def get_list_of_silences(times_lst):
    """
    This function analyses a list of subtitle times and returns a list of 'silences' for
    this list.
    :param times_lst: a list of subtitle times
    :return: a list of 'silences'
    """
    silence_lst = []
    for i in range(len(times_lst)-1):
        first_sub = times_lst[i][1]
        first_sub_lst = first_sub.split(":")
        first_sub_seconds = int(first_sub_lst[0]) * subtitles_parser.HOUR_MULTIPLIER + \
                            int(first_sub_lst[1]) * subtitles_parser.MINUTE_MULTIPLIER + \
                            int(first_sub_lst[2])
        second_sub = times_lst[i + 1][0]
        second_sub_lst = second_sub.split(":")
        second_sub_seconds = int(second_sub_lst[0]) * subtitles_parser.HOUR_MULTIPLIER + \
                             int(second_sub_lst[1]) * subtitles_parser.MINUTE_MULTIPLIER \
                             + int(second_sub_lst[2])
        diff = second_sub_seconds - first_sub_seconds
        silence_lst.append(diff)
    return silence_lst


def sum_silence_peaks(mypath):
    """
    This function iterates over 'silence files' and sums the 'silence peaks' of each
    movie. The results are written into a new csv file.
    :param mypath: path to the directory with 'silence files'
    """
    all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    res = []
    for file_name in all_files:
        with open(file=mypath+"/"+file_name, mode="r", encoding="utf8") as silence_file:
            try:
                # read the file:
                csv_reader = list(csv.reader(silence_file))
                percent_lst = csv_reader[0]
                silence_lst = csv_reader[1]
                count_lst = count_list_creator.count_silence_peaks(percent_lst, silence_lst)
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


def parse_subs_silence(input_path, output_path):
    """
    This function iterates over movie subtitle files and finds all the 'silence' moments
    (moments without any text in them). For every movie, it creates a file that contains
    'silences' and their percents in the movie.
    :param input_path: path to the input directory
    :return:
    """
    all_files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    for file_name in all_files:
        new_file_name = input_path + "/" + file_name
        try:
            percent_lst, times_lst = subtitles_parser.get_list_of_times(new_file_name)
            if times_lst == -1:
                print(file_name + " --- File failed")
                continue
            else:
                silence_lst = get_list_of_silences(times_lst)
                with open(output_path + "/" + file_name[:len(file_name) - 4] +
                          " Silence.csv", 'w', newline='') as silence_file:
                    csv_writer = csv.writer(silence_file)
                    csv_writer.writerow(percent_lst)
                    csv_writer.writerow(silence_lst)
                    print(file_name + " file was created successfully")
        except Exception:
            print(new_file_name + " has made an error")


if __name__ == "__main__":
    # call this function with ("HollywoodSubs", "HollywoodSilence") or ("BollywoodSubs",
    # "BollywoodSilence") to parse all subtitle files and create a file of 'silences'
    # for each one:
    # parse_subs_silence("HollywoodSubs", "HollywoodSilence")

    # after creating silence files, call this function with "HollywoodSilence" or
    # "BollywoodSilence" to sum the silence peaks of every movie:
    sum_silence_peaks("BollywoodSilence")
