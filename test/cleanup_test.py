import unittest
from cleanup_data import CleanupData
from load_data import LoadData


class TestCleanupData(unittest.TestCase):

    def test_cleanup(self):

        with open("../data/pt_BR/nnp") as f:
            nnp = [line.rstrip() for line in f.readlines()]
        with open("../data/pt_BR/terms") as f:
            terms = [line.rstrip() for line in f.readlines()]
        with open("../data/pt_BR/patterns") as f:
            patterns = [line.rstrip() for line in f.readlines()]

        data = LoadData(['../corpus/sel1.csv', '../corpus/sel2.csv'], ['D', 'C']).load()
        p = CleanupData(nnp, terms, patterns)
        new_data = p.clean(data)

        with open("results/clean.txt", "w") as f:
            f.write("\n".join("%s;%s;%s" % (d.identifier, d.text, d.status) for d in new_data))

        for i, d in enumerate(new_data):
            dirname = "conectado" if d.status == "C" else "desconectado"
            filename = "results/%s/clt_%s.txt" % (dirname, i)
            with open(filename, "w") as f:
                f.write(d.text)

