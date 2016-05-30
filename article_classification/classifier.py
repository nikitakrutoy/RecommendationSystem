import numpy as np
import random
import sklearn.feature_extraction.text, re
import sklearn.linear_model
import sklearn.metrics
import sklearn.grid_search

WORD_PATTERN = '[a-z]+'


def get_text(article_path):
    with open(article_path, 'r') as html:
        page = html.read()
    return page

def scorer(estimator, X, Y):
    metric = sklearn.metrics.roc_auc_score
    return metric(Y, estimator.predict_proba(X)[:, 1])


def main():
    interesting = set()
    boring = set()
    data = list()

    with open('interesting.txt', 'r') as lines:
        while True:
            article_name = lines.readline().rstrip()
            if article_name == '':
                break
            article = get_text(article_name)
            interesting.add(article)
            data.append(article)

    with open('boring.txt', 'r') as lines:
        while True:
            article_name = lines.readline().rstrip()
            if article_name == '':
                break
            article = get_text(article_name)
            boring.add(article)
            data.append(article)

    random.shuffle(data)
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(token_pattern=WORD_PATTERN)
    X = vectorizer.fit_transform(data)
    Y = np.array([1 if t in interesting else 0 for t in data])


    X_train, X_search, X_test = X[:80], X[80:100], X[100:120]
    Y_train, Y_search, Y_test = Y[:80], Y[80:100], Y[100:120]

    cls = sklearn.linear_model.SGDClassifier(loss='log')
    cls.fit(X_train, Y_train)

    metric = sklearn.metrics.roc_auc_score

    Y_pred = cls.predict_proba(X_test)[:, 1]

    score = metric(Y_test, Y_pred)
    print('Score: ', score)

    grid = {
        'penalty': ['elasticnet'],
        'alpha': [0.001, 0.0001, 0.00001, 0.000001, 0.0000001],
        'l1_ratio': [0.0, 0.01, 0.05, 0.10, 0.2, 0.3, 0.4, 0.5],
    }

    searcher = sklearn.grid_search.GridSearchCV(
        estimator=sklearn.linear_model.SGDClassifier(loss='log'),
        param_grid=grid,
        scoring=scorer,
        cv=5,
        n_jobs=1
    )

    searcher.fit(X_search, Y_search);
    print(searcher.best_score_)
    print(searcher.best_params_)

    best_cls = searcher.best_estimator_

    print(scorer(best_cls, X_test, Y_test))



if __name__ == '__main__':
    main()