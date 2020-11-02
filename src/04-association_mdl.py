"""
Extract the top associations, based on raw frequency
"""

import pandas as pd
from collections import Counter

def getallist(l,match):
    return [i for i, x in enumerate(l) if x == match]

# Read in previous pair associations
df = pd.read_csv("in/associations.dat", header = 0, index_col = None)
source = df["source"].tolist()

# preprocessing target
target = [w.lower() for w in df["target"].tolist()]


#dist_total = Counter(target)

#Create empty lists for results and for pronoun, id tuples
res = []
pr_source = []

# Define max number of top values to extract
n = 25
for pron in sorted(set(source)):
    idxs = getallist(source,pron)
    pr_source.append(len(idxs))
    print("{} occurs {}".format(pron, len(idxs)))
    wordlist = [target[idx] for idx in idxs]
    dist = Counter(wordlist)
    res.append([pron, dist.most_common(n)])

# Create temp list for data
TMP = []
colnames = [l[0] for l in res]
print(pr_source)
for i in range(n):
    tmp = []
    for l in res:
        t = l[1][i]
        print(t)
        tmp.append(t)
    TMP.append(tmp)

# Create dataframe and save to DAT
df = pd.DataFrame(TMP)
df.columns = [l[0] for l in res]
df.to_csv("out/assocations_{}.dat".format(n), index = False)
