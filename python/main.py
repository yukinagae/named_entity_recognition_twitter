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
wv_filename = "glove.twitter.27B.50d.txt"

# output file
out_filedir = current_file_dir + "/"
out_filename = "train_twitter_5_gram.tsv"

# the number of vectors
vector_for_one_word = 50

# n-gram
ngram = 2 # TODO can be changed to 1 or 3 or 5
# 0 => unigram
# 1 => trigram
# 2 => 5-gram
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

sentences = []

with open(train_filepath) as in_f:
    for line in in_f:
        words = line.split()
        if len(words) == 2: # should be two
            word = words[0]
            label = words[1]
            sentences.append((word, label))

# print sentences

asis = []

index = 0
while index < len(sentences):
    if sentences[index][0] == "BOS":
        asi = []
        while sentences[index][0] != "EOS":
            asi.append(sentences[index])
            index += 1
        asi.append(sentences[index])
        asis.append(asi)
        index += 1

def get_vectors(d, a, index, ngram = 0):

    if index < 0 or index >= len(a):
        return zero_list

    before = []
    after = []

    if ngram > 0:
        for n in range(1, ngram+1):
            before = around_vectors(d, a, index - n) + before # TODO
            after  = after + around_vectors(d, a, index + n)

    word = a[index][0]

    if (word != "BOS" and word != "EOS") and word.lower() in dict:
        return before + d[word.lower()] + after
    else:
        return before + zero_list + after

def around_vectors(d, a, index):
    if index < 0 or index >= len(a):
        return zero_list

    word = a[index][0]

    if (word != "BOS" and word != "EOS") and word.lower() in dict:
        return d[word.lower()]
    else:
        return zero_list


# read train data
with open(out_filepath, 'w') as out_f:
    for asi in asis:
        for i, a in enumerate(asi, start=0):
            word = a[0]
            label = a[1]
            out_f.write(word)
            out_f.write(" ")
            #  n-gram
            vectors = get_vectors(dict, asi, i, ngram)
            out_f.write(" ".join(vectors))
            out_f.write(" ")
            out_f.write(label)
            out_f.write("\n")

# end
print ("[finish] " + unicode(datetime.datetime.now()))
