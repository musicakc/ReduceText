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
    i=0;
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

 
