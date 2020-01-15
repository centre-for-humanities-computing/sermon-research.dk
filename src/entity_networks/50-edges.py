import pandas as pd
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict

def character_pairings_in(l):
    """
    Function to create list of tuples of character pairings from extracted data

    This also (quite crudely) removes any Act or Scene divisions, which have all
    been tagged using an asterisk.
    """
    # Create list from Pandas DF
    #l = dataframe[0].tolist()
    # Create pairings from list
    l2 = [(l[i],l[i+1]) for i in range(len(l)-1)]
    # Remove all Act and Scene markers
    x = [[t for t in a if not '#' in t] for a in l2]
    # Keep only pairs of characters
    y = [row for row in x if len(row) > 1]
    # Create list of tuples
    character_pairings = [tuple(l) for l in y]

    return character_pairings

def create_edgelist_from(pairs):
    """
    Function to create edgelists for "speaking-in-turn" pairs

    Returns results in a way that will be useful in Gephi
    """
    # Create edgelist using defaultDict
    edges = defaultdict(int)
    for people in pairs:
        for personA in people:
            for personB in people:
                if personA < personB:
                    edges[personA + ",undirected," + personB] += 1

    # Create a dataframe from the defaultDict
    df = pd.DataFrame.from_dict(edges, orient='index')
    df.reset_index(level=0, inplace=True)

    # Split cell on comma into muliple columns
    split = (df['index'].str.split(',', expand=True).rename(columns=lambda x: f"col{x+1}"))

    # Merge these split columns with the 'weights' from the first df
    merged = split.join(df[0])

    # Rename columns for use in Gephi
    merged.columns = ["Source", "Type", "Target", "Weight"]

    return merged

# Read data
data = pd.read_csv("../data/gender/entities/all_ents.csv", sep="\t")
#w = data[data["køn"] == 2]
# Select subset
#subset = w[["fname", "Entity"]]
# Drop weird entries
#subset = subset[subset["fname"] != "Thumbs"]
# Group by sermon
grouped = pd.DataFrame(data.groupby('fname')['Entity'].apply(lambda x: x.str.cat(sep=', ')))

# Join as lists
l = [''.join(row) for row in grouped["Entity"]]

# Tokenize strings
#tokenizer = RegexpTokenizer(r'\w+')
#w = [tokenizer.tokenize(s) for s in l]
w = [[x.strip() for x in my_string.split(',')] for my_string in l]
# Create pairs
pairs = [character_pairings_in(p) for p in w]

# Create edgelist
edgelist = [item for sublist in pairs for item in sublist]
final_edges = create_edgelist_from(edgelist)

# Save
final_edges.to_csv("../data/gender/edges/all_edges.csv", sep=",", index=False, header=True)
