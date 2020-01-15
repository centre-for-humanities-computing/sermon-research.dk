# coding=utf-8

"""
Modified from an earlier script in the shared folder.
I think that was written by Kristoffer?
"""

import os, re
import docx2txt, textract
import pandas as pd

def list_files(dirpath):
    """
    Walk all files in directory 'dir' and subdirectories
    """
    r = []
    for root, dirs, files in os.walk(dirpath):
        for name in files:
            r.append(os.path.join(root, name))
    return r

# denoise fnames
pattern = re.compile("~")
path = "../data/PRÆDIKENER_RENSET"
fnames = sorted(list_files(path))
errors = []
clean_fnames = []
for i, fname in enumerate(fnames):
    tmp = fname.split("/")[-1]
    if pattern.match(tmp):
        errors.append(i)
    else:
        clean_fnames.append(fname)

# classify file type and remove metadata
clean_fnames.pop(0)
clean_fnames.pop(0)
data = []
pat1 = re.compile(r"% \S+")
pat2 = re.compile(r"\n+")
i = 0
for fname in clean_fnames:
    print("file {}".format(i))
    i += 1
    filetype = fname.split(".")[-1]
    if filetype == "doc":
        text = textract.process(fname).decode('utf-8')
    elif filetype == "docx":
        text = docx2txt.process(fname)
    else:
        print(fname)# TODO read odt
    # remove metadata
    text = pat1.sub("", text)
    text = pat2.sub("\n", text)
    data.append([fname.split("/")[-1].split(".")[0], text])
    
df = pd.DataFrame(data)
df.columns = ["id", "content"]
df.to_csv("../data/content/content.dat", encoding='utf-8')
