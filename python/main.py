#
# add word vectors to train file
#
import datetime
import os
current_file_dir = os.path.dirname(os.path.abspath(__file__))

######################################################################################
# setting
######################################################################################
# train data
train_filedir = current_file_dir + "/../data/"
train_filename = "train.tsv"

# word vectors
wv_filedir = current_file_dir + "/../glove.6B/"
wv_filename = "glove.6B.50d.txt"

# output file
out_filedir = current_file_dir + "/"
out_filename = "aloha.tsv"

# the number of vectors
vector_for_one_word = 50

# n-gram
ngram = 1 # TODO can be changed to 1 or 3 or 5
######################################################################################

# concatinate file directory and filename, and get filepath
train_filepath = train_filedir + train_filename
wv_filepath = wv_filedir + wv_filename
out_filepath = out_filedir + out_filename

# start
print ("[start]  " + unicode(datetime.datetime.now()))

# dictionary
# {"good": ['-0.35586'..'0.92771']}
dict = {}
with open(wv_filepath) as wvs:
    for vs in wvs:
        v = vs.split()
        dict[v[0]] = v[1:]

# print dict["good"]

zero_list = ["0"] * vector_for_one_word

# read train data
with open(out_filepath, 'w') as out_f:
    with open(train_filepath) as in_f:
        for line in in_f:
            words = line.split()
            if len(words) == 2: # TODO should be two
                word = words[0]
                label = words[1]
                if (word != "BOS" and word != "EOS") and word.lower() in dict:
                    out_f.write(word)
                    out_f.write(" ")
                    out_f.write(" ".join(dict[word.lower()]))
                    out_f.write(" ")
                    out_f.write(label)
                else:
                    out_f.write(word)
                    out_f.write(" ")
                    out_f.write(" ".join(zero_list))
                    out_f.write(" ")
                    out_f.write(label)
                out_f.write("\n")


# end
print ("[finish] " + unicode(datetime.datetime.now()))
