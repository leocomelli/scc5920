import re
import unicodedata
import numpy as np
import logging
from nltk import stem
from itertools import islice
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)


class PreProcessing:

    LANGUAGE = "portuguese"

    def __init__(self, nnp=None, terms=None, patterns=None, language=LANGUAGE):
        self.nnp = nnp
        self.terms = terms
        self.patterns = patterns
        self.language = language

        self.stopwords = stopwords.words(language)
        self.stemmer = stem.RSLPStemmer() if language == self.LANGUAGE else stem.porter.PorterStemmer()

    @staticmethod
    def build_bow(tokens):
        vectorizer = CountVectorizer()

        bow = vectorizer.fit_transform(tokens)
        bow_features = bow.toarray()
        bow_features_names = vectorizer.get_feature_names()

        logging.debug("dimensions of bow: %s", bow.shape)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(bow_features_names)

            dist = np.sum(bow_features, axis=0)
            for term, count in zip(bow_features_names, dist):
                logging.debug("{ count: %s, term: %s }", count, term)

        return bow, bow_features_names

    def compute_tfidf(self, text, top_n=None, eliminate_zeros=False):
        tfidf = TfidfVectorizer(tokenizer=self.clean_and_stem)
        tfs = tfidf.fit_transform(text)

        features = tfidf.get_feature_names()
        terms = {}
        for col in tfs.nonzero()[1]:
            term = features[col]
            score = tfs[0, col]
            if not eliminate_zeros or (eliminate_zeros and score != 0.0):
                terms[term] = score
            logging.debug("{ term: %s, score: %s }", term, score)

        return terms if top_n is None else dict(list(islice(terms.iteritems(), top_n)))

    def clean_and_stem(self, text):
        tks = self.clean(text)
        return self.stem(tks)

    def clean(self, text):
        tokens = self.__normalize__(text)
        tokens = self.__obfuscate__(tokens)
        tokens = self.__remove_stopwords__(tokens)

        return tokens

    def stem(self, tokens):
        stemmed = []
        for item in tokens:
            stemmed.append(self.stemmer.stem(item))

        return stemmed

    @staticmethod
    def __normalize__(text):
        # strip newlines
        text = text.strip()
        # lowercase and remove accents
        text = text.decode('utf-8', 'ignore') if isinstance(text, str) else text
        text = ''.join((c for c in unicodedata.normalize('NFD', text)
                        if unicodedata.category(c) != 'Mn')).lower().encode('utf-8')
        # remove special chars
        text = re.sub(r"[^\w\s]+", "", text)

        return word_tokenize(text)

    def __obfuscate__(self, tokens):
        tokens = [t for t in tokens if t not in self.nnp]
        tokens = [t for t in tokens if t not in self.terms]

        for i, t in enumerate(tokens):
            for p in self.patterns:
                if re.match(r'%s' % p, t):
                    del tokens[i]

        return tokens

    def __remove_stopwords__(self, tokens):
        return [t for t in tokens if t not in self.stopwords]
