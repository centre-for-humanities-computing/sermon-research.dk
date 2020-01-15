import pandas as pd

"""
Read in metadata and data
"""

metadata = pd.read_excel("in/Joined_Meta.xlsx", sep=";")
data = pd.read_csv("in/content.dat")

"""
Filter
"""

m = metadata[metadata["køn"] == 1]
f = metadata[metadata["køn"] == 2]

male_corpus = data[data["id"].isin(list(m["ID-dok"]))]
female_corpus = data[data["id"].isin(list(f["ID-dok"]))]

"""
Save
"""
male_corpus.to_csv("../m/in/content.dat")
female_corpus.to_csv("../f/in/content.dat")
