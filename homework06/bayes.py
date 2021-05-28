from collections import defaultdict, Counter
from math import log
from statistics import mean
import string


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.words_in_classes_count = defaultdict(dict)  # словарь словарей?
        self.words_in_classes_probabilities = defaultdict(dict)
        self.classes_count = defaultdict(int)
        self.classes_probabilities = {}

    def fit(self, X, y):
        size = len(y)

        # считаем вероятности классов
        self.classes_probabilities = Counter(y)
        for i in self.classes_probabilities:
            self.classes_probabilities[i] /= size

        # подсчитываем слова в каждом классе
        for line, value in zip(X, y):
            line = clean(line).lower()
            for word in line.split(' '):

                if word not in self.words_in_classes_count:
                    self.words_in_classes_count[word] = \
                        dict({k: 0 for k in self.classes_probabilities.keys()})

                self.words_in_classes_count[word][value] += 1

                # подсчитываем размерность классов
                self.classes_count[value] += 1

        # подсчитываем вероятность для каждого слова в каждом классе
        for word, dct in self.words_in_classes_count.items():
            for _class, count in dct.items():
                self.words_in_classes_probabilities[word][_class] = \
                    (count + self.alpha) / (self.classes_count[_class] + self.alpha * len(self.words_in_classes_count))

    def predict(self, X):
        y = []
        for line in X:
            probs = defaultdict(float)
            for _class in self.classes_count:
                probs[_class] = log(self.classes_probabilities[_class])
                line = clean(line).lower()
                for word in line.split(' '):
                    if word in self.words_in_classes_probabilities:
                        probs[_class] += log(self.words_in_classes_probabilities[word][_class])

            y.append(max(probs, key=probs.get))
        return y

    def score(self, X_test, y_test):
        scoring = []

        y_predicted = self.predict(X_test)
        for predicted, expected in zip(y_predicted, y_test):
            scoring.append(int(predicted == expected))
        return mean(scoring)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)
