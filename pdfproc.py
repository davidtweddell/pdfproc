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
TEXT_OUTPUT = False

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

    # open the file and make a pdftotext.PDF object
    try:
        with open(item, "rb") as f:
            pdf = pdftotext.PDF(f)
    except IOError:
        print("could not read file {0}".format(fn))

    if DEBUG:
        print("Document {0} has {1} page(s).".format(bn,len(pdf)))

    # add the text representation to the list
    for i, page in enumerate(pdf):
        the_text.append(page)
        the_source.append(bn)
        the_pageid.append('{0}-{1}'.format(bn,i+1))

    # save as a text file
    if TEXT_OUTPUT:
        of = "{0}.txt".format(file_root)
        try:
            with open(of, "w") as f:
                f.write("\n\n".join(pdf))
        except IOError:
            print("could not write to {0}".format(of))


# convert to a dataframe and write out
df = pd.DataFrame()
df["SOURCEFILE"] = the_source
df["PAGE_ID"] = the_pageid
df["SUMMARY"] = the_text


# TODO: better file name??
output_file = "./text_from_pdf.csv"
df.to_csv(output_file, index=False)
print("Corpus consists of {0} texts written to file {1}.".format(len(the_text), output_file))