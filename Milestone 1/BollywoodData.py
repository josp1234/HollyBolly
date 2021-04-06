import csv
from collections import Counter
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
nltk.download()


def read_bollywood_csv():
    # open a csv file
    with open("Bollywood Plot Summary.csv", "r") as my_file:
        final_data = []
        # read the data from the csv
        csv_data = csv.reader(my_file, delimiter=";")
        # add all of the words to one list
        for row in csv_data:
            row_txt = row[0]
            txt_as_words = row_txt.split()
            final_data.append(txt_as_words)
        final_data = list(itertools.chain.from_iterable(final_data))
        return final_data


if __name__ == "__main__":
    # create a stemmer object
    stemmer = SnowballStemmer("english")
    # define stopwords using nltk
    the_stopwords = set(stopwords.words('english'))
    # add specific stopwords
    additional_stopwords = {"'s", "get", "find", "take", "come", "one",
                                 "meet", "tell", "doe", "ask", "day", "also",
                                 "become", "make", "tri", "leav", "live", "life",
                                           "becom", "back", "go", "want", "see",
                                 "man"}
    # unite the stopwords to one set
    the_stopwords.update(additional_stopwords)
    csv_content = read_bollywood_csv()
    # filter the words by the stopwords and do stemming
    filtered_words = [stemmer.stem(word) for word in csv_content if stemmer.stem(
        word.lower())
                      not in the_stopwords]
    # open a file for the final words
    stemmed_words = open("bollywood_after_stem", "w")
    # insert the words to the file
    for word in filtered_words:
        stemmed_words.writelines(word + " ")
    # show the most frequent words
    print(Counter(filtered_words))
