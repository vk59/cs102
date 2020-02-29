from collections import (Counter, defaultdict)
from math import log


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.prior_probably = {}
        self.dict_probably = {}
        self.words = set()
        self.labels = set()

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        c = Counter()
        for label in y:
            c[label] += 1
        self.labels = set(y)

        # априорная вероятность p(label)
        for label in self.labels:
            self.prior_probably[label] = c[label] / len(y)
        
        dict_words = {}
        for label in self.labels:
            dict_words[label] = defaultdict(int)
            self.dict_probably[label] = dict()

        words_list = []
        for i in range(len(X)):
            s = X[i].split()
            label = y[i]
            for word in s:
                dict_words[label][word] += 1
                words_list.append(word)

        self.words = set(words_list)
        for word in self.words:
            mentions = {}
            sum_ment = 0
            for label in self.labels:
                if not word in dict_words[label]:
                    mentions[label] = 0
                else:
                    mentions[label] = dict_words[label][word]
                sum_ment += mentions[label]
                # p(w(i) | C)
                # Laplacian smoothing
                self.dict_probably[label][word] = (mentions[label]
                    + self.alpha) / (sum_ment + self.alpha * len(self.words))
        

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predict_list = []
        for x in X:
            s = x.split()
            prob = {}
            for l in self.labels:
                prob[l] = log(self.prior_probably[l])
                for word in s:
                    if word in self.dict_probably[l]:
                        # p_wc - вероятность данного слова
                        p_wc = self.dict_probably[l][word]
                    else:
                        # Laplacian smoothing
                        p_wc = 1 / len(self.words)
                    prob[l] += log(p_wc)
            max_label = ''
            maximum = -1000000000
            for l in self.labels:
                if prob[l] > maximum:
                    max_label = l
                    maximum = prob[l]
            predict_list.append(dict(title=x, label=max_label))
        return predict_list
                    
                    
    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        count = 0
        classifier_answers = self.predict(X_test)
        for i in range(len(X_test)):
            if classifier_answers[i]['label'] == y_test[i]:
                count += 1
        return count / len(y_test)
