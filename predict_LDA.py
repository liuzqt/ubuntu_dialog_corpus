# encoding: utf-8

'''

@author: ZiqiLiu


@file: LDA.py

@time: 2017/11/11 下午1:34

@desc:
'''

from gensim import corpora, models
import codecs
import sys
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import pickle
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

tk = RegexpTokenizer(r'\w\S+\w')

en_stop = get_stop_words('en')

dictionary = corpora.Dictionary.load('ubuntu.dict')
model = models.LdaMulticore.load('ubuntu.lda')

with open('stopword_processor.pkl', 'rb') as f:
    stopword_processor = pickle.load(f)

if __name__ == '__main__':
    assert len(sys.argv) > 1
    files = sys.argv[1:]
    for fi in files:
        with codecs.open(fi, 'r', 'utf-8') as f:
            raw = f.readlines()

        dialog = [line.strip().lower().split('\t')[-1] for line in raw]
        tokens = tk.tokenize(' '.join(dialog))
        stem_tokens = [stemmer.stem(w) for w in tokens]
        corpus = dictionary.doc2bow(stopword_processor.replace_keywords(
            ' '.join(tokens)).split())
        # get the topic with highest prob
        topic = sorted(model[corpus], key=lambda x: x[1], reverse=True)[:15]
        potential_topic = topic
        topic = topic[0][0]
        # list of (index, prob)

        LDA_keywords = sorted(model.get_topic_terms(topic), key=lambda x: x[1],
                              reverse=True)[:5]
        LDA_keywords = set([dictionary[i[0]] for i in LDA_keywords])

        # see if words in dialog appear in topic keyword
        filtered_keyword = set(w for w in stem_tokens if w in LDA_keywords)

        print('+' * 80)
        print()
        print('file:\t' + fi)
        print('-' * 50)
        print('raw dialog:')
        print(''.join(raw) + '\n')
        print('-' * 50)
        print('LDA predict:')
        print('\npotential topic')
        print(potential_topic)
        print('\npotential keywords:')
        print(model.print_topic(topic))
        print('\nfiltered keywords:')
        print(filtered_keyword)
        print()
        print('+' * 80)
