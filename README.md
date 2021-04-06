# HollyBolly - The Mystery of Bollywood Drama

## Intro
**We're Maayan Magenheim and Jehonathan Spigelman, two guys who love cinema, Indians, kitsch and stupidity, not necessarily in this order**. 
The Indian film industry, which in contrast to Hollywood serves more or less one unique culture, intrigues us and raises interesting questions about how kitsch is created, and whether it is the content or form that creates it. **We tried to use data analysis of films' plots and subtitles to try to figure out what the sources of Bollywood kitsch were**. This project was created as part of the course "Big Data Analysis" as part of the Department of Internet and Society at the Hebrew University of Jerusalem, under the supervision of Prof. Dafna Shahaf.

## Project structure
The project consists of two milestones, each of which uses a different data, and a different type of examination and analysis.
In Milestone #1, we were dealing with plot summaries, and tried to find differences in them. In Milestone #2 we analyze billions of Hollywood & Bollywood movies subtitles, and with the help of an emotional analysis package we tried to test whether some of the dramatic effect of Bollywood was created through dramatic words and through multiple silences (see below).

## Milestone #1
We using [this](https://www.kaggle.com/rounakbanik/the-movies-dataset) and [that](https://github.com/BollywoodData/Bollywood-Data) databases, which contain a huge amount of data about Hollywood and Bollywood movies, and especially plots of the movies. We did stemming, removed stopwords and finding keywords, entered these words into the word-cloud software, which created for us word clouds, from which can be distinguished found some evidence of the profound cultural differences between the Indian society and its film industry, and the American one. You can watch the full milestone and the details of the results right [here](https://docs.google.com/presentation/d/1KKxKNOeBRdmZgX_qUiEZqBcHoxScGFualfpLHDHDVAg/edit?usp=sharing).

## Milestone #2
In this milestone we tried to build an emotional and silence timeline, to see whether interesting trends could be identified. The method for the emotional timeline creation was:

- Getting subtitles using crawler. [Here](https://drive.google.com/drive/folders/1d96FzyqGi20fBvOuVJl8XXg4LUJsEd2Z) and [here](https://drive.google.com/drive/folders/1RtnPfNNa2bcTfXPfH3ZDTJrN5_iBQOTU) you can see the subtitles obtained using the crawler.
- Parsing each file, and for every subtitle - finding its percentage in the movie and its emotional rank.
- Defining an emotional “peak”.
- Creating an integrative emotional timeline, based on an average number of emotional "peaks" per unit of time.

The method for the silence timeline creation was similar: in subtitle files, the exact time of each subtitle is noted. We calculated the difference between the end time of each subtitle and the time of the next subtitle - this is the time of silence.
Again, we divided each film to percentages and found how many silence “peaks” (== silence of more than five seconds) each percentage contains. After that, we calculated the average number of peaks. 

**We found really interesting and cool things. [Here](https://docs.google.com/presentation/d/1R-tbiFE6VO4HuTHPJJz7GieSk3MhdVkuNG7904N0k0Q/edit?usp=sharing) you can view the details of the results (and some really cool GIF's of the artist Eran Mendel!).**

A technical and detailed summary of the project (in Hebrew) can be found [here](https://docs.google.com/document/d/1IXjdRqUyF6k394ISiknMfIBmFOPCBfwl2-r8-n6rGjI/edit?usp=sharing).

## Code structure and files
Like the project itself, the code divided to two folders for each milestone. The code is documented quite well, however in the following lines you can find a general description of it.

```Milestone 1``` folder contains two files (```HolywoodData.py```, ```BolywoodData.py```), one for each film's industry. Each file disassembles all industry plots files into a long list of words, stems it, removes stop words, and writes a new file containing those words. A word-cloud was later produced from this file. In addition, it contains two files that contain the data - movie plots for each industry.

```Milestone 2``` folder contains the following files: 

- ```subtitles_parser.py``` is basically a smart parser for the emotional analysis part of this milestone. This file processes a subtitle file and creates from it two arrays of the same length - one contains a sequence of emotional score given by Vader package, and the other contains for each of these scores what percentage of the film it is in. The percentage is calculated according to the average time between the start time of the subtitle and its end time. 
- ```silence_calculator.py``` does the same thing for the silence timeline. The silences were identified by the differences between the end of one subtitle and the beginning of the next subtitle.
- ```count_list_creator.py``` contains two functions, one for each timeline. The function accepts the arrays created by the files ```subtitles_parser.py``` and  ```silence_calculator.py```, and according to a peak threshold defined for each timeline, it counts how many peaks there are in each percentile in the movie, thus normalizing the data to one thousand percent array for each movie, each cell in the array contains the amount of "peaks" in that percentage.
- ```bolly_holly_main.py``` uses the files described above to parse and analyze the subtitles, and exports a csv file with one score/silence array per industry





