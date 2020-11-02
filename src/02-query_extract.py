"""
Extract context of target query words and related
verbs on a sentence-by-sentence basis.
"""

import ast
import pandas as pd

def str2list(s):
    return ast.literal_eval(s)

# Read query terms
with open("in/queryterms.txt", "r") as f:
    terms = f.read().split()

# Read in POS tagged data
DF = pd.read_csv("in/content_POS.dat", header = 0, index_col = None)
content = DF["POS"].tolist()
fnames = DF["id"].tolist()

# Extract pronoun-verb pairs
for idx in range(len(content)):
    print(idx)
    text = str2list(content[idx])
    reponse = []
    # For each sentence, cycle through pairs of words
    for i, sent in enumerate(text):
        verbs, prons = [], []
        for j, pair in enumerate(sent):
            # If one of those word is a pronoun, extract this
            for term in terms:
                if term == pair[0]:
                    prons.append((j,pair[0]))
                    # If next word is a verb, extract that, too
                    for k, pair in enumerate(sent):
                        if pair[1] == "VERB":
                            verbs.append((k,(pair[0])))
                        continue
                    # Create an entry with filename, pronoun, associated verbs
                    entry = [fnames[idx], i, prons, sorted(list(set(verbs)))]
                    reponse.append(entry)

    # Create a dataframe from all entries
    if reponse:
        df = pd.DataFrame(reponse)
        df.columns = ["id", "sentence_id","pronouns","verbs"]
        idx_list = []
        for ii in list(set(df['sentence_id'])):
            idx_list.append(list(df['sentence_id']).index(ii))
        df = df.iloc[sorted(idx_list),:].reset_index(drop = True)
        if idx == 0:
            DFq = df
        else:
            DFq = pd.concat([DFq, df]).reset_index(drop = True)

# Save dataframe as CSV
print(DFq.shape)
DFq.to_csv("in/content_QUERYTERMS.dat", index = False)
