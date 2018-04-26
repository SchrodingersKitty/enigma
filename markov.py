import random

def generate_chain(filename):
    transitions = {}
    start_words = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            previous = ''
            for word in line.split():
                #word = word.lower()
                if word not in transitions:
                    transitions[word] = []
                if previous:
                    transitions[previous].append(word)
                else:
                    start_words.append(word)
                previous = word
            if previous:
                transitions[previous].append('\n')
    return transitions, start_words

def generate_message(transitions, start_words):
    message = ""
    word = random.choice(start_words)
    while word != '\n':
        message += word + ' '
        word = random.choice(transitions[word])
    return message
