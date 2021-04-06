NUM_OF_PERCENTAGES = 1000
# the minimal value that defines an emotional peak:
THRESHOLD_RANK = 0.35
# the minimal value that defines a silence peak:
THRESHOLD_SILENCE = 5


def count_emotional_peaks(percent_list, rank_list):
    """
    For each subtitles file, this function counts how many emotional peaks are found in
    each percentage of the movie. Every movie is divided into 1000 percentages (so that
    each one is 0.1% of the movie).
    :param percent_list: list of percents
    :param rank_list: list of VADER ranks
    :return: a list with 1000 ints, each one for each percentage, which indicate how many
    emotional peaks were found in this percentage.
    """
    count_lst = [0] * NUM_OF_PERCENTAGES
    for i in range(len(rank_list)):
        rank = rank_list[i]
        if float(rank) < THRESHOLD_RANK:
            continue
        percent = float(percent_list[i])
        # check if an error occurred during parsing:
        if percent > 1:
            return -1
        idx_num = int(round(percent, 4) * NUM_OF_PERCENTAGES)  # provide an index for the percentage
        count_lst[idx_num] += 1

    return count_lst


def count_silence_peaks(percent_list, silence_list):
    """
    For each subtitles file, this function counts how many emotional peaks are found in
    each percentage of the movie. Every movie is divided into 1000 percentages (so that
    each one is 0.1% of the movie).
    :param percent_list: list of percents
    :param silence_list: list of 'silences'
    :return: a list with 1000 ints, each one for each percentage, which indicate how many
    silence peaks were found in this percentage.
    """
    count_lst = [0] * NUM_OF_PERCENTAGES
    for i in range(len(silence_list)):
        silence = silence_list[i]
        if float(silence) < THRESHOLD_SILENCE:
            continue
        percent = percent_list[i]
        # check if an error occurred during parsing:
        if float(percent) > 1:
            return -1
        idx_num = int(round(float(percent), 4) * NUM_OF_PERCENTAGES)  # provide an index for the percentage
        count_lst[idx_num] += 1
    return count_lst
