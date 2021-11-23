from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


def error(y, yPred):
    error = 0
    for i in range(len(y)):
        error += (y[i] - yPred[i]) ** 2
    return error / len(y)


class LinearRegression:
    def __init__(self):
        self.w, self.b = None, None
        self.loss = []
        self.learningRate = 0.01
        self.numOfIterations = 10000

    def predict(self, X):
        return np.dot(X, self.w) + self.b

    def fit(self, X, y):
        self.w = np.zeros(X.shape[1])
        self.b = 0

        for i in range(self.numOfIterations):
            yPred = np.dot(X, self.w) + self.b
            loss = error(y, yPred)
            self.loss.append(loss)

            partialW = (1 / X.shape[0]) * (2 * np.dot(X.T, (yPred - y)))
            partialB = (1 / X.shape[0]) * (2 * np.sum(yPred - y))

            self.w -= self.learningRate * partialW
            self.b -= self.learningRate * partialB


# isWin (1- True| 0 - False)
# enemy (a-star - 0 | bfs - 1 | random - 2)
# player (a-star - 0 | minimax - 1)

res = pd.read_csv('output.csv').astype(float)
scaler = StandardScaler()
scaler.fit(res)

df_norm = pd.DataFrame(scaler.transform(res),
                       columns=['is_win', 'time', 'score', 'enemies_algotithm', 'pacman_algorithm'])

X = df_norm[['enemies_algotithm', 'pacman_algorithm']].to_numpy()

Y1 = df_norm['is_win'].to_numpy()
Y2 = df_norm['time'].to_numpy()
Y3 = df_norm['score'].to_numpy()

X_train = X[:-5]
X_test = X[-5:]
Y1_train = Y1[:-5]
Y1_test = Y1[-5:]
Y2_train = Y2[:-5]
Y2_test = Y2[-5:]
Y3_train = Y3[:-5]
Y3_test = Y3[-5:]



model = LinearRegression()
model.fit(X_train, Y1_train)
prediction1 = model.predict(X_test)

model.fit(X_train, Y2_train)
prediction2 = model.predict(X_test)

model.fit(X_train, Y3_train)
prediction3 = model.predict(X_test)

df_predicted = pd.DataFrame(columns=['is_win r|p', 'time r|p', 'score r|p', 'enemies_algotithm', 'pacman_algorithm'])

for i in range(5):
    s1 = str(Y1_test[i].round(1)) + ' | ' + str(prediction1[i].round(1))
    s2 = str(Y2_test[i].round(1)) + ' | ' + str(prediction2[i].round(1))
    s3 = str(Y3_test[i].round(1)) + ' | ' + str(prediction3[i].round(1))

    df_predicted = df_predicted.append(pd.DataFrame([[s1, s2, s3, X_test[i, 0], X_test[i, 1]]],
                                                    columns=['is_win r|p', 'time r|p', 'score r|p', 'enemies_algotithm',
                                                             'pacman_algorithm']))
print(df_predicted)





