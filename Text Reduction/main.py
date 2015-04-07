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

    def isFunction(self,text,stopWords):
        for w in stopWords:
            if text.lower()==w.lower():
                return True
        return False

    def tag(self,sampleWords,stopWords):
        taggedWords = []
        for w in sampleWords:
            tw = Word()
            tw.text= w
            if self.isContentPunctuation(w):
                tw.Type = WordType.ContentPunctuation
            elif self.isFunctionPunctuation(w):
                tw.Type = WordType.FunctionPunctuation
            elif self.isFunction(w, stopWords):
                tw.Type = WordType.Function
            else:
                tw.Type = WordType.Content
            taggedWords.append(tw)
        return taggedWords

    def tokenize(self,text):
        return filter(lambda w: w!='',re.split('[{0}]'.format(self.punctuationCharacters),text))
    
    def reduce(self,text,reductionRatio):
        stopWordsFile='stopWords.txt'
        stopWords=open(stopWordsFile).read().splitlines()

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

    def getWords(self,sentenceText, stopWords):
        return self.tag(self.tokenize(sentenceText), stopWords)

    def getSentences(self,line,stopWords):
        sentences = []
        sentenceTexts = filter(lambda w: w.strip())
        sentenceEnds = re.findall('[{0}]'.format(self.sentenceEndCharacters),line)
        sentenceEnds.reverse()
        for t in sentenceTexts:
            if len(sentenceEnds) > 0:
                t+=sentenceEnds.pop()
            sentence = Sentence()
            sentence.Words = self.getWords(t, stopWords)
            sentences.append(sentence)
        return sentences

    def getParagraphs(self,lines,stopWords):
        paragraphs=[]
        for line in lines:
            paragraph=Paragraph()
            paragraph.Sentences=self.getSentences(line, stopWords)
            paragraphs.append(paragraph)
        return paragraphs
