from markov import generate_chain, generate_message
import random
import sys

datafile = sys.argv[1]

t, s = generate_chain(datafile)

for i in range(100):
    print(generate_message(t, s))