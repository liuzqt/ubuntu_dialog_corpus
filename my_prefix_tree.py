# encoding: utf-8

'''

@author: ZiqiLiu


@file: my_prefix_tree.py

@time: 2017/11/11 下午4:00

@desc:
'''


class PrefixTree(object):
    def __init__(self):
        self.charset = {}
        self.end = False

    def update(self, word):
        if len(word) == 0:
            self.end = True
            return
        if word[0] not in self.charset:
            self.charset[word[0]] = PrefixTree()
        self.charset[word[0]].update(word[1:])

    def has_keyword(self, word):
        # reach the end of a keyword
        if len(self.charset) == 0:
            return True
        # word end but not reach the each of any keyword
        if len(word) == 0:
            return self.end
        if word[0] in self.charset:
            return self.charset[word[0]].has_keyword(word[1:])
        else:
            return False


if __name__ == '__main__':
    with open('top_words', 'r') as f:
        words = [line.strip().split()[0] for line in f]
    tree = PrefixTree()
    for w in words:
        tree.update(w)
    print(tree.has_keyword('partition'))
