library(tidytext)
library(dplyr)
library(stringr)
library(wordcloud)

library(ggplot2)

path = "./python/"
train = read.delim(paste0(path, "train.tsv"), header = FALSE, sep = " ", quote = "")
test = read.delim(paste0(path, "test.tsv"), header = FALSE, sep = " ", quote = "")

#train_df = data_frame(word = train$V1, type = train$V2)
#train_df$word <- as.character(train_df$word)

# svm
library(e1071)
library(caret)
train_ids <- sample(nrow(train), nrow(train)*0.7)
svm.train <- train[train_ids,] # 70%
svm.test <- train[-train_ids,] # 30%
#svm.train <- train
#svm.test <- test
svm_model <- svm(V52 ~ V2+V3+V4+V5+V6+V7+V8+V9+V10+V11+V12+V13+V14+V15+V16+V17+V18+V19+V20+V21+V22+V23+V24+V25+V26+V27+V28+V29+V30+V31+V32+V33+V34+V35+V36+V37+V38+V39+V40+V41+V42+V43+V44+V45+V46+V47+V48+V49+V50+V51, data=svm.train)
svm.predict <- predict(svm_model, svm.test)

confusionMatrix(svm.predict, svm.test$V52)

write.table(paste(svm.test$V52, svm.predict, sep = "\t"), file = "glove.svm.results", quote = FALSE, row.names = FALSE, col.names = FALSE)

# cat glove.svm.results | tr '\t' ' ' | perl -ne '{chomp;s/\r//g;print $_,"\n";}' | perl connlleval.pl

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
