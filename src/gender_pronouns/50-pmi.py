"""
point-wise mutual information between verb-pronoun combinations
"""
import re
import numpy as np
import pandas as pd
from collections import defaultdict

def getallis(l,match):
    """
    get all indices of match pattern in list
    """
    return [i for i, x in enumerate(l) if x == match]

def wcount(l):
    """
    Word counter for list of tokens
    """
    count = defaultdict(int)
    for w in l:
        count[w] += 1
    return count

def wlist2matrix(row, column):
    M = np.zeros((len(row), len(column)), dtype = int)
    wcounts = []
    for i, pron in enumerate(column):
        idxs = getallis(source,pron)
        wordlist = [target[idx] for idx in idxs]
        wdict = wcount(wordlist)
        for ii, word in enumerate(row):
            M[ii,i] = wdict[word]
    return M

def tokenize(s, nonum = True):
    if nonum:
        s = re.sub(r"\d+","",s)
    tokenizer = re.compile(r"\W+")
    return tokenizer.split(s)

flatten = lambda l: [item for sublist in l for item in sublist]

def pmi(w1,w2,w1w2):
    return np.log(w1w2/(w1*w2))

# data
df = pd.read_csv("in/associations.dat", header = 0, index_col = None)
source = df["source"].tolist()# pronouns
# casefold
target = [w.lower() for w in df["target"].tolist()]# verbs

# lemmatize --> CST

# verb-pronoun matrix
row = sorted(list(set(target)))
#column = sorted(list(set(source)))
column = ["han","ham","hun","hende"]# AA's order
X = wlist2matrix(row, column)

content = pd.read_csv("in/content.dat", header = 0, index_col = None)["content"].tolist()
tmp = []
for text in content:
    tokens = [token.lower() for token in tokenize(text)]
    tmp.append(tokens)

wlist = flatten(tmp)
total = len(wlist)
content_wdict = wcount(wlist)

M = np.zeros((len(row), len(column)), dtype = float)
for i, w1 in enumerate(row):
    pw1 = content_wdict[w1]/total
    for ii, w2 in enumerate(column):
        pw2 = content_wdict[w2]/total
        pw1w2 = X[i,ii]/total
        if (pw1w2 == 0.):
            M[i,ii] = 0.
        elif (pw1 == 0.):
            M[i,ii] = 0.
        elif (pw2 == 0.):
            M[i,ii] = 0.
        else:
            M[i,ii] = pmi(pw1,pw2,pw1w2)

df1 = pd.DataFrame(row)
df1.columns = ['word']
df2 = pd.DataFrame(M)
df2.columns = column
pd.concat([df1, df2], axis = 1).to_csv("out/pmi.dat", index = False)
