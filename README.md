$ git clone git@github.com:leocomelli/scc5920.git
$ cd scc5920

$ docker build -t scc5920 .
$ docker run -v $(pwd):/scc5920 -ti scc5920

$ cd  test
$ python -m unittest pre_processing_corpus_test.TestPreProcessingCorpus
