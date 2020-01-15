"""
extract all pron-verb association
"""
import ast
import pandas as pd
import numpy as np

def str2list(s):
    return ast.literal_eval(s)

def getallis(l,match):
    return [i for i, x in enumerate(l) if x == match]

def sent2asso(row):
    """
    - keep order index in each association tuple for possible sorting
    """
    prons = str2list(row[2])
    verbs = str2list(row[3])
    target = [t[0] for t in verbs]# verb ids
    res = []
    for pron in prons:
        source = pron[0]
        dist = []
        for i in target:
            dist.append(np.abs(i - source))
            ii = getallis(dist, min(dist))
        for i in ii:
            res.append([pron, verbs[i]])
    return res

def sent2asso_df(row):
    """
    remove order index and write to word pair (target, source) dataframe
    """
    doc_id = str(row[0])
    sent_id = int(row[1])
    asso_list = sent2asso(row)
    res = []
    for asso in asso_list:
        res.append([doc_id, sent_id, asso[0][1],asso[1][1]])
    df = pd.DataFrame(res)
    df.columns = ["doc_id", "sent_id", "source", "target"]
    return df

df = pd.read_csv("../data/content/content_query.dat", header = 0, index_col = None)

for idx in range(df.shape[0]):
    print()
    print("sent {} of {}".format(idx,df.shape[0]))
    row = df.iloc[idx,:]
    try:
        asso = sent2asso_df(row)
        if idx == 0:
            df_asso = asso
        else:
            df_asso = pd.concat([df_asso,asso]).reset_index(drop = True)
    except:
        continue

df_asso.to_csv("associations.dat", index = False)
