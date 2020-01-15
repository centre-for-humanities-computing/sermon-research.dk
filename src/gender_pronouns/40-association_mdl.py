"""

- relative frequency
- lemmatize

"""
import pandas as pd
from collections import Counter

def getallis(l,match):
    return [i for i, x in enumerate(l) if x == match]

#def worddist(l):

df = pd.read_csv("associations.dat", header = 0, index_col = None)

source = df["source"].tolist()
# preprocessing target
target = [w.lower() for w in df["target"].tolist()]


dist_total = Counter(target)
res = []
n = 25# number of target maxs
pr_source = []
for pron in sorted(set(source)):
    idxs = getallis(source,pron)
    pr_source.append(len(idxs))
    print("{} occurs {}".format(pron, len(idxs)))
    wordlist = [target[idx] for idx in idxs]
    dist = Counter(wordlist)
    res.append([pron, dist.most_common(n)])

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


df = pd.DataFrame(TMP)
df.columns = [l[0] for l in res]
df.to_csv("assocations_{}.dat".format(n), index = False)
#print()
#print(df)
#print(dist_total)
