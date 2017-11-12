# encoding: utf-8

'''

@author: ZiqiLiu


@file: test.py

@time: 2017/11/11 下午7:40

@desc:
'''

import nltk
from gensim import corpora, models

raw = [['a', 'b', 'a', 'a'], ['b', 'c']]
dictionary = corpora.Dictionary(raw)

corpus = [dictionary.doc2bow(text) for text in raw]
model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=2)

keywords = sorted(model.get_topic_terms(1), key=lambda x: x[1], reverse=True)[
           :5]
keywords = [dictionary[i[0]] for i in keywords]

print(keywords)
