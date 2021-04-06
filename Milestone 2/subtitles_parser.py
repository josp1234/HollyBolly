import csv
from vaderSentiment.vaderSentiment import *

HOUR_MULTIPLIER = 3600
MINUTE_MULTIPLIER = 60
TIME_SPLITTER = ":"

# a lot of subtitle files end with a constant line of "please support our website". This
# is the line's VADER rank, in order to check for it in files.
SUPPORT_VADER_RANK = 0.7739
analyser = SentimentIntensityAnalyzer()


def calculate_vader_rank(sentence):
    """
    Calculates the VADER rank of a sentence.
    :param sentence: the sentence to be checked
    :return: the VADER rank of the sentence
    """
    score = analyser.polarity_scores(sentence)
    return score["compound"]


def parse_sub_file(file_path):
    """
    Parses a single subtitles file. For every subtitle, it is calculated in which percent
    of the movie it appears, and what is its VADER rank.
    :param file_path: path to a csv file to parse
    :return: a list of percentages and a list of VADER ranks that represent the subtitles
    file.
    """
    # open the csv file
    with open(file=file_path, mode="r", encoding="utf8") as subtitle_file:
        try:
            # create a list of lines of the file:
            csv_reader = list(csv.reader(subtitle_file))
        except Exception:
            return -1, -1
        # check file type: if it starts with this bracket - "{" - it is what we call a
        # "type 2 file" and needs another parsing method.
        if csv_reader[0][0][0] == "{":
            percent_lst, rank_lst = parse_type_2_file(csv_reader)
        else:
            percent_lst, rank_lst = parse_type_1_file(csv_reader)
    return percent_lst, rank_lst


# --------- type 1 parsing

def parse_type_1_file(file_list):
    """
    Parses files of "type 1", in which for every subtitle there is one line that
    represents the subtitle's index, another line with the subtitle times, and another
    line with the text. The next line is blank.
    :param file_list: a list that contains the lines of the file
    :return: percent list and VADER rank list
    """
    times_lst = []
    rank_lst = []
    i = 0
    while i < len(file_list):
        try:
            i += 1
            start_time = file_list[i][0]
            temp = file_list[i][1].split(" ")
            end_time = temp[-1]

            i += 1
            line_text = ""
            for text in file_list[i]:
                line_text += text

            # check if there is another line of text
            if file_list[i + 1]:
                i += 1
                for text in file_list[i]:
                    line_text += text

            temp_times_lst = [start_time, end_time]
            times_lst.append(temp_times_lst)
            rank = calculate_vader_rank(line_text)  # using VADER package
            rank_lst.append(rank)

            # move to next subtitle
            i += 2

        except Exception:
            break

    # check if the file ends with "please support us" line:
    if rank_lst[-1] == SUPPORT_VADER_RANK:
        rank_lst = rank_lst[:-1]
    movie_length = times_lst[-1][1]
    percent_lst = []
    for times in times_lst:
        percent = convert_to_percents_type_1(times[0], times[1], movie_length)
        percent_lst.append(percent)
    return percent_lst, rank_lst


def convert_to_percents_type_1(start_time, end_time, movie_length):
    """
    Converts the subtitle time to percent in the specific movie by calculating the middle time of
    the subtitle and dividing it by movie length
    :param start_time: a string that represents the start time of the subtitle
    :param end_time: a string that represents the end time of the subtitle
    :param movie_length: a string that represents the total length of the movie
    :return: the percent in the movie of the subtitle
    """
    time1_lst = start_time.split(TIME_SPLITTER)
    time1_seconds = int(time1_lst[0]) * HOUR_MULTIPLIER + int(time1_lst[1]) \
                    * MINUTE_MULTIPLIER + int(time1_lst[2])
    time2_lst = end_time.split(TIME_SPLITTER)
    time2_seconds = int(time2_lst[0]) * HOUR_MULTIPLIER + int(time2_lst[1]) \
                    * MINUTE_MULTIPLIER + int(time2_lst[2])
    # take the middle time between the start time and the end time as
    # "the time" of the subtitle:
    mid_time = (time1_seconds + time2_seconds) / 2

    movie_length = movie_length.split(TIME_SPLITTER)
    movie_length = int(movie_length[0])*HOUR_MULTIPLIER + \
                   int(movie_length[1])*MINUTE_MULTIPLIER + \
                   int(movie_length[2])
    return mid_time / movie_length


# --------- type 2 parsing


def parse_type_2_file(file_list):
    """
    Parses files of "type 2", in which the time and the text of the subtitle is in the
    same line. Times are mentioned in brackets.
    :param file_list: a list of lines of the file
    :return: percent list and rank list
    """
    times_lst = []
    rank_lst = []
    for line in file_list:
        line_string = ""
        for substring in line:
            line_string += substring
        first_ending_bracket_idx = 0
        second_ending_bracket_idx = 0
        first_ending_bracket_found = False
        for i in range(len(line_string)):
            if line_string[i] == "}":
                if not first_ending_bracket_found:
                    first_ending_bracket_idx = i
                    first_ending_bracket_found = True
                else:
                    second_ending_bracket_idx = i
                    break

        start_time = int(line_string[1:first_ending_bracket_idx])
        end_time = int(
            line_string[first_ending_bracket_idx + 2:second_ending_bracket_idx])
        times_lst.append([start_time, end_time])
        line_text = line_string[second_ending_bracket_idx + 1:]
        rank = calculate_vader_rank(line_text)  # using VADER package
        rank_lst.append(rank)
    movie_length = times_lst[-1][1]
    percent_lst = []
    for times in times_lst:
        temp = convert_to_percents_type_2(times[0], times[1], movie_length)
        percent_lst.append(temp)
    return percent_lst, rank_lst


def convert_to_percents_type_2(start_time, end_time, movie_length):
    """
    Converts time of subtitle to percent in the movie by calculating the middle time of
    the subtitle and dividing it by movie length
    :param start_time: an int that represents the start time of the subtitle
    :param end_time: an int that represents the end time of the subtitle
    :param movie_length: an int that represents the total length of the movie
    :return: the percent in the movie of the subtitle
    """
    mid_time = (start_time + end_time) / 2
    return mid_time / movie_length


# --------- silence parsing


def get_list_of_times(file_name):
    """
    This function parses a single movie file and returns its list of percentages and a
    parallel list of times (in what time the subtitle appears).
    :param file_name: the file to parse
    :return: a list of percents and a list of times
    """
    times_lst = []
    percent_lst = []
    with open(file=file_name, mode="r", encoding="utf8") as subtitle_file:
        # create a list of lines of the file:
        file_lines = list(csv.reader(subtitle_file))

        # we had a problem understanding the times of type 2 files, so we didn't include
        # them:
        if file_lines[0][0][0] == "{":
            return -1

        i = 0
        while i < len(file_lines):
            try:

                i += 1
                start_time = file_lines[i][0]
                temp = file_lines[i][1].split(" ")
                end_time = temp[-1]
                temp_lst = [start_time, end_time]
                times_lst.append(temp_lst)

                # check if there is one or two text lines
                if file_lines[i + 1]:
                    i += 1
                if file_lines[i + 1]:
                    i += 1

                i += 2

            except Exception:
                break

        movie_length = times_lst[-1][1]

        for times in times_lst:
            temp = convert_to_percents_silence(times[0], movie_length)
            percent_lst.append(temp)
        percent_lst.remove(percent_lst[0])
        return percent_lst, times_lst


def convert_to_percents_silence(start_time, movie_length):
    """
    Converts time of subtitle to percent in the movie by finding the start time of
    the subtitle and dividing it by movie length
    :param start_time: a string that represents the start time of the subtitle
    :param movie_length: a string that represents the length of the movie
    :return: the percent of the 'silence'
    """
    time_lst = start_time.split(TIME_SPLITTER)
    time_seconds = int(time_lst[0]) * HOUR_MULTIPLIER + int(time_lst[1]) \
                    * MINUTE_MULTIPLIER + int(time_lst[2])
    movie_length = movie_length.split(TIME_SPLITTER)
    movie_length = int(movie_length[0]) * HOUR_MULTIPLIER + \
                   int(movie_length[1]) * MINUTE_MULTIPLIER + \
                   int(movie_length[2])
    return time_seconds/movie_length




#     # write the results csv file
#     with open(name[:len(name)-4] + " Ranks.csv", 'w', newline='') as rank_file:
#         csv_writer = csv.writer(rank_file)
#         csv_writer.writerow(percent_lst)
#         csv_writer.writerow(rank_lst)
#         print("I created the file successfully")
#
#
# if __name__ == "__main__":
#     parse_sub_file("Babe.csv")
#

