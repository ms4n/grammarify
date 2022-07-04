from transfer import transfer

import warnings

warnings.filterwarnings("ignore")


def grammar_corrector(incorrect_sentence):
    correct_sentence = transfer(incorrect_sentence, 1)
    if correct_sentence is not None:
        return next(iter(correct_sentence)).capitalize()
    else:
        return "No good quality corrections available!"


def formal_transfer(casual_sentence):
    formal_sentence = transfer(casual_sentence, 0)
    if formal_sentence is not None:
        return formal_sentence
    else:
        return "No good quality formal transfers available!"
