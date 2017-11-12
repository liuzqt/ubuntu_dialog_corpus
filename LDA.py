# encoding: utf-8

'''

@author: ZiqiLiu


@file: LDA.py

@time: 2017/11/11 下午1:34

@desc:
'''

from gensim import corpora, models
import codecs
from tqdm import tqdm

print('loading data...')
with codecs.open('whole_dialogs_stem', 'r', 'utf-8') as f:
    raw_corpus = [line.split() for line in f]
print("%d dialogs loaded." % len(raw_corpus))

print('begin training...')
dictionary = corpora.Dictionary(raw_corpus)
dictionary.filter_extremes(keep_n=200000)

corpus = [dictionary.doc2bow(text) for text in raw_corpus]
model = models.LdaMulticore(corpus, id2word=dictionary, workers=3,
                            num_topics=50)

dictionary.save('ubuntu.dict')
model.save('ubuntu.lda')

print(
    'training finished. Model saved in ubuntu.lda. Dictionary saved in ubuntu.dic')
