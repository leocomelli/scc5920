import re
import unicodedata
from nltk import word_tokenize


class CleanupData:

    LANGUAGE = "portuguese"

    def __init__(self, nnp=None, terms=None, patterns=None, language=LANGUAGE):
        self.nnp = nnp
        self.terms = terms
        self.patterns = patterns
        self.language = language

    def clean(self, data):

        for d in data:
            text = d.text.strip()
            text = text.decode('utf-8', 'ignore') if isinstance(text, str) else text
            text = ''.join((c for c in unicodedata.normalize('NFD', text)
                        if unicodedata.category(c) != 'Mn')).lower().encode('utf-8')
            text = re.sub(r"[^\w\s]+", " ", text)
            text = re.sub(r"_", " ", text)
            tokens = word_tokenize(text)
            tokens = self.__obfuscate__(tokens)

            d.text = ' '.join(tokens)

        return data

    def __obfuscate__(self, tokens):
        tokens = [t for t in tokens if t not in self.nnp]
        tokens = [t for t in tokens if t not in self.terms]

        ntokens = []
        for i, t in enumerate(tokens):
            found = False
            for p in self.patterns:
                if re.match(r'%s' % p, t):
                    found = True
                    break

            if not found:
                ntokens.append(t)

        return ntokens
