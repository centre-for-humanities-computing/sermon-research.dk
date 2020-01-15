"""
extract context of query words

"""

import ast
import pandas as pd

def str2list(s):
    return ast.literal_eval(s)

# query terms
#with open("queryterms.txt", "r") as f:
#    terms = f.read().split()

# data
DF = pd.read_csv("../data/content/content_pos.dat", header = 0, index_col = None)
content = DF["POS"].tolist()
fnames = DF["id"].tolist()

# get pronoun verb combinations
for idx in range(len(content)):
    print(idx)
    text = str2list(content[idx])
    reponse = []
    for i, sent in enumerate(text):
        verbs, prons = [], []
            if pair[1] == "NOUN":
                verbs.append((j,(pair[0])))
                continue
            entry = [fnames[idx], i, sorted(list(set(verbs)))]
            reponse.append(entry)

    if reponse:
        df = pd.DataFrame(reponse)
        df.columns = ["id", "sentence_id","noun"]
        idx_list = []
        for ii in list(set(df['sentence_id'])):
            idx_list.append(list(df['sentence_id']).index(ii))
        df = df.iloc[sorted(idx_list),:].reset_index(drop = True)
        if idx == 0:
            DFq = df
        else:
            DFq = pd.concat([DFq, df]).reset_index(drop = True)

print(DFq.shape)
DFq["noun"].value_counts().to_csv("../data/content/content_query.dat", index = False)