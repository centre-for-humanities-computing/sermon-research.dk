"""
Join up frequency and PMI score.
"""

import pandas as pd
from collections import Counter

# Read in the relevant data
data = pd.read_csv("in/content_FULL.dat")
data["id"] = data["id"].str.strip()
# Read in pronoun-verb PMI data
verbs_all = pd.read_csv("out/pmi.dat")

# Create an empty counter
counts_all = Counter()
# Update counter based on words per sermon
for row in data["content"]:
    counts_all.update(word.strip('.,?!"\'').lower() for word in row.split())

# Filter out only the verbs that appear in the PMI results
filtered_d = dict((k, counts_all[k]) for k in verbs_all["word"] if k in counts_all)
# Count frequency of that verb across all sermons
verbs_all["frequency"] = list(filtered_d.values())

# Create dataframe; save to csv
verbs_all = verbs_all[["word", "frequency", "han", "ham", "hun", "hende"]]
verbs_all.to_csv("out/freq+PMI.csv")
