import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import datetime

if __name__ == '__main__':
    sal = pd.read_csv("demo.csv", header=0, index_col=None)
    print(sal)
    X = sal[['x']]
    y = sal[['y']]

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25, random_state=42)

    lm = LinearRegression()
    lm.fit(X_train, y_train)

    print('Intercept :', round(lm.intercept_[0],2))
    print('Slope :', round(lm.coef_[0][0],2))


    filename = 'demo_model.pkl'
    joblib.dump(lm, filename)
