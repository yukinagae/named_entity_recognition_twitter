#
# TODO description
#

# TODO imports
# import logging
# import timeit
import datetime

# train data
train_filepath = "../data/dev"

# word vectors
wv_path = "../glove.6B/"
wv_filename = "glove.6B.50d.txt"
wv_filepath = wv_path + wv_filename

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

zero_list = ["0"] * 50

# read train data
with open('dev.tsv', 'w') as out_f:
    with open(train_filepath) as in_f:
        for line in in_f:
            words = line.split()
            if len(words) == 2: # TODO should be two
                word = words[0]
                label = words[1]
                if word.lower() in dict:
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





