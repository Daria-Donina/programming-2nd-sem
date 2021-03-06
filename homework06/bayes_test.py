from bayes import NaiveBayesClassifier
import csv
import string


def my_test():
    X_train = ["I love this sandwich",
               "This is an amazing place",
               "I feel very good about these beers",
               "This is my best work",
               "What an awesome view",
               "I do not like this restaurant",
               "I am tired of this stuff",
               "I can't deal with this",
               "He is my sworn enemy",
               "My boss is horrible"]

    y_train = ['Positive', 'Positive', 'Positive', 'Positive', 'Positive',
               'Negative', 'Negative', 'Negative', 'Negative', 'Negative']

    X_test = ['The beer was good', 'I do not enjoy my job', "I ain't feeling dandy today",
              'I feel amazing', 'Gary is a friend of mine', "I can't believe I'm doing this"]

    y_test = ['Positive', 'Negative', 'Negative', 'Positive', 'Positive', 'Negative']

    classifier = NaiveBayesClassifier(alpha=1)
    classifier.fit(X_train, y_train)

    print(classifier.classes_probabilities)
    print(classifier.classes_count)
    print(sorted(classifier.words_in_classes_count.items()))
    print(sorted(classifier.words_in_classes_probabilities.items()))

    print(classifier.predict(X_test))
    print(classifier.score(X_test, y_test))


def sms_test():
    with open("data/SMSSpamCollection", encoding='utf-8') as f:
        data = list(csv.reader(f, delimiter="\t"))

    def clean(s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)

    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X = [clean(x).lower() for x in X]

    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

    model = NaiveBayesClassifier(alpha=1)
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))

# my_test()
# sms_test()
