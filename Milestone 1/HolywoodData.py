import csv
from collections import Counter
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
nltk.download()


def read_hollywood_csv():
    # open a csv file
    with open("Hollywood Plot Summary.csv", "r", encoding="utf8") as my_file:
        final_data = []
        # read the data from the csv
        csv_data = csv.reader(my_file, delimiter=";")
        # unite the lines to separate words
        for row in csv_data:
            row_txt = ''.join(row)
            txt_as_words = row_txt.split()
            for word in txt_as_words:
                # make sure that is a legal word
                if not word.isalpha():
                    txt_as_words.remove(word)
            final_data.append(txt_as_words)
        # build a final list
        final_data = list(itertools.chain.from_iterable(final_data))
        print(len(final_data))
        return final_data


if __name__ == "__main__":
    # create a stemmer object
    stemmer = SnowballStemmer("english")
    # define stopwords using nltk
    the_stopwords = set(stopwords.words('english'))
    # add specific stopwords that common in the subtitles but not included in the stopwords
    my_hollywood_stopwords = {"'s", "get", "find", "take", "come", "one", "meet",
                       "tell", "doe", "ask", "day", "also", "become", "make",
                       "film", "new", "life", "two", "live", "becom", "man",
                       "year", "onli", "begin", "go", "set", "stori", "tri",
                       "time", "turn", "fall", "back", "want", "follow", "peopl",
                               "use", "befor", "start", "return", "way", "three",
                                      "group", "dure", "decid", "must", "world"}
    # unite the stopwords to one set
    the_stopwords.update(my_hollywood_stopwords)
    read_csv = read_hollywood_csv()
    # filter the words by the stopwords and do stemming
    filtered_words = [stemmer.stem(word) for word in read_csv if stemmer.stem(
        word.lower())
                      not in the_stopwords]

    print(len(filtered_words))
    # open a file for the final words
    final_filtered_file = open("holly_only_holly", "w", encoding="utf8")
    # insert the words to the file
    for word in filtered_words:
        final_filtered_file.writelines(word + " ")
    # show me a the words according to their frequency
    print(Counter(filtered_words))
