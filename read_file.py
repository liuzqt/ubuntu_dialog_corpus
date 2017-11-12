# encoding: utf-8

'''

@author: ZiqiLiu


@file: read_file.py

@time: 2017/11/11 下午3:24

@desc:
'''
import codecs

def read_f(fname):
    with codecs.open(fname, 'r', 'utf-8') as f:
        dialog = [line.strip().split('\t')[-1] for line in f]
    return dialog
