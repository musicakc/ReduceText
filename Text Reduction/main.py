import re, pdb, sys, math
from collections import defaultdict


class Reduction:
    functionPunctuation = ' ,-'
    contentPunctuation = '.?!\n'
    punctuationCharacters = functionPunctuation+contentPunctuation
    sentenceEndCharacters = '.?!'

    def isContentPunctuation(self,text):
        for c in self.contentPunctuation:
            if text.lower()== c.lower():
                return True
        return False

    def isFunctionPunctuation(self,text):
        for c in self.functionPunctuation:
            if text.lower() == c.lower():
                return True
        return False

    def isFunction(self,text,sWords):
        for w in sWords:
            if text.lower()==w.lower():
                return True
        return False

    def tag(self,sampleWords,sWords):
        taggedWords = []
        for w in sampleWords:
            tw = Word()
            tw.text= w
            if self.isContentPunctuation(w):
                tw.Type = WordType.ContentPunctuation
            elif self.isFunctionPunctuation(w):
                tw.Type = WordType.FunctionPunctuation
            elif self.isFunction(w, sWords):
                tw.Type = WordType.Function
            else:
                tw.Type = WordType.Content
            taggedWords.append(tw)
        return taggedWords

    #Tokenizes sentences by splitting words
    def tokenize(self,text):
        return filter(lambda w: w!='',re.split('[{0}]'.format(self.punctuationCharacters),text))
    
    def reduce(self,text,reductionRatio):
        sWordsFile='sWords.txt'
        sWords=open(sWordsFile).read().splitlines()

        lines=text.splitlines()
        # Removing trailing whitespaces
        contentLines = filter(lambda w: w.strip() != '',lines)

        paragraphs=self.getParagraphs(contentLines)

        rankedSentences=self.sentenceRank(paragraphs)

        orderedSentences = []
        for p in paragraphs:
            for s in p.Sentences:
                orderedSentences.append(s)

        reducedSentences = []
        i=0
        while i< math.trunc(len (rankedSentences) * reductionRatio):
            s=rankedSentences[i][0].Sentence
            position = orderedSentences.index(s)
            reducedSentences.append((s,position))
            i=i+1
        reducedSentences = sorted(reducedSentences, key= lambda x: x[1])

        reducedText =[]

        for s,r in reducedSentences:
            reducedText.append(s.getFullSentence())
        return reducedText

    def getWords(self,sentenceText, sWords):
        return self.tag(self.tokenize(sentenceText), sWords)

    def getSentences(self,line,sWords):
        sentences = []
        sentenceTexts = filter(lambda w: w.strip())
        sentenceEnds = re.findall('[{0}]'.format(self.sentenceEndCharacters),line)
        sentenceEnds.reverse()
        for t in sentenceTexts:
            if len(sentenceEnds) > 0:
                t+=sentenceEnds.pop()
            sentence = Sentence()
            sentence.Words = self.getWords(t, sWords)
            sentences.append(sentence)
        return sentences

    def getParagraphs(self,lines,sWords):
        paragraphs=[]
        for line in lines:
            paragraph=Paragraph()
            paragraph.Sentences=self.getSentences(line, sWords)
            paragraphs.append(paragraph)
        return paragraphs


class Graph:
    def __init__(self):
        self.Vertices = []
        self.edges = []

    def getRankedVertices(self):
        res = defaultdict(float)
        for e in self.Edges:
            res[e.Vertex1]+=e.Weight
        return sorted(res.items(), key=lambda x: x[1], reverse=True)


class Vertex:
    def __init__(self):
        self.Sentence = None


class Edge:
    def __init__(self):
        self.Vertex1 = None
        self.Vertex2 = None
        self.Weight = None


class WordType:
    Content = 0
    Function = 1
    ContentPunctuation = 2
    FunctionPunctuation = 3
    

class Word:
    def __init__(self):
        self.Text=''
        self.Type=''

class Sentence:
    def __init__(self):
        self.Words=[]

    def getFullSentence(self):
        text = ''
        for w in self.Words:
            text +=w.Text
        return text.strip()

    def getReducedSentence(self):
        sentenceText = ''
        sentenceEnd = self.Words[len(self.Words)-1]
        contentWords = filter(lambda w:w.Type == WordType.Content, self.Words)
        i=0
        while i < len(contentWords):
            w=contentWords[i]
            if i==0:
                li= list(w.Text)
                li[0] = li[0].upper()
                w.Text = ''.join(li)
            sentenceText += w.Text
            if i <len(contentWords)-1:
                sentenceText += ' '
            elif sentenceEnd.Text != w.Text:
                sentenceText += sentenceEnd
            i = i+1
        return sentenceText


class Paragraph:
    def __init__(self):
        self.sentences = []
