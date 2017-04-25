library(tidytext)
library(dplyr)
library(stringr)
library(wordcloud)

library(ggplot2)

path = "./data/"
train = read.delim(paste0(path, "train.tsv"), header = FALSE, sep = " ")
train_df = data_frame(word = train$V1, type = train$V2)
train_df$word <- as.character(train_df$word)

# GloVe
wv_path = "/Applications/r_workspace/named_entity_recognition_twitter/glove.6B/"
wv_filename = "glove.6B.50d.txt"
wv = read.delim(paste0(wv_path, wv_filename), header = FALSE, sep = " ")

# NLP
# see: https://github.com/statsmaths/coreNLP
devtools::install_github("statsmaths/coreNLP")
coreNLP::downloadCoreNLP()
library(coreNLP)
initCoreNLP()

output = annotateString(train_df$word[1:100])
getToken(output)[,c(1:3,7:8)]

#

train_df %>% mutate(tweet = cumsum(str_detect(word, regex("^BOS"))))

train_df %>% count(type) %>% with(wordcloud(type, n, max.words = 100))

train_df %>% count(type, sort=TRUE) %>%
             mutate(type = reorder(type, n)) %>%
             ggplot(aes(type, n)) + geom_col() + xlab(NULL) + coord_flip()

#levels(train_df$word) <- tolower(levels(train_df$word))

#filtered_train_df <- train_df %>%
#                     filter(word != "bos") %>%
#                     filter(word != "eos") %>%
#                     filter(!str_detect(word, regex("^@"))) %>%
#                     filter(!str_detect(word, regex("^http"))) %>%
#                     anti_join(stop_words) %>%
#                     filter(word != ".") %>%
#                     filter(word != "...") %>%
#                     filter(word != ",") %>%
#                     filter(word != ":") %>%
#                     filter(word != "?") %>%
#                     filter(word != "!")

#filtered_train_df %>% count(word, sort=TRUE)

#filtered_train_df %>% count(word) %>% with(wordcloud(word, n, max.words = 100))
