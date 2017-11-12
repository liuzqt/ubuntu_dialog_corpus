# encoding: utf-8

'''

@author: ZiqiLiu


@file: predict_naive.py

@time: 2017/11/11 下午1:29

@desc:
'''

import sys
import codecs
import pickle
from nltk.tokenize import RegexpTokenizer

tk = RegexpTokenizer(r'\w\S+\w')

with open('keyword_processor.pkl', 'rb') as f:
    keyword_processor = pickle.load(f)

if __name__ == '__main__':
    assert len(sys.argv) > 1
    files = sys.argv[1:]
    for fi in files:
        with codecs.open(fi, 'r', 'utf-8') as f:
            raw = f.readlines()

            dialog = [line.strip().lower().split('\t')[-1] for line in raw]
            tokens = tk.tokenize(' '.join(dialog))
            keywords = [w for w in tokens if keyword_processor.has_keyword(w)]
        print('+' * 50)
        print('file:\t' + fi)
        print('-' * 30)
        print('raw dialog:')
        print(''.join(raw) + '\n')
        print('-' * 30)
        print('keywords:')
        print(keywords)
        print('+' * 50)
