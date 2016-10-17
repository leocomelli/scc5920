import unittest
import numpy as np
from nltk.corpus import machado
from pre_processing import PreProcessing


class TestPreProcessingMachado(unittest.TestCase):

    def test(self):
        p = PreProcessing([], [], [])
        cts = machado.fileids()[:5]

        tokens = []
        for c in cts:
            text = machado.raw(c)
            tokens += p.clean_and_stem(text)

        bow, bow_features_names = p.build_bow(tokens)
        dist = np.sum(bow.toarray(), axis=0)
        tbow = {}
        for term, count in zip(bow_features_names, dist):
            tbow[term] = count

        import operator
        print sorted(tbow.items(), key=operator.itemgetter(1), reverse=True)

        texts = {}
        for c in cts:
            text = machado.raw(c)
            texts[c] = text

        terms = p.compute_tfidf(texts.values(), top_n=10, eliminate_zeros=True)
        print terms
