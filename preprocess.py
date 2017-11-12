# encoding: utf-8

'''

@author: ZiqiLiu


@file: preprocess.py

@time: 2017/11/11 上午1:56

@desc: combine all dialogs into one text file, retaining dialogs only
'''
from glob import glob
from tqdm import tqdm
import codecs
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from flashtext import KeywordProcessor
import pickle
import re
import os
from multiprocessing import Pool
import functools

files = glob('./dialogs/**/*.tsv')


# pattern1 = re.compile(r'[1-9\\.]+')
# pattern2 = re.compile(r'.+//.+')
# pattern3 = re.compile(r'\w+')
#
#
# def filter1(s):
#     return pattern1.match(s) and pattern2.match(s) and pattern3.match(s)



def processing(i, file_list):
    tk = RegexpTokenizer(r'\w\S+\w')

    # create English stop words list
    en_stop = get_stop_words('en')

    stopword_processor = KeywordProcessor()
    for w in en_stop:
        stopword_processor.add_keyword(w, ' ')

    with open('stopword_processor.pkl', 'wb') as f:
        pickle.dump(stopword_processor, f)

    p_stemmer = PorterStemmer()

    with codecs.open('whole_dialogs_stem_%d' % i, 'w', 'utf-8') as out:
        for fi in tqdm(file_list):
            with codecs.open(fi, 'r', 'utf-8') as f:
                sentences = [stopword_processor.replace_keywords(
                    line.strip().split('\t')[-1].lower()) for
                    line in f]
                words = functools.reduce(lambda x, y: x + y,
                                         map(tk.tokenize, sentences))
                words = map(p_stemmer.stem, words)
                out.write(' '.join(words) + '\n')


def div_list(l, n):
    length = len(l)
    t = length // n
    quaters = [t * i for i in range(0, n)]
    ran = range(0, n - 1)
    result = [l[quaters[i]:quaters[i + 1]] for i in ran]
    result.append(l[quaters[n - 1]:len(l)])
    return result


if __name__ == '__main__':
    process_num = 8
    p = Pool()
    div_files = div_list(files, process_num)
    for i in range(process_num):
        p.apply_async(processing, args=(
            i, div_files[i]))
    p.close()
    p.join()

    output_list = glob('./whole_dialogs_stem_*')
    for output in output_list:
        os.system('cat %s >> whole_dialogs_stem' % output)
        os.system('rm %s' % output)
