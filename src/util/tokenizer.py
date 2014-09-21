import re
from util import isnum

# Utility function to return a list of all words that are have a length greater than a specified number of characters.
# @param text The text that must be split in to words.
# @param minWordReturnSize The minimum no of characters a word must have to be included.
def separatewords(text, minWordReturnSize):
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for singleWord in splitter.split(text):
        currWord = singleWord.strip().lower()
        # leave numbers in phrase, but don't count as words, since they tend to invlate scores of their phrases
        if len(currWord) > minWordReturnSize and currWord != '' and not isnum(currWord): 
            words.append(currWord)
    return words

# Utility function to return a list of sentences.
# @param text The text that must be split in to sentences.
def splitSentences(text):
    sentenceDelimiters = re.compile(u'[.!?,;:\t\\-\\"\\(\\)\\\'\u2019\u2013]')
    sentenceList = sentenceDelimiters.split(text)
    return sentenceList
