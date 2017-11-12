# encoding: utf-8

'''

@author: ZiqiLiu


@file: word_count.py

@time: 2017/11/11 上午2:58

@desc:
'''

import codecs
from collections import Counter
import pickle
from tqdm import tqdm
import re
from flashtext import KeywordProcessor
from my_prefix_tree import PrefixTree

with open('stopword_for_wc', 'r') as f:
    stop_word_addon = [line.strip() for line in f]

split_pattern = re.compile(r'\s+')

word_counter = Counter()

with codecs.open('whole_dialogs', 'r', 'utf-8') as f:
    for line in tqdm(f):
        word_list = split_pattern.split(line)
        word_counter.update(word_list)
for stop_w in stop_word_addon:
    del word_counter[stop_w]
top_words = sorted(word_counter.items(), key=lambda a: a[1], reverse=True)[:5000]

with codecs.open('wc', 'w', 'utf-8') as out:
    for key, value in top_words:
        out.write('%s\t%d\n' % (key, value))

keyword_processer = PrefixTree()
for w in top_words:
    keyword_processer.update(w[0])

with open('keyword_processor.pkl', 'wb') as f:
    pickle.dump(keyword_processer, f)
