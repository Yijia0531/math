import codecs
import collections

def read_data(filename):
    sentences=[]
    with codecs.open(filename,'r','utf-8') as f:
        for line in f:
            sentence = []
            line = line.strip()
            if line == 'null':
                sentence.append('null')
            else:
                sentence = [char for char in line]
            sentences.append(sentence)
    return sentences

def get_word2id(train_sentences):
    chars=[]
    for sentence in train_sentences:
        for char in sentence:
            chars.append(char)
    chars.append('unk')
    c=collections.Counter(chars)
    word2id=dict([(key,i) for i,key in enumerate(c.keys())])
    return word2id

def sentences2id(train_sentences,word2id):
    sentences_id=[]
    for sentence in train_sentences:
        sentence_id=[]
        for char in sentence:
            if word2id.get(char) is not None:
                sentence_id.append(word2id[char])
            else:
                sentence_id.append(word2id['unk'])
        sentences_id.append(sentence_id)
    return sentences_id



if __name__ == '__main__':
    d=read_data('target_file')
    word2id=get_word2id(d)
    s2id=sentences2id(d,word2id)
    print(s2id[0])