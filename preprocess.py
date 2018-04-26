import re
import sys

def preprocess(infile, outfile):
    #punctuation = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    punctuation = "!\"#$%&()*,/:;<>?@[\]^_`{|}~"
    strip_punctuation = str.maketrans('', '', punctuation)
    newline_punctuation = "."
    with open(infile, "r", encoding="utf-8") as f:
        with open(outfile, "w", encoding="utf-8") as s:
            for line in f:
                line = re.sub(r'https?:\S+', '', line)
                line = re.sub(r'<:\S+>', '', line)
                line = line.translate(strip_punctuation)
                #line = line.lower()
                lines = line.split(newline_punctuation)
                for l in lines:
                    l = l.strip()
                    if l:
                        s.write(l)
                        s.write('\n')

infile = sys.argv[1]
outfile = sys.argv[2]
preprocess(infile, outfile)
