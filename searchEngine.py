from os import listdir, remove
from spacy import load
from nltk import regexp_tokenize, pos_tag
from shutil import copy


class SearchEngine:
    def __init__(self):
        self.nlp = load("en_core_web_sm")
        self.docs = {}
        self.wordsLemmaDict = {}
        self.stopWords = set()
        self.stopTegs = set()
        self.docsTitles = set()
        self.readStopWords()
        self.readStopTegs()
        self.readDocs()

    def getWordLemma(self, word: str) -> str:
        return self.nlp(word)[0].lemma_

    def getTokens(self, text: str) -> list:
        return regexp_tokenize(text, r'\b\w+\b|\W')

    def getFilesTitles(self, folder) -> set:
        return set(listdir(folder))

    def readStopWords(self):
        with open("./data/stopwords.txt", "r") as file:
            for line in file:
                self.stopWords.add(line.strip())

    def readStopTegs(self):
        with open("./data/stoptegs.txt", "r") as file:
            for line in file:
                self.stopTegs.add(line.strip())

    def readDocs(self):
        docs = self.getFilesTitles("./docs")
        sids = self.getFilesTitles("./sids")
        for sid in sids:
            if sid not in docs:
                remove(f"./sids/{sid}")
        for doc in docs:
            if doc not in sids:
                self.getSid(doc)
        for doc in docs:
            self.readSid(doc)

    def readSid(self, sid):
        wordsDict = {}
        with open(f"./sids/{sid}", 'r') as file:
            for line in file:
                word, freq = line.split()
                wordsDict[word] = float(freq)
        self.docs[sid] = wordsDict

    def getSid(self, doc):
        with open(f"./docs/{doc}", 'r') as file:
            wordsDict = {}
            text = file.read().lower()
            tokens = self.getTokens(text)
            tags = pos_tag(tokens)
            for word, tag in tags:
                if len(word) == 0 or not word[0].isalpha():
                    continue
                if word in self.stopWords or tag in self.stopTegs:
                    continue
                lemma = self.getWordLemma(word)
                if lemma in self.stopWords:
                    continue
                wordsDict[lemma] = wordsDict.get(lemma, 0) + 1
            maxFreq = max(wordsDict.values())
            for word, frequency in wordsDict.items():
                wordsDict[word] = frequency / maxFreq
            self.docs[doc] = wordsDict
            self.writeSid(doc, wordsDict)

    def writeSid(self, sid, wordsDict):
        with open(f"./sids/{sid}", "w") as file:
            for word, frequency in wordsDict.items():
                file.write(f"{word} {frequency}\n")

    def addDoc(self, filepath):
        filename = filepath[filepath.rfind('/') + 1:]
        copy(filepath, f"./docs/{filename}")
        self.getSid(filename)

    def getDocumentsList(self, searchText: str) -> list:
        searchText = searchText.lower()
        tokens = self.getTokens(searchText)
        lemmas = [self.getWordLemma(token) for token in tokens]
        print(lemmas)
        documentsList = []
        for doc, wordsDict in self.docs.items():
            for lemma in lemmas:
                if lemma in wordsDict:
                    documentsList.append(doc)
                    break
        documentsList.sort(reverse=True, key=lambda doc: sum(
            [
                self.docs[doc].get(word, 0) / max(self.docs[doc].values())
                for word in lemmas
            ]))
        return documentsList
