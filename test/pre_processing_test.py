# -*- coding: utf-8 -*-

import logging
import unittest
from pre_processing import PreProcessing


class TestPreProcessing(unittest.TestCase):

    logging.basicConfig(level=logging.DEBUG)

    def test_should_lowercase(self):
        c = PreProcessing()
        expected = ['converter', 'para', 'caixa', 'baixa']
        self.assertEquals(expected, c.__normalize__("ConverTer para CAIXA baiXa"))

    def test_should_remove_accents(self):
        c = PreProcessing()
        expected = ['que', 'horas', 'sao', 'sr', 'joao']
        self.assertEquals(expected, c.__normalize__("que horas são Sr João"))

    def test_should_remove_accents_and_special_chars(self):
        c = PreProcessing()
        expected = ['oi', 'qual', 'e', 'o', 'email', 'do', 'sr', 'joao', 'e', 'joaogmailcom', 'ah', 'eu', 'ja', 'sabia']
        self.assertEquals(expected, c.__normalize__("Oi, qual é o e-mail do Sr. João? "
                                                    "É joao@gmail.com! Ah eu já sabia!"))
        expected = ['o', 'cpf', 'do', 'joao', 'e', '12345678900']
        self.assertEquals(expected, c.__normalize__("o cpf do joao é 123.456.789-00"))

    def test_should_remove_newline(self):
        c = PreProcessing()
        expected = ['linha1', 'linha2', 'linha3']
        self.assertEquals(expected, c.__normalize__("\nlinha1 linha2 linha3\n"))

    def test_should_remove_nnp(self):
        c = PreProcessing(["joao"], [], [])
        expected = ["ola", ",", "tudo", "bem", "?"]
        self.assertEquals(expected, c.__obfuscate__(["ola", "joao", ",", "tudo", "bem", "?"]))

    def test_should_remove_nnps(self):
        c = PreProcessing(["joao", "victor", "almeida"], [], [])
        expected = ["ola", "vitor", ",", "tudo", "bem", "?"]
        self.assertEquals(expected, c.__obfuscate__(["ola", "joao", "vitor", "almeida", ",", "tudo", "bem", "?"]))

    def test_should_remove_digits(self):
        c = PreProcessing(["joao"], [], ["\d+"])
        self.assertEquals(["tem", "anos"],
                          c.__obfuscate__(["joao", "tem", "12", "anos"]))
        self.assertEquals(["anos", "e", "amigos", "no", "facebook"],
                          c.__obfuscate__(["joao", "12", "anos", "e", "1765546587", "amigos", "no", "facebook"]))
        self.assertEquals(["o", "cpf", "do",  "e"],
                          c.__obfuscate__(["o", "cpf", "do", "joao", "e", "123.456.789-00"]))

    def test_should_remove_noisy(self):
        c = PreProcessing([], ["ruido"], [])
        self.assertEquals(["dados", "com", "deve", "ser", "removido"],
                          c.__obfuscate__(["dados", "com", "ruido", "deve", "ser", "removido"]))

    def test_should_remove_stopwords(self):
        c = PreProcessing()
        self.assertEqual(["gostaram", "comida"],
                         c.__remove_stopwords__(["eles", "gostaram", "da", "nossa", "comida"]))

    def test_should_clean_text(self):
        c = PreProcessing(["joao", "maria"], [], ["\d+", "nomeemp*"])
        text = "O técnico joão foi até a casa da maria (nomeempresa) e solucionou o problema. " \
               "Ele ainda persisti? nomeempprod"
        expected = ["tecnico", "ate", "casa", "solucionou", "problema", "ainda", "persisti"]
        self.assertEqual(expected, c.clean(text))

    def test_should_stem(self):
        c = PreProcessing()
        tokens = ["tecnico", "ate", "casa", "solucionou", "problema", "ainda", "persisti"]
        expected = ["tecn", "ate", "cas", "solucion", "problem", "aind", "persist"]
        self.assertEquals(expected, c.stem(tokens))

    def test_should_build_bag_of_words(self):
        p = PreProcessing(["joao", "maria"], [], ["\d+", "nomeemp*"])

        text = "O técnico João foi até a casa da Maria (NOMEEMPRESA) e solucionou o problema. " \
               "Ele não foi solucionado? NomeempProd"
        tokens = p.clean(text)
        tokens = p.stem(tokens)

        bow, bfn = p.build_bow(tokens)
        self.assertEquals("(7, 6)", bow.shape.__str__())

    def test_should_compute_tdidf(self):
        p = PreProcessing(["joao", "maria"], [], ["\d+", "nomeemp*"])

        text_1 = "O técnico João foi até a casa da cliente Maria (NOMEEMPRESA) e solucionou o problema. " \
                 "Ele não foi solucionado? NomeempProd"
        text_2 = "A cliente Maria disse que continua sem sinal de Internet e " \
                 "reclamou que o problema não foi resolvido, ela continua sem sinal"
        text_3 = "Maria solicitou reparo, cliente reclama que esta sem sinal de Internet e Telefone após chuva"

        texts = [text_1, text_2, text_3]

        terms = p.compute_tfidf(texts)
        print terms

        import operator
        print sorted(terms.items(), key=operator.itemgetter(1), reverse=True)
