# coding=UTF-8
import codecs
import re
import os
import tensorflow as tf

_PAD = "_PAD"
_GO = "_GO"
_EOS = "_EOS"
_UNK = "_UNK"
_NUM = "_NUM"
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3
NUM_ID = 4

def basic_target_tokenizer(line):
    sentence = []
    line = line.strip()
    if line == "null":
        sentence.append("null")
    elif line == "Question":
        sentence.append("Question")
    elif line == "question":
        sentence.append("Question")
    else:
        sentence = re.split(" ", line)
        # m = re.findall(r'(\w*[\.0-9]+)\w*', line)
        # index = []
        # for int in m:
        #     i = line.find(int)
        #     index.append([i, len(int), int])
        # j = 0
        # while True:
        #     if j < len(line):
        #         for ix in index:
        #             if j == ix[0]:
        #                 j = j + ix[1]
        #                 sentence.append(ix[2])
        #         if j < len(line):
        #             sentence.append(line[j])
        #             j = j + 1
        #         else:
        #             break
        #     else:
        #         break
    return sentence

def basic_source_tokenizer(line):
    line = line.replace(",", " ").replace(".", " ").replace("?", " ")
    line = line.strip()
    regex = ",|，|\\s+"
    regex1 = r'(\w*[\.0-9]+)\w*'
    sentence = re.split(regex, line)
    rs = []
    for word in sentence:
        if re.match(regex1, word):
            rs.append(_NUM)
        else:
            rs.append(word)
    return rs

def read_data(filename,flag):
    sentences = []
    with codecs.open(filename, "r", "UTF-8") as f:
        for line in f:
            if flag == "target":
                sentence = basic_target_tokenizer(line)
            else:
                sentence = basic_source_tokenizer(line)
            sentences.append(sentence)
    return sentences

def create_vocabulary(vocabulary_path,filename,flag, max_vocabulary_size):
    vocab = {}
    sentences = read_data(filename, flag)
    for sentence in sentences:
        for word in sentence:
            if word in vocab:
                vocab[word] += 1
            else:
                vocab[word] = 1
    vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)

    if len(vocab_list) > max_vocabulary_size:
        vocab_list = vocab_list[:max_vocabulary_size]

    with codecs.open(vocabulary_path, "w", "UTF-8") as f:
        for word in vocab_list:
            f.write(word+"\n")

def initialize_vocabulary(vocabulary_path):
    rev_vocab = []
    with codecs.open(vocabulary_path, "r", "UTF-8") as f:
        for line in f:
            line = line.strip()
            rev_vocab.append(line)
    vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
    return vocab, rev_vocab

def sentence_to_id(sentence,vocabulary,flag):
    if flag == "target":
        s = basic_target_tokenizer(sentence)
    else:
        s = basic_source_tokenizer(sentence)
    sentence_id = []
    for word in s:
        word_id = vocabulary.get(word, UNK_ID)
        sentence_id.append(word_id)
    return sentence_id

def data_to_id(data_path, target_path, vocabulary_path, flag):
    vocab, _ = initialize_vocabulary(vocabulary_path)
    tokens_file = codecs.open(target_path, "w", "UTF-8")
    with codecs.open(data_path, "r", "UTF-8") as data_file:
        for line in data_file:
            sentence_id = sentence_to_id(line, vocab, flag)
            for s_id in sentence_id:
                tokens_file.write(str(s_id) + " ")
            tokens_file.write("\n")

def prepare_data(data_path, from_train_path, to_train_path, from_dev_path, to_dev_path, from_vocabulary_size, to_vocabulary_size):
    to_vocab_path = os.path.join(data_path, "vocab%d.to" % to_vocabulary_size)
    from_vocab_path = os.path.join(data_path, "vocab%d.from" % from_vocabulary_size)
    create_vocabulary(to_vocab_path, to_train_path, "target", to_vocabulary_size)
    create_vocabulary(from_vocab_path, from_train_path, "source", from_vocabulary_size)

    # Create token ids for the train data
    to_train_ids_path = to_train_path + (".ids%d" % to_vocabulary_size)
    from_train_ids_path = from_train_path + (".ids%d" % from_vocabulary_size)
    data_to_id(to_train_path, to_train_ids_path, to_vocab_path, "target")
    data_to_id(from_train_path, from_train_ids_path, from_vocab_path, "source")

    # Create token ids for the development data.
    to_dev_ids_path = to_dev_path + (".ids%d" % to_vocabulary_size)
    from_dev_ids_path = from_dev_path + (".ids%d" % from_vocabulary_size)
    data_to_id(to_dev_path, to_dev_ids_path, to_vocab_path, "target")
    data_to_id(from_train_path, from_dev_ids_path, from_vocab_path, "source")

    return (from_train_ids_path, to_train_ids_path,
            from_dev_ids_path, to_dev_ids_path,
            from_vocab_path, to_vocab_path)