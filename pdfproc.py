import sys
import glob
import os
import pdftotext
import pandas as pd
import argparse





# ==============================================================================
# Main Program
# ==============================================================================
DEBUG = True
TEXT_OUTPUT = True

def getargs():
    p = argparse.ArgumentParser()
    p.add_argument("files", action='store', help="pdf files using filename globbing", nargs='*')
    arguments = p.parse_args()
    return arguments

args = getargs()
the_files = args.files
print("Found {0} file(s) to operate on.".format(len(the_files)))

# empty list to contain texts
the_text = []
the_pageid  = []
the_source = []

# iterate over the files
for item in the_files:

    # get the root filename and generate an outfile name (if saving to .txt)
    file_root = os.path.splitext(item)[0]
    bn = os.path.basename(item)
    bb = os.path.splitext(bn)[0]

    # open the file and make a pdftotext.PDF object
    try:
        with open(item, "rb") as f:
            pdf = pdftotext.PDF(f)
    except IOError:
        print(f"could not read file {f}")

    if DEBUG:
        print(f"Document {bn} has {len(pdf)} page(s).")

    # add the text representation to the list
    for i, page in enumerate(pdf):
        the_text.append(page)
        the_source.append(bn)
        the_pageid.append(f'{bn}-{i}')

    # save as a text file
    if TEXT_OUTPUT:
        of = f"converted-{bb}.txt"
        try:
            with open(of, "w") as f:
                f.write("\n\n".join(pdf))
        except IOError:
            print("could not write to {0}".format(of))

        print(f"Document {bn} was converted to text file {of}.")

# convert to a dataframe and write out
df = pd.DataFrame()
df["SOURCEFILE"] = the_source
df["PAGE_ID"] = the_pageid
df["SUMMARY"] = the_text


# TODO: better file name??
output_file = f"converted-{bb}.csv"
df.to_csv(output_file, index=False)
print(f"Corpus consists of {len(the_text)} texts written to file {output_file}.")
