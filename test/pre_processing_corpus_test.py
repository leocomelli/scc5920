import unittest
import numpy as np
from pre_processing import PreProcessing
from load_data import LoadData


class TestPreProcessingCorpus(unittest.TestCase):

    def test_corpus(self):

        with open("../data/pt_BR/nnp") as f:
            nnp = [line.rstrip() for line in f.readlines()]
        with open("../data/pt_BR/terms") as f:
            terms = [line.rstrip() for line in f.readlines()]
        with open("../data/pt_BR/patterns") as f:
            patterns = [line.rstrip() for line in f.readlines()]

        data = LoadData(['../corpus/sel1.csv', '../corpus/sel2.csv']).load()
        p = PreProcessing(nnp, terms, patterns)

        tokens = []
        for d in data.values():
            tokens += p.clean_and_stem(d)

        bow, bow_features_names = p.build_bow(tokens)
        dist = np.sum(bow.toarray(), axis=0)
        tbow = {}
        for term, count in zip(bow_features_names, dist):
            tbow[term] = count

        import operator
        with open("bow", "w") as f:
            f.write(str(len(tbow)))
            f.write(str(sorted(tbow.items(), key=operator.itemgetter(1), reverse=True)))

        terms = p.compute_tfidf(data.values(), eliminate_zeros=True)
        with open("terms", "w") as f:
            f.write(str(terms))

