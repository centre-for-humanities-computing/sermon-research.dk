"""
Calculate PMI between pronoun-verb combinations
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

# Read in association data
df = pd.read_csv("in/associations.dat", header = 0, index_col = None)
source = df["source"].tolist()# pronouns
# To lowercase
target = [w.lower() for w in df["target"].tolist()]# verbs

# verb-pronoun matrix
row = sorted(list(set(target)))
column = ["han","ham","hun","hende"]
X = wlist2matrix(row, column)

# Read in original sermon data and tokenize
content = pd.read_csv("in/content_ALL.dat", header = 0, index_col = None)["content"].tolist()
tmp = []
for text in content:
    tokens = [token.lower() for token in tokenize(text)]
    tmp.append(tokens)

# Create a word list, calculate number of sermons, and number of words
wlist = flatten(tmp)
total = len(wlist)
content_wdict = wcount(wlist)

# Calculate PMI for pronoun-verb pairs based on all sermons
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

# Create deataframe of search terms and PIM results
df1 = pd.DataFrame(row)
df1.columns = ['word']
df2 = pd.DataFrame(M)
df2.columns = column
# Concatenate and save
pd.concat([df1, df2], axis = 1).to_csv("out/pmi.dat", index = False)
