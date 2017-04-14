# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import defaultdict
from random import shuffle
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def normalizeLines(line, size=20):
    words = line.split()
    for i in range(0, len(words), size):
        yield words[i:i + size]

#Iterates a list of lines, tokenizes each line and returns a list of with
#the individual tokens
def getTokens(lines):
    badChars = u'0123456789«»()[]{}<>¡!¿?“”".,_:;'
    tokens = []
    wordCount,charCount = 0,0
    for line in lines:
        words = line.split()
        wordCount += len(words)
        for w in words:
#            print w
            ww = "".join(ch for ch in w if ch not in badChars)
            tokens.append(ww.lower())
            charCount += len(ww)
    return tokens

#ignore blank lines and return normalized 20 word lines
def readFile(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            if len(line)>1:
                line=line.encode('utf8')
                lineGenerator = normalizeLines(line.strip())
                for l in lineGenerator:
                    ll = " ".join(l)
                    lines.append(ll)
    return lines

#Split the given language samples into 90% Training and 10% Testing...
def splitSample(sample, split=0.9):
    trainSample = []
    testSample = []
    cutOff = int(len(sample) * split)
    shuffle(sample)
    trainSample = sample[:cutOff]
    testSample = sample[cutOff:]
    return trainSample, testSample


#Takes any word and any given size and produces a list of all the possible n-grams for that word from 1 to size
def ngramize(word,size):
    ngrams = []
    word = "_"+word
    for i in range(size):
        word += "_"
    for j in range(len(word)-size):
        ngrams.append(word[j:j+size])
    return ngrams

#Takes a list of tokens, produces all possible [1,2,3,4,5]-grams and returns a dictionary containing all unique n-grams with their frequency counts
def buildNgramDict(langToks):
    tokenCounts = defaultdict(int)
    for token in langToks:
        for i in range(1,5):
            ngrams = ngramize(token,i)
            for ng in ngrams:
                tokenCounts[ng]+=1
    return tokenCounts

#Takes a languageSample object (name and source_file) and builds the language model for that splitSample.
#Language model is a list of unique 1-grams to 5-grams ranked by their frequency
def buildLanguageProfile(langSample):
    print("******** Building model for {} ********".format(langSample["name"].upper()))
    langToks = getTokens(langSample["training"])
    langDict = buildNgramDict(langToks)
    sortedCounts = sorted(langDict.items(),key=lambda x: x[1], reverse=True)
    print("Found with {} different n-grams, but only top {} will be considered...".format(len(sortedCounts),TOP_NGRAMS))
    sortedCounts = sortedCounts[:TOP_NGRAMS]
    langProfile = {}
    for i in range(len(sortedCounts)):
        langProfile[sortedCounts[i][0]] = {"rank":i+1,"count":sortedCounts[i][1]}
    return {"name":langSample["name"],"profile":langProfile}

#Takes a string and builds a profile for it,in the same manner as the language model profile of a file
def buildTextProfile(text):
    langToks = getTokens([text])
    langDict = buildNgramDict(langToks)
    sortedCounts = sorted(langDict.items(),key=lambda x: x[1], reverse=True)
    sortedCounts = sortedCounts[:TOP_NGRAMS]
    langProfile = {}
    for i in range(len(sortedCounts)):
        langProfile[sortedCounts[i][0]] = {"rank":i+1,"count":sortedCounts[i][1]}
    return {"name":"test_case","profile":langProfile}

#Returns the ranking of an n-gram in a given profile
def getRankInProfile(ngram,langProfile):
    elem = langProfile.get(ngram,None)
    if elem:
        return elem["rank"]
    else:
        return None

def compareProfiles(testProfile,langProfile):
    totalDistance = 0
    for ngram in testProfile.keys():
        outOfPlace = DEFAULT_PENALTY
        rankedInProfile = getRankInProfile(ngram,langProfile)
        if rankedInProfile: outOfPlace = abs(testProfile[ngram]["rank"] - rankedInProfile)
        totalDistance += outOfPlace
    return totalDistance

#Takes a test string and the constructed language profiles. Computes the distance between the test string and each of the profiles
def getTextLanguage(testCase):
    testProfile = buildTextProfile(testCase)
    scores = [(lang["name"],compareProfiles(testProfile["profile"],lang["profile"])) for lang in languageProfiles]
    sortedScores = sorted(scores,key=lambda x: x[1])
    return sortedScores[0][0]      
    
#get TPR score

def testLanguageProfiles(profiles,testSet):
    tp,fn = 0,0
    for tag,testCase in testSet:
        result = getTextLanguage(testCase,profiles)
        if result != tag:
            fn += 1
        else:
            tp+=1
    TPR = tp/float(fn+tp)
    print("\n\nTPR in testing cases was: {}\n".format(TPR))
    return TPR

def train():
    testingSamples = []
    for samp in LANGUAGE_SAMPLES:
        lines = readFile(samp["file"])
        samp["training"] = lines
        langProfile = buildLanguageProfile(samp)
        languageProfiles.append(langProfile)

languageProfiles = []
TOP_NGRAMS = 400
DEFAULT_PENALTY = 250
TEST_ENABLED = False
LANGUAGE_SAMPLES = [{"name":"English","file":"resources/english_sample.txt"},
                    {"name":"Pinyin","file":"resources/pinyin_sample.txt"},]

if __name__ == "__main__":
    train()


def setup():
    train() 

