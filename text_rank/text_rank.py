# coding=utf-8

import math
import numpy as np

class TextRank:
    """ This class is the implementation of TextRank proposed by following paper.
    TextRank is a graph-based summarization model that use PageRank like algorithm.
    This class does not perform tokenization and normalization of texts, so you should preprocess your data beforehand.

    Original Paper: TextRank: Bringing Order into Texts, Mihalcea+, EMNLP 2004.
    https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf
    """

    def __init__(self, conv_thr=0.0001, damping_factor=0.85, stopwords_path="./smart_common_words.txt"):
        """ Initializer for TextRank Class
        Params:
            conv_thr(float): convergence threshold on TextRank
            damping_factor(float): damping factor in TextRank
            stopwords_path(str): stopword list (this file should be represent 1 word per line)
        """
        self.CONV_THR = conv_thr
        self.D_FACTOR = damping_factor
        try:
            with open(stopwords_path) as f:
                self.stopwords_list = [w for w in f.read().strip().split("\n")]
        except IOError:
            print("Warning: Cannot find stopwords file. No stopwords will be used.")
            self.stopwords_list = []
 
    def __calc_similarity(self):
        """ Calculate similarity based on similarity function in Sec. 4.1.
        """
        def __sim_func(i, j):
            tokens1, tokens2 = self.sents[i], self.sents[j]
            overlap = len(set(tokens1) & set(tokens2))

            if i==j or overlap==0:
                return 0.0
            return overlap / (math.log(len(tokens1)) + math.log(len(tokens2)))
        
        N = len(self.sents)
        _sim_mat = np.asarray([[__sim_func(i, j) for j in xrange(N)] for i in xrange(N)], dtype=np.float32)
        # normalize (sum of row equals 1)
        self.sim_mat = np.asarray([_sim_mat[i]/sum(_sim_mat[i]) if sum(_sim_mat[i]!=0.0) else _sim_mat[i] for i in xrange(N)], dtype=np.float32)
        print self.sim_mat
  
    def __calc_diff(self, vec1, vec2):
        """ Calculate difference between vec1 and vec2.
        Params:
            vec1(numpy.array): numpy array that we want to calculate difference
            vec2(numpy.array): numpy array that we want to calculate difference
        """
        return sum(np.fabs(vec1 - vec2))

    def set_sentences(self, sents):
        """ Set sentences that you want to calculate TextRank score
        Params:
            sents(list): list of sentences, a sentence should be represented on list of tokens
        """
        self.sents = sents

    def run(self, debug=False):
        """ Run iteration to calculate TextRank score.
        Params:
            debug(boolean): if debug equals True, #_of_iter and diff will be presented at each iter.
        """
        self.__calc_similarity()
        
        diff = 1
        N = len(self.sents)
        tr = np.asarray([1.0 / N for _ in xrange(N)], dtype=np.float32)
        iter_count = 0
        while diff > self.CONV_THR:
            next_tr = (1.0 - self.D_FACTOR) + self.D_FACTOR * self.sim_mat.T.dot(tr)
            diff = self.__calc_diff(next_tr, tr)
            tr = next_tr

            if debug:
                iter_count += 1
                print("Iteration {0}: diff={1}".format(iter_count, diff))

        self.text_rank = tr / sum(tr)

if __name__ == '__main__':
    tr = TextRank()
    sentences = [
            "BC-Hurricane Gilbert 09-11 0339",
            "BC-Hurricane Gilbert 0348",
            "Hurricane Gilbert Heads Toward Dominican Coast",
            "By RUDDY GONZALEZ",
            "Associated Press Writer",
            "SANTO DOMINGO Dominican Republic (AP)",
            "Hurricane Gilbert swept toward the Dominican Republic Sunday and the Civil Defense alerted its heavily populated south coast to prepare for high winds heavy rains and high seas",
            "The storm was approaching from the southeast with sustained winds of 75 mph gusting to 92 mph",
            "There is no need for alarm Civil Defense Director Eugenio Cabral said in a television alert shortly before midnight Saturday",
            "Cabral said residents of the province of Barahona should closely follow Gilbert 's movement",
            "An estimated 100,000 people live in the province including 70,000 in the city of Barahona about 125 miles west of Santo Domingo",
            "Tropical Storm Gilbert formed in the eastern Caribbean and strengthened into a hurricane Saturday night",
            "The National Hurricane Center in Miami reported its position at 2 a.m. Sunday at latitude 16.1 north longitude 67.5 west about 140 miles south of Ponce Puerto Rico and 200 miles southeast of Santo Domingo",
            "The National Weather Service in San Juan Puerto Rico said Gilbert was moving westward at 15 mph with a broad area of cloudiness and heavy weather rotating around the center of the storm",
            "The weather service issued a flash flood watch for Puerto Rico and the Virgin Islands until at least 6 p.m. Sunday",
            "Strong winds associated with the Gilbert brought coastal flooding strong southeast winds and up to 12 feet feet to Puerto Rico 's south coast",
            "There were no reports of casualties",
            "San Juan on the north coast had heavy rains and gusts Saturday but they subsided during the night",
            "On Saturday Hurricane Florence was downgraded to a tropical storm and its remnants pushed inland from the U.S. Gulf Coast",
            "Residents returned home happy to find little damage from 80 mph winds and sheets of rain",
            "Florence the sixth named storm of the 1988 Atlantic storm season was the second hurricane",
            "The first Debby reached minimal hurricane strength briefly before hitting the Mexican coast last month"]
    sents_toks = [sent.split(" ") for sent in sentences]
    tr.set_sentences(sents_toks)
    tr.run(debug=True)
    ids = [i for i, _ in sorted(enumerate(tr.text_rank), key=lambda x: x[1], reverse=True)[:5]]
    print "\n".join(["["+str(i)+":"+str(tr.text_rank[i])+"]"+" "+sentences[i] for i in ids])
